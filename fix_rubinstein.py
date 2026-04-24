import json, urllib.request, time

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_bib(key, retries=4, wait=2):
    url = f"https://dblp.org/rec/{key}.bib?param=1"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=15) as r:
                return r.read().decode('utf-8').strip()
        except Exception as e:
            print(f"  attempt {attempt+1} failed: {e}")
            time.sleep(wait * (attempt + 1))
    return None

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

# Fix "Combinatorial Prophet Inequalities" by Rubinstein & Singla
# Correct DBLP keys: conf/soda/RubinsteinS17, journals/corr/abs-1611-00665
for p in papers:
    if p['title'] == 'Combinatorial Prophet Inequalities' and 'Rubinstein' in p.get('authors', ''):
        print(f"Found: {p['title']}")
        bib_conf = fetch_bib('conf/soda/RubinsteinS17')
        time.sleep(1.5)
        bib_arxiv = fetch_bib('journals/corr/abs-1611-00665')
        
        bibs = []
        if bib_arxiv:
            bibs.append(bib_arxiv.replace('{CoRR}', '{arXiv}'))
        if bib_conf:
            bibs.append(bib_conf)
        
        p['bibtex'] = bibs
        p['versions'] = ['arXiv', 'SODA 2017']
        p['venue'] = 'SODA 2017'
        p['dblp_url'] = 'https://dblp.org/rec/conf/soda/RubinsteinS17'
        print(f"  Fixed: {len(bibs)} BibTeX blocks, versions: {p['versions']}")

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)
print("Done.")
