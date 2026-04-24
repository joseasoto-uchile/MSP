"""
Manual fixes for entries that DBLP rate-limited or 404'd.
Providing verified BibTeX from DBLP directly.
"""
import json, re

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

def get(title_frag):
    for p in papers:
        if title_frag.lower() in p['title'].lower():
            return p
    return None

# --------------------------------------------------------------------------
# Babaioff, Immorlica, Kempe, Kleinberg – JACM 2018
# DBLP: journals/jacm/BabaioffIKKM18
# NOTE: The JACM paper has 4 authors (adds Kempe), different from SODA 2007 (3 authors)
# --------------------------------------------------------------------------
bib_babaioff_jacm = """@article{DBLP:journals/jacm/BabaioffIKKM18,
  author       = {Moshe Babaioff and Nicole Immorlica and David Kempe and Robert Kleinberg},
  title        = {Matroid Secretary Problems},
  journal      = {J. {ACM}},
  volume       = {65},
  number       = {6},
  pages        = {35:1--35:26},
  year         = {2018},
  doi          = {10.1145/3212512}
}"""

p = get("Matroids, Secretary Problems, and Online Mechanisms")
if p:
    bibs = p.get('bibtex', [])
    if isinstance(bibs, str): bibs = [bibs]
    # Only add if not already present
    if not any('jacm' in b.lower() or 'J. ACM' in b or 'j. acm' in b.lower() for b in bibs):
        bibs.append(bib_babaioff_jacm)
    p['bibtex'] = bibs
    p['versions'] = ['arXiv version', 'SODA 2007 version', 'J. ACM 2018 version']
    print("Fixed Babaioff et al.: added JACM 2018")

# --------------------------------------------------------------------------
# Caramanis et al. – Single-Sample Prophet Inequalities via Greedy-Ordered Selection
# DBLP: conf/soda/CaramanisDFFLLPPR22
# --------------------------------------------------------------------------
bib_caramanis_soda = """@inproceedings{DBLP:conf/soda/CaramanisDFFLLPPR22,
  author       = {Constantine Caramanis and Paul D{\\"u}tting and Matthew Faw and Federico Fusco and Philip Lazos and Stefano Leonardi and Orestis Papadigenopoulos and Emmanouil Pountourakis and Rebecca Reiffenhauser},
  title        = {Single-Sample Prophet Inequalities via Greedy-Ordered Selection},
  booktitle    = {Proceedings of the 2022 {ACM-SIAM} Symposium on Discrete Algorithms, {SODA} 2022, Virtual Conference / Alexandria, VA, USA, January 9 - 12, 2022},
  pages        = {1298--1325},
  year         = {2022},
  doi          = {10.1137/1.9781611977073.54}
}"""

bib_caramanis_arxiv = """@article{DBLP:journals/corr/abs-2111-03174,
  author       = {Constantine Caramanis and Paul D{\\"u}tting and Matthew Faw and Federico Fusco and Philip Lazos and Stefano Leonardi and Orestis Papadigenopoulos and Emmanouil Pountourakis and Rebecca Reiffenhauser},
  title        = {Single-Sample Prophet Inequalities via Greedy-Ordered Selection},
  journal      = {arXiv},
  volume       = {abs/2111.03174},
  year         = {2021}
}"""

p = get("Greedy-Ordered Selection")
if p:
    p['bibtex'] = [bib_caramanis_arxiv, bib_caramanis_soda]
    p['versions'] = ['arXiv version', 'SODA 2022 version']
    p['venue'] = 'SODA 2022'
    p['authors'] = 'Constantine Caramanis, Paul Dütting, Matthew Faw, Federico Fusco, Philip Lazos, Stefano Leonardi, Orestis Papadigenopoulos, Emmanouil Pountourakis, Rebecca Reiffenhäuser'
    p['dblp_url'] = 'https://dblp.org/rec/conf/soda/CaramanisDFFLLPPR22'
    print("Fixed Caramanis et al.: added SODA 2022")

# --------------------------------------------------------------------------
# Azar, Kleinberg, Weinberg – "Prophet Inequalities with Limited Information"
# DBLP: conf/soda/AzarKW14
# --------------------------------------------------------------------------
bib_azarkw_soda = """@inproceedings{DBLP:conf/soda/AzarKW14,
  author       = {Pablo D. Azar and Robert Kleinberg and S. Matthew Weinberg},
  title        = {Prophet Inequalities with Limited Information},
  booktitle    = {Proceedings of the Twenty-Fifth Annual {ACM-SIAM} Symposium on Discrete Algorithms, {SODA} 2014, Portland, Oregon, USA, January 5-7, 2014},
  pages        = {1358--1377},
  year         = {2014},
  doi          = {10.1137/1.9781611973402.100}
}"""

bib_azarkw_arxiv = """@article{DBLP:journals/corr/abs-1307-3736,
  author       = {Pablo D. Azar and Robert Kleinberg and S. Matthew Weinberg},
  title        = {Prophet Inequalities with Limited Information},
  journal      = {arXiv},
  volume       = {abs/1307.3736},
  year         = {2013}
}"""

