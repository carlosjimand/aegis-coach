import os
import json
from playwright.sync_api import sync_playwright

output_pdf = r"c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\Rutinas_Gimnasio_Carlos_Visual.pdf"
output_html = r"c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\scripts\gym_routines_v2.html"
img_base_dir = r"c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\data\gym_images"


routines_data = [
    {
        "page_num": 1,
        "title": "RUTINA 1 · PIERNA 1",
        "subtitle": "DOMINANCIA RODILLA · FUERZA NEURAL & CUÁDRICEPS",
        "badge": "LUNES 18:00 · 45-50 MIN",
        "theme_color": "#16a34a", # Green 600
        "theme_bg": "#f0fdf4",
        "theme_border": "#bbf7d0",
        "exercises": [
            {
                "num": "1",
                "name": "SENTADILLA CON BARRA",
                "subname": "Back Squat en Jaula",
                "folder": "Barbell_Full_Squat",
                "series_reps": "4 SERIES × 4-6 REPS",
                "weight": "85 KG",
                "rest": "3 MIN",
                "tempo": "3-1-X-0 (3s bajada, 1s pausa, subida explosiva)",
                "rir": "RIR 1-2",
                "cue": "Rompe el paralelo. Empuja con todo el pie sin meter rodillas."
            },
            {
                "num": "2",
                "name": "PRENSA DE PIERNAS 45°",
                "subname": "Incline Leg Press",
                "folder": "Leg_Press",
                "series_reps": "3 SERIES × 6-8 REPS",
                "weight": "+40 KG / LADO",
                "rest": "2.5 MIN",
                "tempo": "3-0-1-0 (bajada controlada profunda)",
                "rir": "RIR 1",
                "cue": "Pies a anchura de caderas. Cero despegue lumbar del respaldo."
            },
            {
                "num": "3",
                "name": "CURL FEMORAL TUMBADO",
                "subname": "Lying Leg Curl",
                "folder": "Lying_Leg_Curls",
                "series_reps": "3 SERIES × 6-8 REPS",
                "weight": "42 KG",
                "rest": "2 MIN",
                "tempo": "3-1-1-0 (HSR: excéntrica en 3s)",
                "rir": "RIR 1",
                "cue": "Frena la bajada. Estimula sarcómeros en serie del isquio."
            },
            {
                "num": "4",
                "name": "EXTENSIÓN DE CUÁDRICEPS",
                "subname": "Leg Extension en Máquina",
                "folder": "Leg_Extensions",
                "series_reps": "3 SERIES × 8-10 REPS",
                "weight": "66 KG",
                "rest": "90 SEG",
                "tempo": "2-0-1-1 (1s contracción isométrica arriba)",
                "rir": "RIR 1",
                "cue": "Aislamiento del recto femoral sin fatiga en columna."
            },
            {
                "num": "5",
                "name": "GEMELOS DE PIE CON BARRA",
                "subname": "Standing Calf Raise",
                "folder": "Standing_Calf_Raises",
                "series_reps": "4 SERIES × 6-8 REPS",
                "weight": "85 KG",
                "rest": "90 SEG",
                "tempo": "3-2-X-0 (PAUSA OBLIGATORIA 2s ABAJO)",
                "rir": "RIR 1",
                "cue": "La pausa abajo anula el rebote elástico y carga el gastrocnemio."
            },
            {
                "num": "6",
                "name": "RUEDA ABDOMINAL (CORE)",
                "subname": "Ab Wheel Rollout",
                "folder": "Barbell_Ab_Rollout_-_On_Knees",
                "series_reps": "3 SERIES × 8-10 REPS",
                "weight": "AUTOCARGA",
                "rest": "60 SEG",
                "tempo": "2-1-2-0 (control lumbo-pélvico)",
                "rir": "Estricto",
                "cue": "Anti-extensión. Retroversión pélvica activa: bloquea la pelvis neutra."
            }
        ]
    },
    {
        "page_num": 2,
        "title": "RUTINA 2 · TORSO TRACCIÓN",
        "subtitle": "DORSAL ANCHO · ESPALDA ALTA · BÍCEPS & DENSIDAD",
        "badge": "MIÉRCOLES 17:30 · 50 MIN",
        "theme_color": "#0284c7", # Sky 600
        "theme_bg": "#f0f9ff",
        "theme_border": "#bae6fd",
        "exercises": [
            {
                "num": "1",
                "name": "JALÓN AGARRE CERRADO V",
                "subname": "Close-Grip Lat Pulldown",
                "folder": "Close-Grip_Front_Lat_Pulldown",
                "series_reps": "4 SERIES × 4-6 REPS",
                "weight": "PESADO (progresivo)",
                "rest": "2.5 MIN",
                "tempo": "3-0-X-1 (tirón explosivo al pecho)",
                "rir": "RIR 1",
                "cue": "Codos pegados viajando a las costillas. Máxima carga en dorsal."
            },
            {
                "num": "2",
                "name": "REMO DORIAN UNILATERAL",
                "subname": "One-Arm Row Máquina / Mancuerna",
                "folder": "One-Arm_Dumbbell_Row",
                "series_reps": "3 SERIES × 6-8 REPS",
                "weight": "28 – 34 KG",
                "rest": "2 MIN",
                "tempo": "2-0-1-1 (1s de apriete en cadera)",
                "rir": "RIR 1",
                "cue": "Pecho firme. Conduce el codo directamente hacia el bolsillo trasero."
            },
            {
                "num": "3",
                "name": "REMO GIRONDA AMPLIO",
                "subname": "Seated Cable Row Wide Grip",
                "folder": "Seated_Cable_Rows",
                "series_reps": "3 SERIES × 8-10 REPS",
                "weight": "MEDIO-PESADO",
                "rest": "90 SEG",
                "tempo": "2-0-1-2 (2s retracción escapular)",
                "rir": "RIR 1",
                "cue": "Codos a 45°-60°. Junta escápulas para soporte postural de carrera."
            },
            {
                "num": "4",
                "name": "FACE PULL EN POLEA ALTA",
                "subname": "Rope Face Pull a la Frente",
                "folder": "Face_Pull",
                "series_reps": "3 SERIES × 10-12 REPS",
                "weight": "MEDIO",
                "rest": "75 SEG",
                "tempo": "2-0-1-1 (rotación externa alta)",
                "rir": "RIR 2",
                "cue": "Manos a la altura de los ojos separando la cuerda. Salud de manguito."
            },
            {
                "num": "5",
                "name": "CURL INCLINADO 45°",
                "subname": "Incline Dumbbell Bicep Curl",
                "folder": "Alternate_Incline_Dumbbell_Curl",
                "series_reps": "3 SERIES × 6-8 REPS",
                "weight": "PESADO",
                "rest": "90 SEG",
                "tempo": "3-0-1-0 (estiramiento profundo)",
                "rir": "RIR 1",
                "cue": "Brazos cuelgan atrás. Máxima tensión en la cabeza larga del bíceps."
            },
            {
                "num": "6",
                "name": "BÍCEPS EN MÁQUINA / SCOTT",
                "subname": "Machine Preacher Curl",
                "folder": "Machine_Preacher_Curls",
                "series_reps": "2 SERIES × 8-10 REPS",
                "weight": "MEDIO-ALTO",
                "rest": "75 SEG",
                "tempo": "2-0-1-1 (tensión continua)",
                "rir": "RIR 0-1",
                "cue": "Codos firmes en el apoyo. Contracción pico para densidad de brazo."
            }
        ]
    },
    {
        "page_num": 3,
        "title": "RUTINA 3 · PIERNA 2",
        "subtitle": "DOMINANCIA CADERA · CADENA POSTERIOR & BLINDAJE ISQUIOS",
        "badge": "VIERNES 17:30 · 50 MIN",
        "theme_color": "#d97706", # Amber 600
        "theme_bg": "#fffbeb",
        "theme_border": "#fde68a",
        "exercises": [
            {
                "num": "1",
                "name": "HIP THRUST CON BARRA",
                "subname": "Barbell Hip Thrust en Banco",
                "folder": "Barbell_Hip_Thrust",
                "series_reps": "4 SERIES × 4-6 REPS",
                "weight": "120 – 130 KG",
                "rest": "3 MIN",
                "tempo": "2-1-X-1 (1s bloqueo arriba)",
                "rir": "RIR 1",
                "cue": "Empuje con talones. Extensión total de cadera apretando glúteos."
            },
            {
                "num": "2",
                "name": "PESO MUERTO RUMANO 1P",
                "subname": "Single-Leg / Staggered RDL",
                "folder": "Romanian_Deadlift",
                "series_reps": "3 SERIES × 6-8 REPS",
                "weight": "20 – 22 KG / MANO",
                "rest": "2 MIN",
                "tempo": "3-1-1-0 (3s excéntrica lenta)",
                "rir": "RIR 1-2",
                "cue": "El ejercicio rey: bisagra de cadera con espalda neutra y tensión en isquio."
            },
            {
                "num": "3",
                "name": "PRENSA PIES ALTOS / ANCHOS",
                "subname": "High Foot Stance Leg Press",
                "folder": "Narrow_Stance_Leg_Press",
                "series_reps": "3 SERIES × 6-8 REPS",
                "weight": "+40-45 KG / LADO",
                "rest": "2 MIN",
                "tempo": "3-0-1-0 (freno excéntrico)",
                "rir": "RIR 1",
                "cue": "Pies arriba en la plancha para activar glúteos y aductores."
            },
            {
                "num": "4",
                "name": "CURL FEMORAL CONTROLADO",
                "subname": "Lying Leg Curl (HSR)",
                "folder": "Lying_Leg_Curls",
                "series_reps": "3 SERIES × 6-8 REPS",
                "weight": "42 KG",
                "rest": "90 SEG",
                "tempo": "3-1-1-0 (tempo estricto)",
                "rir": "RIR 1",
                "cue": "Cero inercia o impulso de cadera. Carga excéntrica pura sin cizallamiento."
            },
            {
                "num": "5",
                "name": "SÓLEO SENTADO EN MÁQUINA",
                "subname": "Seated Calf Raise",
                "folder": "Seated_Calf_Raise",
                "series_reps": "3 SERIES × 8-10 REPS",
                "weight": "PESADO",
                "rest": "90 SEG",
                "tempo": "3-2-1-0 (pausa 2s abajo)",
                "rir": "RIR 1",
                "cue": "Rodilla a 90° aísla el sóleo (absorbe 6-8x tu peso en cada apoyo al correr)."
            },
            {
                "num": "6",
                "name": "PALLOF PRESS + GRANJERO",
                "subname": "Anti-rotación y Estabilidad",
                "folder": "Pallof_Press",
                "series_reps": "3 SERIES × 10 R + 30M",
                "weight": "MEDIO-PESADO",
                "rest": "60 SEG",
                "tempo": "Isométrico",
                "rir": "Estricto",
                "cue": "Anti-rotación pura. Elimina el balanceo lateral de la pelvis en carrera."
            }
        ]
    },
    {
        "page_num": 4,
        "title": "RUTINA 4 · TORSO EMPUJE",
        "subtitle": "PECTORAL · HOMBRO LATERAL · TRÍCEPS & DEFINICIÓN",
        "badge": "SÁBADO MAÑANA · 50 MIN",
        "theme_color": "#db2777", # Pink 600
        "theme_bg": "#fdf2f8",
        "theme_border": "#fbcfe8",
        "exercises": [
            {
                "num": "1",
                "name": "PRESS DE BANCA PLANO",
                "subname": "Barbell Bench Press",
                "folder": "Barbell_Bench_Press_-_Medium_Grip",
                "series_reps": "4 SERIES × 4-6 REPS",
                "weight": "PESADO (progresivo)",
                "rest": "2.5 MIN",
                "tempo": "3-1-X-0 (pausa 1s en pecho)",
                "rir": "RIR 1-2",
                "cue": "Retracción escapular firme. Barra toca el pecho sin rebote y subida explosiva."
            },
            {
                "num": "2",
                "name": "PRESS INCLINADO MANCUERNA",
                "subname": "Incline 30° Dumbbell Press",
                "folder": "Incline_Dumbbell_Press",
                "series_reps": "3 SERIES × 6-8 REPS",
                "weight": "PESADO",
                "rest": "2 MIN",
                "tempo": "3-0-1-0 (bajada controlada)",
                "rir": "RIR 1",
                "cue": "Banco a 30° para enfatizar la porción clavicular y deltoides anterior."
            },
            {
                "num": "3",
                "name": "PEC DEC / APERTURAS",
                "subname": "Machine Butterfly / Pec Deck",
                "folder": "Butterfly",
                "series_reps": "3 SERIES × 8-10 REPS",
                "weight": "MEDIO",
                "rest": "90 SEG",
                "tempo": "2-0-1-1 (1s apriete al frente)",
                "rir": "RIR 1",
                "cue": "Junta los codos al frente y aprieta el pecho 1 segundo en máxima contracción."
            },
            {
                "num": "4",
                "name": "ELEVACIONES LATERALES",
                "subname": "Side Lateral Raise Mancuerna/Polea",
                "folder": "Side_Lateral_Raise",
                "series_reps": "4 SERIES × 8-10 REPS",
                "weight": "PESADO ESTRICTO",
                "rest": "75 SEG",
                "tempo": "2-0-1-1 (sin inercia)",
                "rir": "RIR 1",
                "cue": "Codos ligeramente flexionados. Clave para la amplitud y corte del hombro."
            },
            {
                "num": "5",
                "name": "PRESS FRANCÉS BARRA Z",
                "subname": "Lying Triceps Press en Banco",
                "folder": "Lying_Triceps_Press",
                "series_reps": "3 SERIES × 6-8 REPS",
                "weight": "MEDIO-PESADO",
                "rest": "90 SEG",
                "tempo": "3-0-1-0 (hacia coronilla)",
                "rir": "RIR 1",
                "cue": "Codos fijos apuntando al techo. Estímulo directo a la cabeza larga del tríceps."
            },
            {
                "num": "6",
                "name": "TRÍCEPS POLEA CON CUERDA",
                "subname": "Triceps Pushdown con Cuerda",
                "folder": "Triceps_Pushdown_-_Rope_Attachment",
                "series_reps": "3 SERIES × 8-10 REPS",
                "weight": "MEDIO-ALTO",
                "rest": "75 SEG",
                "tempo": "2-0-1-1 (apertura abajo)",
                "rir": "RIR 0-1",
                "cue": "Abre la cuerda al final del recorrido para acortar las cabezas lateral y medial."
            }
        ]
    }
]

