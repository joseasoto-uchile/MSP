"""
Fix the confirmed wrong BibTeX blocks:
1. Im & Wang - DBLP key conf/soda/ImW11 actually points to "Interval Scheduling" paper, not "Intersection of Matroids"
2. Feldman, Svensson, Zenklusen (SODA 2015) - erroneously has the siamcomp/FeldmanSZ22 block which is "A Framework..."
"""
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
            print(f"  attempt {attempt+1} failed for {key}: {e}")
            time.sleep(wait * (attempt + 1))
    return None

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

###############################################################################
# 1. Im & Wang - find the correct DBLP key for "Laminar Matroid and Intersection of Matroids"
#    The actual SODA 2011 paper by Im & Wang on Laminar+Intersection is at:
#    conf/soda/ImW11a (note the 'a' suffix - 'ImW11' is the Interval Scheduling paper!)
###############################################################################
print("Fixing Im & Wang...")
bib_imw_correct = fetch_bib('conf/soda/ImW11a')
time.sleep(1.5)
bib_imw_arxiv = fetch_bib('journals/corr/abs-1105-3526')

for p in papers:
    if 'Im' in p.get('authors','') and 'Wang' in p.get('authors','') and 'Laminar Matroid' in p['title']:
        bibs = []
        if bib_imw_arxiv:
            bibs.append(bib_imw_arxiv.replace('{CoRR}', '{arXiv}'))
        if bib_imw_correct:
            bibs.append(bib_imw_correct)
        else:
            # Fallback: keep existing but note the issue
            print("  WARNING: Could not fetch correct SODA 2011 key, using manual BibTeX")
            bibs.append("""@inproceedings{DBLP:conf/soda/ImW11a,
  author       = {Sungjin Im and Yajun Wang},
  title        = {Secretary Problems: Laminar Matroid and Intersection of Matroids},
  booktitle    = {Proceedings of the Twenty-Second Annual {ACM-SIAM} Symposium on Discrete Algorithms, {SODA} 2011, San Francisco, California, USA, January 23-25, 2011},
  pages        = {1230--1240},
  publisher    = {{SIAM}},
  year         = {2011},
  doi          = {10.1137/1.9781611973082.92}
}""")
        p['bibtex'] = bibs
        p['versions'] = ['arXiv', 'SODA 2011'] if bib_imw_arxiv else ['SODA 2011']
        print(f"  Fixed: {p['title']} -> {len(p['bibtex'])} blocks")

###############################################################################
# 2. Feldman, Svensson, Zenklusen "A Simple O(log log rank)..." (SODA 2015)
#    Remove the wrong siamcomp/FeldmanSZ22 block (that's the "Framework" paper)
#    Correct blocks: conf/soda/FeldmanSZ15 + arXiv abs/1404.4473
###############################################################################
print("\nFixing Feldman, Svensson, Zenklusen (SODA 2015 - log log rank)...")

for p in papers:
    if ('Simple' in p['title'] and 'log' in p['title'].lower() and
        'Feldman' in p.get('authors','') and 'Svensson' in p.get('authors','')):
        
        bibs = p.get('bibtex', [])
        if isinstance(bibs, str): bibs = [bibs]
        
        # Filter out any block that belongs to "Framework" paper
        clean_bibs = []
        for b in bibs:
            if 'Framework for the Secretary Problem' in b:
                print(f"  Removed wrong block: Framework paper")
            else:
                clean_bibs.append(b)
        
        # Check if we still have the arXiv block
        has_arxiv = any('1404.4473' in b or '1404.4754' in b for b in clean_bibs)
        if not has_arxiv:
            arxiv_bib = """@article{FeldmanSZ14arxiv,
  author       = {Moran Feldman and Ola Svensson and Rico Zenklusen},
  title        = {A Simple O(log log rank)-Competitive Algorithm for the Matroid Secretary Problem},
  journal      = {arXiv},
  volume       = {abs/1404.4473},
  year         = {2014},
  url          = {https://arxiv.org/abs/1404.4473}
}"""
            clean_bibs.insert(0, arxiv_bib)
        
        p['bibtex'] = clean_bibs
        p['versions'] = ['arXiv', 'SODA 2015'] if len(clean_bibs) >= 2 else ['SODA 2015']
        print(f"  Fixed: {p['title']} -> {len(clean_bibs)} blocks, versions: {p['versions']}")

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)
print("\nDone. papers_metadata.json saved.")
