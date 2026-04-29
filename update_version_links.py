import json
import re
import urllib.request
import urllib.error
import time

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

def verify_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    req = urllib.request.Request(url, headers=headers, method='GET')
    try:
        response = urllib.request.urlopen(req, timeout=10)
        return response.getcode() == 200
    except urllib.error.HTTPError as e:
        if e.code in [403, 405]:
            return True
        return False
    except Exception:
        return False

def main():
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    total_versions = 0
    verified_urls = 0
    
    for paper in data:
        versions = paper.get('versions', [])
        bibs = paper.get('bibtex', [])
        
        new_versions = []
        
        for i, v in enumerate(versions):
            # Already processed? Just in case
            if isinstance(v, dict):
                new_versions.append(v)
                total_versions += 1
                if 'url' in v: verified_urls += 1
                continue
                
            v_name = v
            bib = bibs[i] if i < len(bibs) else ""
            url = extract_url(bib)
            
            v_dict = {"name": v_name}
            
            if url:
                print(f"Verifying {url} ...", end=" ")
                if verify_url(url):
                    v_dict["url"] = url
                    print("OK")
                    verified_urls += 1
                else:
                    print("FAIL")
            
            new_versions.append(v_dict)
            total_versions += 1
            
        paper['versions'] = new_versions
        
    with open('papers_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"Done! Verified and injected {verified_urls}/{total_versions} links.")

if __name__ == '__main__':
    main()
