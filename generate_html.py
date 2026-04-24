import json
import os
import re

def find_paper_index(papers, search_terms):
    for i, p in enumerate(papers):
        text_to_search = (p['authors'] + " " + p['title'] + " " + p.get('venue', '')).lower()
        if all(term.lower() in text_to_search for term in search_terms):
            return i
    return -1

def generate_html(language="en"):
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)
        
    is_en = (language == "en")
    
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
        
        "special_cases_title": "4. Special Cases and Small Parameters" if is_en else "4. Casos Especiales y Parámetros Pequeños",
        "special_cases_desc": "Certain matroid classes exhibit stronger competitive ratios for small ranks or parameters." if is_en else "Ciertas clases de matroides exhiben ratios competitivos más fuertes para rangos o parámetros pequeños.",
        "k_uniform_desc": r"The multiple-choice secretary problem. Kleinberg (2005) achieves \( 1 - O(1/\sqrt{k}) \). Albers and Ladewig (2019) provide explicit guarantees for small \( k \)." if is_en else r"El problema de la secretaria de opción múltiple. Kleinberg (2005) logra \( 1 - O(1/\sqrt{k}) \). Albers y Ladewig (2019) proveen garantías explícitas para \( k \) pequeño.",
        "rank_2_desc": r"General matroids of rank 2. Bérczi et al. (2025) achieved a \( 0.3462 \) probability-competitive ratio." if is_en else r"Matroides generales de rango 2. Bérczi et al. (2025) lograron un ratio de probabilidad de \( 0.3462 \).",
        
        "ratios_title": "Chronological Progression of Competitive Guarantees" if is_en else "Evolución Cronológica de Garantías Competitivas",
        "ratios_desc": r"The table below groups results by Matroid Class, detailing the exact constant or formula achieved by each paper historically. All constants have been normalized so that <strong>values \( \le 1 \) represent the approximation factor</strong> (i.e. \( 1/\alpha \) where \( \alpha \) is the traditional competitive ratio \( \ge 1 \)). We also note whether the guarantee is <strong>Probability-Competitive</strong> (\( p \)) or the traditional <strong>Utility-Competitive Ratio</strong>." if is_en else r"La siguiente tabla agrupa los resultados por clase de matroide, detallando la constante exacta o fórmula alcanzada por cada paper a lo largo de la historia. Todas las constantes han sido normalizadas para que <strong>valores \( \le 1 \) representen el factor de aproximación</strong> (es decir, \( 1/\alpha \) donde \( \alpha \) es el ratio competitivo tradicional \( \ge 1 \)). Se indica si la garantía es <strong>Probability-Competitive</strong> (\( p \)) o el tradicional <strong>Ratio de Utilidad</strong>.",
        
        "th_class": "Matroid Class" if is_en else "Clase de Matroide",
        "th_ref": "Reference" if is_en else "Referencia",
        "th_type": "Guarantee Type" if is_en else "Tipo de Garantía",
        "th_guarantee": r"Exact Bound ($\le 1$)" if is_en else r"Cota Exacta ($\le 1$)",
        
        "variants_title": "Neighboring Models and Variants" if is_en else "Modelos Vecinos y Variantes",
        "variants_desc": "The following table groups results that fall outside the standard Matroid Secretary Problem (e.g. relaxed arrival orders, submodular objectives, or correlation)." if is_en else "La siguiente tabla agrupa resultados que se escapan del modelo estándar (ej. orden de llegada relajado, objetivos submodulares, o correlación).",
        
        "reading_title": "Reading List and Bibliography" if is_en else "Lista de Lectura y Bibliografía",
        "reading_desc": f"Below are <strong>{len(papers)}</strong> relevant articles on the Matroid Secretary Problem, including their export in <strong>BibTeX</strong>." if is_en else f"A continuación se presentan <strong>{len(papers)}</strong> artículos relevantes sobre el Problema de la Secretaria en Matroides, incluyendo su exportación en <strong>BibTeX</strong>.",
        
        "core_msp_title": "Core MSP Reading List" if is_en else "Lista de Lectura Principal",
        "related_work_title": "Related Work (Variants, Prophet Inequalities, Contention Resolution)" if is_en else "Trabajo Relacionado (Variantes, Desigualdades del Profeta, Resolución de Contienda)",
        
        "by": "By:" if is_en else "Por:",
        "abstract": "Abstract:" if is_en else "Resumen:",
        "read_local": "PDF",
        "view_arxiv": "View on arXiv",
        "show_bibtex": "BibTeX \u25be",
        "table_note": "All guarantees are normalized as values \u2264 1. Labels denote notions: Prob (\(p\)), Util (\(u\)), Ordinal (\(o\)). Since \(p\) implies \(u\), every \(p\) row also provides the corresponding utility guarantee." if is_en else "Todas las garant\u00edas est\u00e1n normalizadas como valores \u2264 1. Las etiquetas denotan nociones: Prob (\(p\)), Util (\(u\)), Ordinal (\(o\)). Como \(p\) implica \(u\), cada fila \(p\) tambi\u00e9n otorga la correspondiente garant\u00eda de utilidad."
    }

    table_data = [
        {
            "class": "General Matroids (Random Order)",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": r"\( \Omega(1/\log \rho) \)"},
                {"ref": "Chakraborty & Lachish (2012)", "search": ["Lachish", "Chakraborty"], "type": "Util", "val": r"\( \Omega(1/\sqrt{\log \rho}) \)"},
                {"ref": "Lachish (2014) / Feldman et al. (2015)", "search": ["Feldman"], "type": "Util", "val": r"\( \Omega(1/\log \log \rho) \)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2018/2021)", "search": ["Soto", "ordinal"], "type": "Prob", "val": r"\( \Omega(1/\log \rho) \)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2018/2021)", "search": ["Soto", "ordinal"], "type": "Ordinal", "val": r"\( \Omega(1/\log \log \rho) \)"}
            ]
        },
        {
            "class": "Graphic",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": r"\( 1/16 = 0.0625 \)"},
                {"ref": "Korula & P\u00e1l (2009)", "search": ["Korula", "P\u00e1l"], "type": "Util", "val": r"\( 1/(2e) \approx 0.184 \)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2018/2021)", "search": ["Soto", "Turkieltaub", "ordinal"], "type": "Prob", "val": r"\( 1/4 = 0.25 \)"},
                {"ref": "Banihashem et al. (2025)", "search": ["Banihashem", "graphic"], "type": "Prob", "val": r"\( 1/3.95 \approx 0.253 \) (General graphs) / \( 1/3.77 \approx 0.265 \) (Simple graphs)"},
                {"ref": "B\u00e9rczi, Livanos, Soto, Verdugo (2025)", "search": ["Livanos", "labeling"], "type": "Prob", "val": r"\( 0.2504 \) (General graphs) / \( 0.2693 \) (Simple graphs)"}
            ]
        },
        {
            "class": "Laminar",
            "entries": [
                {"ref": "Im & Wang (2011)", "search": ["Im", "Wang"], "type": "Util", "val": r"\( 3/16000 \approx 0.00018 \)"},
                {"ref": "Harris & Purohit (2013)", "search": ["Harris", "Purohit"], "type": "Util", "val": r"\( 0.053 \)"},
                {"ref": "Jaillet, Soto, Zenklusen (2012/2016)", "search": ["Jaillet", "Zenklusen"], "type": "Util", "val": r"\( \frac{1}{3\sqrt{3}e} \approx 0.070 \)"},
                {"ref": "Ma, Tang, Wang (2013/2016)", "search": ["Tang", "submodular"], "type": "Util", "val": r"\( 1/9.6 \approx 0.104 \)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2018/2021)", "search": ["Soto", "ordinal"], "type": "Prob", "val": r"\( \frac{1}{3\sqrt{3}} \approx 0.192 \)"},
                {"ref": "Huang, Parsaeian, Zhu (ESA 2024)", "search": ["Parsaeian"], "type": "Prob", "val": r"\( 1/4.75 \approx 0.2105 \)"},
                {"ref": "B\u00e9rczi, Livanos, Soto, Verdugo (2025)", "search": ["Livanos", "labeling"], "type": "Prob", "val": r"\( 1 - \ln(2) \approx 0.3068 \)"}
            ]
        },
        {
            "class": "Transversal",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": r"\( 1/16 = 0.0625 \)"},
                {"ref": "Dimitrov & Plaxton (2012)", "search": ["Dimitrov", "Plaxton"], "type": "Util", "val": r"\( 1/8 = 0.125 \)"},
                {"ref": "Kesselheim et al. (ESA 2013)", "search": ["Kesselheim"], "type": "Util", "val": r"\( 1/e \approx 0.367 \)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2021)", "search": ["Soto", "ordinal"], "type": "Prob", "val": r"\( 1/e \approx 0.367 \)"}
            ]
        },
        {
            "class": "Rank-2 Matroids",
            "entries": [
                {"ref": "Bérczi, Livanos, Soto, Verdugo (2025)", "search": ["Livanos", "labeling"], "type": "Prob", "val": r"\( 0.3462 \)"}
            ]
        },
        {
            "class": "Cographic",
            "entries": [
                {"ref": "Soto (2011)", "search": ["Soto", "random assignment"], "type": "Util", "val": r"\( 1/(3e) \approx 0.122 \)"}
            ]
        },
        {
            "class": "k-Uniform",
            "entries": [
                {"ref": "Dynkin (1963)", "search": ["Dynkin"], "type": "Prob", "val": r"\( 1/e \approx 0.367 \)"},
                {"ref": "Kleinberg (2005) / Soto et al. (2021)", "search": ["Kleinberg"], "type": "Prob", "val": r"\( 1 - O(\sqrt{\frac{\log k}{k}}) \)"},
                {"ref": "Chan, Chen, Jiang (2015)", "search": ["Jiang"], "type": "Prob", "val": r"Exact thresholds (k-choice)"},
                {"ref": "Albers & Ladewig (2019/2021)", "search": ["Albers"], "type": "Prob", "val": r"\( > 1/e \) for \( k \ge 2 \)"}
            ]
        },
        {
            "class": "k-Fold Matroid Union",
            "entries": [
                {"ref": "Gujjar et al. (arXiv 2025 / SOSA 2026)", "search": ["Gujjar"], "type": "Prob", "val": r"\( 1 - O(\sqrt{\frac{\log(n)}{k}}) \)"}
            ]
        },
        {
            "class": "Partition",
            "entries": [
                {"ref": "Folklore", "search": ["Folklore"], "type": "Prob", "val": r"\( 1/e \approx 0.367 \)"}
            ]
        },
        {
            "class": "Truncated Partition",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": r"\( 1/e^2 \approx 0.135 \)"}
            ]
        },
        {
            "class": "Regular & Max-Flow Min-Cut",
            "entries": [
                {"ref": "Dinitz & Kortsarz (2012/2014)", "search": ["Dinitz"], "type": "Util", "val": r"\( 1/(9e) \approx 0.0408 \)"}
            ]
        },
        {
            "class": "K-Column Sparse Linear",
            "entries": [
                {"ref": "Soto (2011)", "search": ["Soto", "random assignment"], "type": "Util", "val": r"\( 1/(k \cdot e) \)"}
            ]
        },
        {
            "class": "Paving (Huynh & Nelson 2016/2020)",
            "entries": [
                {"ref": "Minor-Closed F_p-representable", "search": ["Huynh"], "type": "Util", "val": r"\( \Omega(1) \)"},
                {"ref": "Almost all matroids (Random)", "search": ["Huynh"], "type": "Util", "val": r"\( 1/(2+o(1)) \approx 0.5 \)"},
                {"ref": "Conditional on Paving Conjecture", "search": ["Huynh"], "type": "Util", "val": r"\( 1/(1+o(1)) \approx 1.0 \)"}
            ]
        },
        }
    ]

    variants_data = [
        {
            "class": "Random Assignment Model",
            "entries": [
                {"ref": "Soto (2011)", "search": ["Soto", "random assignment"], "type": "Util", "val": r"\( (e-1)/(2e^2) \approx 0.117 \)"},
                {"ref": "Santiago, Sergeev, Zenklusen (2023)", "search": ["Santiago", "Sergeev"], "type": "Util", "val": r"\( \Omega(1) \) (Random Assignment Model, matroid initially unknown)"}
            ]
        },
        {
            "class": "Free Order Model",
            "entries": [
                {"ref": "Jaillet, Soto, Zenklusen (2012/2016)", "search": ["Jaillet", "Zenklusen"], "type": "Util", "val": r"\( 1/4 = 0.25 \)"}
            ]
        }
    ]

    def render_table(t_data):
        t_html = ""
        for group in t_data:
            entries = group["entries"]
            rowspan = len(entries)
            for i, entry in enumerate(entries):
                badge_class = entry["type"].lower()
                badge_text = entry["type"]
                
                p_idx = find_paper_index(papers, entry.get("search", []))
                if p_idx != -1:
                    card_anchor = f"paper-card-{p_idx}"
                    ref_html = (f"<a class='table-link' href='#{card_anchor}' "
                                f"onclick='goToPaper({p_idx}); return false;'>{entry['ref']}</a>")
                else:
                    ref_html = entry['ref']
                
                row_class = "group-start" if i == 0 else ""
                t_html += f"                    <tr class='{row_class}'>\n"
                if i == 0:
                    t_html += f"                        <td rowspan='{rowspan}' class='class-cell'>{group['class']}</td>\n"
                t_html += f"                        <td>{ref_html}</td>\n"
                t_html += f"                        <td style='text-align: center;'><span class='badge {badge_class}'>{badge_text}</span></td>\n"
                t_html += f"                        <td style='font-weight: 500;'>{entry['val']}</td>\n"
                t_html += "                    </tr>\n"
        return t_html

    table_html = render_table(table_data)
    variants_table_html = render_table(variants_data)

    reading_list_html = ""
    related_work_html = ""
    core_idx = 1
    related_idx = 1
    
    # Collect all unique tags
    all_tags = set()
    for p in papers:
        for t_val in p.get('tags', []):
            all_tags.add(t_val)
    t['all_tags'] = sorted(list(all_tags))

    for i, paper in enumerate(papers):
        bibtex_id = f"bibtex-{i}"
        
        tags_html = ""
        tags_list = paper.get('tags', [])
        for tag in tags_list:
            tags_html += f'<span class="badge tag-badge">{tag}</span> '
        tags_data = ",".join(tags_list)
        
        bib_data = paper.get('bibtex', 'No BibTeX available.')
        if isinstance(bib_data, list):
            bibs = bib_data
        else:
            bibs = [bib_data]

        # Build BibTeX container with copy button and <pre> blocks
        bib_inner = ''
        for j, bib_block in enumerate(bibs):
            label = paper.get('versions', [])
            lbl = label[j] if j < len(label) else f'Version {j+1}'
            bib_inner += f'<span class="bibtex-section-label"># {lbl}</span>'
            bib_inner += f'<pre>{bib_block}</pre>'
        bib_html = (f'<div id="{bibtex_id}" class="bibtex-container">'
                    f'<button class="bibtex-copy-btn" onclick="copyBibtex(this)">Copy</button>'
                    f'{bib_inner}</div>')

        is_core = (paper.get('category') == 'A')
        display_idx = core_idx if is_core else related_idx
        if is_core:
            core_idx += 1
        else:
            related_idx += 1

        has_arxiv = 'arxiv.org' in paper.get('pdf_url', '')
        has_local = paper.get('local_pdf', '#') not in ('#', '')

        # Action buttons
        btn_local  = (f'<a href="{paper["local_pdf"]}" class="paper-link" target="_blank">{t["read_local"]}</a>'
                      if has_local else '')
        btn_arxiv  = (f'<a href="{paper["pdf_url"]}" class="paper-link secondary" target="_blank">{t["view_arxiv"]}</a>'
                      if has_arxiv else '')
        btn_dblp   = (f'<a href="{paper["dblp_url"]}" class="paper-link" style="background-color:#3182ce;" target="_blank">DBLP</a>'
                      if paper.get('dblp_url') else '')
        btn_bib    = (f'<button class="paper-link dark bibtex-toggle" '
                      f'data-show-label="BibTeX \u25be" data-hide-label="BibTeX \u25b4" '
                      f'onclick="toggleBibtex(\'{bibtex_id}\')">BibTeX &#9660;</button>')

        card_id = f'paper-card-{i}'
        versions_li = "".join(f"<li>{v}</li>" for v in paper.get('versions', [paper.get('venue', 'arXiv preprint')]))

        card_html = f"""
            <div class="paper-card filterable-card" id="{card_id}" data-tags="{tags_data}">
                <div class="card-header" onclick="toggleCard('{card_id}')">
                    <div class="card-header-left">
                        <div style="float:right;margin-left:8px;">{tags_html}</div>
                        <h3 class="paper-title" style="margin-top:0;">{paper['title']}
                            <a class="permalink" href="#{card_id}" data-id="{card_id}" title="Copy link" onclick="event.stopPropagation()">&#128279;</a>
                        </h3>
                        <div class="paper-authors">{t['by']} {paper['authors']}</div>
                    </div>
                    <button class="card-toggle-btn" onclick="event.stopPropagation(); toggleCard('{card_id}')" title="Expand/collapse">&#9660; Hide</button>
                </div>
                <div class="card-body collapsed">
                    <ul class="paper-versions" style="color:var(--secondary-color);font-weight:600;margin-top:0.3rem;margin-bottom:0.8rem;list-style-type:disc;padding-left:20px;font-size:0.9em;">
                        {versions_li}
                    </ul>
                    <div class="paper-summary">
                        <strong>{t['abstract']}</strong> {paper['summary']}
                    </div>
                    <div class="action-buttons">
                        {btn_local}{btn_arxiv}{btn_dblp}{btn_bib}
                    </div>
                    {bib_html}
                </div>
            </div>
"""
        if paper.get('category') == 'A':
            reading_list_html += card_html
        else:
            related_work_html += card_html
            
    reading_list_html = f'<div id="reading-list-container">{reading_list_html}</div>'
    related_work_html = f'<div id="related-work-container">{related_work_html}</div>'

    tag_buttons_html = "<button class='tag-filter-btn active' data-tag='All' onclick='filterByTag(\"All\")'>All</button>"
    for tag in t['all_tags']:
        tag_buttons_html += f"<button class='tag-filter-btn' data-tag='{tag}' onclick='filterByTag(\"{tag}\")'>{tag}</button>"
    t['tag_filters_html'] = tag_buttons_html

    t['table_content'] = table_html
    t['variants_table_content'] = variants_table_html
    t['reading_list_content'] = reading_list_html
    t['related_work_content'] = related_work_html

    with open('template.html', 'r', encoding='utf-8') as f:
        html = f.read()

    for key, value in t.items():
        html = html.replace(f"{{{key}}}", str(value))

    filename = 'index.html' if is_en else 'index_es.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Successfully generated {filename}")

if __name__ == '__main__':
    generate_html(language="en")
    generate_html(language="es")
