"""
Fix Im & Wang paper - the actual SODA 2011 paper is:
"Secretary Problems: Laminar Matroid and Interval Scheduling"
NOT "Intersection of Matroids"

The BibTeX for conf/soda/ImW11 is correct (it IS the laminar paper).
We just need to fix the title and summary in papers_metadata.json.
"""
import json

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

for p in papers:
    if p.get('id') == 'im2011' or (
        'Im' in p.get('authors','') and 'Wang' in p.get('authors','') and
        'Laminar Matroid' in p['title']
    ):
        print(f"Fixing: {p['title']}")
        # Correct title - DBLP confirms this is the right title
        p['title'] = 'Secretary Problems: Laminar Matroid and Interval Scheduling'
        # Correct BibTeX - conf/soda/ImW11 IS the correct block, just had wrong title in page
        bib_correct = """@inproceedings{DBLP:conf/soda/ImW11,
  author       = {Sungjin Im and Yajun Wang},
  title        = {Secretary Problems: Laminar Matroid and Interval Scheduling},
  booktitle    = {Proceedings of the Twenty-Second Annual {ACM-SIAM} Symposium on Discrete Algorithms, {SODA} 2011, San Francisco, California, USA, January 23-25, 2011},
  pages        = {1265--1274},
  publisher    = {{SIAM}},
  year         = {2011},
  doi          = {10.1137/1.9781611973082.97}
}"""
        p['bibtex'] = [bib_correct]
        p['versions'] = ['SODA 2011']
        p['venue'] = 'SODA 2011'
        p['dblp_url'] = 'https://dblp.org/rec/conf/soda/ImW11'
        print(f"  -> New title: {p['title']}")
        print(f"  -> Versions: {p['versions']}")

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)
print("Done.")
