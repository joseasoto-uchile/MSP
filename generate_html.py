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
        "title": "Survey on Matroid Secretary Problem",
        "subtitle": "Lecture Notes, Exhaustive Chronological Guarantees and Reading List" if is_en else "Notas de Clase, Evolución Cronológica y Lista de Lectura",
        "lang_en": "English",
        "lang_es": "Español",
        "tab_notes": "Lecture Notes" if is_en else "Notas de Clase",
        "tab_ratios": "Chronological Bounds" if is_en else "Evolución de Competitividades",
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
            "class": "Uniform",
            "entries": [
                {"ref": "Dynkin (1963)", "search": ["Dynkin"], "type": "Prob", "val": "\\( 1/e \\approx 0.367 \\)"},
                {"ref": "Kleinberg (2005) / Soto et al. (2021)", "search": ["Kleinberg"], "type": "Prob", "val": "\\( 1 - O(\\sqrt{\\frac{\\log \\rho}{\\rho}}) \\)"},
                {"ref": "Gujjar et al. (2025)", "search": ["Gujjar"], "type": "Prob", "val": "\\( 1 - O(\\sqrt{\\frac{\\log(n)}{k}}) \\) (k-Fold)"}
            ]
        },
        {
            "class": "Partition",
            "entries": [
                {"ref": "Folklore", "search": ["Folklore"], "type": "Prob", "val": "\\( 1 - 1/e \\approx 0.632 \\)"}
            ]
        },
        {
            "class": "Regular & Max-Flow Min-Cut",
            "entries": [
                {"ref": "Dinitz & Kortsarz (2012)", "search": ["Dinitz"], "type": "Util", "val": "\\( O(1) \\)"}
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
            "class": "General Matroids (Random Order)",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": "\\( \\Omega(1/\\log \\rho) \\)"},
                {"ref": "Chakraborty & Lachish (2012)", "search": ["Lachish"], "type": "Util", "val": "\\( \\Omega(1/\\sqrt{\\log \\rho}) \\)"},
                {"ref": "Lachish (2014) / Feldman et al. (2014)", "search": ["Feldman"], "type": "Util", "val": "\\( \\Omega(1/\\log \\log \\rho) \\)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2021)", "search": ["Soto", "ordinal"], "type": "Prob", "val": "\\( \\Omega(1/\\log \\rho) \\) (Ordinal access)"}
            ]
        },
        {
            "class": "General (Random Assignment Model)",
            "entries": [
                {"ref": "Soto (2011)", "search": ["Soto", "random assignment"], "type": "Util", "val": "\\( \\frac{e-1}{2e^2} \\approx 0.117 \\)"},
                {"ref": "Santiago, Sergeev, Zenklusen (2023)", "search": ["Santiago", "Sergeev"], "type": "Util", "val": "\\( \\Omega(1) \\) (Without knowing matroid)"}
            ]
        },
        {
            "class": "General (Free Order Model)",
            "entries": [
                {"ref": "Jaillet, Soto, Zenklusen (2012)", "search": ["Jaillet", "Zenklusen"], "type": "Util", "val": "\\( 1/4 = 0.25 \\)"}
            ]
        }
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
            --primary-color: #1a365d;
            --secondary-color: #2b6cb0;
            --accent-color: #ebf8ff;
            --border-color: #e2e8f0;
        }}

        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            line-height: 1.6;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 0;
            scroll-behavior: smooth;
        }}

        header {{
            background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
            color: white;
            padding: 3rem 0;
            text-align: center;
            position: relative;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        
        .lang-switch {{
            position: absolute;
            top: 20px;
            right: 30px;
            background-color: rgba(255,255,255,0.15);
            padding: 8px 20px;
            border-radius: 30px;
            backdrop-filter: blur(5px);
        }}
        
        .lang-switch a {{
            color: white;
            text-decoration: none;
            font-weight: bold;
            margin: 0 8px;
            letter-spacing: 1px;
            opacity: 0.8;
            transition: opacity 0.2s;
        }}
        
        .lang-switch a:hover {{
            opacity: 1;
        }}
        
        .lang-switch a.active {{
            text-decoration: underline;
            text-underline-offset: 4px;
            opacity: 1;
        }}

        h1 {{
            margin: 0;
            font-size: 2.8rem;
            font-weight: 800;
            letter-spacing: -0.5px;
        }}
        
        header p {{
            font-size: 1.2rem;
            opacity: 0.9;
            margin-top: 0.5rem;
        }}

        .container {{
            max-width: 1000px;
            margin: -2rem auto 3rem;
            background: var(--container-bg);
            padding: 2.5rem 4rem;
            border-radius: 12px;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
            position: relative;
            z-index: 10;
        }}

        /* Tabs Styles */
        .tabs {{
            display: flex;
            border-bottom: 2px solid var(--border-color);
            margin-bottom: 2.5rem;
            gap: 10px;
        }}

        .tab-button {{
            background: none;
            border: none;
            outline: none;
            padding: 1rem 1.5rem;
            font-size: 1.1rem;
            font-weight: 600;
            color: #718096;
            cursor: pointer;
            transition: all 0.2s;
            border-bottom: 3px solid transparent;
            border-radius: 6px 6px 0 0;
        }}

        .tab-button:hover {{
            color: var(--primary-color);
            background-color: var(--accent-color);
        }}

        .tab-button.active {{
            color: var(--secondary-color);
            border-bottom: 3px solid var(--secondary-color);
            background-color: var(--accent-color);
        }}

        .tab-content {{
            display: none;
            animation: fadeIn 0.4s ease-in-out;
        }}

        .tab-content.active {{
            display: block;
        }}

        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(5px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        @keyframes highlightCard {{
            0% {{ box-shadow: 0 0 0 4px rgba(66, 153, 225, 0.6); transform: scale(1.02); }}
            100% {{ box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05); transform: scale(1); }}
        }}

        .highlight-animation {{
            animation: highlightCard 2s ease-out;
        }}

        h2 {{
            color: var(--primary-color);
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 0.5rem;
            margin-top: 1rem;
        }}

        h3 {{
            color: var(--secondary-color);
            margin-top: 2rem;
        }}

        .definition {{
            background-color: var(--accent-color);
            border-left: 4px solid var(--secondary-color);
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-radius: 0 8px 8px 0;
        }}

        /* Modern Table Styles */
        table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            margin: 2rem 0;
            font-size: 0.95em;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            border: 1px solid var(--border-color);
        }}

        table thead tr {{
            background-color: var(--primary-color);
            color: #ffffff;
            text-align: left;
        }}

        table th {{
            padding: 15px 20px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            font-size: 0.85em;
        }}

        table td {{
            padding: 12px 20px;
            border-bottom: 1px solid var(--border-color);
            border-right: 1px solid var(--border-color);
        }}
        
        table td:last-child {{
            border-right: none;
        }}

        table tbody tr:last-child td {{
            border-bottom: none;
        }}

        table tbody tr:hover td:not(.class-cell) {{
            background-color: #f7fafc;
        }}
        
        td.class-cell {{
            background-color: #edf2f7;
            font-weight: 700;
            color: var(--primary-color);
            vertical-align: middle;
            font-size: 1.05em;
        }}
        
        a.table-link {{
            color: var(--secondary-color);
            text-decoration: none;
            font-weight: 600;
            border-bottom: 1px dashed var(--secondary-color);
            cursor: pointer;
        }}
        
        a.table-link:hover {{
            color: var(--primary-color);
            border-bottom-style: solid;
        }}
        
        .badge {{
            display: inline-block;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: bold;
        }}
        
        .badge.prob {{
            background-color: #e6ffed;
            color: #1e7e34;
            border: 1px solid #c3e6cb;
        }}
        
        .badge.util {{
            background-color: #e2e3e5;
            color: #383d41;
            border: 1px solid #d6d8db;
        }}

        .paper-card {{
            border: 1px solid var(--border-color);
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            background: white;
            transition: all 0.3s ease;
        }}

        .paper-card:hover {{
            transform: translateY(-3px);
            box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
            border-color: #cbd5e0;
        }}

        .paper-title {{
            font-size: 1.3rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-top: 0;
            line-height: 1.3;
        }}

        .paper-authors {{
            font-style: italic;
            color: #4a5568;
            margin-bottom: 1rem;
            font-weight: 500;
        }}

        .paper-summary {{
            font-size: 0.95rem;
            color: #4a5568;
            line-height: 1.6;
        }}

        .action-buttons {{
            margin-top: 1.2rem;
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .paper-link {{
            display: inline-block;
            padding: 0.6rem 1.2rem;
            background-color: var(--secondary-color);
            color: white;
            text-decoration: none;
            border-radius: 6px;
            font-weight: 600;
            font-size: 0.9rem;
            transition: background-color 0.2s;
            border: none;
            cursor: pointer;
        }}

        .paper-link:hover {{
            background-color: #2c5282;
        }}
        
        .paper-link.secondary {{
            background-color: #718096;
        }}
        
        .paper-link.secondary:hover {{
            background-color: #4a5568;
        }}
        
        .paper-link.dark {{
            background-color: #2d3748;
        }}
        
        .paper-link.dark:hover {{
            background-color: #1a202c;
        }}

        .bibtex-container {{
            display: none;
            background-color: #1a202c;
            color: #e2e8f0;
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 1rem;
            font-family: 'Courier New', Courier, monospace;
            font-size: 0.9rem;
            white-space: pre-wrap;
            overflow-x: auto;
            border-left: 4px solid var(--secondary-color);
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
            <button class="tab-button active" id="btn-lecture-notes" onclick="openTab(event, 'lecture-notes')">{t['tab_notes']}</button>
            <button class="tab-button" id="btn-ratios-table" onclick="openTab(event, 'ratios-table')">{t['tab_ratios']}</button>
            <button class="tab-button" id="btn-reading-list" onclick="openTab(event, 'reading-list')">{t['tab_list']}</button>
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
            
            <table>
                <thead>
                    <tr>
                        <th>{t['th_class']}</th>
                        <th>{t['th_ref']}</th>
                        <th style="width: 120px; text-align: center;">{t['th_type']}</th>
                        <th>{t['th_guarantee']}</th>
                    </tr>
                </thead>
                <tbody>
"""
    
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
            
            html += "                    <tr>\n"
            if i == 0:
                html += f"                        <td rowspan='{rowspan}' class='class-cell'>{group['class']}</td>\n"
            html += f"                        <td>{ref_html}</td>\n"
            html += f"                        <td style='text-align: center;'><span class='badge {badge_class}'>{badge_text}</span></td>\n"
            html += f"                        <td style='font-weight: 500;'>{entry['val']}</td>\n"
            html += "                    </tr>\n"

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
                    <button class="paper-link dark bibtex-toggle" onclick="toggleBibtex('{bibtex_id}')">{t['show_bibtex']}</button>
                </div>
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
            
            if (evt && evt.currentTarget) {
                evt.currentTarget.className += " active";
            } else {
                // If triggered by JS directly without event
                document.getElementById('btn-' + tabId).className += " active";
            }
        }

        function toggleBibtex(id) {
            var el = document.getElementById(id);
            if (el.style.display === "block") {
                el.style.display = "none";
            } else {
                el.style.display = "block";
            }
        }
        
        function goToPaper(idx) {
            // Switch tab
            openTab(null, 'reading-list');
            
            // Wait for display to apply
            setTimeout(() => {
                var card = document.getElementById('paper-card-' + idx);
                card.scrollIntoView({ behavior: 'smooth', block: 'center' });
                
                // Add highlight animation
                card.classList.remove('highlight-animation');
                // Trigger reflow
                void card.offsetWidth;
                card.classList.add('highlight-animation');
            }, 100);
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
