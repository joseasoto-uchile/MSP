import json
import re
import urllib.request
import urllib.parse

def search_crossref(title):
    query = urllib.parse.quote(title)
    url = f"https://api.crossref.org/works?query.title={query}&rows=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    try:
        resp = urllib.request.urlopen(req, timeout=5)
        data = json.loads(resp.read())
        if data['message']['items']:
            item = data['message']['items'][0]
            # Simple check if the result title is similar
            res_title = item.get('title', [''])[0].lower()
            if title.split()[0].lower() in res_title:
                return item.get('URL')
    except:
        pass
    return None

def main():
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    for p in data:
        for i, v in enumerate(p.get('versions', [])):
            if isinstance(v, dict) and 'url' not in v:
                # Missing URL!
                title = p['title']
                print(f"Searching Crossref for: {title} ({v['name']})")
                url = search_crossref(title)
                if url:
                    print(f" -> Found: {url}")
                else:
                    print(" -> Not found.")

if __name__ == '__main__':
    main()
