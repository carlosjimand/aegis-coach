import re
import json

html_path = r'C:\Users\carlo\.gemini\antigravity\brain\d4e37e51-1f92-46c9-9a99-dcfde448f82c\.system_generated\steps\92\content.md'
with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Pattern for filename and id: typically in Drive HTML it's like ["file_id", "filename.pdf", ...] or similar
# Let's search for occurrences of each pdf name and surrounding context
pdf_names = [
    "Bases de la NUTRICIÓN en el TRAIL - RUN4TRAIL.pdf",
    "CALCULADORA de zonas de entrenamiento RUN4TRAIL.pdf",
    "Claves del ENTRENAMIENTO DE FUERZA para Trail - RUN4TRAIL.pdf",
    "Ejercicios de fuerza. Comunidad.pdf",
    "Mejora la fuerza en las  BAJADAS- RUN4TRAIL.pdf",
    "Pautas de RECUPERACIÓN -  RUN4TRAIL .pdf",
    "Planificación de la temporada.pdf",
    "Psicologia_Trail_RUN4TRAIL.pdf"
]

results = {}
for name in pdf_names:
    pos = text.find(name)
    if pos != -1:
        # get 500 chars before and after
        context = text[max(0, pos-400):min(len(text), pos+400)]
        # Google drive IDs are typically 28-40 chars [a-zA-Z0-9_-]
        ids = re.findall(r'[a-zA-Z0-9_-]{28,40}', context)
        # filter out common words
        ids = [i for i in ids if not any(w in i.lower() for w in ['google', 'drive', 'download', 'recuperaci', 'comunidad', 'planificaci', 'psicologia', 'nutrici', 'entrenamiento'])]
        results[name] = ids
        print(f"File: {name} -> Candidate IDs: {ids}")
    else:
        print(f"File: {name} -> NOT FOUND in text")

with open(r'c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\scripts\file_ids.json', 'w', encoding='utf-8') as out:
    json.dump(results, out, indent=2)