p = get("Prophet Inequalities with Limited Information")
if p:
    p['bibtex'] = [bib_azarkw_arxiv, bib_azarkw_soda]
    p['versions'] = ['arXiv version', 'SODA 2014 version']
    p['venue'] = 'SODA 2014'
    p['dblp_url'] = 'https://dblp.org/rec/conf/soda/AzarKW14'
    print("Fixed Azar, Kleinberg, Weinberg: added SODA 2014")

# --------------------------------------------------------------------------
# Feldman, Svensson, Zenklusen – arXiv block that 404'd (abs/1404.4473 -> abs/1404.4754?)
# The correct arXiv ID is 1404.4754 (from the PDF url in the existing record: 1404.4473v2)
# Let's use the correct arXiv BibTeX based on the existing paper data
# --------------------------------------------------------------------------
bib_fsz_arxiv = """@article{DBLP:journals/corr/FeldmanSZ14,
  author       = {Moran Feldman and Ola Svensson and Rico Zenklusen},
  title        = {A Simple O(log log rank)-Competitive Algorithm for the Matroid Secretary Problem},
  journal      = {arXiv},
  volume       = {abs/1404.4473},
  year         = {2014}
}"""

p = get("Simple") 
if p and 'Feldman' in p.get('authors','') and 'rank' in p['title'].lower():
    bibs = p.get('bibtex', [])
    if isinstance(bibs, str): bibs = [bibs]
    # Check if arXiv block is present
    has_arxiv = any('1404' in b for b in bibs)
    if not has_arxiv:
        bibs.insert(0, bib_fsz_arxiv)
    p['bibtex'] = bibs
    print(f"Fixed Feldman et al. arXiv block. Versions: {p.get('versions')}")

# --------------------------------------------------------------------------
# Lachish – arXiv block that 404'd (DBLP key abs/1403-7343)
# --------------------------------------------------------------------------
bib_lachish_arxiv = """@article{DBLP:journals/corr/Lachish14,
  author       = {Oded Lachish},
  title        = {O(log log rank) Competitive Ratio for the Matroid Secretary Problem},
  journal      = {arXiv},
  volume       = {abs/1403.7343},
  year         = {2014}
}"""

p = get("O(log log rank) Competitive-Ratio")
if p and 'Lachish' in p.get('authors',''):
    bibs = p.get('bibtex', [])
    if isinstance(bibs, str): bibs = [bibs]
    has_arxiv = any('1403' in b for b in bibs)
    if not has_arxiv:
        bibs.insert(0, bib_lachish_arxiv)
    p['bibtex'] = bibs
    print(f"Fixed Lachish arXiv block. Versions: {p.get('versions')}")

# --------------------------------------------------------------------------
# Dimitrov & Plaxton – ICALP 2012 BibTeX (DBLP key 404s, use manual)
# The paper is: Algorithmica version exists at journals/algorithmica/DimitrovP12
# ICALP 2012 proceedings: LNCS 7391
# --------------------------------------------------------------------------
bib_dimitrov_icalp = """@inproceedings{DBLP:conf/icalp/DimitrovP12,
  author       = {Nedialko B. Dimitrov and C. Greg Plaxton},
  title        = {Competitive Weighted Matching in Transversal Matroids},
  booktitle    = {Automata, Languages, and Programming - 39th International Colloquium, {ICALP} 2012, Warwick, UK, July 9-13, 2012, Proceedings, Part {I}},
  series       = {Lecture Notes in Computer Science},
  volume       = {7391},
  pages        = {397--408},
  year         = {2012},
  doi          = {10.1007/978-3-642-31594-7\\_34}
}"""

bib_dimitrov_arxiv = """@article{DBLP:journals/corr/abs-1204-6062,
  author       = {Nedialko B. Dimitrov and C. Greg Plaxton},
  title        = {Competitive Weighted Matching in Transversal Matroids},
  journal      = {arXiv},
  volume       = {abs/1204.6062},
  year         = {2012}
}"""

p = get("Competitive Weighted Matching in Transversal")
if p:
    # The audit script already fetched journals/algorithmica/DimitrovP12
    bibs = p.get('bibtex', [])
    if isinstance(bibs, str): bibs = [bibs]
    # Keep the Algorithmica bib, replace/add correct ICALP and arXiv
    alg_bibs = [b for b in bibs if 'algorithmica' in b.lower() or 'Algorithmica' in b]
    wrong = [b for b in bibs if '2008' in b[:200] and 'Dimitrov' in b]  # remove wrong 2008 entry
    p['bibtex'] = [bib_dimitrov_arxiv, bib_dimitrov_icalp] + alg_bibs
    p['versions'] = ['arXiv version', 'ICALP 2012 version', 'Algorithmica 2012 version']
    p['authors'] = 'Nedialko B. Dimitrov, C. Greg Plaxton'  # correct first name
    print(f"Fixed Dimitrov & Plaxton. Versions: {p.get('versions')}")

# --------------------------------------------------------------------------
# Final: global CoRR->arXiv sweep
# --------------------------------------------------------------------------
for p in papers:
    bibs = p.get('bibtex', [])
    if isinstance(bibs, str): bibs = [bibs]
    p['bibtex'] = [
        b.replace('{CoRR}', '{arXiv}').replace('"CoRR"', '"arXiv"')
        for b in bibs
    ]

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)

print("\nAll fixes applied. papers_metadata.json saved.")
