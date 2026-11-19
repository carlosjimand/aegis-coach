import os
from playwright.sync_api import sync_playwright

# Definición anatómica realista con curvas Bezier (Anatomía Deportiva 2D)
svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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
      <stop offset="0%" stop-color="#F7D0B2"/>
      <stop offset="100%" stop-color="#E5AF8C"/>
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

  <!-- LÍNEA DE SUELO ELEGANTE CON DEGRADADO -->
  <line x1="30" y1="330" x2="770" y2="330" stroke="#294D61" stroke-width="2" stroke-dasharray="6 4" stroke-opacity="0.4"/>
  <rect x="30" y="331" width="740" height="1" fill="#0F969C" fill-opacity="0.2"/>

  <!-- DIVISOR CENTRAL CON CHEVRON ACTIVO -->
  <line x1="400" y1="45" x2="400" y2="330" stroke="#294D61" stroke-width="1" stroke-dasharray="4 6" stroke-opacity="0.3"/>
  <g transform="translate(400, 185)">
    <circle cx="0" cy="0" r="17" fill="#05161A" stroke="#0F969C" stroke-width="1.8" filter="url(#glow)"/>
    <path d="M-6 0 H6 M2 -4 L6 0 L2 4" stroke="#0F969C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- INSIGNIAS SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="135" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="67" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · EXCÉNTRICA</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="155" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="88" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · CONTRACCIÓN</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-180" y="-14" width="360" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-160" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      HIP THRUST CON BARRA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">GLÚTEO MAYOR (BLOQUEO 1s)</tspan>
    </text>
  </g>

  <!-- ========================================== -->
  <!-- FASE 1: HIP THRUST - CADERA ABAJO (FLEXIÓN) -->
  <!-- ========================================== -->
  <g id="hip-thrust-phase1">
    <!-- Banco Plano Acolchado -->
    <rect x="65" y="215" width="55" height="90" rx="6" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="70" y="220" width="45" height="80" rx="4" fill="#072E33" fill-opacity="0.4"/>
    <!-- Patas del banco -->
    <rect x="80" y="305" width="10" height="25" fill="#1E293B"/>
    <line x1="68" y1="330" x2="102" y2="330" stroke="#334155" stroke-width="3.5" stroke-linecap="round"/>

    <!-- Pierna Lejana (Sombra para dar volumen 3D) -->
    <g opacity="0.45">
      <!-- Muslo lejano -->
      <path d="M 165 260 C 185 240, 215 220, 235 225 C 242 230, 240 245, 230 252 C 210 265, 185 285, 170 285 Z" fill="#C6835F"/>
      <!-- Pantorrilla lejana con curva de gemelo -->
      <path d="M 235 225 C 248 250, 258 280, 255 315 L 268 318 L 268 328 L 240 328 C 242 295, 236 265, 228 245 Z" fill="#C6835F"/>
    </g>

    <!-- Torso Atlético Inclinado (Top Deportivo Teal) -->
    <!-- Contorno anatómico: escápula apoyada, pecho, cintura estrecha -->
    <path d="M 115 210 
             C 125 205, 135 212, 142 225 
             C 152 242, 162 260, 168 275 
             C 160 282, 150 282, 142 276 
             C 132 255, 122 235, 112 222 Z" 
          fill="url(#tealGrad)" stroke="#0C7075" stroke-width="1"/>

    <!-- Detalle de costura deportiva -->
    <path d="M 130 220 C 140 240, 150 260, 156 276" stroke="#05161A" stroke-width="1.2" stroke-linecap="round" fill="none"/>

    <!-- Cuello Atlético -->
    <path d="M 112 210 C 108 200, 102 195, 98 190 L 106 186 C 112 192, 118 200, 120 206 Z" fill="url(#skin)"/>

    <!-- Cabeza y Cabello con Coleta Deportiva -->
    <circle cx="95" cy="178" r="12" fill="url(#skin)"/>
    <!-- Cabello estilizado corriendo hacia atrás -->
    <path d="M 88 168 C 98 165, 106 172, 106 182 C 106 190, 98 194, 90 192 C 84 190, 82 180, 84 174 Z" fill="#1C1917"/>
    <!-- Coleta aerodinámica -->
    <path d="M 85 180 C 72 186, 70 198, 75 204 C 80 200, 83 194, 88 186 Z" fill="#1C1917"/>

    <!-- Mallas / Pantalones Cortos Oscuros -->
    <path d="M 148 268 C 160 262, 175 258, 185 262 C 188 275, 182 288, 172 292 C 160 295, 150 285, 148 268 Z" 
          fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <path d="M 155 272 C 165 270, 175 272, 180 278" stroke="#0F969C" stroke-width="1.2" fill="none"/>

    <!-- Muslo Cercano Anatómico (Curva de Cuádriceps y Tendón) -->
    <path d="M 182 262 
             C 200 242, 222 230, 240 236 
             C 246 242, 245 252, 238 258 
             C 220 272, 195 288, 174 290 Z" 
          fill="url(#skin)"/>

    <!-- Rodilla y Pantorrilla Cercana (Anatomía del Gemelo/Gastrocnemio) -->
    <path d="M 238 238 
             C 246 244, 252 258, 250 278 
             C 248 296, 244 312, 245 322 
             L 235 322 
             C 232 305, 230 285, 226 268 
             C 224 256, 228 246, 236 240 Z" 
          fill="url(#skin)"/>

    <!-- Zapatilla Deportiva Técnica -->
    <path d="M 232 322 L 255 322 C 260 324, 260 328, 255 330 L 228 330 C 226 326, 228 322, 232 322 Z" fill="#1E293B"/>
    <rect x="227" y="327" width="32" height="3" rx="1.5" fill="#E2E8F0"/>
    <path d="M 238 323 L 246 323" stroke="#0F969C" stroke-width="1.5" stroke-linecap="round"/>

    <!-- Brazo Sujetando Barra -->
    <path d="M 125 215 C 138 235, 150 252, 168 266" stroke="url(#skin)" stroke-width="7" stroke-linecap="round" fill="none"/>
    <circle cx="168" cy="266" r="4.5" fill="#DE9E78"/>

    <!-- Barra Olímpica y Disco 20kg -->
    <rect x="165" y="210" width="6" height="110" rx="2" fill="url(#barChrome)"/>
    <!-- Disco 20kg Bumper con borde y ranura -->
    <circle cx="168" cy="266" r="30" fill="url(#plateGrad)" stroke="#0F969C" stroke-width="2.5" opacity="0.95"/>
    <circle cx="168" cy="266" r="22" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <circle cx="168" cy="266" r="12" fill="#1E293B"/>
    <circle cx="168" cy="266" r="4" fill="#E2E8F0"/>
    <text x="168" y="250" fill="#6DA5C0" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">20 KG</text>
  </g>

  <!-- ======================================================== -->
  <!-- FASE 2: HIP THRUST - BLOQUEO TOTAL HORIZONTAL & GLÚTEO   -->
  <!-- ======================================================== -->
  <g id="hip-thrust-phase2">
    <!-- Banco Plano Acolchado -->
    <rect x="445" y="215" width="55" height="90" rx="6" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="450" y="220" width="45" height="80" rx="4" fill="#072E33" fill-opacity="0.4"/>
    <rect x="460" y="305" width="10" height="25" fill="#1E293B"/>
    <line x1="448" y1="330" x2="482" y2="330" stroke="#334155" stroke-width="3.5" stroke-linecap="round"/>

    <!-- Pierna Lejana Fase 2 (Sombra) -->
    <g opacity="0.45">
      <path d="M 570 205 L 650 205 L 650 322 L 664 322 L 664 330 L 638 330 L 638 220 L 570 220 Z" fill="#C6835F"/>
    </g>

    <!-- Torso Horizontal de Alto Rendimiento -->
    <path d="M 485 204 
             C 515 204, 545 204, 575 204 
             C 572 216, 565 228, 555 228 
             C 525 228, 500 226, 482 222 Z" 
          fill="url(#tealGrad)" stroke="#0C7075" stroke-width="1"/>

    <!-- Costura deportiva -->
    <line x1="500" y1="216" x2="560" y2="216" stroke="#05161A" stroke-width="1.2" stroke-linecap="round"/>

    <!-- Cuello y Cabeza Neutra con Mentón Recogido -->
    <path d="M 484 206 C 476 200, 468 196, 458 192 L 464 186 C 472 192, 480 198, 488 202 Z" fill="url(#skin)"/>
    <circle cx="452" cy="184" r="12" fill="url(#skin)"/>
    <path d="M 445 174 C 455 171, 463 178, 463 188 C 463 196, 455 200, 447 198 C 441 196, 439 186, 441 180 Z" fill="#1C1917"/>
    <path d="M 442 186 C 429 192, 427 204, 432 210 C 437 206, 440 200, 445 192 Z" fill="#1C1917"/>

    <!-- FOCO NEUROMUSCULAR RESPLANDECIENTE: GLÚTEO MAYOR -->
    <!-- Resplandor exterior -->
    <path d="M 555 202 C 585 202, 600 216, 588 235 C 575 244, 550 236, 545 222 Z" 
          fill="#0F969C" fill-opacity="0.35" filter="url(#glow)"/>

    <!-- Mallas con tensión muscular -->
    <path d="M 552 202 
             C 578 202, 592 212, 582 230 
             C 572 238, 550 232, 546 220 Z" 
          fill="#05161A" stroke="#0F969C" stroke-width="1.5"/>

    <!-- Vector de contracción glútea -->
    <path d="M 560 214 C 572 210, 580 216, 576 225" stroke="#6DA5C0" stroke-width="2" stroke-linecap="round" fill="none"/>

    <!-- Muslo Horizontal Anatómico (Cuádriceps e Isquiotibial) -->
    <path d="M 578 204 
             C 605 204, 635 204, 658 208 
             C 658 218, 645 228, 625 228 
             C 595 228, 575 225, 568 215 Z" 
          fill="url(#skin)"/>

    <!-- Rodilla a 90 Grados Estricta y Tibia Vertical -->
    <path d="M 648 208 
             C 660 212, 664 225, 664 250 
             C 664 275, 662 300, 662 322 
             L 648 322 
             C 648 300, 646 270, 646 245 
             C 646 230, 644 218, 648 208 Z" 
          fill="url(#skin)"/>

    <!-- Zapatilla Deportiva Plantada a 90° -->
    <path d="M 642 322 L 670 322 C 675 324, 675 328, 670 330 L 638 330 C 636 326, 638 322, 642 322 Z" fill="#1E293B"/>
    <rect x="637" y="327" width="37" height="3" rx="1.5" fill="#E2E8F0"/>
    <path d="M 650 323 L 660 323" stroke="#0F969C" stroke-width="1.5" stroke-linecap="round"/>

    <!-- Brazo Estabilizando Barra en la Cadera -->
    <path d="M 488 208 C 518 206, 545 206, 568 208" stroke="url(#skin)" stroke-width="7" stroke-linecap="round" fill="none"/>
    <circle cx="568" cy="208" r="4.5" fill="#DE9E78"/>

    <!-- Barra Olímpica Elevada en Bloqueo y Disco 20kg -->
    <rect x="565" y="152" width="6" height="110" rx="2" fill="url(#barChrome)"/>
    <circle cx="568" cy="208" r="30" fill="url(#plateGrad)" stroke="#0F969C" stroke-width="2.5" opacity="0.95" filter="url(#glow)"/>
    <circle cx="568" cy="208" r="22" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <circle cx="568" cy="208" r="12" fill="#1E293B"/>
    <circle cx="568" cy="208" r="4" fill="#E2E8F0"/>
    <text x="568" y="192" fill="#0F969C" font-family="monospace" font-size="6.5" font-weight="700" text-anchor="middle">20 KG</text>
  </g>
</svg>'''

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 840, "height": 420})
    page.set_content(f"""<!DOCTYPE html>
<html>
<body style="margin:0; background:#000; display:flex; justify-content:center; align-items:center; min-height:100vh;">
{svg_content}
</body>
</html>""")
    page.screenshot(path='test_hip_thrust_v2.png')
    browser.close()

print("Generated test_hip_thrust_v2.png successfully!")
