"""
Post-process: fix a few label quirks and sort versions so arXiv always comes first.
"""
import json, re

CONF_MAP_EXTRAS = {
    'innovations': 'ITCS',
    'sagt': 'SAGT',
    'nips': 'NeurIPS',
    'sigecom': 'EC',
    'isaac': 'ISAAC',
}

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

def fix_label(label):
    # Fix 'INNOVATIONS 2022' -> 'ITCS 2022'
    for wrong, right in CONF_MAP_EXTRAS.items():
        label = re.sub(rf'\b{wrong.upper()}\b', right, label, flags=re.IGNORECASE)
    return label

def sort_versions(versions):
    """Put arXiv first, then conferences, then journals."""
    arxiv = [v for v in versions if 'arXiv' in v]
    conf = [v for v in versions if 'arXiv' not in v and any(
        c in v for c in ['SODA','FOCS','STOC','ESA','ICALP','IPCO','STACS','SOSA','WINE','ITCS','ISAAC','SAGT','NeurIPS','EC','SODA','NeurIPS']
    )]
    journals = [v for v in versions if v not in arxiv and v not in conf]
    return arxiv + conf + journals

for p in papers:
    versions = p.get('versions', [])
    versions = [fix_label(v) for v in versions]
    versions = sort_versions(versions)
    p['versions'] = versions

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)

print("Labels fixed and sorted.")
print("\nSample output:")
for p in papers[:12]:
    print(f"  {p['title'][:55]:55s} -> {p.get('versions')}")
