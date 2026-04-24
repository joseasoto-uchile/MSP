"""
Fix version labels - derive short clean labels from the DBLP key embedded
in the first line of each BibTeX block (e.g. @inproceedings{DBLP:conf/soda/FeldmanSZ15, ...)
"""
import json, re

CONF_MAP = {
    'soda':  'SODA',
    'focs':  'FOCS',
    'stoc':  'STOC',
    'esa':   'ESA',
    'icalp': 'ICALP',
    'ipco':  'IPCO',
    'stacs': 'STACS',
    'sosa':  'SOSA',
    'wine':  'WINE',
    'itcs':  'ITCS',
    'isaac': 'ISAAC',
    'sagt':  'SAGT',
    'nips':  'NeurIPS',
    'sigecom': 'EC',
    'fct':   'FCT',
}

JOURNAL_MAP = {
    'siamcomp':    'SIAM J. Comput.',
    'siamdm':      'SIAM J. Discrete Math.',
    'mor':         'Math. Oper. Res.',
    'mp':          'Math. Program.',
    'mst':         'Theory Comput. Syst.',
    'algorithmica':'Algorithmica',
    'jacm':        'J. ACM',
    'tcs':         'Theor. Comput. Sci.',
    'networks':    'Networks',
    'disopt':      'Discret. Optim.',
    'jcss':        'J. Comput. Syst. Sci.',
    'orf':         'Oper. Res. Forum',
    'corr':        'arXiv',
}

def label_from_key(key):
    """
    Derive a clean version label from a DBLP key.
    key examples:
      conf/soda/FeldmanSZ15    -> 'SODA 2015'
      journals/siamcomp/Soto13 -> 'SIAM J. Comput. 2013'
      journals/corr/abs-2111-03174 -> 'arXiv'
    """
    key = key.strip().lower()
    
    # Year: last digits in key
    year_m = re.search(r'(\d{2,4})$', key.split('/')[-1])
    year_short = year_m.group(1) if year_m else ''
    year = ('20' + year_short) if (year_short and len(year_short) == 2) else year_short
    
    parts = key.split('/')
    if len(parts) < 2:
        return key
    
    kind = parts[0]  # 'conf' or 'journals'
    sub  = parts[1]  # 'soda', 'siamcomp', 'corr', etc.
    
    if kind == 'conf':
        conf = CONF_MAP.get(sub, sub.upper())
        return f'{conf} {year}' if year else conf
    elif kind == 'journals':
        if sub == 'corr':
            return 'arXiv'
        journal = JOURNAL_MAP.get(sub, sub)
        return f'{journal} {year}' if year else journal
    return key

def extract_dblp_key(bib_block):
    """Extract DBLP key from first line of BibTeX, e.g. @inproceedings{DBLP:conf/soda/FeldmanSZ15,"""
    m = re.search(r'@\w+\{(?:DBLP:)?([^,\s]+)', bib_block)
    return m.group(1) if m else None

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

for p in papers:
    bibs = p.get('bibtex', [])
    if isinstance(bibs, str):
        bibs = [bibs]
    
    labels = []
    for bib in bibs:
        key = extract_dblp_key(bib)
        if key:
            label = label_from_key(key)
        else:
            # Fallback: try to read year + venue from BibTeX fields
            year_m = re.search(r'year\s*=\s*[\{"]?(\d{4})', bib)
            year = year_m.group(1) if year_m else ''
            bib_type = re.search(r'^@(\w+)', bib)
            bt = bib_type.group(1).lower() if bib_type else ''
            label = f'arXiv {year}' if 'corr' in bib.lower()[:200] or 'arxiv' in bib.lower()[:200] else f'{bt} {year}'
        labels.append(label)
    
    if labels:
        p['versions'] = labels

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)

print("Version labels regenerated cleanly.")
print("\nSample output:")
for p in papers[:8]:
    print(f"  {p['title'][:55]:55s} -> {p.get('versions')}")
