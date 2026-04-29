import json

renames = {
    "dimitrovplaxton2008icalp": "ICALP 2008",
    "dimitrovplaxton2008tr": "Tech Report 2008",
    "dimitrovplaxton2012algorithmica": "Algorithmica 2012",
    "feldmansz14arxiv": "arXiv",
    "rubinsteins16arxiv": "arXiv",
    "turkieltaubmelo2025": "Ph.D. Thesis 2025"
}

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for p in data:
    for v in p.get('versions', []):
        if isinstance(v, dict) and v['name'] in renames:
            old = v['name']
            v['name'] = renames[old]
            print(f"Renamed {old} to {v['name']}")

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
