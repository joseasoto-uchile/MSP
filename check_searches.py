import json
import re

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

with open('generate_html.py', 'r', encoding='utf-8') as f:
    data = f.read()

searches = re.findall(r'"search":\s*\[(.*?)\]', data)
failed = []

for search_str in searches:
    # "Babaioff", "Dinitz", "2009"
    terms = [t.strip(' "\'') for t in search_str.split(',')]
    found = False
    for i, p in enumerate(papers):
        text_to_search = (p['authors'] + " " + p['title'] + " " + p.get('venue', '')).lower()
        if all(t.lower() in text_to_search for t in terms):
            found = True
            break
    if not found:
        failed.append(terms)

print(f"Failed searches: {len(failed)}")
for f in failed:
    print(f)
