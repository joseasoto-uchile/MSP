content = open('index.html', encoding='utf-8').read()
checks = [
    ('C1 table links real href', "onclick='goToPaper(" in content and "return false" in content),
    ('C2 cards collapsed by default', 'card-body collapsed' in content),
    ('H1 back-to-top button', 'id="back-to-top"' in content),
    ('H3 clear filter / resetFilters', 'resetFilters' in content),
    ('H4 unified filter-bar', 'filter-bar' in content),
    ('H5 pre block in bibtex', '<pre>' in content),
    ('H5 copy button', 'copyBibtex' in content),
    ('H6 table overflow-x', 'overflow-x: auto' in content),
    ('M1 bibtex label toggle', 'data-show-label' in content),
    ('M2 hash routing', 'history.replaceState' in content),
    ('M4 result counter', 'result-count' in content),
    ('M6 lang-switch preserves hash', 'lang-switch' in content),
    ('L1 ARIA tablist', 'role="tablist"' in content),
    ('L3 skip to content link', 'Skip to content' in content),
    ('L6 dark mode', 'prefers-color-scheme: dark' in content),
    ('permalink per card', 'class="permalink"' in content),
    ('card-toggle-btn', 'card-toggle-btn' in content),
    ('arrow-key nav for tabs', 'ArrowRight' in content),
]
all_pass = True
for name, ok in checks:
    mark = 'PASS' if ok else 'FAIL'
    if not ok: all_pass = False
    print(f'  [{mark}] {name}')
print()
print('All checks passed!' if all_pass else 'Some checks FAILED - see above.')
