import os
from playwright.sync_api import sync_playwright

squat_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#05161A"/>
      <stop offset="100%" stop-color="#072E33"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F969C"/>
      <stop offset="100%" stop-color="#0C7075"/>
    </linearGradient>
    <linearGradient id="skin" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F8D3B8"/>
      <stop offset="100%" stop-color="#E8B490"/>
    </linearGradient>
    <linearGradient id="skinShadow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#DE9E78"/>
      <stop offset="100%" stop-color="#C6835F"/>
    </linearGradient>
    <linearGradient id="plateGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="barChrome" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#64748B"/>
      <stop offset="50%" stop-color="#E2E8F0"/>
      <stop offset="100%" stop-color="#475569"/>
    </linearGradient>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- TARJETA BASE -->
  <rect width="800" height="380" rx="18" fill="url(#bgGrad)" stroke="#294D61" stroke-width="1.5" stroke-opacity="0.45"/>

  <!-- SUELO Y CUADRÍCULA SUTIL -->
  <line x1="30" y1="330" x2="770" y2="330" stroke="#294D61" stroke-width="2" stroke-dasharray="6 4" stroke-opacity="0.4"/>
  <rect x="30" y="331" width="740" height="1" fill="#0F969C" fill-opacity="0.2"/>

  <!-- DIVISOR CENTRAL CON CHEVRON -->
  <line x1="400" y1="45" x2="400" y2="330" stroke="#294D61" stroke-width="1" stroke-dasharray="4 6" stroke-opacity="0.3"/>
  <g transform="translate(400, 185)">
    <circle cx="0" cy="0" r="17" fill="#05161A" stroke="#0F969C" stroke-width="1.8" filter="url(#glow)"/>
    <path d="M-6 0 H6 M2 -4 L6 0 L2 4" stroke="#0F969C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- BADGES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · INICIAL ERGUIDA</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="155" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="88" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · FONDO PARALELO</text>
  </g>

  <!-- DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-195" y="-14" width="390" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-175" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      SENTADILLA TRASERA (BACK SQUAT) &bull; FOCO: <tspan fill="#0F969C" font-weight="700">CUÁDRICEPS &amp; GLÚTEOS</tspan>
    </text>
  </g>

  <!-- ============================================== -->
  <!-- FASE 1: SENTADILLA ERGUIDA (POSICIÓN INICIAL)   -->
  <!-- ============================================== -->
  <g id="squat-phase1" transform="translate(195, 60)">
    <!-- Pierna Lejana (Sombra) -->
    <g opacity="0.45">
      <path d="M 0 135 C 5 160, 5 190, 2 215 C 2 235, 6 250, 4 265 L 14 265 C 16 250, 14 235, 12 215 C 15 190, 15 160, 10 135 Z" fill="#C6835F"/>
      <path d="M 2 265 L 18 265 L 18 270 L -1 270 Z" fill="#1E293B"/>
    </g>

    <!-- Cabeza y Cabello Atlético -->
    <path d="M -1 8 C 8 8, 12 16, 12 24 C 12 32, 6 36, -2 36 C -10 36, -14 28, -14 20 C -14 12, -8 8, -1 8 Z" fill="url(#skin)"/>
    <!-- Cabello con coleta -->
    <path d="M -6 6 C 6 4, 13 11, 13 21 C 13 28, 7 32, -1 31 C -7 30, -11 22, -9 15 Z" fill="#1C1917"/>
    <path d="M -8 18 C -18 24, -22 34, -18 40 C -14 36, -10 28, -5 22 Z" fill="#1C1917"/>

    <!-- Cuello y Trapecio -->
    <path d="M -2 34 L 2 34 L 4 48 L -4 48 Z" fill="url(#skin)"/>

    <!-- Torso Atlético (Top Teal #0F969C) -->
    <path d="M -14 48 
             C -2 46, 6 46, 16 48 
             C 14 68, 10 95, 8 115 
             C 2 118, -4 118, -10 115 
             C -12 95, -14 68, -14 48 Z" 
          fill="url(#tealGrad)" stroke="#0C7075" stroke-width="1"/>

    <!-- Mallas / Shorts Oscuros -->
    <path d="M -11 114 
             C -3 117, 3 117, 9 114 
             C 12 125, 12 140, 10 148 
             C 3 151, -5 151, -12 148 
             C -14 140, -13 125, -11 114 Z" 
          fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <path d="M -9 118 L -9 146" stroke="#0F969C" stroke-width="1.2"/>

    <!-- Muslo Cercano Anatómico (Curva de Cuádriceps) -->
    <path d="M -12 146 
             C -16 168, -15 195, -10 216 
             C -6 220, 2 220, 6 216 
             C 10 195, 10 168, 8 146 Z" 
          fill="url(#skin)"/>

    <!-- Rodilla y Gemelo Diamond Shape (Curva Anatómica) -->
    <path d="M -10 216 
             C -14 228, -14 242, -9 256 
             C -6 264, -5 268, -6 268 
             L 4 268 
             C 5 268, 5 262, 7 252 
             C 10 238, 9 226, 6 216 Z" 
          fill="url(#skin)"/>

    <!-- Zapatilla Deportiva Estable -->
    <path d="M -10 266 L 8 266 C 12 268, 12 270, 8 270 L -12 270 C -14 268, -12 266, -10 266 Z" fill="#1E293B"/>
    <rect x="-13" y="268" width="24" height="2.5" rx="1" fill="#E2E8F0"/>
    <path d="M -5 267 L 2 267" stroke="#0F969C" stroke-width="1" stroke-linecap="round"/>

    <!-- Brazos Sosteniendo Barra en Espalda Alta -->
    <path d="M -12 50 C -22 62, -24 76, -18 84 C -12 78, -6 68, -4 54" stroke="url(#skin)" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="-16" cy="80" r="3.5" fill="#DE9E78"/>

    <!-- Barra Olímpica sobre Hombros y Discos Bumper 20kg -->
    <rect x="-65" y="50" width="130" height="5" rx="2" fill="url(#barChrome)"/>
    <circle cx="50" cy="52" r="26" fill="url(#plateGrad)" stroke="#0F969C" stroke-width="2.5" opacity="0.95"/>
    <circle cx="50" cy="52" r="18" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <circle cx="50" cy="52" r="10" fill="#1E293B"/>
    <circle cx="50" cy="52" r="3.5" fill="#E2E8F0"/>
    <text x="50" y="40" fill="#6DA5C0" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">20 KG</text>
  </g>

  <!-- ============================================== -->
  <!-- FASE 2: SENTADILLA PROFUNDA / PARALELO A 90°    -->
  <!-- ============================================== -->
  <g id="squat-phase2" transform="translate(585, 115)">
    <!-- Pierna Lejana Profunda (Sombra) -->
    <g opacity="0.45">
      <path d="M -45 130 C -25 125, 0 125, 20 135 C 22 155, 18 185, 14 212 L 28 212 L 28 217 L 6 217 C 8 185, 10 155, 6 138 Z" fill="#C6835F"/>
    </g>

    <!-- Torso Inclinado 45° Fuerte y Estable -->
    <path d="M -15 28 
             C 5 18, 20 25, 28 40 
             C 15 58, -5 85, -28 102 
             C -38 98, -45 90, -45 80 
             C -35 60, -25 42, -15 28 Z" 
          fill="url(#tealGrad)" stroke="#0C7075" stroke-width="1"/>

    <!-- Cabeza y Cuello con Mirada al Frente -->
    <path d="M 18 22 C 24 16, 28 12, 34 8 L 40 14 C 36 20, 30 26, 26 30 Z" fill="url(#skin)"/>
    <circle cx="40" cy="4" r="12" fill="url(#skin)"/>
    <path d="M 33 -6 C 43 -9, 51 -2, 51 8 C 51 16, 43 20, 35 18 C 29 16, 27 6, 29 0 Z" fill="#1C1917"/>
    <path d="M 30 6 C 17 12, 15 24, 20 30 C 25 26, 28 20, 33 12 Z" fill="#1C1917"/>

    <!-- FOCO NEUROMUSCULAR RESPLANDECIENTE: CUÁDRICEPS & GLÚTEO EN TENSIÓN MÁXIMA -->
    <path d="M -50 82 C -42 68, -25 78, -12 92 C 5 106, 22 108, 30 115 C 28 128, 12 135, -5 130 C -25 122, -45 110, -50 82 Z" 
          fill="#0F969C" fill-opacity="0.38" filter="url(#glow)"/>

    <!-- Mallas / Shorts en Ángulo -->
    <path d="M -44 80 C -36 72, -22 82, -14 94 C -22 106, -34 116, -45 114 C -50 102, -50 90, -44 80 Z" 
          fill="#05161A" stroke="#0F969C" stroke-width="1.5"/>

    <!-- Muslo Paralelo al Suelo (Cuádriceps en Pico Excéntrico) -->
    <path d="M -22 92 
             C -2 95, 12 98, 28 108 
             C 32 115, 30 125, 22 130 
             C 5 130, -12 125, -30 116 Z" 
          fill="url(#skin)"/>

    <!-- Vector de fuerza del cuádriceps -->
    <path d="M -5 106 C 8 108, 18 114, 22 122" stroke="#6DA5C0" stroke-width="2" stroke-linecap="round" fill="none"/>

    <!-- Rodilla a 90° y Pantorrilla Estable -->
    <path d="M 24 110 
             C 34 118, 35 135, 32 155 
             C 30 175, 26 195, 25 212 
             L 12 212 
             C 14 195, 18 175, 20 155 
             C 22 138, 20 124, 18 116 Z" 
          fill="url(#skin)"/>

    <!-- Zapatilla Deportiva Apoyada Firmemente -->
    <path d="M 8 210 L 32 210 C 36 212, 36 215, 32 217 L 4 217 C 2 215, 4 212, 8 210 Z" fill="#1E293B"/>
    <rect x="3" y="214" width="31" height="2.8" rx="1" fill="#E2E8F0"/>
    <path d="M 14 211 L 22 211" stroke="#0F969C" stroke-width="1.2" stroke-linecap="round"/>

    <!-- Brazos Sujetando la Barra en la Sentadilla -->
    <path d="M 4 36 C -4 52, -8 68, -2 76 C 4 70, 8 58, 12 42" stroke="url(#skin)" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="0" cy="72" r="3.5" fill="#DE9E78"/>

    <!-- Barra Olímpica Nivelada y Disco 20kg -->
    <rect x="-45" y="32" width="130" height="5" rx="2" fill="url(#barChrome)"/>
    <circle cx="70" cy="34" r="26" fill="url(#plateGrad)" stroke="#0F969C" stroke-width="2.5" opacity="0.95" filter="url(#glow)"/>
    <circle cx="70" cy="34" r="18" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <circle cx="70" cy="34" r="10" fill="#1E293B"/>
    <circle cx="70" cy="34" r="3.5" fill="#E2E8F0"/>
    <text x="70" y="22" fill="#0F969C" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">20 KG</text>
  </g>
</svg>'''

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 840, "height": 420})
    page.set_content(f"""<!DOCTYPE html>
<html>
<body style="margin:0; background:#000; display:flex; justify-content:center; align-items:center; min-height:100vh;">
{squat_svg}
</body>
</html>""")
    page.screenshot(path='test_squat.png')
    browser.close()

print("Generated test_squat.png successfully!")