html_content = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>AEGIS COACH · Cuaderno de Fuerza de Carlos</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700;800;900&family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }
    
    @page {
        size: A4 portrait;
        margin: 0;
    }
    
    body {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #f8fafc;
        color: #0f172a;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }
    
    .page {
        width: 210mm;
        height: 297mm;
        page-break-after: always;
        padding: 10mm 12mm;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: #ffffff;
        position: relative;
        overflow: hidden;
    }
    
    /* Top Header */
    .header {
        border-bottom: 2.5px solid #0f172a;
        padding-bottom: 6px;
        margin-bottom: 8px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }
    
    .header-left h1 {
        font-family: 'Montserrat', sans-serif;
        font-size: 22px;
        font-weight: 900;
        letter-spacing: -0.5px;
        text-transform: uppercase;
        color: #0f172a;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    .header-left p {
        font-size: 10px;
        color: #475569;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-top: 1px;
    }
    
    .badge {
        font-family: 'Montserrat', sans-serif;
        font-size: 10px;
        font-weight: 900;
        padding: 4px 12px;
        border-radius: 999px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: #0f172a;
        color: #ffffff;
    }
    
    /* 2 Columns x 3 Rows Grid */
    .exercise-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        grid-template-rows: repeat(3, 1fr);
        gap: 9px;
        flex-grow: 1;
    }
    
    .card {
        background: #ffffff;
        border: 1.5px solid #e2e8f0;
        border-radius: 10px;
        padding: 8px 10px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        position: relative;
    }
    
    .card-top {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 4px;
    }
    
    .num-badge {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        color: #ffffff;
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        font-weight: 900;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .name-container {
        overflow: hidden;
    }
    
    .ex-name {
        font-family: 'Montserrat', sans-serif;
        font-size: 12px;
        font-weight: 900;
        color: #0f172a;
        line-height: 1.15;
        text-transform: uppercase;
        letter-spacing: -0.2px;
    }
    
    .ex-subname {
        font-size: 8.5px;
        color: #64748b;
        font-weight: 600;
    }
    
    /* Big Highlight for Series and Reps */
    .highlight-banner {
        background: #f8fafc;
        border: 1.5px solid #e2e8f0;
        border-radius: 6px;
        padding: 3px 6px;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .series-reps-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 13px;
        font-weight: 900;
        letter-spacing: -0.2px;
    }
    
    .weight-text {
        font-family: 'Montserrat', sans-serif;
        font-size: 11.5px;
        font-weight: 800;
        color: #0f172a;
        background: #e2e8f0;
        padding: 1px 6px;
        border-radius: 4px;
    }
    
    /* Image Comparison (Phase 0 and Phase 1) */
    .image-row {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        margin-bottom: 5px;
        align-items: center;
    }
    
    .img-wrapper {
        position: relative;
        width: 100%;
        height: 72px;
        border-radius: 6px;
        overflow: hidden;
        background: #f1f5f9;
        border: 1px solid #cbd5e1;
    }
    
    .img-wrapper img {
        width: 100%;
        height: 100%;
        object-fit: cover;
        object-position: center;
    }
    
    .phase-label {
        position: absolute;
        bottom: 2px;
        left: 3px;
        background: rgba(15, 23, 42, 0.75);
        color: #ffffff;
        font-size: 7px;
        font-weight: 800;
        padding: 1px 4px;
        border-radius: 3px;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    
    /* Bottom Info & Cues */
    .card-bottom {
        display: flex;
        flex-direction: column;
        gap: 2px;
    }
    
    .pills-row {
        display: flex;
        gap: 4px;
        align-items: center;
    }
    
    .pill {
        font-size: 8px;
        font-weight: 800;
        padding: 1px 5px;
        border-radius: 3px;
        background: #f1f5f9;
        color: #334155;
        border: 1px solid #cbd5e1;
    }
    
    .cue-text {
        font-size: 8px;
        color: #475569;
        line-height: 1.25;
        margin-top: 1px;
    }
    
    .cue-text strong {
        color: #0f172a;
    }
    
    /* Footer */
    .footer {
        border-top: 1.5px solid #0f172a;
        padding-top: 5px;
        margin-top: 6px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 9px;
        font-weight: 700;
        color: #475569;
    }
    
    .footer strong {
        color: #0f172a;
    }
</style>
</head>
<body>
"""

for r in routines_data:
    color = r["theme_color"]
    bg_tint = r["theme_bg"]
    border_tint = r["theme_border"]
    
    html_content += f"""
    <div class="page">
        <div class="header">
            <div class="header-left">
                <h1><span style="color: {color};">●</span> {r["title"]}</h1>
                <p>{r["subtitle"]}</p>
            </div>
            <div class="badge" style="background: {color};">
                {r["badge"]}
            </div>
        </div>
        
        <div class="exercise-grid">
    """
    
    for ex in r["exercises"]:
        folder = ex["folder"]
        img0_path = f"file:///{os.path.join(img_base_dir, folder, '0.jpg').replace(os.sep, '/')}"
        img1_path = f"file:///{os.path.join(img_base_dir, folder, '1.jpg').replace(os.sep, '/')}"
        
        html_content += f"""
            <div class="card" style="border-top: 3.5px solid {color};">
                <div class="card-top">
                    <div class="num-badge" style="background: {color};">{ex["num"]}</div>
                    <div class="name-container">
                        <div class="ex-name">{ex["name"]}</div>
                        <div class="ex-subname">{ex["subname"]}</div>
                    </div>
                </div>
                
                <div class="highlight-banner" style="background: {bg_tint}; border-color: {border_tint};">
                    <span class="series-reps-text" style="color: {color};">{ex["series_reps"]}</span>
                    <span class="weight-text">{ex["weight"]}</span>
                </div>
                
                <div class="image-row">
                    <div class="img-wrapper">
                        <img src="{img0_path}" alt="{ex['name']} Inicio">
                        <span class="phase-label">Inicio</span>
                    </div>
                    <div class="img-wrapper">
                        <img src="{img1_path}" alt="{ex['name']} Final">
                        <span class="phase-label">Final</span>
                    </div>
                </div>
                
                <div class="card-bottom">
                    <div class="pills-row">
                        <span class="pill" style="background: #e2e8f0; color: #0f172a; font-weight: 800;">Descanso: {ex["rest"]}</span>
                        <span class="pill">{ex["rir"]}</span>
                        <span class="pill">Tempo: {ex["tempo"][:7]}</span>
                    </div>
                    <div class="cue-text">
                        <strong>Clave:</strong> {ex["cue"]}
                    </div>
                </div>
            </div>
        """
        
    html_content += f"""
        </div>
        
        <div class="footer">
            <span>AEGIS COACH &bull; ATLETA: <strong>CARLOS GÓMEZ (63 KG)</strong></span>
            <span>OBJETIVO: <strong>10K ÁVILA (8 NOV) &bull; SAN SILVESTRE (31 DIC)</strong></span>
            <span>PROGRESIÓN: <strong>RIR 1-2 &bull; SUBIR +2.5 KG AL COMPLETAR</strong></span>
        </div>
    </div>
    """

html_content += """
</body>
</html>
"""

with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"HTML saved to: {output_html}")

# Playwright PDF and Screenshots for review
print("Rendering PDF and Screenshots via Playwright...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1700})
    page.goto(f"file:///{output_html.replace(os.sep, '/')}")
    page.wait_for_timeout(1000)
    
    # Save PDF
    page.pdf(
        path=output_pdf,
        format="A4",
        print_background=True,
        margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
    )
    print(f"SUCCESS: PDF created at {output_pdf}")
    
    # Take screenshot of each page for visual verification
    pages = page.locator(".page")
    count = pages.count()
    print(f"Pages detected: {count}")
    for i in range(count):
        screenshot_path = rf"c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\data\page_{i+1}_review.png"
        pages.nth(i).screenshot(path=screenshot_path)
        print(f"Screenshot page {i+1} saved to {screenshot_path}")
        
    browser.close()

print("ALL RENDERS COMPLETED SUCCESSFULLY!")
