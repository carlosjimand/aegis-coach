import re
import json

html_path = r'C:\Users\carlo\.gemini\antigravity\brain\d4e37e51-1f92-46c9-9a99-dcfde448f82c\.system_generated\steps\92\content.md'
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

print("File size:", len(text))
matches = re.findall(r'([^"\'\<\>\n\r\t\\]+\.pdf)', text, re.IGNORECASE)
unique_matches = sorted(list(set([m.strip() for m in matches])))
print(f"Total regex pdf matches: {len(matches)}")
print(f"Unique pdf matches: {len(unique_matches)}")
with open(r'c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\scripts\pdf_list.txt', 'w', encoding='utf-8') as out:
    for m in unique_matches:
        out.write(m + '\n')
print("Written to scripts/pdf_list.txt")

