with open('generate_html.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if "t_html += f\"" in line and "class='" in line and "'>" in line and not line.endswith("\\n\"\n"):
        line = line.replace("'>\n", "'>\\n\"\n")
    elif "t_html += f\"" in line and "class-cell" in line and "</td>" in line and not line.endswith("\\n\"\n"):
        line = line.replace("</td>\n", "</td>\\n\"\n")
    elif "t_html += f\"" in line and "<td>" in line and "</td>" in line and not line.endswith("\\n\"\n"):
        line = line.replace("</td>\n", "</td>\\n\"\n")
    elif "t_html += f\"" in line and "<td style" in line and "</span></td>" in line and not line.endswith("\\n\"\n"):
        line = line.replace("</td>\n", "</td>\\n\"\n")
    elif "t_html += f\"" in line and "<td style" in line and "font-weight" in line and "</td>" in line and not line.endswith("\\n\"\n"):
        line = line.replace("</td>\n", "</td>\\n\"\n")
    elif "t_html +=" in line and "</tr>" in line and not line.endswith("\\n\"\n"):
        line = line.replace("</tr>\n", "</tr>\\n\"\n")
    elif "card_html += f'" in line and "DBLP" in line and not line.endswith("\\n'\n"):
        line = line.replace("</a>\n", "</a>\\n'\n")
    
    new_lines.append(line)

with open('generate_html.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Fixed")
