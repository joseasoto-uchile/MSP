import json
import re
import urllib.request
import urllib.error
from urllib.parse import urlparse
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
    # Some publishers block default user-agents or HEAD requests
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers, method='GET')
    try:
        # We just need to start the request to see if it's 200
        # We don't read the whole body to save time
        response = urllib.request.urlopen(req, timeout=10)
        return response.getcode() == 200
    except urllib.error.HTTPError as e:
        # If it's a 403 Forbidden, the URL is probably correct but they block bots
        if e.code in [403, 405]:
            return True
        return False
    except Exception as e:
        print(f"Error on {url}: {e}")
        return False

def main():
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    to_verify = []
    
    for paper in data:
        versions = paper.get('versions', [])
        bibs = paper.get('bibtex', [])
        
        for i, v_name in enumerate(versions):
            # Skip if already a dict
            if isinstance(v_name, dict):
                continue
                
            bib = bibs[i] if i < len(bibs) else ""
            url = extract_url(bib)
            
            if url:
                to_verify.append((paper['title'][:30], v_name, url))
                
    print(f"Found {len(to_verify)} URLs to verify.")
    # Test just the first 5 to see if verification logic works
    for t, v, u in to_verify[:5]:
        print(f"Verifying {v} -> {u} ...", end=" ")
        ok = verify_url(u)
        print("OK" if ok else "FAIL")

if __name__ == '__main__':
    main()
