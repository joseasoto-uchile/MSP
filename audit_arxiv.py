import json
import re

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

# IDs to verify from user request
arxiv_id_map = {
    "The matroid secretary problem for minor-closed classes and random matroids": "1603.06822",
    "Improved algorithms and analysis for the laminar matroid secretary problem": "1301.4958",
    "On Variants of the Matroid Secretary Problem": "1104.4081",
    "Beating Competitive Ratio 4 for Graphic Matroid Secretary": "2501.08846",
    "Constant-Competitiveness for Random Assignment Matroid Secretary Without Knowing the Matroid": "2305.05353",
    "Matroid Secretary for Regular and Decomposable Matroids": "1207.5146",
    "A Simple O(log log rank)-Competitive Algorithm for the Matroid Secretary Problem": "1404.4473",
    "Laminar Matroid Secretary: Greedy Strikes Back": "2308.09880",
    "Matroid Secretary via Labeling Schemes": "2411.12069",
    "Strong Algorithms for the Ordinal Matroid Secretary Problem": "1802.01997",
    "Extension of Simple Algorithms to the Matroid Secretary Problem": "2211.02755",
    "Formal Barriers to Simple Algorithms for the Matroid Secretary Problem": "2111.04114",
    "The k-Fold Matroid Secretary Problem": "2512.06611",
    "Matroid Secretary Problem in the Random Assignment Model": "1007.2152",
    "Matroid Partition Property and the Secretary Problem": "2111.12436",
    "The Outer Limits of Contention Resolution on Matroids and Connections to the Secretary Problem": "1909.04268",
    "Beyond Matroids: Secretary Problem and Prophet Inequality with General Constraints": "1604.00357",
    "Submodular Matroid Secretary Problem with Shortlists": "2001.00894",
    "Secretary problem: graphs, matroids and greedoids": "1801.00814",
    "Prophet Secretary for Combinatorial Auctions and Matroids": "1710.11213",
    "The secretary returns": "1404.0614",
    "Combinatorial Secretary Problems with Ordinal Information": "1702.01290",
    "Online Matroid Embeddings": "2407.10316",
    "Improved Submodular Secretary Problem with Shortlists": "2010.01901",
    "Robust Secretary and Prophet Algorithms for Packing Integer Programs": "2112.12920",
    "Free-order secretary for two-sided independence systems": "2511.04390",
    "Sample-Based Matroid Prophet Inequalities": "2406.12799",
    "Constrained Non-Monotone Submodular Maximization: Offline and Secretary Algorithms": "1003.1517",
    "Secretary and Online Matching Problems with Machine Learned Advice": "2006.01026",
    "Building a Good Team: Secretary Problems and the Supermodular Degree": "1507.06199",
    "Simple Random Order Contention Resolution for Graphic Matroids with Almost no Prior Information": "2211.15146",
    "Universal Online Contention Resolution with Preselected Order": "2504.16327",
    "Maximizing Profit with Convex Costs in the Random-order Model": "1804.08172",
    "Single-Sample Prophet Inequalities Revisited": "2103.13089",
    "On Submodular Prophet Inequalities and Correlation Gap": "2107.03662",
    "Single-Sample Prophet Inequalities via Greedy-Ordered Selection": "2111.03174"
}

