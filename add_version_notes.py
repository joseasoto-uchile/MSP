import json
import re

def clean_text(text):
    if not text: return ""
    text = re.sub(r'[\n\r]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.replace('{', '').replace('}', '').strip()
    return text.lower()

def extract_field(bib, field):
    # Matches field = {value} or field = "value"
    # DOTALL allows matching across newlines
    m = re.search(r'\b' + field + r'\s*=\s*[{"](.*?(?<!\\))(?:[}"])(?=\s*[,}])', bib, re.IGNORECASE | re.DOTALL)
    if not m:
        # Fallback simpler regex
        m = re.search(r'\b' + field + r'\s*=\s*[{"]([^}"]+)[}"]', bib, re.IGNORECASE | re.DOTALL)
    if m:
        return clean_text(m.group(1))
    return None

def are_authors_similar(main_authors, bib_authors):
    if not bib_authors: return True
    main = clean_text(main_authors)
    # Bib authors are usually "A and B and C"
    # Just check if main length is reasonably close and they share some words
    main_words = set(re.findall(r'\w+', main))
    bib_words = set(re.findall(r'\w+', bib_authors))
    intersection = main_words.intersection(bib_words)
    if len(intersection) < min(len(main_words), len(bib_words)) * 0.5:
        return False
    return True

def are_titles_similar(main_title, bib_title):
    if not bib_title: return True
    main = clean_text(main_title)
    # Remove punctuation
    main_words = set(re.findall(r'\w+', main))
    bib_words = set(re.findall(r'\w+', bib_title))
    if not main_words or not bib_words: return True
    intersection = main_words.intersection(bib_words)
    # If they share less than 60% of words, it's a different title
    if len(intersection) < max(len(main_words), len(bib_words)) * 0.6:
        return False
    return True

def main():
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    notes_added = 0
    for p in data:
        main_title = p.get('title', '')
        main_authors = p.get('authors', '')
        bibs = p.get('bibtex', [])
        versions = p.get('versions', [])
        
        for i, v in enumerate(versions):
            if i >= len(bibs): continue
            if not isinstance(v, dict): continue
            
            bib = bibs[i]
            bib_title = extract_field(bib, 'title')
            bib_author = extract_field(bib, 'author')
            
            notes = []
            if bib_title and not are_titles_similar(main_title, bib_title):
                # Restore original capitalization for display
                m = re.search(r'\btitle\s*=\s*[{"]([^}"]+)[}"]', bib, re.IGNORECASE | re.DOTALL)
                orig_title = re.sub(r'[\n\r]+', ' ', m.group(1)).replace('{', '').replace('}', '').strip()
                notes.append(f'Título diferente: "{orig_title}"')
                
            if bib_author and not are_authors_similar(main_authors, bib_author):
                m = re.search(r'\bauthor\s*=\s*[{"]([^}"]+)[}"]', bib, re.IGNORECASE | re.DOTALL)
                orig_author = re.sub(r'[\n\r]+', ' ', m.group(1)).replace('{', '').replace('}', '').strip()
                notes.append(f'Autores: {orig_author}')
                
            if notes:
                v['note'] = " | ".join(notes)
                print(f"Added note to {p['title']} ({v['name']}): {v['note']}")
                notes_added += 1

    with open('papers_metadata.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        
    print(f"Total notes added: {notes_added}")

if __name__ == '__main__':
    main()
