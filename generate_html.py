import json
import os
import re
import urllib.parse

def find_paper_index(papers, search_terms):
    """
    Search for a paper in the list using keywords (e.g. authors or year).
    Returns the index if found, else -1.
    """
    for i, p in enumerate(papers):
        text_to_search = (p['authors'] + " " + p['title'] + " " + p.get('venue', '')).lower()
        # If all search terms are in the text, it's a match
        if all(term.lower() in text_to_search for term in search_terms):
            return i
    return -1

def generate_html(language="en"):
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)
        
    is_en = (language == "en")
    
    # Translations
    t = {
        "language": language,
        "en_active": "active" if is_en else "",
        "es_active": "" if is_en else "active",
        "seo_description": "Comprehensive survey on the Matroid Secretary Problem, featuring lecture notes, chronological competitive guarantees, and a curated reading list." if is_en else "Survey exhaustivo sobre el Problema de la Secretaria en Matroides, incluyendo notas de clase, garantías competitivas cronológicas y una lista de lectura.",
        "search_placeholder": "Search by title, author, or keyword..." if is_en else "Buscar por título, autor o palabra clave...",
        "disclaimer": "This page was automatically generated using Antigravity/Gemini." if is_en else "Esta página fue generada automáticamente usando Antigravity/Gemini.",
        
        "title": "Survey on Matroid Secretary Problem",
        "subtitle": "Lecture Notes, Exhaustive Chronological Guarantees and Reading List" if is_en else "Notas de Clase, Evolución Cronológica y Lista de Lectura",
        "tab_notes": "Lecture Notes" if is_en else "Notas de Clase",
        "tab_ratios": "Chronological Bounds" if is_en else "Evolución de Competitividades",
        "tab_list": f"Reading List ({len(papers)})" if is_en else f"Lista de Lectura ({len(papers)})",
        "notes_title": "Lecture Notes",
        "matroids_title": "1. Matroids" if is_en else "1. Matroides",
        "matroids_desc": r"A <strong>matroid</strong> is a combinatorial structure that generalizes the concept of linear independence in vector spaces. Formally, a matroid \( M \) is a pair \( (E, \mathcal{I}) \), where \( E \) is a finite set (the ground set) and \( \mathcal{I} \) is a family of subsets of \( E \) (called independent sets) that satisfies the following axioms:" if is_en else r"Un <strong>matroide</strong> es una estructura combinatoria que generaliza el concepto de independencia lineal en espacios vectoriales. Formalmente, un matroide \( M \) es un par \( (E, \mathcal{I}) \), donde \( E \) es un conjunto finito (llamado conjunto base) y \( \mathcal{I} \) es una familia de subconjuntos de \( E \) (llamados conjuntos independientes) que satisface los siguientes axiomas:",
        "ax1": r"The empty set is independent: \( \emptyset \in \mathcal{I} \)." if is_en else r"El conjunto vacío es independiente: \( \emptyset \in \mathcal{I} \).",
        "ax2": r"Hereditary property: If \( A \in \mathcal{I} \) and \( B \subseteq A \), then \( B \in \mathcal{I} \)." if is_en else r"Propiedad hereditaria: Si \( A \in \mathcal{I} \) y \( B \subseteq A \), entonces \( B \in \mathcal{I} \).",
        "ax3": r"Augmentation (or exchange) property: If \( A, B \in \mathcal{I} \) and \( |A| > |B| \), there exists an element \( x \in A \setminus B \) such that \( B \cup \{x\} \in \mathcal{I} \)." if is_en else r"Propiedad de aumento (o intercambio): Si \( A, B \in \mathcal{I} \) y \( |A| > |B| \), existe un elemento \( x \in A \setminus B \) tal que \( B \cup \{x\} \in \mathcal{I} \).",
        "rank_desc": r"The maximal independent sets of a matroid are called <strong>bases</strong>. All bases of a matroid have the same size, known as the <strong>rank</strong> of the matroid, denoted by \( r(M) \)." if is_en else r"Los conjuntos independientes maximales de un matroide se llaman <strong>bases</strong>. Todas las bases de un matroide tienen el mismo tamaño, conocido como el <strong>rango</strong> del matroide, denotado por \( r(M) \).",
        "classic_title": "2. The Classical Secretary Problem" if is_en else "2. El Problema Clásico de la Secretaria",
        "classic_desc": r"In the classical problem, \( n \) candidates are presented in a sequential and random order. A decision must be made immediately after interviewing each candidate on whether to hire or reject them. The goal is to maximize the probability of hiring the <strong>best</strong> candidate. The optimal algorithm involves observing the first \( n/e \) candidates without hiring anyone, and then hiring the first candidate who is better than all those observed so far. This algorithm achieves a success probability of \( 1/e \)." if is_en else r"En el problema clásico, \( n \) candidatos se presentan de forma secuencial y aleatoria. Se debe decidir inmediatamente después de entrevistar a cada candidato si se le contrata o se le rechaza. El objetivo es maximizar la probabilidad de contratar al <strong>mejor</strong> candidato. El algoritmo óptimo consiste en observar a los primeros \( n/e \) candidatos sin contratar a ninguno, y luego contratar al primer candidato que sea mejor que todos los observados hasta el momento. Este algoritmo logra una probabilidad de éxito de \( 1/e \).",
        "msp_title": "3. The Matroid Secretary Problem" if is_en else "3. El Problema de la Secretaria en Matroides (Matroid Secretary Problem)",
        "msp_desc": r"Introduced by Babaioff, Immorlica, and Kleinberg (2007), the <strong>Matroid Secretary Problem</strong> combines optimal stopping with combinatorial optimization. Suppose we have a matroid \( M = (E, \mathcal{I}) \) with a weight function \( w: E \to \mathbb{R}^+ \) assigned to each element." if is_en else r"Introducido por Babaioff, Immorlica y Kleinberg (2007), el <strong>Matroid Secretary Problem</strong> combina la parada óptima con la optimización combinatoria. Supongamos que tenemos un matroide \( M = (E, \mathcal{I}) \) con una función de peso \( w: E \to \mathbb{R}^+ \) asignada a cada elemento.",
        "dynamics_title": "Problem Dynamics:" if is_en else "Dinámica del Problema:",
        "dyn1": r"The elements of \( E \) are revealed sequentially in a uniformly random order." if is_en else r"Los elementos de \( E \) se revelan de forma secuencial en un orden aleatorio uniforme.",
        "dyn2": r"When an element \( e \) is revealed, its weight \( w(e) \) is discovered." if is_en else r"Cuando un elemento \( e \) es revelado, se descubre su peso \( w(e) \).",
        "dyn3": r"An irrevocable and immediate decision must be made: accept or reject \( e \)." if is_en else r"Se debe tomar una decisión irrevocable e inmediata: aceptar o rechazar \( e \).",
        "dyn4": r"The set of accepted elements at any time must be an independent set \( I \in \mathcal{I} \)." if is_en else r"El conjunto de elementos aceptados en cualquier momento debe ser un conjunto independiente \( I \in \mathcal{I} \).",
        "msp_obj": r"<strong>Objective:</strong> Design an online algorithm that maximizes the expected value of the selected elements, compared to the maximum weight basis offline. The grand conjecture (Matroid Secretary Conjecture) states that there exists an algorithm with a constant competitive ratio \( \Omega(1) \) for any matroid." if is_en else r"<strong>Objetivo:</strong> Diseñar un algoritmo online que maximice el valor esperado de los elementos seleccionados, comparado con la base de peso máximo en offline. La gran conjetura (Matroid Secretary Conjecture) afirma que existe un algoritmo con un factor de competitividad constante \( \Omega(1) \) para cualquier matroide.",
        
        "ratios_title": "Chronological Progression of Competitive Guarantees" if is_en else "Evolución Cronológica de Garantías Competitivas",
        "ratios_desc": "The table below groups results by Matroid Class, detailing the exact constant or formula achieved by each paper historically. All constants have been normalized so that <strong>values $\\le 1$ represent the approximation factor</strong> (i.e. $1/\\alpha$ where $\\alpha$ is the traditional competitive ratio $\\ge 1$). We also note whether the guarantee is <strong>Probability-Competitive</strong> ($p$) or the traditional <strong>Utility-Competitive Ratio</strong>." if is_en else "La siguiente tabla agrupa los resultados por clase de matroide, detallando la constante exacta o fórmula alcanzada por cada paper a lo largo de la historia. Todas las constantes han sido normalizadas para que <strong>valores $\\le 1$ representen el factor de aproximación</strong> (es decir, $1/\\alpha$ donde $\\alpha$ es el ratio competitivo tradicional $\\ge 1$). Se indica si la garantía es <strong>Probability-Competitive</strong> ($p$) o el tradicional <strong>Ratio de Utilidad</strong>.",
        
        "th_class": "Matroid Class" if is_en else "Clase de Matroide",
        "th_ref": "Reference" if is_en else "Referencia",
        "th_type": "Guarantee Type" if is_en else "Tipo de Garantía",
        "th_guarantee": "Exact Bound ($\\le 1$)" if is_en else "Cota Exacta ($\\le 1$)",
        
        "reading_title": "Reading List and Bibliography" if is_en else "Lista de Lectura y Bibliografía",
        "reading_desc": f"Below are <strong>{len(papers)}</strong> relevant articles on the Matroid Secretary Problem, including their export in <strong>BibTeX</strong>." if is_en else f"A continuación se presentan <strong>{len(papers)}</strong> artículos relevantes sobre el Problema de la Secretaria en Matroides, incluyendo su exportación en <strong>BibTeX</strong>.",
        "by": "By:" if is_en else "Por:",
        "abstract": "Abstract:" if is_en else "Resumen:",
        "read_local": "Read Local PDF" if is_en else "Leer PDF Local",
        "view_arxiv": "View on arXiv" if is_en else "Ver en arXiv",
        "show_bibtex": "Show BibTeX" if is_en else "Mostrar BibTeX"
    }

    # Data structure grouped by class
    # "search" are keywords to find the paper in the reading list for auto-linking
    table_data = [
        {
            "class": "Graphic",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": "\\( 1/16 = 0.0625 \\)"},
                {"ref": "Korula & Pál (2009)", "search": ["Korula", "Pál"], "type": "Util", "val": "\\( 1/(2e) \\approx 0.184 \\)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2018/2021)", "search": ["Soto", "Turkieltaub", "ordinal"], "type": "Prob", "val": "\\( 1/4 = 0.25 \\)"},
                {"ref": "Banihashem et al. (2025)", "search": ["Banihashem", "graphic"], "type": "Util", "val": "\\( 1/3.95 \\approx 0.253 \\) (Gen) / \\( 1/3.77 \\approx 0.265 \\) (Simple)"},
                {"ref": "Bérczi, Livanos, Soto, Verdugo (2025)", "search": ["Livanos", "labeling"], "type": "Prob", "val": "\\( 0.2504 \\) (Gen) / \\( 0.2693 \\) (Simple)"}
            ]
        },
        {
            "class": "Laminar",
            "entries": [
                {"ref": "Im & Wang (2011)", "search": ["Im", "Wang"], "type": "Util", "val": "\\( 3/16000 \\approx 0.00018 \\)"},
                {"ref": "Jaillet, Soto, Zenklusen (2012)", "search": ["Jaillet", "Zenklusen"], "type": "Util", "val": "\\( \\frac{1}{3\\sqrt{3}e} \\approx 0.070 \\)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2018/2021)", "search": ["Soto", "ordinal"], "type": "Prob", "val": "\\( \\frac{1}{3\\sqrt{3}} \\approx 0.192 \\)"},
                {"ref": "Huang, Parsaeian, Zhu (2023)", "search": ["Parsaeian"], "type": "Util", "val": "\\( 1/4.75 \\approx 0.210 \\)"},
                {"ref": "Bérczi, Livanos, Soto, Verdugo (2025)", "search": ["Livanos", "labeling"], "type": "Prob", "val": "\\( 1 - \\ln(2) \\approx 0.3068 \\)"}
            ]
        },
        {
            "class": "Transversal",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": "\\( 1/16 = 0.0625 \\)"},
                {"ref": "Dimitrov & Plaxton (2012)", "search": ["Dimitrov", "Plaxton"], "type": "Util", "val": "\\( 1/8 = 0.125 \\)"},
                {"ref": "Kesselheim et al. (2013)", "search": ["Kesselheim"], "type": "Util", "val": "\\( 1/e \\approx 0.367 \\)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2021)", "search": ["Soto", "ordinal"], "type": "Prob", "val": "\\( 1/e \\approx 0.367 \\)"}
            ]
        },
        {
            "class": "Rank-2 Matroids",
            "entries": [
                {"ref": "Bérczi, Livanos, Soto, Verdugo (2025)", "search": ["Livanos", "labeling"], "type": "Prob", "val": "\\( 0.3462 \\)"}
            ]
        },
        {
            "class": "Cographic",
            "entries": [
                {"ref": "Soto (2011)", "search": ["Soto", "random assignment"], "type": "Util", "val": "\\( 1/(3e) \\approx 0.122 \\)"}
            ]
        },
        {
            "class": "k-Uniform",
            "entries": [
                {"ref": "Dynkin (1963)", "search": ["Dynkin"], "type": "Prob", "val": "\\( 1/e \\approx 0.367 \\)"},
                {"ref": "Kleinberg (2005) / Soto et al. (2021)", "search": ["Kleinberg"], "type": "Prob", "val": "\\( 1 - O(\\sqrt{\\frac{\\log \\rho}{\\rho}}) \\)"},
                {"ref": "Gujjar et al. (2025)", "search": ["Gujjar"], "type": "Prob", "val": "\\( 1 - O(\\sqrt{\\frac{\\log(n)}{k}}) \\) (k-Fold)"}
            ]
        },
        {
            "class": "Partition",
            "entries": [
                {"ref": "Folklore", "search": ["Folklore"], "type": "Prob", "val": "\\( 1/e \\approx 0.367 \\)"}
            ]
        },
        {
            "class": "Truncated Partition",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": "\\( 1/e^2 \\approx 0.135 \\)"}
            ]
        },
        {
            "class": "Regular & Max-Flow Min-Cut",
            "entries": [
                {"ref": "Dinitz & Kortsarz (2012)", "search": ["Dinitz"], "type": "Util", "val": "\\( \\Omega(1) \\)"}
            ]
        },
        {
            "class": "K-Column Sparse Linear",
            "entries": [
                {"ref": "Soto (2011)", "search": ["Soto", "random assignment"], "type": "Util", "val": "\\( 1/(k \\cdot e) \\)"}
            ]
        },
        {
            "class": "Paving",
            "entries": [
                {"ref": "Huynh & Nelson (2016)", "search": ["Huynh"], "type": "Util", "val": "\\( \\approx 1/2 = 0.5 \\)"}
            ]
        },
        {
            "class": "Open Conjecture: General Matroids (Random Order)",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": "\\( \\Omega(1/\\log \\rho) \\)"},
                {"ref": "Chakraborty & Lachish (2012)", "search": ["Lachish"], "type": "Util", "val": "\\( \\Omega(1/\\sqrt{\\log \\rho}) \\)"},
                {"ref": "Lachish (2014) / Feldman et al. (2014)", "search": ["Feldman"], "type": "Util", "val": "\\( \\Omega(1/\\log \\log \\rho) \\)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2021)", "search": ["Soto", "ordinal"], "type": "Prob", "val": "\\( \\Omega(1/\\log \\rho) \\) (Ordinal access)"}
            ]
        },
        {
            "class": "Open Conjecture: General (Random Assignment Model)",
            "entries": [
                {"ref": "Soto (2011)", "search": ["Soto", "random assignment"], "type": "Util", "val": "\\( \\frac{e-1}{2e^2} \\approx 0.117 \\)"},
                {"ref": "Santiago, Sergeev, Zenklusen (2023)", "search": ["Santiago", "Sergeev"], "type": "Util", "val": "\\( \\Omega(1) \\) (Without knowing matroid)"}
            ]
        },
        {
            "class": "Open Conjecture: General (Free Order Model)",
            "entries": [
                {"ref": "Jaillet, Soto, Zenklusen (2012)", "search": ["Jaillet", "Zenklusen"], "type": "Util", "val": "\\( 1/4 = 0.25 \\)"}
            ]
        }
    ]
        
    table_html = ""
    for group in table_data:
        entries = group["entries"]
        rowspan = len(entries)
        for i, entry in enumerate(entries):
            badge_class = "prob" if entry["type"] == "Prob" else "util"
            badge_text = "Prob" if entry["type"] == "Prob" else "Util"
            
            # Find paper index to create hyperlink
            p_idx = find_paper_index(papers, entry.get("search", []))
            if p_idx != -1:
                ref_html = f"<a class='table-link' onclick='goToPaper({p_idx})'>{entry['ref']}</a>"
            else:
                ref_html = entry['ref']
            
            row_class = "group-start" if i == 0 else ""
            table_html += f"                    <tr class='{row_class}'>\n"
            if i == 0:
                table_html += f"                        <td rowspan='{rowspan}' class='class-cell'>{group['class']}</td>\n"
            table_html += f"                        <td>{ref_html}</td>\n"
            table_html += f"                        <td style='text-align: center;'><span class='badge {badge_class}'>{badge_text}</span></td>\n"
            table_html += f"                        <td style='font-weight: 500;'>{entry['val']}</td>\n"
            table_html += "                    </tr>\n"

    reading_list_html = ""
    for i, paper in enumerate(papers):
        bibtex_id = f"bibtex-{i}"
        reading_list_html += f"""
            <div class="paper-card" id="paper-card-{i}">
                <h3 class="paper-title">{i+1}. {paper['title']}</h3>
                <div class="paper-authors">{t['by']} {paper['authors']}</div>
                <div class="paper-authors" style="color: var(--secondary-color); font-weight: 600; margin-top: -0.5rem; margin-bottom: 1rem;">
                    {paper.get('venue', 'arXiv preprint')}
                </div>
                <div class="paper-summary">
                    <strong>{t['abstract']}</strong> {paper['summary']}
                </div>
                <div class="action-buttons">
                    <a href="{paper['local_pdf']}" class="paper-link" target="_blank">{t['read_local']}</a>
                    <a href="{paper['pdf_url']}" class="paper-link secondary" target="_blank">{t['view_arxiv']}</a>
                    """
        if paper.get('dblp_url'):
            reading_list_html += f'<a href="{paper["dblp_url"]}" class="paper-link" style="background-color: #3182ce;" target="_blank">DBLP</a>'
        reading_list_html += f"""
                    <button class="paper-link dark bibtex-toggle" onclick="toggleBibtex('{bibtex_id}')">{t['show_bibtex']}</button>
                </div>
                <div id="{bibtex_id}" class="bibtex-container">{paper.get('bibtex', 'No BibTeX available.')}</div>
            </div>
"""

    # Add components to translation dict for replacement
    t['table_content'] = table_html
    t['reading_list_content'] = reading_list_html

    # Read template
    with open('template.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Replace placeholders
    for key, value in t.items():
        html = html.replace(f"{{{key}}}", str(value))

    filename = 'index.html' if is_en else 'index_es.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Successfully generated {filename}")

if __name__ == '__main__':
    generate_html(language="en")
    generate_html(language="es")
