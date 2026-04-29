import json
import re

def clean_arxiv_bibtex(bib):
    """Remove eprint and arXiv URLs from BibTeX block"""
    if not bib: return bib
    bib = re.sub(r',\s*\burl\b\s*=\s*{https?://arxiv\.org[^}]+}', '', bib)
    bib = re.sub(r',\s*\beprinttype\b\s*=\s*{[^}]+}', '', bib)
    bib = re.sub(r',\s*\beprint\b\s*=\s*{[^}]+}', '', bib)
    
    # Also handle without leading commas just in case
    bib = re.sub(r'\s*\burl\b\s*=\s*{https?://arxiv\.org[^}]+}', '', bib)
    bib = re.sub(r'\s*\beprinttype\b\s*=\s*{[^}]+}', '', bib)
    bib = re.sub(r'\s*\beprint\b\s*=\s*{[^}]+}', '', bib)
    return bib

def inject_arxiv_bibtex(bib, arxiv_id):
    """Inject eprint and arXiv URLs into BibTeX block"""
    if not bib: return bib
    # Clean first
    bib = clean_arxiv_bibtex(bib)
    
    lines = bib.strip().split('\n')
    lines = [l for l in lines if l.strip() and l.strip() != ',']
    
    if lines[-1].strip() == '}':
        if '=' in lines[-2] and not lines[-2].strip().endswith(','):
            lines[-2] = lines[-2].rstrip() + ','
        
        lines.insert(-1, f'  url = {{https://arxiv.org/abs/{arxiv_id}}},')
        lines.insert(-1, f'  eprinttype = {{arXiv}},')
        lines.insert(-1, f'  eprint = {{{arxiv_id}}}')
    
    return '\n'.join(lines)

def main():
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    with open('link_actions.json', 'r', encoding='utf-8') as f:
        actions = json.load(f)
        
    for action in actions:
        idx = action['index']
        paper = data[idx]
        
        if action['type'] == 'remove_arxiv':
            # Remove pdf_url if it's an arxiv link
            if 'arxiv.org' in paper.get('pdf_url', ''):
                paper['pdf_url'] = paper.get('dblp_url', '')
            
            # Clean bibtex
            if paper.get('bibtex'):
                paper['bibtex'] = [clean_arxiv_bibtex(b) for b in paper['bibtex']]
                
        elif action['type'] == 'update_arxiv':
            arxiv_id = action['new_id']
            paper['pdf_url'] = f"https://arxiv.org/abs/{arxiv_id}"
            
            # Inject bibtex
            if paper.get('bibtex'):
                paper['bibtex'] = [inject_arxiv_bibtex(b, arxiv_id) for b in paper['bibtex']]
                
    with open('papers_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print("Successfully applied link fixes to papers_metadata.json")

if __name__ == '__main__':
    main()
