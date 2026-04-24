import json
import urllib.request
import urllib.parse
import urllib.error
import time

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

def fetch_dblp(title):
    query = urllib.parse.quote(title)
    url = f"https://dblp.org/search/publ/api?q={query}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {title}: {e}")
            time.sleep(2)
    return None

def fetch_bibtex(key):
    url = f"https://dblp.org/rec/{key}.bib?param=1"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode()
        except Exception as e:
            print(f"Attempt {attempt+1} failed for {key}: {e}")
            time.sleep(2)
    return None

results = {}

for p in papers:
    pid = p.get('id', p['title'][:10])
    title = p['title']
    print(f"Fetching: {title}")
    
    data = fetch_dblp(title)
    if data:
        hits = data.get("result", {}).get("hits", {}).get("hit", [])
        results[pid] = {
            "original_title": title,
            "original_authors": p['authors'],
            "original_venue": p['venue'],
            "dblp_hits": []
        }
        for hit in hits:
            info = hit["info"]
            # To be strict, grab the bibtex for every hit so we can audit
            key = info.get("key")
            if key:
                bibtex = fetch_bibtex(key)
                time.sleep(0.5)
                results[pid]["dblp_hits"].append({
                    "info": info,
                    "bibtex": bibtex
                })
    time.sleep(1)

with open('dblp_cache.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=4)
print("Finished fetching DBLP data")
