import json
import urllib.request
import urllib.parse
import urllib.error
import xml.etree.ElementTree as ET
import time
import re

def search_arxiv_by_title(title):
    clean_title = re.sub(r'[^a-zA-Z0-9\s\-]', ' ', title)
    clean_title = ' '.join(clean_title.split())
    query = urllib.parse.quote(f'ti:"{clean_title}"')
    url = f'http://export.arxiv.org/api/query?search_query={query}&max_results=1'
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            time.sleep(3) # Respect API rate limits
            response = urllib.request.urlopen(req)
            xml_data = response.read()
            root = ET.fromstring(xml_data)
            
            namespace = {'atom': 'http://www.w3.org/2005/Atom'}
            entry = root.find('atom:entry', namespace)
            
            if entry is not None:
                id_url = entry.find('atom:id', namespace).text
                # Extract just the ID, e.g., from http://arxiv.org/abs/1404.4473v1
                arxiv_id_match = re.search(r'/abs/(\d+\.\d+)(v\d+)?', id_url)
                if arxiv_id_match:
                    return arxiv_id_match.group(1)
                # Handle old style ids like math/9901001
                arxiv_old_match = re.search(r'/abs/([a-z\-]+/\d+)(v\d+)?', id_url)
                if arxiv_old_match:
                    return arxiv_old_match.group(1)
                
            return None
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code} for '{title}'. Retrying in 5s...")
            time.sleep(5)
        except Exception as e:
            print(f"Error querying arXiv for '{title}': {e}")
            return None
            
    print(f"Failed to fetch '{title}' after {max_retries} retries.")
    return None

def main():
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    report_lines = []
    actions = []
    
    report_lines.append("# Link Verification Report\n")
    
    for i, paper in enumerate(data):
        title = paper.get('title', '')
        pdf_url = paper.get('pdf_url', '')
        
        current_arxiv_id = None
        is_arxiv_link = False
        
        if 'arxiv.org/abs/' in pdf_url or 'arxiv.org/pdf/' in pdf_url:
            is_arxiv_link = True
            m = re.search(r'arxiv\.org/(?:abs|pdf)/(\d+\.\d+|[a-z\-]+/\d+)', pdf_url)
            if m:
                current_arxiv_id = m.group(1)
                
        bibtex = paper.get('bibtex', [''])[0] if paper.get('bibtex') else ''
        bib_arxiv_id = None
        if 'eprint' in bibtex and 'arXiv' in bibtex:
            m = re.search(r'eprint\s*=\s*\{?([^},]+)\}?', bibtex)
            if m:
                bib_arxiv_id = m.group(1).strip()
        
        print(f"Checking: {title}")
        
        actual_arxiv_id = search_arxiv_by_title(title)
        
        if actual_arxiv_id:
            # Arxiv version exists
            if current_arxiv_id != actual_arxiv_id:
                report_lines.append(f"**{title}**")
                report_lines.append(f"- Exists on arXiv: Yes (Actual ID: {actual_arxiv_id})")
                if current_arxiv_id:
                    report_lines.append(f"- Current link points to WRONG ID: {current_arxiv_id}")
                else:
                    report_lines.append(f"- Current link is not an arXiv link but one exists: {pdf_url}")
                report_lines.append("- Action: Will update `pdf_url` and bibtex to use correct arXiv ID.\n")
                
                actions.append({
                    "index": i,
                    "title": title,
                    "type": "update_arxiv",
                    "new_id": actual_arxiv_id
                })
            else:
                pass # All good
        else:
            # Does not exist on arXiv (or search failed)
            if is_arxiv_link or bib_arxiv_id:
                report_lines.append(f"**{title}**")
                report_lines.append(f"- Exists on arXiv: NO (Not found via API search for exact title)")
                report_lines.append(f"- Current link points to IMAGINARY ID: {current_arxiv_id or bib_arxiv_id}")
                report_lines.append("- Action: Needs manual verification. Will remove fake arXiv links and fallback to DBLP/publisher link.\n")
                
                actions.append({
                    "index": i,
                    "title": title,
                    "type": "remove_arxiv"
                })

    with open('link_verification_report.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(report_lines))
        
    with open('link_actions.json', 'w', encoding='utf-8') as f:
        json.dump(actions, f, indent=2)

if __name__ == '__main__':
    main()
