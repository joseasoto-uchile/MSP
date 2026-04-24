import json
import urllib.request
import urllib.parse
import time

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

def get_dblp_info(title):
    query = urllib.parse.quote(title)
    url = f"https://dblp.org/search/publ/api?q={query}&format=json"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            hits = data.get("result", {}).get("hits", {}).get("hit", [])
            results = []
            for hit in hits:
                info = hit["info"]
                # Only keep if title roughly matches (DBLP sometimes returns partial matches)
                t1 = info.get("title", "").lower().replace(".", "").strip()
                t2 = title.lower().replace(".", "").strip()
                # If they share at least 50% of words
                w1 = set(t1.split())
                w2 = set(t2.split())
                if len(w1.intersection(w2)) / max(1, len(w2)) > 0.6:
                    key = info["key"]
                    venue = info.get("venue", "")
                    year = info.get("year", "")
                    # Fetch bibtex
                    bib_url = f"https://dblp.org/rec/{key}.bib?param=1"
                    try:
                        time.sleep(0.5) # respect rate limit
                        with urllib.request.urlopen(bib_url) as bib_res:
                            bibtex = bib_res.read().decode()
                            results.append({"key": key, "venue": venue, "year": year, "bibtex": bibtex, "info": info})
                    except Exception as e:
                        pass
            return results
    except Exception as e:
        print(f"Error querying {title}: {e}")
        return []

audit_report = []

for i, p in enumerate(papers):
    title = p['title']
    print(f"Querying: {title}")
    dblp_results = get_dblp_info(title)
    
    audit_report.append({
        "original_title": title,
        "original_venue": p.get("venue"),
        "original_bibtex": p.get("bibtex"),
        "dblp_results": dblp_results
    })

with open('dblp_audit.json', 'w', encoding='utf-8') as f:
    json.dump(audit_report, f, indent=4)
print("Done querying DBLP")
