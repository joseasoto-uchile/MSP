import json
import os

new_papers = [
    {
        "id": "babaioff2007",
        "title": "Matroids, Secretary Problems, and Online Mechanisms",
        "authors": "Moshe Babaioff, Nicole Immorlica, Robert Kleinberg",
        "venue": "SODA 2007",
        "summary": "Introduces the Matroid Secretary Problem and gives the first constant-competitive algorithms for Transversal, Graphic, and Truncated Partition matroids.",
        "pdf_url": "https://dl.acm.org/doi/10.5555/1283383.1283430",
        "local_pdf": "#",
        "dblp_url": "https://dblp.org/rec/conf/soda/BabaioffIK07",
        "bibtex": "@inproceedings{babaioff2007matroids,\n  title={Matroids, secretary problems, and online mechanisms},\n  author={Babaioff, Moshe and Immorlica, Nicole and Kleinberg, Robert},\n  booktitle={Proceedings of the eighteenth annual ACM-SIAM symposium on Discrete algorithms},\n  pages={434--443},\n  year={2007},\n  organization={Society for Industrial and Applied Mathematics}\n}"
    },
    {
        "id": "kesselheim2013",
        "title": "An Optimal Online Algorithm for Bipartite Matching and Generalizations to Matroids",
        "authors": "Thomas Kesselheim, Klaus Radke, Andreas Tönnis, Berthold Vöcking",
        "venue": "SODA 2013",
        "summary": "Provides an optimal 1/e-competitive online algorithm for the bipartite matching problem and generalizes it to transversal matroids.",
        "pdf_url": "https://epubs.siam.org/doi/10.1137/1.9781611973105.42",
        "local_pdf": "#",
        "dblp_url": "https://dblp.org/rec/conf/soda/KesselheimRTV13",
        "bibtex": '@inproceedings{kesselheim2013optimal,\n  title={An optimal online algorithm for bipartite matching and generalizations to matroids},\n  author={Kesselheim, Thomas and Radke, Klaus and T{\\"o}nnis, Andreas and V{\\"o}cking, Berthold},\n  booktitle={Proceedings of the twenty-fourth annual ACM-SIAM symposium on Discrete algorithms},\n  pages={589--600},\n  year={2013},\n  organization={SIAM}\n}'
    },
    {
        "id": "im2011",
        "title": "Secretary Problems: Laminar Matroid and Intersection of Matroids",
        "authors": "Sungjin Im, Yajun Wang",
        "venue": "SODA 2011",
        "summary": "Presents the first constant competitive ratio algorithm for the Matroid Secretary Problem on laminar matroids.",
        "pdf_url": "https://dl.acm.org/doi/10.5555/2133036.2133068",
        "local_pdf": "#",
        "dblp_url": "https://dblp.org/rec/conf/soda/ImW11",
        "bibtex": "@inproceedings{im2011secretary,\n  title={Secretary problems: laminar matroid and intersection of matroids},\n  author={Im, Sungjin and Wang, Yajun},\n  booktitle={Proceedings of the twenty-second annual ACM-SIAM symposium on Discrete Algorithms},\n  pages={400--409},\n  year={2011},\n  organization={SIAM}\n}"
    },
    {
        "id": "dimitrov2012",
        "title": "Competitive Weighted Matching in Transversal Matroids",
        "authors": "Nenad Dimitrov, C. Greg Plaxton",
        "venue": "ICALP 2012",
        "summary": "Improves the competitive ratio for the transversal matroid secretary problem to 1/8.",
        "pdf_url": "https://link.springer.com/chapter/10.1007/978-3-642-31594-7_34",
        "local_pdf": "#",
        "dblp_url": "https://dblp.org/rec/conf/icalp/DimitrovP12",
        "bibtex": "@inproceedings{dimitrov2012competitive,\n  title={Competitive weighted matching in transversal matroids},\n  author={Dimitrov, Nenad and Plaxton, C Greg},\n  booktitle={Automata, Languages, and Programming: 39th International Colloquium, ICALP 2012},\n  pages={397--408},\n  year={2012},\n  organization={Springer}\n}"
    },
    {
        "id": "chakraborty2012",
        "title": "Improved Competitive Ratio for the Matroid Secretary Problem",
        "authors": "Sourav Chakraborty, Oded Lachish",
        "venue": "SODA 2012",
        "summary": "Provides an improved O(sqrt(log rank)) competitive algorithm for the general Matroid Secretary Problem.",
        "pdf_url": "https://dl.acm.org/doi/10.5555/2095116.2095208",
        "local_pdf": "#",
        "dblp_url": "https://dblp.org/rec/conf/soda/ChakrabortyL12",
        "bibtex": "@inproceedings{chakraborty2012improved,\n  title={Improved competitive ratio for the matroid secretary problem},\n  author={Chakraborty, Sourav and Lachish, Oded},\n  booktitle={Proceedings of the twenty-third annual ACM-SIAM symposium on Discrete Algorithms},\n  pages={1141--1153},\n  year={2012},\n  organization={SIAM}\n}"
    },
    {
        "id": "kleinberg2005",
        "title": "A Multiple-Choice Secretary Algorithm with Applications to Online Auctions",
        "authors": "Robert Kleinberg",
        "venue": "SODA 2005",
        "summary": "Solves the multiple-choice secretary problem (equivalent to k-uniform matroids) with an asymptotically optimal success probability of 1 - O(1/sqrt(k)).",
        "pdf_url": "https://dl.acm.org/doi/10.5555/1070432.1070523",
        "local_pdf": "#",
        "dblp_url": "https://dblp.org/rec/conf/soda/Kleinberg05",
        "bibtex": "@inproceedings{kleinberg2005multiple,\n  title={A multiple-choice secretary algorithm with applications to online auctions},\n  author={Kleinberg, Robert},\n  booktitle={Proceedings of the sixteenth annual ACM-SIAM symposium on Discrete algorithms},\n  pages={630--631},\n  year={2005},\n  organization={Society for Industrial and Applied Mathematics}\n}"
    }
]

file_path = 'papers_metadata.json'
with open(file_path, 'r', encoding='utf-8') as f:
    papers = json.load(f)

# Append only if not already present
existing_titles = [p.get("title", "").lower() for p in papers]

added = 0
for np in new_papers:
    if np["title"].lower() not in existing_titles:
        papers.insert(0, np)  # Insert at the beginning so they appear prominent or at least exist
        added += 1

if added > 0:
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=4, ensure_ascii=False)
    print(f"Added {added} missing papers.")
else:
    print("No new papers added.")
