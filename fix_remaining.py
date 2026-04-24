"""
Fix the 5 papers that failed due to rate limiting.
Also fix the Dimitrov & Plaxton ICALP 2012 key (returned 404 - DBLP key changed).
Also update the dblp_url for Kesselheim to point to ESA not SODA.
"""
import json, time, urllib.request, urllib.error

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def fetch_bib(key, retries=5, wait=3):
    url = f"https://dblp.org/rec/{key}.bib?param=1"
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode('utf-8').strip()
        except Exception as e:
            print(f"  attempt {attempt+1} failed: {e}")
            time.sleep(wait * (attempt + 1))
    return None

with open('papers_metadata.json', 'r', encoding='utf-8') as f:
    papers = json.load(f)

def find(pid):
    for p in papers:
        if p.get('id') == pid or p['title'] == pid:
            return p
    return None

###############################################################################
# 1. Feldman, Svensson, Zenklusen – "A Simple O(log log rank)..."
#    DBLP keys: conf/soda/FeldmanSZ15, journals/siamcomp/FeldmanSZ22, journals/corr/abs-1404-4473
###############################################################################
print("Fixing Feldman, Svensson, Zenklusen (log log rank)...")
keys_fsz = ['conf/soda/FeldmanSZ15', 'journals/siamcomp/FeldmanSZ22', 'journals/corr/abs-1404-4473']
bibs_fsz = []
for k in keys_fsz:
    b = fetch_bib(k)
    if b:
        bibs_fsz.append(b.replace('journal      = {CoRR}', 'journal      = {arXiv}'))
        print(f"  OK: {k}")
    time.sleep(2)

for p in papers:
    if 'Simple' in p['title'] and 'log' in p['title'].lower() and 'Feldman' in p['authors']:
        p['bibtex'] = bibs_fsz
        p['versions'] = ['arXiv version', 'SODA 2015 version', 'SIAM J. Comput. 2022 version']
        p['dblp_url'] = 'https://dblp.org/rec/conf/soda/FeldmanSZ15'
        print(f"  Updated: {p['title']}")

###############################################################################
# 2. Lachish – "O(log log rank) Competitive-Ratio..."
#    DBLP keys: conf/focs/Lachish14, journals/corr/abs-1403-7343
###############################################################################
print("\nFixing Lachish (log log rank FOCS)...")
keys_lachish = ['conf/focs/Lachish14', 'journals/corr/abs-1403-7343']
bibs_lachish = []
for k in keys_lachish:
    b = fetch_bib(k)
    if b:
        bibs_lachish.append(b.replace('journal      = {CoRR}', 'journal      = {arXiv}'))
        print(f"  OK: {k}")
    time.sleep(2)

for p in papers:
    if 'Lachish' in p['authors'] and 'log' in p['title'].lower() and 'Competitive' in p['title']:
        p['bibtex'] = bibs_lachish
        p['versions'] = ['arXiv version', 'FOCS 2014 version']
        p['dblp_url'] = 'https://dblp.org/rec/conf/focs/Lachish14'
        print(f"  Updated: {p['title']}")

###############################################################################
# 3. Caramanis et al. – "Single-Sample Prophet Inequalities via Greedy-Ordered Selection"
#    DBLP key: conf/soda/CaramanisDFFL022
###############################################################################
print("\nFixing Caramanis et al. (Single-Sample Prophet via Greedy)...")
keys_ss = ['conf/soda/CaramanisDFFL022', 'journals/corr/abs-2111-03174']
bibs_ss = []
for k in keys_ss:
    b = fetch_bib(k)
    if b:
        bibs_ss.append(b.replace('journal      = {CoRR}', 'journal      = {arXiv}'))
        print(f"  OK: {k}")
    time.sleep(2)

for p in papers:
    if 'Greedy-Ordered' in p['title']:
        p['bibtex'] = bibs_ss
        p['versions'] = ['arXiv version', 'SODA 2022 version']
        p['venue'] = 'SODA 2022'
        p['dblp_url'] = 'https://dblp.org/rec/conf/soda/CaramanisDFFL022'
        print(f"  Updated: {p['title']}")

###############################################################################
# 4. Azar, Kleinberg, Weinberg – "Prophet Inequalities with Limited Information"
#    DBLP key: conf/soda/AzarKW14
###############################################################################
print("\nFixing Azar, Kleinberg, Weinberg (Prophet with Limited Info)...")
keys_akw = ['conf/soda/AzarKW14', 'journals/corr/abs-1307-3736']
bibs_akw = []
for k in keys_akw:
    b = fetch_bib(k)
    if b:
        bibs_akw.append(b.replace('journal      = {CoRR}', 'journal      = {arXiv}'))
        print(f"  OK: {k}")
    time.sleep(2)

