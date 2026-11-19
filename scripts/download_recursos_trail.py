import os
import requests
import pypdf

files = [
    {
        "id": "1xaB1bBFpFvEjT-l5PSY6yiT09rIWKM5z",
        "name": "Bases de la NUTRICIÓN en el TRAIL - RUN4TRAIL.pdf",
        "slug": "nutricion_trail"
    },
    {
        "id": "1vtxCPNx5M8TqbhrQJa8b-iLmehDlGAid",
        "name": "CALCULADORA de zonas de entrenamiento RUN4TRAIL.pdf",
        "slug": "calculadora_zonas"
    },
    {
        "id": "1SWBk3RKL_a9HCNi3XyQqTGbTgrlh-hEi",
        "name": "Claves del ENTRENAMIENTO DE FUERZA para Trail - RUN4TRAIL.pdf",
        "slug": "fuerza_trail"
    },
    {
        "id": "1NPmI73Y4kDsYsKkICk8mdKNeKJ_5Dtft",
        "name": "Ejercicios de fuerza. Comunidad.pdf",
        "slug": "ejercicios_fuerza"
    },
    {
        "id": "1190VBfn7dXNwggSN1_Jm4Pu_uydIaoxA",
        "name": "Mejora la fuerza en las BAJADAS- RUN4TRAIL.pdf",
        "slug": "fuerza_bajadas"
    },
    {
        "id": "17YE0z3JMcUGFBelJ585f4tA1krCAVhjH",
        "name": "Pautas de RECUPERACIÓN - RUN4TRAIL.pdf",
        "slug": "recuperacion_trail"
    },
    {
        "id": "1YgXfmr6_2R4oXDTquSP3bjGTe8OBJgQ_",
        "name": "Planificación de la temporada.pdf",
        "slug": "planificacion_temporada"
    },
    {
        "id": "12PeKVQCw77tVhwmYiPJoT3RS7XqZHfMl",
        "name": "Psicologia_Trail_RUN4TRAIL.pdf",
        "slug": "psicologia_trail"
    }
]

pdf_dir = r"c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\data\recursos_trail\pdfs"
md_dir = r"c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\data\recursos_trail\markdown"
os.makedirs(pdf_dir, exist_ok=True)
os.makedirs(md_dir, exist_ok=True)

for item in files:
    fid = item["id"]
    name = item["name"]
    slug = item["slug"]
    pdf_path = os.path.join(pdf_dir, f"{slug}.pdf")
    md_path = os.path.join(md_dir, f"{slug}.md")
    
    print(f"Downloading: {name} (ID: {fid})...")
    url = f"https://drive.google.com/uc?export=download&id={fid}"
    resp = requests.get(url, allow_redirects=True)
    if resp.status_code == 200 and resp.content[:4] == b'%PDF':
        with open(pdf_path, 'wb') as f:
            f.write(resp.content)
        print(f"  -> Saved PDF ({len(resp.content)} bytes).")
        
        # Extract text
        try:
            reader = pypdf.PdfReader(pdf_path)
            extracted = []
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted.append(f"--- Página {i+1} ---\n" + text)
            full_text = f"# {name}\n\n" + "\n\n".join(extracted)
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(full_text)
            print(f"  -> Extracted text ({len(reader.pages)} pages, {len(full_text)} chars) to {slug}.md")
        except Exception as e:
            print(f"  -> Error extracting text: {e}")
    else:
        print(f"  -> Failed to download PDF: status={resp.status_code}, content-type={resp.headers.get('content-type')}")

print("\nAll downloads and extractions completed!")
