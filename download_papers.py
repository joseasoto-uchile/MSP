import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import os
import json
import time
import re

def clean_text(text):
    if text is None:
        return ""
    return re.sub(r'\s+', ' ', text).strip()

def download_papers():
    base_url = 'http://export.arxiv.org/api/query?'
    search_query = 'all:matroid+AND+all:secretary'
    start = 0
    max_results = 20
    
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
        
        authors = []
        for author in entry.findall('atom:author', ns):
            name = author.find('atom:name', ns).text
            authors.append(name)
            
        pdf_url = ""
        for link in entry.findall('atom:link', ns):
            if link.attrib.get('title') == 'pdf':
                pdf_url = link.attrib.get('href')
                break
                
        # Some pdf urls don't end in .pdf, force it
        if pdf_url and not pdf_url.endswith('.pdf'):
            pdf_url += '.pdf'
            
        paper_id = entry.find('atom:id', ns).text.split('/')[-1]
        filename = f"{paper_id}.pdf"
        filepath = os.path.join('papers', filename)
        
        print(f"[{i+1}/{max_results}] Downloading {title}...")
        try:
            if not os.path.exists(filepath):
                urllib.request.urlretrieve(pdf_url, filepath)
                time.sleep(1) # Be nice to arXiv API
        except Exception as e:
            print(f"Error downloading {pdf_url}: {e}")
            
        papers.append({
            'title': title,
            'authors': ', '.join(authors),
            'summary': summary,
            'published': published,
            'pdf_url': pdf_url,
            'local_pdf': f"papers/{filename}"
        })
        
    with open('papers_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(papers, f, indent=4, ensure_ascii=False)
        
    print(f"Successfully downloaded {len(papers)} papers and saved metadata.")

if __name__ == '__main__':
    download_papers()
