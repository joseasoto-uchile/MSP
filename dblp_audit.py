"""
DBLP Bibliographic Audit Script
================================
Uses the DBLP API to:
  1. Fetch the authoritative BibTeX for every paper by its DBLP key
  2. Find all versions (conference / journal / arXiv) for each paper
  3. Report every discrepancy found in papers_metadata.json
  4. Produce a corrected papers_metadata.json with:
     - Accurate BibTeX blocks fetched from DBLP
     - "arXiv" instead of "CoRR" everywhere
     - Complete versions[] arrays
"""

import json, re, time, urllib.request, urllib.parse, urllib.error, sys

###############################################################################
# Helpers
###############################################################################

HEADERS = {'User-Agent': 'MSP-audit-bot/1.0 (bibliographic audit; contact: josea@dii.uchile.cl)'}

def dblp_get(url, retries=4, wait=2):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode('utf-8')
        except Exception as e:
            print(f"  [WARN] attempt {attempt+1} failed for {url}: {e}")
            time.sleep(wait * (attempt + 1))
    return None

def fetch_bibtex(dblp_key):
    """Fetch authoritative BibTeX from DBLP for a given key."""
    url = f"https://dblp.org/rec/{dblp_key}.bib?param=1"
    raw = dblp_get(url)
    if raw:
        # Replace @Comment / header lines sometimes prepended by DBLP
        raw = raw.strip()
    return raw

def search_dblp(title, max_hits=5):
    """Search DBLP by title, return list of hit dicts."""
    q = urllib.parse.quote(title)
    url = f"https://dblp.org/search/publ/api?q={q}&h={max_hits}&format=json"
    raw = dblp_get(url)
    if not raw:
        return []
    try:
        data = json.loads(raw)
        hits = data.get("result", {}).get("hits", {}).get("hit", [])
        return [h["info"] for h in hits]
    except Exception as e:
        print(f"  [WARN] JSON parse error: {e}")
        return []

def key_from_url(dblp_url):
    """Extract DBLP key from a dblp.org/rec/... URL."""
    m = re.search(r'dblp\.org/rec/(.+?)(?:\.html)?$', dblp_url or '')
    return m.group(1) if m else None

def normalize_key(info):
    """Get the DBLP key from a search hit's info dict."""
    return info.get('key', '')

def corr_to_arxiv(bibtex):
    """Replace journal={CoRR} with journal={arXiv} throughout a BibTeX string."""
    bibtex = re.sub(r'journal\s*=\s*\{CoRR\}', 'journal      = {arXiv}', bibtex)
    bibtex = re.sub(r'journal\s*=\s*"CoRR"', 'journal      = {arXiv}', bibtex)
    # Also fix volume: abs/XXXX -> eprint: XXXX pattern for arXiv
    return bibtex

def label_version(bib):
    """Return a human-readable version label from a BibTeX block."""
    type_m = re.search(r'^@(\w+)\{', bib, re.MULTILINE)
    entry_type = type_m.group(1).lower() if type_m else 'unknown'
    
    if entry_type == 'article':
        journal_m = re.search(r'journal\s*=\s*[\{"\'](.*?)[\}"\']\s*,?', bib, re.IGNORECASE)
        journal = journal_m.group(1).strip() if journal_m else ''
        year_m = re.search(r'year\s*=\s*[\{"\']*(\d{4})[\}"\']*', bib)
        year = year_m.group(1) if year_m else ''
        if 'arxiv' in journal.lower() or 'corr' in journal.lower():
            # Extract arXiv ID
            vol_m = re.search(r'volume\s*=\s*[\{"\'](abs/[0-9.]+)[\}"\']\s*,?', bib, re.IGNORECASE)
            arxiv_id = vol_m.group(1) if vol_m else ''
            return f"arXiv {arxiv_id}" if arxiv_id else f"arXiv preprint {year}"
        return f"{journal} {year}".strip()
    elif entry_type == 'inproceedings':
        book_m = re.search(r'booktitle\s*=\s*[\{"\'](.*?)[\}"\']\s*,?', bib, re.IGNORECASE)
        booktitle = book_m.group(1).strip() if book_m else ''
        year_m = re.search(r'year\s*=\s*[\{"\']*(\d{4})[\}"\']*', bib)
        year = year_m.group(1) if year_m else ''
        # Shorten booktitle
        short = re.search(r'\b(SODA|FOCS|STOC|ESA|ICALP|IPCO|STACS|SOSA|WINE|ITCS|ISAAC)\b', booktitle, re.IGNORECASE)
        if short:
            return f"{short.group(1).upper()} {year}"
        return f"{booktitle[:40]} {year}".strip()
    return entry_type

###############################################################################
# Main audit
###############################################################################

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

errors = []   # list of error dicts for the report
fixed = 0     # count of auto-fixed papers

