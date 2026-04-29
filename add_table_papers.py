import json

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

# 1. Fix Martin Pál
for p in papers:
    if "Martin Pal" in p['authors']:
        p['authors'] = p['authors'].replace("Martin Pal", "Martin Pál")

# 2. Add Babaioff et al. 2009
babaioff2009 = {
    "title": "Secretary Problems: Weights and Discounts",
    "authors": "Moshe Babaioff, Michael Dinitz, Anupam Gupta, Nicole Immorlica, Kunal Talwar",
    "venue": "SODA 2009",
    "summary": "We study several extensions of the classic secretary problem. In the weighted secretary problem, each candidate has a weight, and the goal is to select candidates to maximize the sum of their weights times their qualities. We give constant-competitive algorithms for this and related problems.",
    "category": "A",
    "tags": ["Secretary", "Weights", "Discounts"],
    "pdf_url": "https://doi.org/10.1137/1.9781611973068.135",
    "dblp_url": "https://dblp.org/rec/conf/soda/BabaioffDGIT09",
    "bibtex": [
"""@inproceedings{babaioff2009secretary,
  author    = {Moshe Babaioff and Michael Dinitz and Anupam Gupta and Nicole Immorlica and Kunal Talwar},
  title     = {Secretary problems: weights and discounts},
  booktitle = {Proceedings of the Twentieth Annual {ACM-SIAM} Symposium on Discrete Algorithms, {SODA} 2009},
  pages     = {1245--1254},
  publisher = {SIAM},
  year      = {2009},
  doi       = {10.1137/1.9781611973068.135}
}"""
    ],
    "versions": [
        {"name": "SODA 2009", "url": "https://doi.org/10.1137/1.9781611973068.135"}
    ]
}

# 3. Add Dynkin 1963
dynkin1963 = {
    "title": "The optimum choice of the instant for stopping a Markov process",
    "authors": "Eugene B. Dynkin",
    "venue": "Sov. Math. Dokl. 1963",
    "summary": "This foundational paper presents the mathematical formulation of the optimal stopping problem (also known as the secretary problem) as a Markov process. It rigorously derives the optimal 1/e stopping strategy.",
    "category": "B",
    "tags": ["Classical Secretary", "Optimal Stopping"],
    "pdf_url": "",
    "dblp_url": "",
    "bibtex": [
"""@article{dynkin1963optimum,
  title={The optimum choice of the instant for stopping a Markov process},
  author={Dynkin, Evgenii Borisovich},
  journal={Soviet Mathematics Doklady},
  volume={4},
  pages={627--629},
  year={1963}
}"""
    ],
    "versions": [
        {"name": "Sov. Math. Dokl. 1963"}
    ]
}

# Check if they exist to avoid duplicates
babaioff_exists = any("Weights and Discounts" in p['title'] for p in papers)
dynkin_exists = any("Dynkin" in p['authors'] for p in papers)

if not babaioff_exists:
    papers.append(babaioff2009)
    print("Added Babaioff et al. 2009")

if not dynkin_exists:
    papers.append(dynkin1963)
    print("Added Dynkin 1963")

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)
