import re
with open('generate_html.py', 'r', encoding='utf-8') as f:
    content = f.read()

content = content.replace('html += "                    <tr>\\n"', 'row_class = "group-start" if i == 0 else ""\n            html += f"                    <tr class=\'{row_class}\'>\\n"')

with open('generate_html.py', 'w', encoding='utf-8') as f:
    f.write(content)
