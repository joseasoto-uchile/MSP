import json

fixes = {
    "SODA 2005": "https://dl.acm.org/doi/10.5555/1070432.1070519",
    "SODA 2007": "https://dl.acm.org/doi/10.1145/1283383.1283429",
    "dimitrovplaxton2008tr": "https://www.cs.utexas.edu/~plaxton/c/336/techrep.html"
}

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for p in data:
    for v in p.get('versions', []):
        if isinstance(v, dict) and v['name'] in fixes:
            old = v.get('url')
            v['url'] = fixes[v['name']]
            print(f"Fixed {v['name']}: {old} -> {v['url']}")

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
