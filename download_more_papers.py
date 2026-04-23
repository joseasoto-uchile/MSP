import urllib.request
import xml.etree.ElementTree as ET
import os
import json
import time
import re

def clean_text(text):
    if text is None:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def generate_bibtex(paper_id, title, authors, year):
    # authors: "Name 1, Name 2" -> "Name 1 and Name 2"
    author_bib = " and ".join(authors.split(", "))
    first_author_last = authors.split(",")[0].split(" ")[-1] if authors else "Unknown"
    title_key = title.split(" ")[0].lower() if title else "paper"
    key = f"{first_author_last}{year}{title_key}"
    # strip non-alphanumeric from key
    key = re.sub(r'[^a-zA-Z0-9]', '', key)
    
    bib = f"""@article{{{key},
  title={{{title}}},
  author={{{author_bib}}},
  journal={{arXiv preprint arXiv:{paper_id}}},
  year={{{year}}}
}}"""
    return bib

def download_more_papers():
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = 'all:matroid+AND+all:secretary'
    start = 0
    max_results = 50
    
    query = f'search_query={search_query}&start={start}&max_results={max_results}&sortBy=relevance&sortOrder=descending'
    
    print(f"Querying arXiv with: {base_url}{query}")
    try:
        response = urllib.request.urlopen(base_url + query)
        xml_data = response.read()
    except Exception as e:
        print(f"Error querying arXiv: {e}")
        return

    root = ET.fromstring(xml_data)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}
    
    papers = []
    os.makedirs('papers', exist_ok=True)
    
    for i, entry in enumerate(root.findall('atom:entry', ns)):
        title = clean_text(entry.find('atom:title', ns).text)
        summary = clean_text(entry.find('atom:summary', ns).text)
        published = entry.find('atom:published', ns).text
        year = published[:4] if published else "2024"
        
        authors = []
        for author in entry.findall('atom:author', ns):
            name = author.find('atom:name', ns).text
            authors.append(name)
        authors_str = ', '.join(authors)
            
        pdf_url = ""
        for link in entry.findall('atom:link', ns):
            if link.attrib.get('title') == 'pdf':
                pdf_url = link.attrib.get('href')
                break
                
        if pdf_url and not pdf_url.endswith('.pdf'):
            pdf_url += '.pdf'
            
        # extract arxiv id
        id_str = entry.find('atom:id', ns).text
        paper_id = id_str.split('/')[-1]
        # handle versions like 2103.04205v3
        paper_id_clean = paper_id.split('v')[0] if 'v' in paper_id else paper_id
        
        filename = f"{paper_id}.pdf"
        filepath = os.path.join('papers', filename)
        
        bibtex = generate_bibtex(paper_id_clean, title, authors_str, year)
        
        print(f"[{i+1}/{max_results}] Checking/Downloading {title}...")
        try:
            if not os.path.exists(filepath) and pdf_url:
                urllib.request.urlretrieve(pdf_url, filepath)
                time.sleep(1) # Be nice to arXiv API
        except Exception as e:
            print(f"Error downloading {pdf_url}: {e}")
            
        papers.append({
            'title': title,
            'authors': authors_str,
            'summary': summary,
            'published': published,
            'pdf_url': pdf_url,
            'local_pdf': f"papers/{filename}",
            'bibtex': bibtex
        })
        
    with open('papers_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully downloaded {len(papers)} papers and saved metadata.")

if __name__ == '__main__':
    download_more_papers()
