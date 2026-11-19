import os
from playwright.sync_api import sync_playwright

test_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
  <defs>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- TARJETA BASE -->
  <rect width="800" height="380" rx="18" fill="#072E33" stroke="#294D61" stroke-width="1.5" stroke-opacity="0.6"/>
  <rect x="2" y="2" width="796" height="376" rx="16" fill="#05161A" fill-opacity="0.85"/>

  <!-- SUELO Y CUADRÍCULA -->
  <line x1="30" y1="330" x2="770" y2="330" stroke="#294D61" stroke-width="2" stroke-dasharray="6 4" stroke-opacity="0.5"/>
  <rect x="30" y="331" width="740" height="1.5" fill="#0F969C" fill-opacity="0.3"/>

  <!-- DIVISOR CENTRAL CON CHEVRON -->
  <line x1="400" y1="45" x2="400" y2="330" stroke="#294D61" stroke-width="1" stroke-dasharray="4 6" stroke-opacity="0.4"/>
  <g transform="translate(400, 185)">
    <circle cx="0" cy="0" r="18" fill="#072E33" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    <path d="M-6 0 H6 M2 -4 L6 0 L2 4" stroke="#0F969C" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- BADGES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · TALONES ABAJO</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#072E33" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · PUNTILLAS MÁXIMA</text>
  </g>

  <!-- PIE DE TARJETA -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      GEMELOS DE PIE CON BARRA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">GASTROCNEMIO / GEMELOS PICO</tspan>
    </text>
  </g>

  <!-- ==================== FASE 1: TALONES ABAJO EN TACO ==================== -->
  <g id="calf-p1">
    <!-- Taco Elevador -->
    <rect x="175" y="315" width="55" height="15" rx="3" fill="#1E293B" stroke="#294D61" stroke-width="1.5"/>
    <line x1="175" y1="318" x2="230" y2="318" stroke="#0F969C" stroke-width="1.5" stroke-opacity="0.5"/>

    <!-- Pierna Lejana (Sombra anatómica) -->
    <path d="M 195 180 C 190 215, 188 255, 190 280 C 188 300, 185 315, 182 328 L 195 328 L 210 315 L 210 280 C 208 255, 208 215, 205 180 Z" fill="#C6835F" opacity="0.4"/>

    <!-- Cabeza y Cabello -->
    <circle cx="200" cy="80" r="13" fill="#F5CBA7"/>
    <path d="M 194 68 C 204 66, 212 73, 212 83 C 212 90, 206 94, 198 93 C 192 92, 190 83, 191 76 Z" fill="#1C1917"/>
    <path d="M 192 81 C 182 87, 178 97, 182 103 C 186 99, 190 91, 195 85 Z" fill="#1C1917"/>
    <rect x="196" y="92" width="8" height="16" fill="#F5CBA7"/>

    <!-- Torso Erguido Atlético (Top Teal #0F969C) -->
    <path d="M 188 108 C 200 106, 210 106, 220 108 C 217 130, 213 155, 210 175 C 203 178, 197 178, 191 175 C 188 155, 186 130, 188 108 Z" fill="#0F969C" stroke="#0C7075" stroke-width="1.2"/>
    <line x1="204" y1="112" x2="201" y2="175" stroke="#05161A" stroke-width="1.2"/>

    <!-- Shorts Oscuros -->
    <path d="M 190 174 C 198 177, 206 177, 212 174 C 214 188, 214 202, 212 210 C 205 213, 197 213, 189 210 C 187 202, 188 188, 190 174 Z" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <path d="M 192 178 L 192 208" stroke="#0F969C" stroke-width="1.2"/>

    <!-- Muslo (Cuádriceps) -->
    <path d="M 189 208 C 184 230, 185 258, 191 278 C 195 282, 203 282, 207 278 C 210 258, 210 230, 209 208 Z" fill="#F5CBA7"/>

    <!-- Gemelo en Estiramiento Completo (Talón abajo en y=328) -->
    <path d="M 191 278 C 187 290, 186 304, 189 324 L 202 324 C 206 306, 208 292, 207 278 Z" fill="#F5CBA7"/>

    <!-- Zapatilla Deportiva Inclinada con Talón Caído -->
    <path d="M 184 328 L 210 315 L 218 315 L 212 322 L 186 332 Z" fill="#1E293B"/>
    <line x1="186" y1="331" x2="214" y2="317" stroke="#E2E8F0" stroke-width="2.5"/>
    <circle cx="200" cy="324" r="2" fill="#0F969C"/>

    <!-- Brazos Sujetando Barra -->
    <path d="M 188 110 C 178 122, 175 136, 181 144 C 187 138, 193 128, 197 114" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="181" cy="140" r="3.5" fill="#DE9E78"/>

    <!-- Barra Olímpica y Disco 20kg -->
    <rect x="135" y="108" width="130" height="5" rx="2" fill="#CBD5E1"/>
    <circle cx="245" cy="110" r="26" fill="#1E293B" stroke="#0F969C" stroke-width="2.5"/>
    <circle cx="245" cy="110" r="18" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <circle cx="245" cy="110" r="10" fill="#1E293B"/>
    <circle cx="245" cy="110" r="3.5" fill="#E2E8F0"/>
    <text x="245" y="98" fill="#6DA5C0" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">20 KG</text>
  </g>

  <!-- ==================== FASE 2: PUNTILLAS MÁXIMA ALTURA ==================== -->
  <g id="calf-p2">
    <!-- Taco Elevador -->
    <rect x="575" y="315" width="55" height="15" rx="3" fill="#1E293B" stroke="#294D61" stroke-width="1.5"/>
    <line x1="575" y1="318" x2="630" y2="318" stroke="#0F969C" stroke-width="1.5" stroke-opacity="0.5"/>

    <!-- Pierna Lejana (Sombra) -->
    <path d="M 595 155 C 590 190, 588 230, 590 255 C 588 275, 592 295, 596 308 L 610 308 L 610 255 C 608 230, 608 190, 605 155 Z" fill="#C6835F" opacity="0.4"/>

    <!-- Cabeza y Cabello Elevados (Cuerpo sube 25px) -->
    <circle cx="600" cy="55" r="13" fill="#F5CBA7"/>
    <path d="M 594 43 C 604 41, 612 48, 612 58 C 612 65, 606 69, 598 68 C 592 67, 590 58, 591 51 Z" fill="#1C1917"/>
    <path d="M 592 56 C 582 62, 578 72, 582 78 C 586 74, 590 66, 595 60 Z" fill="#1C1917"/>
    <rect x="596" y="67" width="8" height="16" fill="#F5CBA7"/>

    <!-- Torso Erguido Elevado -->
    <path d="M 588 83 C 600 81, 610 81, 620 83 C 617 105, 613 130, 610 150 C 603 153, 597 153, 591 150 C 588 130, 586 105, 588 83 Z" fill="#0F969C" stroke="#0C7075" stroke-width="1.2"/>
    <line x1="604" y1="87" x2="601" y2="150" stroke="#05161A" stroke-width="1.2"/>

    <!-- Shorts Oscuros -->
    <path d="M 590 149 C 598 152, 606 152, 612 149 C 614 163, 614 177, 612 185 C 605 188, 597 188, 589 185 C 587 177, 588 163, 590 149 Z" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <path d="M 592 153 L 592 183" stroke="#0F969C" stroke-width="1.2"/>

    <!-- Muslo -->
    <path d="M 589 183 C 584 205, 585 233, 591 253 C 595 257, 603 257, 607 253 C 610 233, 610 205, 609 183 Z" fill="#F5CBA7"/>

    <!-- FOCO NEUROMUSCULAR: GASTROCNEMIO EN FORMA DE DIAMANTE CONTRÍDO AL MÁXIMO -->
    <!-- Resplandor exterior -->
    <ellipse cx="600" cy="275" rx="18" ry="24" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 594 268 C 600 262, 606 262, 608 272" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>

    <!-- Curva muscular del gemelo hipertrofiado -->
    <path d="M 591 253 C 578 268, 580 288, 594 305 L 606 305 C 618 288, 616 268, 607 253 Z" fill="#F5CBA7"/>

    <!-- Zapatilla en FLEXIÓN PLANTAR ALTA SOBRE EL TACO -->
    <path d="M 596 305 L 606 305 L 618 315 L 610 322 L 598 312 Z" fill="#1E293B"/>
    <line x1="600" y1="310" x2="618" y2="315" stroke="#E2E8F0" stroke-width="2.5"/>
    <circle cx="608" cy="312" r="2" fill="#0F969C"/>

    <!-- Brazos con Barra Elevada -->
    <path d="M 588 85 C 578 97, 575 111, 581 119 C 587 113, 593 103, 597 89" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="581" cy="115" r="3.5" fill="#DE9E78"/>

    <!-- Barra Olímpica Elevada Arriba con Resplandor -->
    <rect x="535" y="83" width="130" height="5" rx="2" fill="#CBD5E1"/>
    <circle cx="645" cy="85" r="26" fill="#1E293B" stroke="#0F969C" stroke-width="2.5" filter="url(#glow)"/>
    <circle cx="645" cy="85" r="18" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <circle cx="645" cy="85" r="10" fill="#1E293B"/>
    <circle cx="645" cy="85" r="3.5" fill="#E2E8F0"/>
    <text x="645" y="73" fill="#0F969C" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">20 KG</text>
  </g>
</svg>'''

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 840, "height": 420})
    page.set_content(f"""<!DOCTYPE html>
<html>
<body style="margin:0; background:#000; display:flex; justify-content:center; align-items:center; min-height:100vh;">
{test_svg}
</body>
</html>""")
    page.screenshot(path='test_solid_calf.png')
    browser.close()

print("Generated test_solid_calf.png successfully!")
