import json
import os

def generate_html(language="en"):
    with open('papers_metadata.json', 'r', encoding='utf-8') as f:
        papers = json.load(f)
        
    is_en = (language == "en")
    
    # Translations
    t = {
        "title": "Survey on Matroid Secretary Problem",
        "subtitle": "Lecture Notes, Extensive Competitive Ratios and Reading List" if is_en else "Notas de Clase, Tabla de Competitividades (Extensiva) y Lista de Lectura",
        "lang_en": "English",
        "lang_es": "Español",
        "tab_notes": "Lecture Notes" if is_en else "Notas de Clase",
        "tab_ratios": "Extensive Ratios" if is_en else "Competitividades Extensivas",
        "tab_list": f"Reading List ({len(papers)})" if is_en else f"Lista de Lectura ({len(papers)})",
        "notes_title": "Lecture Notes",
        "matroids_title": "1. Matroids" if is_en else "1. Matroides",
        "matroids_desc": "A <strong>matroid</strong> is a combinatorial structure that generalizes the concept of linear independence in vector spaces. Formally, a matroid \\( M \\) is a pair \\( (E, \mathcal{I}) \\), where \\( E \\) is a finite set (the ground set) and \\( \mathcal{I} \\) is a family of subsets of \\( E \\) (called independent sets) that satisfies the following axioms:" if is_en else "Un <strong>matroide</strong> es una estructura combinatoria que generaliza el concepto de independencia lineal en espacios vectoriales. Formalmente, un matroide \\( M \\) es un par \\( (E, \mathcal{I}) \\), donde \\( E \\) es un conjunto finito (llamado conjunto base) y \\( \mathcal{I} \\) es una familia de subconjuntos de \\( E \\) (llamados conjuntos independientes) que satisface los siguientes axiomas:",
        "ax1": "The empty set is independent: \\( \emptyset \in \mathcal{I} \\)." if is_en else "El conjunto vacío es independiente: \\( \emptyset \in \mathcal{I} \\).",
        "ax2": "Hereditary property: If \\( A \in \mathcal{I} \\) and \\( B \subseteq A \\), then \\( B \in \mathcal{I} \\)." if is_en else "Propiedad hereditaria: Si \\( A \in \mathcal{I} \\) y \\( B \subseteq A \\), entonces \\( B \in \mathcal{I} \\).",
        "ax3": "Augmentation (or exchange) property: If \\( A, B \in \mathcal{I} \\) and \\( |A| > |B| \\), there exists an element \\( x \in A \setminus B \\) such that \\( B \cup \\{x\\} \in \mathcal{I} \\)." if is_en else "Propiedad de aumento (o intercambio): Si \\( A, B \in \mathcal{I} \\) y \\( |A| > |B| \\), existe un elemento \\( x \in A \setminus B \\) tal que \\( B \cup \\{x\\} \in \mathcal{I} \\).",
        "rank_desc": "The maximal independent sets of a matroid are called <strong>bases</strong>. All bases of a matroid have the same size, known as the <strong>rank</strong> of the matroid, denoted by \\( r(M) \\)." if is_en else "Los conjuntos independientes maximales de un matroide se llaman <strong>bases</strong>. Todas las bases de un matroide tienen el mismo tamaño, conocido como el <strong>rango</strong> del matroide, denotado por \\( r(M) \\).",
        "classic_title": "2. The Classical Secretary Problem" if is_en else "2. El Problema Clásico de la Secretaria",
        "classic_desc": "In the classical problem, \\( n \\) candidates are presented in a sequential and random order. A decision must be made immediately after interviewing each candidate on whether to hire or reject them. The goal is to maximize the probability of hiring the <strong>best</strong> candidate. The optimal algorithm involves observing the first \\( n/e \\) candidates without hiring anyone, and then hiring the first candidate who is better than all those observed so far. This algorithm achieves a success probability of \\( 1/e \\)." if is_en else "En el problema clásico, \\( n \\) candidatos se presentan de forma secuencial y aleatoria. Se debe decidir inmediatamente después de entrevistar a cada candidato si se le contrata o se le rechaza. El objetivo es maximizar la probabilidad de contratar al <strong>mejor</strong> candidato. El algoritmo óptimo consiste en observar a los primeros \\( n/e \\) candidatos sin contratar a ninguno, y luego contratar al primer candidato que sea mejor que todos los observados hasta el momento. Este algoritmo logra una probabilidad de éxito de \\( 1/e \\).",
        "msp_title": "3. The Matroid Secretary Problem" if is_en else "3. El Problema de la Secretaria en Matroides (Matroid Secretary Problem)",
        "msp_desc": "Introduced by Babaioff, Immorlica, and Kleinberg (2007), the <strong>Matroid Secretary Problem</strong> combines optimal stopping with combinatorial optimization. Suppose we have a matroid \\( M = (E, \mathcal{I}) \\) with a weight function \\( w: E \\to \mathbb{R}^+ \\) assigned to each element." if is_en else "Introducido por Babaioff, Immorlica y Kleinberg (2007), el <strong>Matroid Secretary Problem</strong> combina la parada óptima con la optimización combinatoria. Supongamos que tenemos un matroide \\( M = (E, \mathcal{I}) \\) con una función de peso \\( w: E \\to \mathbb{R}^+ \\) asignada a cada elemento.",
        "dynamics_title": "Problem Dynamics:" if is_en else "Dinámica del Problema:",
        "dyn1": "The elements of \\( E \\) are revealed sequentially in a uniformly random order." if is_en else "Los elementos de \\( E \\) se revelan de forma secuencial en un orden aleatorio uniforme.",
        "dyn2": "When an element \\( e \\) is revealed, its weight \\( w(e) \\) is discovered." if is_en else "Cuando un elemento \\( e \\) es revelado, se descubre su peso \\( w(e) \\).",
        "dyn3": "An irrevocable and immediate decision must be made: accept or reject \\( e \\)." if is_en else "Se debe tomar una decisión irrevocable e inmediata: aceptar o rechazar \\( e \\).",
        "dyn4": "The set of accepted elements at any time must be an independent set \\( I \in \mathcal{I} \\)." if is_en else "El conjunto de elementos aceptados en cualquier momento debe ser un conjunto independiente \\( I \in \mathcal{I} \\).",
        "msp_obj": "<strong>Objective:</strong> Design an online algorithm that maximizes the expected value of the selected elements, compared to the maximum weight basis offline. The grand conjecture (Matroid Secretary Conjecture) states that there exists an algorithm with a constant competitive ratio \\( O(1) \\) for any matroid." if is_en else "<strong>Objetivo:</strong> Diseñar un algoritmo online que maximice el valor esperado de los elementos seleccionados, comparado con la base de peso máximo en offline. La gran conjetura (Matroid Secretary Conjecture) afirma que existe un algoritmo con un factor de competitividad constante \\( O(1) \\) para cualquier matroide.",
        "ratios_title": "Competitive Ratios by Matroid Class and Model (Extensive)" if is_en else "Competitividades por Clase de Matroide y Modelo (Extensivo)",
        "ratios_desc": "The following table consolidates the chronological evolution and the best-known results for various matroid classes, extracted exhaustively from current literature and our reading list." if is_en else "La siguiente tabla consolida la evolución cronológica y los mejores resultados conocidos para diversas clases de matroides, extraídos exhaustivamente de la literatura actual y de nuestra lista de lectura.",
        "standard_model": "Standard Model (Zero Information, Random Order)" if is_en else "Modelo Estándar (Zero Information, Random Order)",
        "th_class": "Matroid Class" if is_en else "Clase de Matroide",
        "th_ratio": "Competitive Ratio / Guarantee" if is_en else "Ratio de Competitividad / Garantía",
        "th_ref": "References and Evolution" if is_en else "Referencias y Evolución",
        "other_models": "Other Models and Variants" if is_en else "Otros Modelos y Variantes",
        "th_model": "Model / Variant" if is_en else "Modelo / Variante",
        "reading_title": "Reading List and Bibliography" if is_en else "Lista de Lectura y Bibliografía",
        "reading_desc": f"Below are <strong>{len(papers)}</strong> relevant articles on the Matroid Secretary Problem, including their export in <strong>BibTeX</strong>." if is_en else f"A continuación se presentan <strong>{len(papers)}</strong> artículos relevantes sobre el Problema de la Secretaria en Matroides, incluyendo su exportación en <strong>BibTeX</strong>.",
        "by": "By:" if is_en else "Por:",
        "abstract": "Abstract:" if is_en else "Resumen:",
        "read_local": "Read Local PDF" if is_en else "Leer PDF Local",
        "view_arxiv": "View on arXiv" if is_en else "Ver en arXiv",
        "show_bibtex": "Show BibTeX" if is_en else "Mostrar BibTeX"
    }

    # Data for standard model table
    std_data = [
        ("General (Main Conjecture)" if is_en else "General (Conjetura Principal)", "\\( O(\\log \\log r) \\)", "BIK 2007 (\\( O(\\log r) \\)) &rarr; Chakraborty & Lachish 2012 (\\( O(\\sqrt{\\log r}) \\)) &rarr; Lachish 2014 / Feldman, Svensson, Zenklusen 2014 (\\( O(\\log \\log r) \\))."),
        ("Uniform (Classic / K-Secretaries)" if is_en else "Uniforme (Clásico / K-Secretarias)", "\\( 1/e \\) (Success Prob.) / \\( 1-O(1/\\sqrt{k}) \\)" if is_en else "\\( 1/e \\) (Prob. Éxito) / \\( 1-O(1/\\sqrt{k}) \\)", "Dynkin (Classic); Kleinberg 2005 (1-O(1/\\(\\sqrt{k}\\))); Gujjar et al., 2025 (k-Fold)."),
        ("Partition (Partition Matroid)" if is_en else "Partición (Partition Matroid)", f"Constant \\( 1-1/e \\)" if is_en else f"Constante \\( 1-1/e \\)", "Follows from classical, or \\( e/(e-1) \\) competitive." if is_en else "Directo del clásico, o \\( e/(e-1) \\) competitivo."),
        ("Graphic" if is_en else "Gráfico", "\\( 3.95 \\) (and \\( 3.77 \\) for simple graphs)" if is_en else "\\( 3.95 \\) (y \\( 3.77 \\) para grafos simples)", "BIK 2007 (\\( 16 \\)) &rarr; Korula & Pál 2009 (\\( 2e \\approx 5.43 \\)) &rarr; Soto, Turkieltaub, Verdugo 2018 (\\( 4 \\)) &rarr; Banihashem et al. 2025 (\\( 3.95 \\))."),
        ("Cographic" if is_en else "Cográfico", "\\( 3e \\approx 8.15 \\)", "Soto 2011."),
        ("Laminar" if is_en else "Laminar", "\\( 4.75 \\)-competitive" if is_en else "\\( 4.75 \\)-competitivo", "Im & Wang 2011 (\\( 16000/3 \\)) &rarr; Jaillet, Soto, Zenklusen 2012 (\\( 3\\sqrt{3}e \\approx 14.12 \\)) &rarr; Huang, Parsaeian, Zhu 2023 (\\( 4.75 \\))."),
        ("Transversal" if is_en else "Transversal", f"Constant \\( O(1) \\)" if is_en else f"Constante \\( O(1) \\)", "Dimand et al. 2006 / BIK 2007 (\\( 16 \\)); Ma, Tang, Wang 2011 (Constant also for submodular valuations)." if is_en else "Dimand et al. 2006 / BIK 2007 (\\( 16 \\)); Ma, Tang, Wang 2011 (Constante también para valoraciones submodulares)."),
        ("Regular & Max-Flow Min-Cut" if is_en else "Regular y Max-Flow Min-Cut", f"Constant \\( O(1) \\)" if is_en else f"Constante \\( O(1) \\)", "Dinitz & Kortsarz 2012 (Via Seymour's decomposition)." if is_en else "Dinitz & Kortsarz 2012 (Por descomposición de Seymour)."),
        ("Truncated Matroids" if is_en else "Truncado (Truncated Matroids)", f"Preserves \\( O(1) \\)" if is_en else f"Conserva \\( O(1) \\)", "If \\( M \\) admits a \\( c \\)-competitive algorithm, its truncation to rank \\( k \\) admits an \\( O(c) \\)-competitive one (Soto 2011)." if is_en else "Si \\( M \\) admite un algoritmo \\( c \\)-competitivo, su truncamiento a rango \\( k \\) admite uno \\( O(c) \\)-competitivo (Soto 2011)."),
        ("K-Column Sparse Linear" if is_en else "K-Column Sparse Linear", "\\( k \\cdot e \\)", "Soto 2011."),
        ("Paving & Almost All Matroids" if is_en else "Paving y Casi Todos los Matroides", "\\( 2+o(1) \\)", "Huynh & Nelson 2016 (For almost all representable matroids. Conjectured to include paving)." if is_en else "Huynh & Nelson 2016 (Para casi todos los matroides representables. Conjeturan incluir los paving)."),
        ("Matroid Intersection" if is_en else "Intersección de Matroides", "\\( O(1) \\) (If number of matroids is constant)" if is_en else "\\( O(1) \\) (Si el número de matroides es constante)", "Feldman, Svensson, Zenklusen 2017.")
    ]
    
    # Data for other models
    other_data = [
        ("Random Assignment", "General", f"Constant \\( O(1) \\) (approx. \\( 8.54 \\))" if is_en else f"Constante \\( O(1) \\) (aprox. \\( 8.54 \\))", "Soto 2011 (Knowing the matroid); Santiago, Sergeev, Zenklusen 2023 (Constant even without knowing the matroid)." if is_en else "Soto 2011 (Conociendo el matroide); Santiago, Sergeev, Zenklusen 2023 (Constante incluso sin conocer el matroide)."),
        ("Free Order", "General", "\\( 9 \\)-competitive" if is_en else "\\( 9 \\)-competitivo", "Jaillet, Soto, Zenklusen 2012. The algorithm chooses the interview order." if is_en else "Jaillet, Soto, Zenklusen 2012. El algoritmo elige el orden de las entrevistas."),
        ("Submodular Valuation" if is_en else "Valoración Submodular", "General", "Requires Shortlists or Restrictions" if is_en else "Requiere Shortlists o Restricciones", "Shadravan 2020 (Shortlists proportional to the rank achieve constant ratios)." if is_en else "Shadravan 2020 (Shortlists proporcionales al rango logran ratios constantes)."),
        ("Independence Systems (Downward Closed)" if is_en else "Sistemas de Independencia (Downward Closed)", "Independence Systems" if is_en else "Sistemas de Independencia", "\\( O(\\log n \\log r) \\)", "Rubinstein 2016 (Approximation for restrictions more general than matroids)." if is_en else "Rubinstein 2016 (Aproximación para restricciones más generales que los matroides).")
    ]
        
    html = f"""<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{t['title']}</title>
    
    <!-- MathJax for rendering LaTeX -->
    <script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
    <script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
    
    <style>
        :root {{
            --bg-color: #f4f4f9;
            --text-color: #333;
            --container-bg: #fff;
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --border-color: #e0e0e0;
        }}

        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
        }}

        header {{
            background-color: var(--primary-color);
            color: white;
            padding: 2rem 0;
            text-align: center;
            position: relative;
        }}
        
        .lang-switch {{
            position: absolute;
            top: 20px;
            right: 20px;
            background-color: rgba(255,255,255,0.2);
            padding: 5px 15px;
            border-radius: 20px;
        }}
        
        .lang-switch a {{
            color: white;
            text-decoration: none;
            font-weight: bold;
            margin: 0 5px;
        }}
        
        .lang-switch a.active {{
            text-decoration: underline;
            color: var(--secondary-color);
        }}

        h1 {{
            margin: 0;
            font-size: 2.5rem;
        }}

        .container {{
            max-width: 900px;
            margin: 2rem auto;
            background: var(--container-bg);
            padding: 2rem 4rem;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}

        /* Tabs Styles */
        .tabs {{
            display: flex;
            border-bottom: 2px solid var(--border-color);
            margin-bottom: 2rem;
            flex-wrap: wrap;
        }}

        .tab-button {{
            background: none;
            border: none;
            outline: none;
            padding: 1rem 2rem;
            font-size: 1.1rem;
            font-weight: bold;
            color: #777;
            cursor: pointer;
            transition: 0.3s;
            border-bottom: 3px solid transparent;
        }}

        .tab-button:hover {{
            color: var(--primary-color);
        }}

        .tab-button.active {{
            color: var(--secondary-color);
            border-bottom: 3px solid var(--secondary-color);
        }}

        .tab-content {{
            display: none;
            animation: fadeEffect 0.5s;
        }}

        .tab-content.active {{
            display: block;
        }}

        @keyframes fadeEffect {{
            from {{opacity: 0;}}
            to {{opacity: 1;}}
        }}

        h2 {{
            color: var(--primary-color);
            border-bottom: 2px solid var(--secondary-color);
            padding-bottom: 0.5rem;
            margin-top: 1rem;
        }}

        h3 {{
            color: var(--secondary-color);
            margin-top: 2rem;
        }}

        .definition {{
            background-color: #e8f4f8;
            border-left: 4px solid var(--secondary-color);
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0 4px 4px 0;
        }}

        .paper-card {{
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }}

        .paper-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        }}

        .paper-title {{
            font-size: 1.25rem;
            font-weight: bold;
            color: var(--primary-color);
            margin-top: 0;
        }}

        .paper-authors {{
            font-style: italic;
            color: #555;
            margin-bottom: 1rem;
        }}

        .paper-summary {{
            font-size: 0.95rem;
            color: #444;
        }}

        .paper-link {{
            display: inline-block;
            margin-top: 1rem;
            padding: 0.5rem 1rem;
            background-color: var(--secondary-color);
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-weight: bold;
        }}

        .paper-link:hover {{
            background-color: #2980b9;
        }}
        
        .bibtex-toggle {{
            background-color: #34495e;
            border: none;
            cursor: pointer;
        }}

        .bibtex-container {{
            display: none;
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 1rem;
            border-radius: 4px;
            margin-top: 1rem;
            font-family: monospace;
            white-space: pre-wrap;
            overflow-x: auto;
        }}

        /* Table Styles */
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
            font-size: 0.95em;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.05);
        }}

        table thead tr {{
            background-color: var(--primary-color);
            color: #ffffff;
            text-align: left;
        }}

        table th,
        table td {{
            padding: 12px 15px;
            border: 1px solid var(--border-color);
        }}

        table tbody tr {{
            border-bottom: 1px solid var(--border-color);
        }}

        table tbody tr:nth-of-type(even) {{
            background-color: #f9f9f9;
        }}
    </style>
</head>
<body>

    <header>
        <div class="lang-switch">
            <a href="index.html" class="{'active' if is_en else ''}">EN</a> | 
            <a href="index_es.html" class="{'active' if not is_en else ''}">ES</a>
        </div>
        <h1>{t['title']}</h1>
        <p>{t['subtitle']}</p>
    </header>

    <div class="container">
        <!-- Tabs Nav -->
        <div class="tabs">
            <button class="tab-button active" onclick="openTab(event, 'lecture-notes')">{t['tab_notes']}</button>
            <button class="tab-button" onclick="openTab(event, 'ratios-table')">{t['tab_ratios']}</button>
            <button class="tab-button" onclick="openTab(event, 'reading-list')">{t['tab_list']}</button>
        </div>

        <!-- Tab 1: Lecture Notes -->
        <section id="lecture-notes" class="tab-content active">
            <h2>{t['notes_title']}</h2>
            
            <h3>{t['matroids_title']}</h3>
            <p>{t['matroids_desc']}</p>
            <div class="definition">
                <ol>
                    <li>{t['ax1']}</li>
                    <li>{t['ax2']}</li>
                    <li>{t['ax3']}</li>
                </ol>
            </div>
            <p>{t['rank_desc']}</p>

            <h3>{t['classic_title']}</h3>
            <p>{t['classic_desc']}</p>

            <h3>{t['msp_title']}</h3>
            <p>{t['msp_desc']}</p>
            <div class="definition">
                <p><strong>{t['dynamics_title']}</strong></p>
                <ul>
                    <li>{t['dyn1']}</li>
                    <li>{t['dyn2']}</li>
                    <li>{t['dyn3']}</li>
                    <li>{t['dyn4']}</li>
                </ul>
            </div>
            <p>{t['msp_obj']}</p>
        </section>

        <!-- Tab 2: Ratios Table -->
        <section id="ratios-table" class="tab-content">
            <h2>{t['ratios_title']}</h2>
            <p>{t['ratios_desc']}</p>
            
            <h3>{t['standard_model']}</h3>
            <table>
                <thead>
                    <tr>
                        <th>{t['th_class']}</th>
                        <th>{t['th_ratio']}</th>
                        <th>{t['th_ref']}</th>
                    </tr>
                </thead>
                <tbody>
"""
    for c, r, ref in std_data:
        html += f"""
                    <tr>
                        <td><strong>{c}</strong></td>
                        <td>{r}</td>
                        <td>{ref}</td>
                    </tr>"""
    html += f"""
                </tbody>
            </table>

            <h3>{t['other_models']}</h3>
            <table>
                <thead>
                    <tr>
                        <th>{t['th_model']}</th>
                        <th>{t['th_class']}</th>
                        <th>{t['th_ratio']}</th>
                        <th>{t['th_ref']}</th>
                    </tr>
                </thead>
                <tbody>
"""
    for m, c, r, ref in other_data:
        html += f"""
                    <tr>
                        <td><strong>{m}</strong></td>
                        <td>{c}</td>
                        <td>{r}</td>
                        <td>{ref}</td>
                    </tr>"""
    html += f"""
                </tbody>
            </table>
        </section>

        <!-- Tab 3: Reading List -->
        <section id="reading-list" class="tab-content">
            <h2>{t['reading_title']}</h2>
            <p>{t['reading_desc']}</p>
"""

    for i, paper in enumerate(papers):
        bibtex_id = f"bibtex-{i}"
        html += f"""
            <div class="paper-card">
                <h3 class="paper-title">{i+1}. {paper['title']}</h3>
                <div class="paper-authors">{t['by']} {paper['authors']}</div>
                <div class="paper-summary">
                    <strong>{t['abstract']}</strong> {paper['summary']}
                </div>
                <a href="{paper['local_pdf']}" class="paper-link" target="_blank">{t['read_local']}</a>
                <a href="{paper['pdf_url']}" class="paper-link" target="_blank" style="background-color: #7f8c8d; margin-left: 10px;">{t['view_arxiv']}</a>
                <button class="paper-link bibtex-toggle" style="margin-left: 10px;" onclick="toggleBibtex('{bibtex_id}')">{t['show_bibtex']}</button>
                
                <div id="{bibtex_id}" class="bibtex-container">{paper.get('bibtex', 'No BibTeX available.')}</div>
            </div>
"""

    html += """
        </section>
    </div>

    <!-- Script for Tabs and BibTeX -->
    <script>
        function openTab(evt, tabId) {
            var i, tabcontent, tablinks;
            
            // Hide all tab content
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
                tabcontent[i].className = tabcontent[i].className.replace(" active", "");
            }
            
            // Remove active class from all buttons
            tablinks = document.getElementsByClassName("tab-button");
            for (i = 0; i < tablinks.length; i++) {
                tablinks[i].className = tablinks[i].className.replace(" active", "");
            }
            
            // Show current tab and add active class to button
            document.getElementById(tabId).style.display = "block";
            document.getElementById(tabId).className += " active";
            evt.currentTarget.className += " active";
        }

        function toggleBibtex(id) {
            var el = document.getElementById(id);
            if (el.style.display === "block") {
                el.style.display = "none";
            } else {
                el.style.display = "block";
            }
        }
    </script>
</body>
</html>
"""

    filename = 'index.html' if is_en else 'index_es.html'
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"Successfully generated {filename}")

if __name__ == '__main__':
    generate_html(language="en")
    generate_html(language="es")