def fix_bibtex_block(bib, arxiv_id):
    if not bib: return bib
    
    # Clean up the mess from previous run (the "bib," and broken urls)
    bib = bib.replace('bib,', '')
    
    # Remove existing arXiv specific fields carefully using word boundaries
    # We want to match 'url =', 'eprinttype =', 'eprint =' but NOT 'biburl ='
    bib = re.sub(r',\s*\burl\b\s*=\s*{[^}]+}', '', bib)
    bib = re.sub(r',\s*\beprinttype\b\s*=\s*{[^}]+}', '', bib)
    bib = re.sub(r',\s*\beprint\b\s*=\s*{[^}]+}', '', bib)
    # Also handle the cases where they were added at the end without leading comma
    bib = re.sub(r'\s*\burl\b\s*=\s*{[^}]+}', '', bib)
    bib = re.sub(r'\s*\beprinttype\b\s*=\s*{[^}]+}', '', bib)
    bib = re.sub(r'\s*\beprint\b\s*=\s*{[^}]+}', '', bib)

    # Insert before the last closing brace
    lines = bib.strip().split('\n')
    # Filter out empty lines or lines that are just commas
    lines = [l for l in lines if l.strip() and l.strip() != ',']
    
    if lines[-1].strip() == '}':
        # Ensure the previous line has a comma if it's a field
        if '=' in lines[-2] and not lines[-2].strip().endswith(','):
            lines[-2] = lines[-2].rstrip() + ','
        
        lines.insert(-1, f'  url = {{https://arxiv.org/abs/{arxiv_id}}},')
        lines.insert(-1, f'  eprinttype = {{arXiv}},')
        lines.insert(-1, f'  eprint = {{{arxiv_id}}}')
    
    return '\n'.join(lines)

for paper in papers:
    title = paper['title']
    
    # Force fix Dimitrov & Plaxton
    if "Dimitrov" in paper['authors'] and "Plaxton" in paper['authors'] and paper['id'] == "dimitrov2012":
        paper["venue"] = "Algorithmica 2012"
        paper["pdf_url"] = "https://doi.org/10.1007/s00453-010-9457-2"
        paper["dblp_url"] = "https://dblp.org/rec/journals/algorithmica/DimitrovP12"
        paper["summary"] = "Presents a 1/16-competitive algorithm for transversal matroids under the ordinal information model."
        paper["versions"] = [
            "UT Austin Technical Report TR-08-03, 2008",
            "ICALP 2008",
            "Algorithmica 2012"
        ]
        paper["bibtex"] = [
            "@techreport{DimitrovPlaxton2008TR,\n  author = {Nedialko B. Dimitrov and C. Greg Plaxton},\n  title = {Competitive Weighted Matching in Transversal Matroids},\n  institution = {University of Texas at Austin},\n  number = {TR-08-03},\n  year = {2008}\n}",
            "@inproceedings{DimitrovPlaxton2008ICALP,\n  author = {Nedialko B. Dimitrov and C. Greg Plaxton},\n  title = {Competitive Weighted Matching in Transversal Matroids},\n  booktitle = {Automata, Languages and Programming (ICALP 2008)},\n  series = {Lecture Notes in Computer Science},\n  volume = {5125},\n  pages = {395--406},\n  year = {2008},\n  doi = {10.1007/978-3-540-70575-8_33}\n}",
            "@article{DimitrovPlaxton2012Algorithmica,\n  author = {Nedialko B. Dimitrov and C. Greg Plaxton},\n  title = {Competitive Weighted Matching in Transversal Matroids},\n  journal = {Algorithmica},\n  volume = {62},\n  number = {1-2},\n  pages = {333--348},\n  year = {2012},\n  doi = {10.1007/s00453-010-9457-2}\n}"
        ]
        continue

    # ArXiv normalization
    arxiv_id = arxiv_id_map.get(title)
    if not arxiv_id:
        # Search by regex in existing pdf_url
        match = re.search(r'(\d{4}\.\d{4,5}|[a-z\-]+/\d{7})', paper.get('pdf_url', ''))
        if match:
            arxiv_id = match.group(1)

    if arxiv_id:
        paper['pdf_url'] = f"https://arxiv.org/abs/{arxiv_id}"
        if paper.get('bibtex'):
            paper['bibtex'] = [fix_bibtex_block(b, arxiv_id) for b in paper['bibtex']]
    else:
        # If no arxiv_id but marked as arXiv version, remove the label
        if paper.get('versions') and 'arXiv' in paper['versions']:
            paper['versions'] = [v for v in paper['versions'] if v != 'arXiv']

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)
