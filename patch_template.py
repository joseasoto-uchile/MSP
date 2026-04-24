import os

with open('template.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Add CSS
css = '''
        .tag-badge {
            background-color: #edf2f7;
            color: #4a5568;
            padding: 0.2rem 0.5rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            display: inline-block;
        }
        .tag-filter-btn {
            background-color: white;
            border: 1px solid #cbd5e0;
            padding: 0.3rem 0.8rem;
            margin: 0.2rem;
            border-radius: 9999px;
            cursor: pointer;
            font-size: 0.85rem;
            transition: all 0.2s;
        }
        .tag-filter-btn:hover {
            background-color: #edf2f7;
        }
        .tag-filter-btn.active {
            background-color: #3182ce;
            color: white;
            border-color: #3182ce;
        }
        details > summary {
            cursor: pointer;
            outline: none;
            user-select: none;
        }
        details > summary h2, details > summary h3 {
            display: inline-block;
        }
'''
html = html.replace('</style>', css + '</style>')

# 2. Make tables collapsible
# First table
t1_start = '<h2>{ratios_title}</h2>'
t1_end = '</table>\n            </div>'
t1_block = html[html.find(t1_start):html.find(t1_end) + len(t1_end)]
t1_new = '<details open>\n                <summary>' + t1_start + '</summary>\n                ' + t1_block[len(t1_start):] + '\n            </details>'
html = html.replace(t1_block, t1_new)

# Second table
t2_start = '<h3 style="margin-top: 3rem;">{variants_title}</h3>'
t2_end = '</table>\n            </div>'
idx_start = html.find(t2_start)
idx_end = html.find(t2_end, idx_start) + len(t2_end)
t2_block = html[idx_start:idx_end]
t2_new = '<details open style="margin-top: 3rem;">\n                <summary><h3 style="margin-top: 0;">{variants_title}</h3></summary>\n                ' + t2_block[len(t2_start):] + '\n            </details>'
html = html.replace(t2_block, t2_new)

# 3. Add {tag_filters_html}
search_container = '<div class="search-container">\n                <input type="text" id="paperSearch" class="search-input" placeholder="{search_placeholder}" onkeyup="filterPapers()">\n            </div>'
html = html.replace(search_container, search_container + '\n            {tag_filters_html}')

# 4. Update JS logic
js_old = '''        function filterPapers() {
            var input, filter, cards, title, authors, summary, i, txtValue;
            input = document.getElementById("paperSearch");
            filter = input.value.toLowerCase();
            cards = document.getElementsByClassName("paper-card");
            
            for (i = 0; i < cards.length; i++) {
                title = cards[i].querySelector(".paper-title");
                authors = cards[i].querySelector(".paper-authors");
                summary = cards[i].querySelector(".paper-summary");
                
                txtValue = (title ? title.textContent || title.innerText : "") + " " + 
                           (authors ? authors.textContent || authors.innerText : "") + " " +
                           (summary ? summary.textContent || summary.innerText : "");
                           
                if (txtValue.toLowerCase().indexOf(filter) > -1) {
                    cards[i].style.display = "";
                } else {
                    cards[i].style.display = "none";
                }
            }
        }'''

js_new = '''        let activeTag = "All";

        function filterByTag(tag) {
            activeTag = tag;
            let btns = document.getElementsByClassName('tag-filter-btn');
            for (let i = 0; i < btns.length; i++) {
                if (btns[i].innerText === tag) {
                    btns[i].classList.add('active');
                } else {
                    btns[i].classList.remove('active');
                }
            }
            filterPapers();
        }

        function filterPapers() {
            var input, filter, cards, title, authors, summary, i, txtValue, tags;
            input = document.getElementById("paperSearch");
            filter = input.value.toLowerCase();
            cards = document.getElementsByClassName("filterable-card");
            
            for (i = 0; i < cards.length; i++) {
                title = cards[i].querySelector(".paper-title");
                authors = cards[i].querySelector(".paper-authors");
                summary = cards[i].querySelector(".paper-summary");
                tags = cards[i].getAttribute("data-tags") || "";
                
                txtValue = (title ? title.textContent || title.innerText : "") + " " + 
                           (authors ? authors.textContent || authors.innerText : "") + " " +
                           (summary ? summary.textContent || summary.innerText : "");
                           
                let matchesText = txtValue.toLowerCase().indexOf(filter) > -1;
                let matchesTag = (activeTag === "All" || tags.split(',').includes(activeTag));
                
                if (matchesText && matchesTag) {
                    cards[i].style.display = "";
                } else {
                    cards[i].style.display = "none";
                }
            }
        }'''

html = html.replace(js_old, js_new)

with open('template.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('template.html patched successfully')
