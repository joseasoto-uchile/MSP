import json
import urllib.request
import urllib.parse
import time

def enrich_with_dblp():
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)

    for i, paper in enumerate(papers):
        # We might already have it or we can overwrite
        title = paper['title']
        print(f"[{i+1}/{len(papers)}] Querying DBLP for: {title}")
        
        # Build query
        query = urllib.parse.quote(title)
        url = f"https://dblp.org/search/publ/api?q={query}&format=json&h=3"
        
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            hits = data.get('result', {}).get('hits', {}).get('hit', [])
            if hits:
                # take first hit
                info = hits[0].get('info', {})
                venue = info.get('venue', '')
                dblp_url = info.get('url', '')
                year = info.get('year', '')
                
                if venue and venue.lower() != 'arxiv':
                    # If it's published in a real venue
                    paper['venue'] = f"{venue} {year}"
                    paper['dblp_url'] = dblp_url
                    print(f"  -> Found in DBLP: {venue} {year}")
                else:
                    # Maybe it's just CoRR / arXiv in DBLP
                    if 'dblp_url' not in paper:
                        paper['dblp_url'] = dblp_url
                    print("  -> Only preprint found in DBLP")
            else:
                print("  -> Not found in DBLP")
        except Exception as e:
            print(f"  -> Error querying DBLP: {e}")
            
        time.sleep(1) # Be nice to DBLP

    with open('papers_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=4, ensure_ascii=False)
        
    print("DBLP enrichment complete.")

if __name__ == "__main__":
    enrich_with_dblp()
