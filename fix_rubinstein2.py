import json

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

bib_arxiv = """@article{RubinsteinS16arxiv,
  author       = {Aviad Rubinstein and Sahil Singla},
  title        = {Combinatorial Prophet Inequalities},
  journal      = {arXiv},
  volume       = {abs/1611.00665},
  year         = {2016},
  url          = {https://arxiv.org/abs/1611.00665}
}"""

for p in papers:
    if p['title'] == 'Combinatorial Prophet Inequalities' and 'Rubinstein' in p.get('authors', ''):
        bibs = p.get('bibtex', [])
        if isinstance(bibs, str): bibs = [bibs]
        # Insert arXiv block first
        p['bibtex'] = [bib_arxiv] + bibs
        p['versions'] = ['arXiv', 'SODA 2017']
        p['pdf_url'] = 'https://arxiv.org/abs/1611.00665'
        print(f"Fixed: {p['title']} -> {p['versions']}")

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)
print("Done.")
