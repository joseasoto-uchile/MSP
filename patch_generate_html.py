import re

with open('generate_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Translations
new_translations = '''
        "special_cases_title": "4. Special Cases and Small Parameters" if is_en else "4. Casos Especiales y Parámetros Pequeños",
        "special_cases_desc": "Certain matroid classes exhibit stronger competitive ratios for small ranks or parameters." if is_en else "Ciertas clases de matroides exhiben ratios competitivos más fuertes para rangos o parámetros pequeños.",
        "k_uniform_desc": "The multiple-choice secretary problem. Kleinberg (2005) achieves $1 - O(1/\sqrt{k})$. Albers and Ladewig (2019) provide explicit guarantees for small $k$." if is_en else "El problema de la secretaria de opción múltiple. Kleinberg (2005) logra $1 - O(1/\sqrt{k})$. Albers y Ladewig (2019) proveen garantías explícitas para $k$ pequeño.",
        "rank_2_desc": "General matroids of rank 2. Bérczi et al. (2025) achieved a $0.3462$ probability-competitive ratio." if is_en else "Matroides generales de rango 2. Bérczi et al. (2025) lograron un ratio de probabilidad de $0.3462$.",
        
        "variants_title": "Neighboring Models and Variants" if is_en else "Modelos Vecinos y Variantes",
        "variants_desc": "The following table groups results that fall outside the standard Matroid Secretary Problem (e.g. relaxed arrival orders, submodular objectives, or correlation)." if is_en else "La siguiente tabla agrupa resultados que se escapan del modelo estándar (ej. orden de llegada relajado, objetivos submodulares, o correlación).",
        "core_msp_title": "Core MSP Reading List" if is_en else "Lista de Lectura Principal",
        "related_work_title": "Related Work (Variants, Prophet Inequalities, Contention Resolution)" if is_en else "Trabajo Relacionado (Variantes, Desigualdades del Profeta, Resolución de Contienda)",
'''
content = content.replace('"msp_obj": r"<strong>Objective:', new_translations + '\n        "msp_obj": r"<strong>Objective:')

# 2. Update Table Data
new_table_data = '''
    table_data = [
        {
            "class": "Graphic",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": "\\\\( 1/16 = 0.0625 \\\\)"},
                {"ref": "Korula & Pál (2009)", "search": ["Korula", "Pál"], "type": "Util", "val": "\\\\( 1/(2e) \\\\approx 0.184 \\\\)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2018/2021)", "search": ["Soto", "Turkieltaub", "ordinal"], "type": "Prob", "val": "\\\\( 1/4 = 0.25 \\\\)"},
                {"ref": "Banihashem et al. (2025)", "search": ["Banihashem", "graphic"], "type": "Util", "val": "\\\\( 1/3.95 \\\\approx 0.253 \\\\) (Gen) / \\\\( 1/3.77 \\\\approx 0.265 \\\\) (Simple)"},
                {"ref": "Bérczi, Livanos, Soto, Verdugo (2025)", "search": ["Livanos", "labeling"], "type": "Prob", "val": "\\\\( 0.2504 \\\\) (Gen) / \\\\( 0.2693 \\\\) (Simple)"}
            ]
        },
        {
            "class": "Laminar",
            "entries": [
                {"ref": "Im & Wang (2011)", "search": ["Im", "Wang"], "type": "Util", "val": "\\\\( 3/16000 \\\\approx 0.00018 \\\\)"},
                {"ref": "Harris & Purohit (2013)", "search": ["Harris", "Purohit"], "type": "Util", "val": "\\\\( 0.053 \\\\)"},
                {"ref": "Jaillet, Soto, Zenklusen (2012/2016)", "search": ["Jaillet", "Zenklusen"], "type": "Util", "val": "\\\\( \\\\frac{1}{3\\\\sqrt{3}e} \\\\approx 0.070 \\\\)"},
                {"ref": "Ma, Tang, Wang (2013/2016)", "search": ["Tang", "submodular"], "type": "Util", "val": "\\\\( 1/9.6 \\\\approx 0.104 \\\\)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2018/2021)", "search": ["Soto", "ordinal"], "type": "Prob", "val": "\\\\( \\\\frac{1}{3\\\\sqrt{3}} \\\\approx 0.192 \\\\)"},
                {"ref": "Huang, Parsaeian, Zhu (2023)", "search": ["Parsaeian"], "type": "Util", "val": "\\\\( 1/4.75 \\\\approx 0.210 \\\\)"},
                {"ref": "Bérczi, Livanos, Soto, Verdugo (2025)", "search": ["Livanos", "labeling"], "type": "Prob", "val": "\\\\( 1 - \\\\ln(2) \\\\approx 0.3068 \\\\)"}
            ]
        },
        {
            "class": "Transversal",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": "\\\\( 1/16 = 0.0625 \\\\)"},
                {"ref": "Dimitrov & Plaxton (2012)", "search": ["Dimitrov", "Plaxton"], "type": "Util", "val": "\\\\( 1/8 = 0.125 \\\\)"},
                {"ref": "Kesselheim et al. (2013)", "search": ["Kesselheim"], "type": "Util", "val": "\\\\( 1/e \\\\approx 0.367 \\\\)"},
                {"ref": "Soto, Turkieltaub, Verdugo (2021)", "search": ["Soto", "ordinal"], "type": "Prob", "val": "\\\\( 1/e \\\\approx 0.367 \\\\)"}
            ]
        },
        {
            "class": "Rank-2 Matroids",
            "entries": [
                {"ref": "Bérczi, Livanos, Soto, Verdugo (2025)", "search": ["Livanos", "labeling"], "type": "Prob", "val": "\\\\( 0.3462 \\\\)"}
            ]
        },
        {
            "class": "Cographic",
            "entries": [
                {"ref": "Soto (2011)", "search": ["Soto", "random assignment"], "type": "Util", "val": "\\\\( 1/(3e) \\\\approx 0.122 \\\\)"}
            ]
        },
        {
            "class": "k-Uniform",
            "entries": [
                {"ref": "Dynkin (1963)", "search": ["Dynkin"], "type": "Prob", "val": "\\\\( 1/e \\\\approx 0.367 \\\\)"},
                {"ref": "Kleinberg (2005) / Soto et al. (2021)", "search": ["Kleinberg"], "type": "Prob", "val": "\\\\( 1 - O(\\\\sqrt{\\\\frac{\\\\log \\\\rho}{\\\\rho}}) \\\\)"},
                {"ref": "Chan, Chen, Jiang (2015)", "search": ["Jiang"], "type": "Prob", "val": "Exact thresholds (k-choice)"},
                {"ref": "Albers & Ladewig (2019/2021)", "search": ["Albers"], "type": "Prob", "val": "\\\\( > 1/e \\\\) for \\\\( k \\\\ge 2 \\\\)"}
            ]
        },
        {
            "class": "k-Fold Matroid Union",
            "entries": [
                {"ref": "Gujjar et al. (2025)", "search": ["Gujjar"], "type": "Prob", "val": "\\\\( 1 - O(\\\\sqrt{\\\\frac{\\\\log(n)}{k}}) \\\\)"}
            ]
        },
        {
            "class": "Partition",
            "entries": [
                {"ref": "Folklore", "search": ["Folklore"], "type": "Prob", "val": "\\\\( 1/e \\\\approx 0.367 \\\\)"}
            ]
        },
        {
            "class": "Truncated Partition",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": "\\\\( 1/e^2 \\\\approx 0.135 \\\\)"}
            ]
        },
        {
            "class": "Regular & Max-Flow Min-Cut",
            "entries": [
                {"ref": "Dinitz & Kortsarz (2012/2014)", "search": ["Dinitz"], "type": "Util", "val": "\\\\( 1/(9e) \\\\approx 0.0408 \\\\)"}
            ]
        },
        {
            "class": "K-Column Sparse Linear",
            "entries": [
                {"ref": "Soto (2011)", "search": ["Soto", "random assignment"], "type": "Util", "val": "\\\\( 1/(k \\\\cdot e) \\\\)"}
            ]
        },
        {
            "class": "Paving (Huynh & Nelson 2016/2020)",
            "entries": [
                {"ref": "Minor-Closed F_p-representable", "search": ["Huynh"], "type": "Util", "val": "\\\\( \\\\Omega(1) \\\\)"},
                {"ref": "Almost all matroids (Random)", "search": ["Huynh"], "type": "Util", "val": "\\\\( 1/(2+o(1)) \\\\approx 0.5 \\\\)"},
                {"ref": "Conditional on Paving Conjecture", "search": ["Huynh"], "type": "Util", "val": "\\\\( 1/(1+o(1)) \\\\approx 1.0 \\\\)"}
            ]
        },
        {
            "class": "Open Conjecture: General Matroids (Random Order)",
            "entries": [
                {"ref": "Babaioff, Immorlica, Kleinberg (2007)", "search": ["Babaioff", "Kleinberg", "2007"], "type": "Util", "val": "\\\\( \\\\Omega(1/\\\\log \\\\rho) \\\\)"},
                {"ref": "Chakraborty & Lachish (2012)", "search": ["Lachish", "Chakraborty"], "type": "Util", "val": "\\\\( \\\\Omega(1/\\\\sqrt{\\\\log \\\\rho}) \\\\)"},
                {"ref": "Lachish (2014) / Feldman et al. (2015)", "search": ["Feldman"], "type": "Util", "val": "\\\\( \\\\Omega(1/\\\\log \\\\log \\\\rho) \\\\)"}
            ]
        }
    ]

    variants_data = [
        {
            "class": "Ordinal Information Model",
            "entries": [
                {"ref": "Soto, Turkieltaub, Verdugo (2018/2021)", "search": ["Soto", "ordinal"], "type": "Prob", "val": "\\\\( \\\\Omega(1/\\\\log \\\\rho) \\\\)"}
            ]
        },
        {
            "class": "Random Assignment Model",
            "entries": [
                {"ref": "Soto (2011)", "search": ["Soto", "random assignment"], "type": "Util", "val": "\\\\( \\\\frac{e-1}{2e^2} \\\\approx 0.117 \\\\)"},
                {"ref": "Santiago, Sergeev, Zenklusen (2023)", "search": ["Santiago", "Sergeev"], "type": "Util", "val": "\\\\( \\\\Omega(1) \\\\) (Without knowing matroid)"}
            ]
        },
        {
            "class": "Free Order Model",
            "entries": [
                {"ref": "Jaillet, Soto, Zenklusen (2012/2016)", "search": ["Jaillet", "Zenklusen"], "type": "Util", "val": "\\\\( 1/4 = 0.25 \\\\)"}
            ]
        }
    ]

    def render_table(t_data):
        t_html = ""
        for group in t_data:
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
                t_html += f"                    <tr class='{row_class}'>\\n"
                if i == 0:
                    t_html += f"                        <td rowspan='{rowspan}' class='class-cell'>{group['class']}</td>\\n"
                t_html += f"                        <td>{ref_html}</td>\\n"
                t_html += f"                        <td style='text-align: center;'><span class='badge {badge_class}'>{badge_text}</span></td>\\n"
                t_html += f"                        <td style='font-weight: 500;'>{entry['val']}</td>\\n"
                t_html += "                    </tr>\\n"
        return t_html

    table_html = render_table(table_data)
    variants_table_html = render_table(variants_data)

    reading_list_html = ""
    related_work_html = ""
    for i, paper in enumerate(papers):
        bibtex_id = f"bibtex-{i}"
        
        # Split bibtex entries if multiple are present
        bib_str = paper.get('bibtex', 'No BibTeX available.')
        bib_html = f'<div id="{bibtex_id}" class="bibtex-container">{bib_str}</div>'

        card_html = f"""
            <div class="paper-card" id="paper-card-{i}">
                <h3 class="paper-title">{i+1}. {paper['title']}</h3>
                <div class="paper-authors">{{t['by']}} {paper['authors']}</div>
                <div class="paper-authors" style="color: var(--secondary-color); font-weight: 600; margin-top: -0.5rem; margin-bottom: 1rem;">
                    {paper.get('venue', 'arXiv preprint')}
                </div>
                <div class="paper-summary">
                    <strong>{{t['abstract']}}</strong> {paper['summary']}
                </div>
                <div class="action-buttons">
                    <a href="{paper['local_pdf']}" class="paper-link" target="_blank">{{t['read_local']}}</a>
                    <a href="{paper['pdf_url']}" class="paper-link secondary" target="_blank">{{t['view_arxiv']}}</a>
"""
        if paper.get('dblp_url'):
            card_html += f'                    <a href="{paper["dblp_url"]}" class="paper-link" style="background-color: #3182ce;" target="_blank">DBLP</a>\\n'
        card_html += f"""                    <button class="paper-link dark bibtex-toggle" onclick="toggleBibtex('{bibtex_id}')">{{t['show_bibtex']}}</button>
                </div>
                {bib_html}
            </div>
"""
        if paper.get('category') == 'A':
            reading_list_html += card_html
        else:
            related_work_html += card_html

    # Add components to translation dict for replacement
    t['table_content'] = table_html
    t['variants_table_content'] = variants_table_html
    t['reading_list_content'] = reading_list_html
    t['related_work_content'] = related_work_html
'''

# Use regex to replace the old block from table_data = [ ... ] up to the end of the reading_list_html loop
content = re.sub(r'    table_data = \[\s*\{.*?    t\[\'table_content\'\] = table_html\n    t\[\'reading_list_content\'\] = reading_list_html', new_table_data + "\n    t['table_content'] = table_html\n    t['variants_table_content'] = variants_table_html\n    t['reading_list_content'] = reading_list_html\n    t['related_work_content'] = related_work_html", content, flags=re.DOTALL)

with open('generate_html.py', 'w', encoding='utf-8') as f:
    f.write(content)
print("generate_html.py updated")