for p in papers:
    if 'Prophet Inequalities with Limited' in p['title']:
        p['bibtex'] = bibs_akw
        p['versions'] = ['arXiv version', 'SODA 2014 version']
        p['venue'] = 'SODA 2014'
        p['dblp_url'] = 'https://dblp.org/rec/conf/soda/AzarKW14'
        print(f"  Updated: {p['title']}")

###############################################################################
# 5. Chan, Chen, Jiang – "Revealing Optimal Thresholds..."
#    DBLP key: conf/soda/ChanCJ15
###############################################################################
print("\nFixing Chan, Chen, Jiang (Revealing Optimal Thresholds)...")
keys_ccj = ['conf/soda/ChanCJ15']
bibs_ccj = []
for k in keys_ccj:
    b = fetch_bib(k)
    if b:
        bibs_ccj.append(b)
        print(f"  OK: {k}")
    time.sleep(2)

for p in papers:
    if 'Revealing Optimal Thresholds' in p['title']:
        p['bibtex'] = bibs_ccj if bibs_ccj else p.get('bibtex', [])
        p['versions'] = ['SODA 2015 version']
        print(f"  Updated: {p['title']}")

###############################################################################
# 6. Dimitrov & Plaxton – fix the wrong extra ICALP key (DimitrovP08 was wrong)
#    The correct key is conf/icalp/DimitrovP12, but it 404s — use the journal version
#    journals/algorithmica/DimitrovP12
###############################################################################
print("\nFixing Dimitrov & Plaxton versions list...")
for p in papers:
    if 'Dimitrov' in p.get('authors', '') and 'Transversal' in p['title']:
        # Filter out bibs that are from DimitrovP08 (wrong paper)
        bibs = p.get('bibtex', [])
        if isinstance(bibs, list):
            bibs = [b for b in bibs if '2008' not in b[:200] or 'Dimitrov' in b]
        # Fetch the correct ICALP 2012 bibtex - DBLP might have it under a different key
        # Let's try the correct keys
        for k in ['conf/icalp/DimitrovP12a', 'conf/icalp/DimitrovP12b']:
            b = fetch_bib(k)
            if b:
                bibs.insert(0, b)
                print(f"  Got ICALP bib from {k}")
                break
            time.sleep(1)
        p['bibtex'] = bibs
        p['versions'] = ['arXiv version', 'ICALP 2012 version', 'Algorithmica 2012 version']
        print(f"  Updated: {p['title']}")

###############################################################################
# 7. Fix Kesselheim dblp_url to point to ESA not SODA
###############################################################################
for p in papers:
    if 'Kesselheim' in p.get('authors', '') and 'Weighted Bipartite' in p['title']:
        p['dblp_url'] = 'https://dblp.org/rec/conf/esa/KesselheimRTV13'
        print(f"\nFixed Kesselheim dblp_url -> ESA")

###############################################################################
# 8. Fix Babaioff et al. — check if JACM 2018 journal version should be added
###############################################################################
print("\nChecking Babaioff et al. for JACM 2018 version...")
bib_babaioff_jacm = fetch_bib('journals/jacm/BabaioffIKKM18')
if bib_babaioff_jacm:
    for p in papers:
        if p.get('id') == 'babaioff2007':
            bibs = p.get('bibtex', [])
            if isinstance(bibs, list) and not any('jacm' in b.lower() or 'j. acm' in b.lower() for b in bibs):
                bibs.append(bib_babaioff_jacm)
                p['bibtex'] = bibs
                versions = p.get('versions', [])
                if 'J. ACM 2018 version' not in str(versions):
                    versions.append('J. ACM 2018 version')
                p['versions'] = versions
                print(f"  Added JACM 2018 version for Babaioff et al.")

###############################################################################
# Final: replace ALL remaining CoRR with arXiv
###############################################################################
print("\nFinal CoRR->arXiv sweep...")
for p in papers:
    bibs = p.get('bibtex', [])
    if isinstance(bibs, str):
        bibs = [bibs]
    p['bibtex'] = [b.replace('journal      = {CoRR}', 'journal      = {arXiv}')
                    .replace('journal = {CoRR}', 'journal = {arXiv}')
                    .replace('{CoRR}', '{arXiv}')
                   for b in bibs]

with open('papers_metadata.json', 'w', encoding='utf-8') as f:
    json.dump(papers, f, indent=4, ensure_ascii=False)

print("Done. papers_metadata.json updated.")
