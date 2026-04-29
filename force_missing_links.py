import json
import re

def extract_url(bib):
    m_doi = re.search(r'\bdoi\s*=\s*[{"]([^}"]+)[}"]', bib, re.IGNORECASE)
    if m_doi:
        return f"https://doi.org/{m_doi.group(1).strip()}"
        
    m_url = re.search(r'\burl\s*=\s*[{"]([^}"]+)[}"]', bib, re.IGNORECASE)
    if m_url:
        return m_url.group(1).strip()
        
    m_key = re.search(r'@\w+\{(?:DBLP:)?([^,\s]+)', bib)
    if m_key:
        return f"https://dblp.org/rec/{m_key.group(1).strip()}"
        
    return None

def main():
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for paper in data:
        versions = paper.get('versions', [])
        bibs = paper.get('bibtex', [])
        
        for i, v in enumerate(versions):
            if isinstance(v, dict):
                # Only try to inject if URL is missing
                if 'url' not in v:
                    bib = bibs[i] if i < len(bibs) else ""
                    url = extract_url(bib)
                    if url:
                        v['url'] = url
                        print(f"Injected {v['name']} -> {url}")
            else:
                # This shouldn't happen if we ran the previous script correctly
                pass

    with open('papers_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

if __name__ == '__main__':
    main()
