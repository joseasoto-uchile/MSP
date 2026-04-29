import json
import re

def extract_url(bib):
    # Try doi
    m_doi = re.search(r'\bdoi\s*=\s*[{"]([^}"]+)[}"]', bib, re.IGNORECASE)
    if m_doi:
        return f"https://doi.org/{m_doi.group(1).strip()}"
        
    # Try url
    m_url = re.search(r'\burl\s*=\s*[{"]([^}"]+)[}"]', bib, re.IGNORECASE)
    if m_url:
        return m_url.group(1).strip()
        
    # Try dblp key
    m_key = re.search(r'@\w+\{(?:DBLP:)?([^,\s]+)', bib)
    if m_key:
        return f"https://dblp.org/rec/{m_key.group(1).strip()}"
        
    return None

def main():
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    stats = {'doi': 0, 'url': 0, 'dblp': 0, 'none': 0}
    
    for paper in data:
        for i, v in enumerate(paper.get('versions', [])):
            bib = paper['bibtex'][i]
            
            # Determine type of link found
            m_doi = re.search(r'\bdoi\s*=\s*[{"]([^}"]+)[}"]', bib, re.IGNORECASE)
            m_url = re.search(r'\burl\s*=\s*[{"]([^}"]+)[}"]', bib, re.IGNORECASE)
            
            if m_doi:
                stats['doi'] += 1
            elif m_url:
                stats['url'] += 1
            elif re.search(r'@\w+\{(?:DBLP:)?([^,\s]+)', bib):
                stats['dblp'] += 1
            else:
                stats['none'] += 1
                
    print(stats)

if __name__ == '__main__':
    main()