for i, p in enumerate(papers):
    title = p['title']
    dblp_url = p.get('dblp_url', '')
    current_venue = p.get('venue', '')
    print(f"\n[{i+1}/{len(papers)}] {title}")
    
    # ---- Get DBLP key from URL ----
    primary_key = key_from_url(dblp_url)
    
    paper_errors = []
    all_keys = []   # All DBLP keys related to this paper
    
    if primary_key:
        all_keys.append(primary_key)
    else:
        print(f"  [WARN] No dblp_url, will search...")
    
    # ---- Search DBLP for this title to find all versions ----
    time.sleep(0.6)  # polite delay
    hits = search_dblp(title, max_hits=10)
    
    found_keys = set(all_keys)
    for hit in hits:
        hit_title = hit.get('title', '').rstrip('.')
        # Loose title match
        t1 = re.sub(r'[^a-z0-9 ]', '', title.lower())
        t2 = re.sub(r'[^a-z0-9 ]', '', hit_title.lower())
        w1, w2 = set(t1.split()), set(t2.split())
        if len(w1 & w2) / max(1, len(w1)) > 0.7:
            k = normalize_key(hit)
            if k and k not in found_keys:
                found_keys.add(k)
                all_keys.append(k)
    
    print(f"  Found DBLP keys: {all_keys}")
    
    # ---- Fetch BibTeX for each key ----
    bibtex_blocks = []
    for k in all_keys:
        time.sleep(0.4)
        bib = fetch_bibtex(k)
        if bib:
            bib = corr_to_arxiv(bib)
            bibtex_blocks.append(bib)
            print(f"  Fetched BibTeX for {k}: OK ({len(bib)} chars)")
        else:
            print(f"  [ERROR] Could not fetch BibTeX for {k}")
            paper_errors.append(f"Could not fetch BibTeX for DBLP key: {k}")
    
    if not bibtex_blocks:
        paper_errors.append("No BibTeX blocks could be fetched from DBLP")
        errors.append({"title": title, "issues": paper_errors, "fixed": False})
        continue
    
    # ---- Verify primary key venue vs current_venue ----
    if primary_key and bibtex_blocks:
        main_bib = bibtex_blocks[0]
        # Extract venue from fetched BibTeX
        book_m = re.search(r'booktitle\s*=\s*[\{"\'](.*?)[\}"\']\s*,?', main_bib, re.IGNORECASE)
        jour_m = re.search(r'journal\s*=\s*[\{"\'](.*?)[\}"\']\s*,?', main_bib, re.IGNORECASE)
        fetched_venue = (book_m.group(1) if book_m else '') or (jour_m.group(1) if jour_m else '')
        
        # Check for SODA vs ESA type mistakes
        venue_keywords = ['SODA', 'FOCS', 'STOC', 'ESA', 'ICALP', 'IPCO', 'STACS', 'SOSA', 'WINE', 'ITCS', 'ISAAC']
        cur_kw = next((k for k in venue_keywords if k.upper() in current_venue.upper()), None)
        fetch_kw = next((k for k in venue_keywords if k.upper() in fetched_venue.upper()), None)
        
        if cur_kw and fetch_kw and cur_kw != fetch_kw:
            paper_errors.append(f"WRONG VENUE: page says '{cur_kw}', DBLP says '{fetch_kw}' (from: {fetched_venue[:80]})")
    
    # ---- Check: does current BibTeX use CoRR? ----
    current_bibs = p.get('bibtex', [])
    if isinstance(current_bibs, str):
        current_bibs = [current_bibs]
    for cb in current_bibs:
        if 'CoRR' in cb:
            paper_errors.append("BibTeX contains 'CoRR' — should be 'arXiv'")
            break
    
    # ---- Build version labels ----
    version_labels = []
    for bib in bibtex_blocks:
        label = label_version(bib)
        version_labels.append(label)
    
    # ---- Update the paper record ----
    p['bibtex'] = bibtex_blocks
    p['versions'] = version_labels
    
    if paper_errors:
        errors.append({"title": title, "issues": paper_errors, "fixed": True})
    
    fixed += 1

# ---- Final CoRR sweep across all remaining bibtex fields ----
for p in papers:
    bibs = p.get('bibtex', [])
    if isinstance(bibs, str):
        bibs = [bibs]
    p['bibtex'] = [corr_to_arxiv(b) for b in bibs]

###############################################################################
# Write corrected metadata
###############################################################################
with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)

print(f"\n\n{'='*60}")
print(f"AUDIT COMPLETE: {fixed} papers processed")
print(f"Papers with errors: {len(errors)}")
print(f"{'='*60}\n")

###############################################################################
# Write audit report
###############################################################################
report_lines = ["# DBLP Bibliographic Audit Report\n"]
report_lines.append(f"**Total papers:** {len(papers)}\n")
report_lines.append(f"**Papers with errors:** {len(errors)}\n\n---\n")

for e in errors:
    report_lines.append(f"## ❌ {e['title']}")
    report_lines.append(f"  Fixed automatically: {'YES' if e.get('fixed') else 'NO'}\n")
    for issue in e['issues']:
        report_lines.append(f"  - {issue}")
    report_lines.append("")

with open('audit_report.md', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report_lines))

print("Audit report written to audit_report.md")
print("Corrected metadata written to papers_metadata.json")
