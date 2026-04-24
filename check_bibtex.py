"""
Strict BibTeX integrity checker.
For every paper, verify that every BibTeX block it contains actually refers
to the same paper (matching title and author) and not a false DBLP hit.
Produces a report of all mismatches.
"""
import json, re

def normalize(s):
    """Lowercase, strip LaTeX commands, punctuation, and extra spaces."""
    s = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', s)   # \cmd{x} -> x
    s = re.sub(r'\{([^}]*)\}', r'\1', s)               # {x} -> x
    s = re.sub(r'[^a-z0-9 ]', ' ', s.lower())
    return re.sub(r'\s+', ' ', s).strip()

def extract_bib_field(bib, field):
    """Extract a BibTeX field value (handles multi-line)."""
    pattern = rf'{field}\s*=\s*[\{{\"\'](.*?)[\}}\"\'](?:\s*,|\s*\}})'
    m = re.search(pattern, bib, re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()
    # Try without closing delimiter (last field)
    pattern2 = rf'{field}\s*=\s*[\{{\"\'](.*)'
    m2 = re.search(pattern2, bib, re.IGNORECASE | re.DOTALL)
    if m2:
        val = m2.group(1).strip()
        # Remove up to first } or "
        val = re.split(r'[}\"]', val)[0].strip().rstrip(',')
        return val
    return ''

def title_match(paper_title, bib_title, threshold=0.70):
    """Check if bib_title is close enough to paper_title."""
    if not bib_title:
        return False
    t1 = set(normalize(paper_title).split())
    t2 = set(normalize(bib_title).split())
    if not t1:
        return False
    overlap = len(t1 & t2) / len(t1)
    return overlap >= threshold

def first_author_match(paper_authors, bib_authors):
    """Check if first author last name appears in bib_authors."""
    if not bib_authors:
        return False
    # Get first author last name from paper record
    first = paper_authors.split(',')[0].strip()
    last_name = first.split()[-1].lower()
    return last_name in normalize(bib_authors)

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

problems = []

for p in papers:
    title = p['title']
    authors = p.get('authors', '')
    bibs = p.get('bibtex', [])
    if isinstance(bibs, str):
        bibs = [bibs]
    
    bad_bibs = []
    for bib in bibs:
        bib_title = extract_bib_field(bib, 'title')
        bib_authors = extract_bib_field(bib, 'author')
        
        t_ok = title_match(title, bib_title)
        a_ok = first_author_match(authors, bib_authors)
        
        if not (t_ok and a_ok):
            # Get the DBLP key from first line
            key_m = re.search(r'@\w+\{([^,\n]+)', bib)
            key = key_m.group(1).strip() if key_m else '???'
            bad_bibs.append({
                'key': key,
                'bib_title': bib_title[:80],
                'bib_authors': bib_authors[:80],
                'title_match': t_ok,
                'author_match': a_ok,
            })
    
    if bad_bibs:
        problems.append({
            'paper_title': title,
            'paper_authors': authors[:80],
            'bad_bibs': bad_bibs
        })

print(f"Papers checked: {len(papers)}")
print(f"Papers with wrong BibTeX blocks: {len(problems)}\n")
print("=" * 70)

for prob in problems:
    print(f"\n❌ PAPER: {prob['paper_title']}")
    print(f"   Authors: {prob['paper_authors']}")
    for b in prob['bad_bibs']:
        print(f"   → BAD BLOCK key: {b['key']}")
        print(f"     BibTeX title:  {b['bib_title']}")
        print(f"     BibTeX author: {b['bib_authors']}")
        print(f"     Title match: {b['title_match']}, Author match: {b['author_match']}")

# Also write JSON for programmatic fixing
with open('bib_problems.json', 'w', encoding='utf-8') as f:
    json.dump(problems, f, indent=2, ensure_ascii=False)

print(f"\nProblems written to bib_problems.json")
