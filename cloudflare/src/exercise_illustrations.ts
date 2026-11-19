// Sistema Visual Anatómico Deportivo 2D para Aegis Coach
// 24 Ejercicios Oficiales en SVG Puro Vectorial de Alta Fidelidad
// Paleta: #05161A (Canvas), #072E33 (Spruce), #0C7075 (Teal Profundo), #0F969C (Luminoso), #6DA5C0 (Cielo), #294D61 (Pizarra)

export const EXERCISE_SVGS: Record<string, string> = {
  "ex_1_1": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · INICIAL ERGUIDA</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · FONDO PARALELO</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      SENTADILLA CON BARRA / BOX SQUAT &bull; FOCO: <tspan fill="#0F969C" font-weight="700">CUÁDRICEPS &amp; GLÚTEO MAYOR (PARALELO)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Cajón de Box Squat al fondo -->
    <rect x="90" y="255" width="55" height="75" rx="4" fill="#0B1519" stroke="#294D61" stroke-width="1.2"/>
    
    <!-- Pierna Lejana (Sombra) -->
    <path d="M 195 185 C 190 215, 188 250, 192 280 C 192 300, 190 315, 188 328 L 202 328 L 202 330 L 182 330 C 184 300, 182 270, 180 240 C 182 215, 185 195, 190 185 Z" fill="#C6835F" opacity="0.4"/>
    
    <!-- Cabeza y Cabello Atlético -->
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
    
    <!-- Gemelo en Forma de Diamante -->
    <path d="M 191 278 C 187 290, 187 304, 192 318 C 194 324, 195 328, 194 328 L 205 328 C 206 328, 207 322, 209 312 C 211 298, 210 286, 207 278 Z" fill="#F5CBA7"/>
    
    <!-- Zapatilla Deportiva Estable -->
    <path d="M 190 325 L 209 325 C 213 327, 213 330, 209 330 L 188 330 C 186 328, 188 325, 190 325 Z" fill="#1E293B"/>
    <rect x="187" y="327" width="24" height="3" rx="1.5" fill="#E2E8F0"/>
    <path d="M 195 326 L 202 326" stroke="#0F969C" stroke-width="1.2" stroke-linecap="round"/>
    
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

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Cajón de Box Squat Paralelo -->
    <rect x="475" y="235" width="55" height="95" rx="4" fill="#0B1519" stroke="#294D61" stroke-width="1.2"/>
    <line x1="475" y1="235" x2="530" y2="235" stroke="#0F969C" stroke-width="2" stroke-opacity="0.8"/>
    
    <!-- Pierna Lejana Profunda (Sombra) -->
    <g opacity="0.4">
      <path d="M 545 235 C 570 232, 600 232, 622 240 C 624 260, 620 290, 616 322 L 630 322 L 630 328 L 608 328 C 610 295, 612 265, 608 248 Z" fill="#C6835F"/>
    </g>
    
    <!-- Torso Inclinado 45° Fuerte y Estable -->
    <path d="M 535 152 C 555 142, 570 148, 578 162 C 565 180, 545 208, 522 225 C 512 220, 505 212, 505 202 C 515 182, 525 165, 535 152 Z" fill="#0F969C" stroke="#0C7075" stroke-width="1.2"/>
    
    <!-- Cabeza y Cuello con Mirada al Frente -->
    <path d="M 568 146 C 574 140, 578 136, 584 132 L 590 138 C 586 144, 580 150, 576 154 Z" fill="#F5CBA7"/>
    <circle cx="590" cy="128" r="12" fill="#F5CBA7"/>
    <path d="M 583 118 C 593 115, 601 122, 601 132 C 601 140, 593 144, 585 142 C 579 140, 577 130, 579 124 Z" fill="#1C1917"/>
    <path d="M 580 130 C 567 136, 565 148, 570 154 C 575 150, 578 144, 583 136 Z" fill="#1C1917"/>
    
    <!-- FOCO NEUROMUSCULAR: CUÁDRICEPS & GLÚTEO EN FONDO -->
    <path d="M 500 204 C 508 190, 525 200, 538 214 C 555 228, 572 230, 580 236 C 578 248, 562 255, 545 250 C 525 242, 505 230, 500 204 Z" fill="#0F969C" fill-opacity="0.45" filter="url(#glow)"/>
    
    <!-- Mallas / Shorts en Ángulo -->
    <path d="M 506 202 C 514 194, 528 204, 536 216 C 528 228, 516 238, 505 236 C 500 224, 500 212, 506 202 Z" fill="#05161A" stroke="#0F969C" stroke-width="1.5"/>
    
    <!-- Muslo Paralelo al Cajón (Cuádriceps en Tensión Excéntrica Pico) -->
    <path d="M 528 214 C 548 218, 562 220, 578 230 C 582 236, 580 246, 572 252 C 555 252, 538 246, 520 238 Z" fill="#F5CBA7"/>
    <path d="M 545 228 C 558 230, 568 236, 572 244" stroke="#6DA5C0" stroke-width="2" stroke-linecap="round" fill="none"/>
    
    <!-- Rodilla a 90° y Pantorrilla Estable -->
    <path d="M 574 232 C 584 240, 585 258, 582 278 C 580 298, 576 318, 575 325 L 562 325 C 564 308, 568 288, 570 268 C 572 250, 570 238, 568 232 Z" fill="#F5CBA7"/>
    
    <!-- Zapatilla Deportiva Apoyada -->
    <path d="M 558 325 L 582 325 C 586 327, 586 330, 582 330 L 554 330 C 552 328, 554 325, 558 325 Z" fill="#1E293B"/>
    <rect x="553" y="327" width="31" height="3" rx="1.5" fill="#E2E8F0"/>
    <path d="M 564 326 L 572 326" stroke="#0F969C" stroke-width="1.2" stroke-linecap="round"/>
    
    <!-- Brazos Sujetando Barra -->
    <path d="M 554 158 C 546 174, 542 190, 548 198 C 554 192, 558 180, 562 164" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="550" cy="194" r="3.5" fill="#DE9E78"/>
    
    <!-- Barra Olímpica y Disco 20kg -->
    <rect x="505" y="155" width="130" height="5" rx="2" fill="#CBD5E1"/>
    <circle cx="620" cy="157" r="26" fill="#1E293B" stroke="#0F969C" stroke-width="2.5" filter="url(#glow)"/>
    <circle cx="620" cy="157" r="18" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <circle cx="620" cy="157" r="10" fill="#1E293B"/>
    <circle cx="620" cy="157" r="3.5" fill="#E2E8F0"/>
    <text x="620" y="145" fill="#0F969C" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">20 KG</text>
    
  </g>
</svg>`,
  "ex_1_2": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · DESCENSO CONTROLADO</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · EXTENSIÓN COMPLETA</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      PRENSA DE PIERNAS 45° &bull; FOCO: <tspan fill="#0F969C" font-weight="700">CUÁDRICEPS &amp; VASTOS (EMPUJE 45°)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Raíles a 45° y Asiento -->
    <line x1="80" y1="320" x2="260" y2="140" stroke="#294D61" stroke-width="6" stroke-linecap="round"/>
    <line x1="90" y1="325" x2="270" y2="145" stroke="#1E293B" stroke-width="4" stroke-linecap="round"/>
    <rect x="110" y="240" width="70" height="20" rx="4" transform="rotate(-45 110 240)" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    
    <!-- Plataforma móvil descendida (Fase 1) -->
    <rect x="190" y="160" width="16" height="50" rx="3" transform="rotate(-45 190 160)" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    <circle cx="215" cy="165" r="20" fill="#1E293B" stroke="#0F969C" stroke-width="2"/>
    
    <!-- Atleta en Prensa: Torso Sólido en Top Teal -->
    <path d="M 125 255 L 165 215 L 175 225 L 135 265 Z" fill="#0F969C"/>
    <circle cx="112" cy="270" r="12" fill="#F5CBA7"/>
    <path d="M 106 260 C 114 257, 122 263, 122 272 C 122 280, 114 283, 107 281 Z" fill="#1C1917"/>
    
    <!-- Manos en asas laterales -->
    <line x1="145" y1="245" x2="138" y2="270" stroke="#F5CBA7" stroke-width="5" stroke-linecap="round"/>
    
    <!-- Pierna flexionada a 90°: Muslo y pantorrilla sólidos -->
    <path d="M 160 220 C 155 195, 165 175, 185 160 L 195 170 C 180 185, 170 205, 172 230 Z" fill="#F5CBA7"/>
    <path d="M 185 160 C 198 172, 212 182, 225 195 L 215 205 C 202 192, 190 180, 175 170 Z" fill="#F5CBA7"/>
    <!-- Zapatilla en plataforma -->
    <rect x="220" y="185" width="22" height="10" rx="2" transform="rotate(-45 220 185)" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Raíles a 45° -->
    <line x1="480" y1="320" x2="660" y2="140" stroke="#294D61" stroke-width="6" stroke-linecap="round"/>
    <line x1="490" y1="325" x2="670" y2="145" stroke="#1E293B" stroke-width="4" stroke-linecap="round"/>
    <rect x="510" y="240" width="70" height="20" rx="4" transform="rotate(-45 510 240)" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    
    <!-- Plataforma móvil empujada arriba (Fase 2) -->
    <rect x="245" y="105" width="16" height="50" rx="3" transform="translate(390, 0) rotate(-45 245 105)" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    <circle cx="655" cy="125" r="20" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    
    <!-- Torso apoyado -->
    <path d="M 525 255 L 565 215 L 575 225 L 535 265 Z" fill="#0F969C"/>
    <circle cx="512" cy="270" r="12" fill="#F5CBA7"/>
    <path d="M 506 260 C 514 257, 522 263, 522 272 C 522 280, 514 283, 507 281 Z" fill="#1C1917"/>
    <line x1="545" y1="245" x2="538" y2="270" stroke="#F5CBA7" stroke-width="5" stroke-linecap="round"/>
    
    <!-- PIERNA EXTENDIDA 45° CON RESPLANDOR -->
    <path d="M 565 215 L 640 140 L 648 148 L 575 225 Z" fill="#F5CBA7"/>
    <!-- Glow en el cuádriceps -->
    <ellipse cx="595" cy="185" rx="30" ry="14" transform="rotate(-45 595 185)" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <line x1="580" y1="200" x2="610" y2="170" stroke="#6DA5C0" stroke-width="2.5" stroke-linecap="round"/>
    
    <!-- Zapatilla en plataforma elevada -->
    <rect x="635" y="130" width="22" height="10" rx="2" transform="rotate(-45 635 130)" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_1_3": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · INICIAL FLEXIONADA</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · EXTENSIÓN 180° PICO</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      EXTENSIÓN DE CUÁDRICEPS EN MÁQUINA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">RECTO FEMORAL &amp; VASTO MEDIAL (BLOQUEO ISOMÉTRICO)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Sillón de Máquina -->
    <rect x="130" y="240" width="60" height="14" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="120" y="150" width="14" height="95" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="150" y="254" width="8" height="76" fill="#1E293B"/>
    
    <!-- Atleta Sentado Erguido (Torso Sólido Teal) -->
    <path d="M 124 165 C 132 165, 140 165, 144 165 L 144 240 C 138 240, 130 240, 124 240 Z" fill="#0F969C"/>
    <circle cx="132" cy="140" r="12" fill="#F5CBA7"/>
    <path d="M 126 130 C 134 128, 142 134, 142 143 C 142 150, 134 153, 127 151 Z" fill="#1C1917"/>
    <line x1="136" y1="210" x2="160" y2="235" stroke="#F5CBA7" stroke-width="5" stroke-linecap="round"/>
    
    <!-- Muslo horizontal sobre el asiento -->
    <path d="M 135 235 L 195 235 L 195 248 L 135 248 Z" fill="#F5CBA7"/>
    <rect x="132" y="232" width="40" height="16" rx="3" fill="#05161A"/>
    
    <!-- Pierna vertical a 90° hacia abajo con rodillo (Fase 1) -->
    <path d="M 188 245 L 188 315 L 200 315 L 200 245 Z" fill="#F5CBA7"/>
    <circle cx="195" cy="310" r="10" fill="#294D61" stroke="#0F969C" stroke-width="1.5"/>
    <rect x="190" y="318" width="22" height="10" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Sillón de Máquina -->
    <rect x="530" y="240" width="60" height="14" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="520" y="150" width="14" height="95" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="550" y="254" width="8" height="76" fill="#1E293B"/>
    
    <!-- Atleta Sentado -->
    <path d="M 524 165 C 532 165, 540 165, 544 165 L 544 240 C 538 240, 530 240, 524 240 Z" fill="#0F969C"/>
    <circle cx="532" cy="140" r="12" fill="#F5CBA7"/>
    <path d="M 526 130 C 534 128, 542 134, 542 143 C 542 150, 534 153, 527 151 Z" fill="#1C1917"/>
    <line x1="536" y1="210" x2="560" y2="235" stroke="#F5CBA7" stroke-width="5" stroke-linecap="round"/>
    
    <!-- Muslo horizontal -->
    <path d="M 535 235 L 595 235 L 595 248 L 535 248 Z" fill="#F5CBA7"/>
    <rect x="532" y="232" width="40" height="16" rx="3" fill="#05161A"/>
    
    <!-- PIERNA EXTENDIDA 180° HORIZONTAL (Fase 2) -->
    <path d="M 595 236 L 675 236 L 675 247 L 595 247 Z" fill="#F5CBA7"/>
    <!-- Glow en el cuádriceps -->
    <ellipse cx="585" cy="235" rx="35" ry="14" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <line x1="565" y1="235" x2="610" y2="235" stroke="#6DA5C0" stroke-width="2.5" stroke-linecap="round"/>
    
    <!-- Rodillo elevado horizontal -->
    <circle cx="670" cy="240" r="10" fill="#294D61" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    <rect x="670" y="232" width="25" height="10" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_1_4": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · TALONES ABAJO (ESTIRAMIENTO)</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · PUNTILLAS MÁXIMA ALTURA</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      GEMELOS DE PIE CON BARRA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">GASTROCNEMIO / GEMELOS (FLEXIÓN PLANTAR PICO)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <rect x="175" y="315" width="55" height="15" rx="3" fill="#1E293B" stroke="#294D61" stroke-width="1.5"/>
    <line x1="175" y1="318" x2="230" y2="318" stroke="#0F969C" stroke-width="1.5" stroke-opacity="0.5"/>
    
    <path d="M 195 180 C 190 215, 188 255, 190 280 C 188 300, 185 315, 182 328 L 195 328 L 210 315 L 210 280 C 208 255, 208 215, 205 180 Z" fill="#C6835F" opacity="0.4"/>
    
    <circle cx="200" cy="80" r="13" fill="#F5CBA7"/>
    <path d="M 194 68 C 204 66, 212 73, 212 83 C 212 90, 206 94, 198 93 C 192 92, 190 83, 191 76 Z" fill="#1C1917"/>
    <path d="M 192 81 C 182 87, 178 97, 182 103 C 186 99, 190 91, 195 85 Z" fill="#1C1917"/>
    <rect x="196" y="92" width="8" height="16" fill="#F5CBA7"/>
    
    <path d="M 188 108 C 200 106, 210 106, 220 108 C 217 130, 213 155, 210 175 C 203 178, 197 178, 191 175 C 188 155, 186 130, 188 108 Z" fill="#0F969C" stroke="#0C7075" stroke-width="1.2"/>
    <line x1="204" y1="112" x2="201" y2="175" stroke="#05161A" stroke-width="1.2"/>
    
    <path d="M 190 174 C 198 177, 206 177, 212 174 C 214 188, 214 202, 212 210 C 205 213, 197 213, 189 210 C 187 202, 188 188, 190 174 Z" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <path d="M 192 178 L 192 208" stroke="#0F969C" stroke-width="1.2"/>
    
    <path d="M 189 208 C 184 230, 185 258, 191 278 C 195 282, 203 282, 207 278 C 210 258, 210 230, 209 208 Z" fill="#F5CBA7"/>
    <path d="M 191 278 C 187 290, 186 304, 189 324 L 202 324 C 206 306, 208 292, 207 278 Z" fill="#F5CBA7"/>
    
    <path d="M 184 328 L 210 315 L 218 315 L 212 322 L 186 332 Z" fill="#1E293B"/>
    <line x1="186" y1="331" x2="214" y2="317" stroke="#E2E8F0" stroke-width="2.5"/>
    <circle cx="200" cy="324" r="2" fill="#0F969C"/>
    
    <path d="M 188 110 C 178 122, 175 136, 181 144 C 187 138, 193 128, 197 114" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="181" cy="140" r="3.5" fill="#DE9E78"/>
    
    <rect x="135" y="108" width="130" height="5" rx="2" fill="#CBD5E1"/>
    <circle cx="245" cy="110" r="26" fill="#1E293B" stroke="#0F969C" stroke-width="2.5"/>
    <circle cx="245" cy="110" r="18" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <circle cx="245" cy="110" r="10" fill="#1E293B"/>
    <circle cx="245" cy="110" r="3.5" fill="#E2E8F0"/>
    <text x="245" y="98" fill="#6DA5C0" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">20 KG</text>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <rect x="575" y="315" width="55" height="15" rx="3" fill="#1E293B" stroke="#294D61" stroke-width="1.5"/>
    <line x1="575" y1="318" x2="630" y2="318" stroke="#0F969C" stroke-width="1.5" stroke-opacity="0.5"/>
    
    <path d="M 595 155 C 590 190, 588 230, 590 255 C 588 275, 592 295, 596 308 L 610 308 L 610 255 C 608 230, 608 190, 605 155 Z" fill="#C6835F" opacity="0.4"/>
    
    <circle cx="600" cy="55" r="13" fill="#F5CBA7"/>
    <path d="M 594 43 C 604 41, 612 48, 612 58 C 612 65, 606 69, 598 68 C 592 67, 590 58, 591 51 Z" fill="#1C1917"/>
    <path d="M 592 56 C 582 62, 578 72, 582 78 C 586 74, 590 66, 595 60 Z" fill="#1C1917"/>
    <rect x="596" y="67" width="8" height="16" fill="#F5CBA7"/>
    
    <path d="M 588 83 C 600 81, 610 81, 620 83 C 617 105, 613 130, 610 150 C 603 153, 597 153, 591 150 C 588 130, 586 105, 588 83 Z" fill="#0F969C" stroke="#0C7075" stroke-width="1.2"/>
    <line x1="604" y1="87" x2="601" y2="150" stroke="#05161A" stroke-width="1.2"/>
    
    <path d="M 590 149 C 598 152, 606 152, 612 149 C 614 163, 614 177, 612 185 C 605 188, 597 188, 589 185 C 587 177, 588 163, 590 149 Z" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <path d="M 592 153 L 592 183" stroke="#0F969C" stroke-width="1.2"/>
    
    <path d="M 589 183 C 584 205, 585 233, 591 253 C 595 257, 603 257, 607 253 C 610 233, 610 205, 609 183 Z" fill="#F5CBA7"/>
    
    <!-- FOCO NEUROMUSCULAR: GASTROCNEMIO EN DIAMANTE -->
    <ellipse cx="600" cy="275" rx="18" ry="24" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 594 268 C 600 262, 606 262, 608 272" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <path d="M 591 253 C 578 268, 580 288, 594 305 L 606 305 C 618 288, 616 268, 607 253 Z" fill="#F5CBA7"/>
    
    <path d="M 596 305 L 606 305 L 618 315 L 610 322 L 598 312 Z" fill="#1E293B"/>
    <line x1="600" y1="310" x2="618" y2="315" stroke="#E2E8F0" stroke-width="2.5"/>
    <circle cx="608" cy="312" r="2" fill="#0F969C"/>
    
    <path d="M 588 85 C 578 97, 575 111, 581 119 C 587 113, 593 103, 597 89" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="581" cy="115" r="3.5" fill="#DE9E78"/>
    
    <rect x="535" y="83" width="130" height="5" rx="2" fill="#CBD5E1"/>
    <circle cx="645" cy="85" r="26" fill="#1E293B" stroke="#0F969C" stroke-width="2.5" filter="url(#glow)"/>
    <circle cx="645" cy="85" r="18" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <circle cx="645" cy="85" r="10" fill="#1E293B"/>
    <circle cx="645" cy="85" r="3.5" fill="#E2E8F0"/>
    <text x="645" y="73" fill="#0F969C" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">20 KG</text>
    
  </g>
</svg>`,
  "ex_1_5": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · INICIAL ERGUIDO</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · ISOMETRÍA 90° VERTICAL</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      SPANISH SQUAT CON BANDA ISOMÉTRICA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">CUÁDRICEPS &amp; BLINDAJE ROTULIANO (TIBIA 90°)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Poste de Jaula -->
    <rect x="60" y="80" width="12" height="250" rx="2" fill="#1E293B" stroke="#294D61" stroke-width="1.5"/>
    <!-- Banda Elástica Anclada -->
    <line x1="72" y1="260" x2="190" y2="260" stroke="#0F969C" stroke-width="5" stroke-dasharray="8 2"/>
    
    <!-- Atleta de Pie Erguido Sólido -->
    <circle cx="195" cy="95" r="12" fill="#F5CBA7"/>
    <path d="M 189 85 C 197 83, 205 89, 205 98 C 205 105, 197 108, 190 106 Z" fill="#1C1917"/>
    <rect x="191" y="105" width="8" height="15" fill="#F5CBA7"/>
    
    <!-- Torso Teal -->
    <path d="M 185 120 L 205 120 L 202 185 L 188 185 Z" fill="#0F969C"/>
    <rect x="185" y="185" width="20" height="35" rx="3" fill="#05161A"/>
    
    <!-- Piernas Erguidas -->
    <path d="M 188 220 L 202 220 L 202 325 L 188 325 Z" fill="#F5CBA7"/>
    <rect x="186" y="322" width="24" height="8" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Poste de Jaula -->
    <rect x="460" y="80" width="12" height="250" rx="2" fill="#1E293B" stroke="#294D61" stroke-width="1.5"/>
    <!-- Banda Elástica Soportando el Peso -->
    <line x1="472" y1="260" x2="575" y2="260" stroke="#0F969C" stroke-width="7" filter="url(#glow)"/>
    
    <!-- Atleta Sentado Atrás con Tibias Rigurosamente Verticales -->
    <circle cx="545" cy="135" r="12" fill="#F5CBA7"/>
    <path d="M 539 125 C 547 123, 555 129, 555 138 C 555 145, 547 148, 540 146 Z" fill="#1C1917"/>
    <rect x="541" y="145" width="8" height="15" fill="#F5CBA7"/>
    
    <!-- Torso Erguido Teal -->
    <path d="M 535 160 L 555 160 L 555 215 L 535 215 Z" fill="#0F969C"/>
    <rect x="530" y="215" width="25" height="20" rx="3" fill="#05161A"/>
    
    <!-- Brazos al frente para equilibrio -->
    <line x1="550" y1="165" x2="515" y2="165" stroke="#F5CBA7" stroke-width="5" stroke-linecap="round"/>
    
    <!-- Muslo horizontal hacia atrás -->
    <path d="M 535 215 L 575 215 L 575 228 L 535 228 Z" fill="#F5CBA7"/>
    <!-- FOCO: VASTO MEDIAL & TENDÓN ROTULIANO (BLINDAJE ISOMÉTRICO) -->
    <ellipse cx="555" cy="220" rx="25" ry="14" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <line x1="540" y1="220" x2="570" y2="220" stroke="#6DA5C0" stroke-width="2.5" stroke-linecap="round"/>
    
    <!-- TIBIA RIGUROSAMENTE VERTICAL A 90° -->
    <path d="M 568 215 L 582 215 L 582 325 L 568 325 Z" fill="#F5CBA7"/>
    <rect x="566" y="322" width="24" height="8" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_1_6": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · INICIAL DE RODILLAS</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · ROLLOUT EXTENDIDO PICO</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      RUEDA ABDOMINAL CORE (AB WHEEL) &bull; FOCO: <tspan fill="#0F969C" font-weight="700">RECTO ABDOMINAL &amp; ANTI-EXTENSIÓN LUMBAR</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <rect x="80" y="324" width="70" height="6" rx="2" fill="#0B1519" stroke="#294D61" stroke-width="1"/>
    
    <!-- Atleta de Rodillas Compacto -->
    <path d="M 115 320 L 115 260 L 128 260 L 128 320 Z" fill="#F5CBA7"/>
    <path d="M 125 255 L 180 245 L 182 260 L 127 270 Z" fill="#0F969C"/>
    <circle cx="195" cy="230" r="12" fill="#F5CBA7"/>
    
    <!-- Brazos verticales apoyados en rueda -->
    <line x1="180" y1="245" x2="180" y2="305" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <circle cx="180" cy="315" r="15" fill="#1E293B" stroke="#0F969C" stroke-width="2"/>
    <circle cx="180" cy="315" r="5" fill="#E2E8F0"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <rect x="450" y="324" width="60" height="6" rx="2" fill="#0B1519" stroke="#294D61" stroke-width="1"/>
    
    <!-- Atleta EXTENDIDO HORIZONTAL TOTAL SUSPENDIDO -->
    <path d="M 470 320 L 540 290 L 545 300 L 475 325 Z" fill="#F5CBA7"/>
    <path d="M 535 290 L 620 270 L 622 284 L 537 304 Z" fill="#0F969C"/>
    <circle cx="635" cy="260" r="11" fill="#F5CBA7"/>
    
    <!-- FOCO NEUROMUSCULAR: CORE & ANTI-EXTENSIÓN LUMBAR -->
    <ellipse cx="560" cy="285" rx="35" ry="12" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <line x1="535" y1="285" x2="585" y2="285" stroke="#6DA5C0" stroke-width="2.5" stroke-linecap="round"/>
    
    <!-- Brazos extendidos hacia rueda -->
    <line x1="620" y1="270" x2="685" y2="305" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <circle cx="685" cy="315" r="15" fill="#1E293B" stroke="#0F969C" stroke-width="2.5" filter="url(#glow)"/>
    <circle cx="685" cy="315" r="5" fill="#E2E8F0"/>
    
  </g>
</svg>`,
  "ex_2_1": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · ESTIRAMIENTO SUPERIOR</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · COMPRESIÓN AL PECHO</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      JALÓN AL PECHO AGARRE CERRADO V &bull; FOCO: <tspan fill="#0F969C" font-weight="700">DORSAL ANCHO &amp; REDONDO MAYOR (TRACCIÓN VERTICAL)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Torre de Polea Alta y Asiento -->
    <line x1="200" y1="40" x2="200" y2="80" stroke="#475569" stroke-width="3"/>
    <circle cx="200" cy="40" r="10" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    <rect x="140" y="240" width="60" height="12" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.2"/>
    <rect x="175" y="210" width="25" height="10" rx="3" fill="#1E293B"/>
    
    <!-- Cable de Acero y Asa en V -->
    <line x1="200" y1="45" x2="200" y2="95" stroke="#6DA5C0" stroke-width="2.5"/>
    <path d="M 193 95 L 200 102 L 207 95" stroke="#E2E8F0" stroke-width="3" fill="none"/>
    
    <!-- Atleta Sentado Erguido con BRAZOS TOTALMENTE ESTIRADOS ARRIBA (Fase 1) -->
    <circle cx="165" cy="148" r="11" fill="#F5CBA7"/>
    <path d="M 160 140 C 168 138, 175 144, 175 152 C 175 158, 168 162, 161 160 Z" fill="#1C1917"/>
    <rect x="162" y="158" width="6" height="12" fill="#F5CBA7"/>
    
    <!-- Torso Sólido Teal -->
    <path d="M 155 170 L 175 170 L 175 240 L 155 240 Z" fill="#0F969C"/>
    <rect x="153" y="238" width="24" height="20" rx="2" fill="#05161A"/>
    
    <!-- Brazos extendidos hacia arriba en V -->
    <line x1="165" y1="172" x2="198" y2="102" stroke="#F5CBA7" stroke-width="7" stroke-linecap="round"/>
    <circle cx="198" cy="102" r="4.5" fill="#DE9E78"/>
    
    <!-- Piernas bajo la rodillera y pie plantado -->
    <path d="M 165 240 L 205 240 L 205 325 L 195 325 L 195 250 L 165 250 Z" fill="#F5CBA7"/>
    <rect x="195" y="322" width="22" height="8" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Torre de Polea Alta -->
    <line x1="600" y1="40" x2="600" y2="80" stroke="#475569" stroke-width="3"/>
    <circle cx="600" cy="40" r="10" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    <rect x="540" y="240" width="60" height="12" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.2"/>
    <rect x="575" y="210" width="25" height="10" rx="3" fill="#1E293B"/>
    
    <!-- Cable bajado al pecho -->
    <line x1="600" y1="45" x2="590" y2="175" stroke="#6DA5C0" stroke-width="2.5"/>
    
    <!-- Atleta Sentado con ASA EN V BAJADA AL PECHO (Fase 2) -->
    <circle cx="578" cy="150" r="11" fill="#F5CBA7"/>
    <path d="M 573 142 C 581 140, 588 146, 588 154 C 588 160, 581 164, 574 162 Z" fill="#1C1917"/>
    <rect x="575" y="160" width="6" height="12" fill="#F5CBA7"/>
    
    <!-- Torso Inclinado 15° Sólido -->
    <path d="M 568 172 L 588 172 L 570 240 L 550 240 Z" fill="#0F969C"/>
    <rect x="548" y="238" width="24" height="20" rx="2" fill="#05161A"/>
    
    <!-- FOCO NEUROMUSCULAR: DORSAL ANCHO COMPRIMIDO -->
    <ellipse cx="568" cy="190" rx="16" ry="24" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 565 180 C 572 188, 572 200, 566 208" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Brazos con Codos Pegados Tirando Abajo -->
    <line x1="580" y1="175" x2="562" y2="210" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <line x1="562" y1="210" x2="588" y2="175" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <path d="M 584 172 L 590 178 L 596 172" stroke="#E2E8F0" stroke-width="3" fill="none"/>
    <circle cx="590" cy="176" r="4.5" fill="#DE9E78"/>
    
    <!-- Piernas -->
    <path d="M 560 240 L 605 240 L 605 325 L 595 325 L 595 250 L 560 250 Z" fill="#F5CBA7"/>
    <rect x="595" y="322" width="22" height="8" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_2_2": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · ESTIRAMIENTO INFERIOR</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · CODO AL BOLSILLO TRASERO</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      REMO DORIAN UNILATERAL MANCUERNA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">DORSAL ANCHO INFERIOR &amp; TRAPECIO MEDIO</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Banco Plano -->
    <rect x="75" y="235" width="130" height="15" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.2"/>
    <rect x="90" y="250" width="8" height="80" fill="#1E293B"/>
    <rect x="180" y="250" width="8" height="80" fill="#1E293B"/>
    
    <!-- Apoyo de rodilla y mano -->
    <path d="M 115 235 L 115 285 L 125 285 L 125 235 Z" fill="#F5CBA7"/>
    <line x1="185" y1="235" x2="185" y2="180" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    
    <!-- Torso Horizontal Espalda Plana (Top Teal) -->
    <path d="M 125 175 L 185 175 L 185 195 L 125 195 Z" fill="#0F969C"/>
    <circle cx="198" cy="172" r="11" fill="#F5CBA7"/>
    <path d="M 193 164 C 201 162, 208 168, 208 176 C 208 182, 201 186, 194 184 Z" fill="#1C1917"/>
    
    <!-- Pierna de pie en el suelo -->
    <path d="M 135 195 L 140 240 L 140 325 L 130 325 L 130 240 Z" fill="#F5CBA7"/>
    <rect x="128" y="322" width="22" height="8" rx="2" fill="#1E293B"/>
    
    <!-- Brazo Libre COLGANDO CON MANCUERNA (Fase 1 Estiramiento) -->
    <line x1="165" y1="185" x2="165" y2="275" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <circle cx="165" cy="275" r="4.5" fill="#DE9E78"/>
    <!-- Mancuerna Hexagonal Abajo -->
    <rect x="155" y="278" width="20" height="25" rx="3" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    <line x1="165" y1="275" x2="165" y2="303" stroke="#94A3B8" stroke-width="3"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Banco Plano -->
    <rect x="475" y="235" width="130" height="15" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.2"/>
    <rect x="490" y="250" width="8" height="80" fill="#1E293B"/>
    <rect x="580" y="250" width="8" height="80" fill="#1E293B"/>
    
    <!-- Apoyo -->
    <path d="M 515 235 L 515 285 L 525 285 L 525 235 Z" fill="#F5CBA7"/>
    <line x1="585" y1="235" x2="585" y2="180" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    
    <!-- Torso Horizontal -->
    <path d="M 525 175 L 585 175 L 585 195 L 525 195 Z" fill="#0F969C"/>
    <circle cx="598" cy="172" r="11" fill="#F5CBA7"/>
    <path d="M 593 164 C 601 162, 608 168, 608 176 C 608 182, 601 186, 594 184 Z" fill="#1C1917"/>
    
    <!-- Pierna de pie -->
    <path d="M 535 195 L 540 240 L 540 325 L 530 325 L 530 240 Z" fill="#F5CBA7"/>
    <rect x="528" y="322" width="22" height="8" rx="2" fill="#1E293B"/>
    
    <!-- FOCO NEUROMUSCULAR: DORSAL ANCHO CONTRACCIÓN PICO -->
    <ellipse cx="548" cy="180" rx="18" ry="14" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 540 180 C 548 176, 555 178, 558 184" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Brazo Remando: CODO ELEVADO HACIA EL BOLSILLO TRASERO (Fase 2) -->
    <path d="M 570 185 L 545 155 L 552 182" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="552" cy="182" r="4.5" fill="#DE9E78"/>
    <!-- Mancuerna Pegada al Costado -->
    <rect x="542" y="170" width="20" height="25" rx="3" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    <line x1="552" y1="170" x2="552" y2="195" stroke="#94A3B8" stroke-width="3"/>
    
  </g>
</svg>`,
  "ex_2_3": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · ESTIRAMIENTO FRONTAL</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · TRACCIÓN AL ESTERNÓN</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      REMO GIRONDA CON AGARRE AMPLIO &bull; FOCO: <tspan fill="#0F969C" font-weight="700">ESPALDA ALTA, ROMBOIDES &amp; TRAPECIO (RETRACCIÓN ESCAPULAR)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Estación de Polea Baja Sentada -->
    <rect x="90" y="270" width="80" height="12" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.2"/>
    <rect x="230" y="250" width="10" height="35" rx="2" fill="#1E293B"/>
    <circle cx="250" cy="265" r="8" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    
    <!-- Cable tenso y Barra Amplia al Frente -->
    <line x1="250" y1="265" x2="190" y2="210" stroke="#6DA5C0" stroke-width="2"/>
    <line x1="190" y1="195" x2="190" y2="225" stroke="#E2E8F0" stroke-width="3"/>
    
    <!-- Atleta Sentado (Fase 1) -->
    <circle cx="140" cy="180" r="11" fill="#F5CBA7"/>
    <path d="M 135 172 C 143 170, 150 176, 150 184 C 150 190, 143 194, 136 192 Z" fill="#1C1917"/>
    <path d="M 125 270 L 140 200 L 155 200 L 140 270 Z" fill="#0F969C"/>
    
    <!-- Brazos rectos al frente -->
    <line x1="145" y1="205" x2="190" y2="210" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    
    <!-- Piernas semiflexionadas -->
    <path d="M 125 270 L 175 255 L 230 265 L 230 275 L 175 265 L 125 275 Z" fill="#F5CBA7"/>
    <rect x="228" y="260" width="10" height="18" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Estación de Polea Baja -->
    <rect x="490" y="270" width="80" height="12" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.2"/>
    <rect x="630" y="250" width="10" height="35" rx="2" fill="#1E293B"/>
    <circle cx="650" cy="265" r="8" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    
    <!-- Cable traccionado -->
    <line x1="650" y1="265" x2="570" y2="205" stroke="#6DA5C0" stroke-width="2"/>
    
    <!-- Atleta Sentado Erguido (Fase 2) -->
    <circle cx="534" cy="175" r="11" fill="#F5CBA7"/>
    <path d="M 529 167 C 537 165, 544 171, 544 179 C 544 185, 537 189, 530 187 Z" fill="#1C1917"/>
    <path d="M 520 270 L 530 195 L 545 195 L 535 270 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: ESPALDA ALTA & ROMBOIDES -->
    <ellipse cx="530" cy="198" rx="16" ry="18" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 525 192 C 532 198, 532 205, 526 210" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Codos Abiertos a 45° Tirando Hacia Atrás -->
    <path d="M 532 200 L 505 210 L 565 205" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <line x1="565" y1="190" x2="565" y2="220" stroke="#E2E8F0" stroke-width="3" filter="url(#glow)"/>
    <circle cx="565" cy="205" r="4.5" fill="#DE9E78"/>
    
    <!-- Piernas -->
    <path d="M 525 270 L 575 255 L 630 265 L 630 275 L 575 265 L 525 275 Z" fill="#F5CBA7"/>
    <rect x="628" y="260" width="10" height="18" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_2_4": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · ESTIRAMIENTO HACIA POLEA</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · ROTACIÓN EXTERNA A SIENES</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      FACE PULL EN POLEA ALTA CON CUERDA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">DELTOIDES POSTERIOR &amp; MANGUITO ROTADOR (SALUD ARTICULAR)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Torre de Polea Alta -->
    <line x1="60" y1="50" x2="60" y2="120" stroke="#475569" stroke-width="3"/>
    <circle cx="60" cy="50" r="10" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    <line x1="60" y1="55" x2="160" y2="135" stroke="#6DA5C0" stroke-width="2"/>
    <line x1="160" y1="135" x2="175" y2="145" stroke="#E2E8F0" stroke-width="3"/>
    
    <!-- Atleta de Pie con Brazos Extendidos Arriba (Fase 1) -->
    <circle cx="218" cy="135" r="11" fill="#F5CBA7"/>
    <path d="M 213 127 C 221 125, 228 131, 228 139 C 228 145, 221 149, 214 147 Z" fill="#1C1917"/>
    
    <!-- Torso Erguido Teal -->
    <path d="M 210 155 L 225 155 L 215 225 L 200 225 Z" fill="#0F969C"/>
    
    <!-- Brazos extendidos hacia polea -->
    <line x1="215" y1="160" x2="175" y2="145" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    
    <!-- Piernas en zancada corta -->
    <path d="M 205 225 L 195 275 L 195 325 L 205 325 L 205 275 Z" fill="#F5CBA7"/>
    <path d="M 215 225 L 230 275 L 235 325 L 225 325 L 220 275 Z" fill="#F5CBA7"/>
    <rect x="188" y="322" width="20" height="8" rx="2" fill="#1E293B"/>
    <rect x="225" y="322" width="20" height="8" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Torre de Polea Alta -->
    <line x1="460" y1="50" x2="460" y2="120" stroke="#475569" stroke-width="3"/>
    <circle cx="460" cy="50" r="10" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    <line x1="460" y1="55" x2="595" y2="135" stroke="#6DA5C0" stroke-width="2"/>
    
    <!-- Atleta con CUERDA TRACCIONADA A LA FRENTE (Fase 2) -->
    <circle cx="618" cy="135" r="11" fill="#F5CBA7"/>
    <path d="M 613 127 C 621 125, 628 131, 628 139 C 628 145, 621 149, 614 147 Z" fill="#1C1917"/>
    <path d="M 610 155 L 625 155 L 615 225 L 600 225 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: DELTOIDES POSTERIOR & ROTADORES -->
    <circle cx="620" cy="155" r="14" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 616 150 C 622 150, 625 156, 622 162" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Codos Altos a 90° con Rotación Externa -->
    <path d="M 615 160 L 640 145 L 600 135" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <line x1="595" y1="125" x2="600" y2="145" stroke="#E2E8F0" stroke-width="3" filter="url(#glow)"/>
    
    <!-- Piernas -->
    <path d="M 605 225 L 595 275 L 595 325 L 605 325 L 605 275 Z" fill="#F5CBA7"/>
    <path d="M 615 225 L 630 275 L 635 325 L 625 325 L 620 275 Z" fill="#F5CBA7"/>
    <rect x="588" y="322" width="20" height="8" rx="2" fill="#1E293B"/>
    <rect x="625" y="322" width="20" height="8" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_2_5": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · ESTIRAMIENTO VERTICAL ATRÁS</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · FLEXIÓN CON SUPINACIÓN</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      CURL DE BÍCEPS EN BANCO INCLINADO 45° &bull; FOCO: <tspan fill="#0F969C" font-weight="700">CABEZA LARGA DEL BÍCEPS (TENSIÓN EXCÉNTRICA EN ESTIRAMIENTO)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Banco Inclinado 45° -->
    <line x1="110" y1="290" x2="185" y2="160" stroke="#294D61" stroke-width="8" stroke-linecap="round"/>
    <rect x="135" y="270" width="8" height="60" fill="#1E293B"/>
    <rect x="155" y="280" width="40" height="12" rx="3" fill="#0B1519"/>
    
    <!-- Atleta Recostado (Fase 1: Brazos Colgando Atrás) -->
    <circle cx="188" cy="165" r="11" fill="#F5CBA7"/>
    <path d="M 125 280 L 175 185 L 188 195 L 138 290 Z" fill="#0F969C"/>
    
    <!-- Brazo colgando recto abajo -->
    <line x1="168" y1="195" x2="168" y2="270" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <circle cx="168" cy="270" r="4.5" fill="#DE9E78"/>
    <!-- Mancuerna Abajo -->
    <rect x="158" y="272" width="20" height="12" rx="2" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    
    <!-- Piernas -->
    <path d="M 155 285 L 195 285 L 195 328 L 185 328 L 185 295 L 155 295 Z" fill="#F5CBA7"/>
    <rect x="185" y="325" width="22" height="6" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Banco Inclinado 45° -->
    <line x1="510" y1="290" x2="585" y2="160" stroke="#294D61" stroke-width="8" stroke-linecap="round"/>
    <rect x="535" y="270" width="8" height="60" fill="#1E293B"/>
    <rect x="555" y="280" width="40" height="12" rx="3" fill="#0B1519"/>
    
    <!-- Atleta Recostado (Fase 2: Flexión Bíceps) -->
    <circle cx="588" cy="165" r="11" fill="#F5CBA7"/>
    <path d="M 525 280 L 575 185 L 588 195 L 538 290 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: CABEZA LARGA DEL BÍCEPS EN PICO -->
    <circle cx="572" cy="205" r="12" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 568 200 C 574 198, 578 204, 575 210" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Antebrazo Flexionado con Supinación -->
    <path d="M 565 195 L 565 240 L 575 200" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="575" cy="200" r="4.5" fill="#DE9E78"/>
    <!-- Mancuerna Arriba -->
    <rect x="565" y="194" width="20" height="12" rx="2" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    
    <!-- Piernas -->
    <path d="M 555 285 L 595 285 L 595 328 L 585 328 L 585 295 L 555 295 Z" fill="#F5CBA7"/>
    <rect x="585" y="325" width="22" height="6" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_2_6": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · APOYO EXTENDIDO EN PAD</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · FLEXIÓN A LA BARBILLA</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      CURL EN BANCO SCOTT / PREDICADOR &bull; FOCO: <tspan fill="#0F969C" font-weight="700">BRAQUIAL ANTERIOR &amp; BÍCEPS (AISLAMIENTO ESTRICTO)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Banco Scott / Predicador -->
    <rect x="110" y="270" width="40" height="12" rx="3" fill="#0B1519"/>
    <rect x="130" y="282" width="8" height="48" fill="#1E293B"/>
    <polygon points="160,230 185,255 195,255 170,230" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    
    <!-- Atleta Sentado con Brazos Apoyados Extendidos (Fase 1) -->
    <circle cx="150" cy="195" r="11" fill="#F5CBA7"/>
    <path d="M 125 270 L 145 210 L 155 210 L 135 270 Z" fill="#0F969C"/>
    
    <!-- Brazos extendidos sobre la almohadilla inclinada -->
    <line x1="145" y1="215" x2="205" y2="250" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <line x1="205" y1="238" x2="205" y2="262" stroke="#E2E8F0" stroke-width="4"/>
    <circle cx="205" cy="250" r="10" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Banco Scott / Predicador -->
    <rect x="510" y="270" width="40" height="12" rx="3" fill="#0B1519"/>
    <rect x="530" y="282" width="8" height="48" fill="#1E293B"/>
    <polygon points="560,230 585,255 595,255 570,230" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    
    <!-- Atleta Sentado (Fase 2: Flexión a la Barbilla) -->
    <circle cx="550" cy="195" r="11" fill="#F5CBA7"/>
    <path d="M 525 270 L 545 210 L 555 210 L 535 270 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: BRAQUIAL ANTERIOR & BÍCEPS AISLADO -->
    <circle cx="568" cy="225" r="12" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 564 220 C 570 218, 574 224, 571 230" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Brazos Flexionados Llevando Barra a la Barbilla -->
    <path d="M 545 215 L 575 235 L 570 205" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <line x1="570" y1="193" x2="570" y2="217" stroke="#E2E8F0" stroke-width="4" filter="url(#glow)"/>
    <circle cx="570" cy="205" r="10" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    
  </g>
</svg>`,
  "ex_3_1": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · DESCENSO PÉLVICO</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · EXTENSIÓN 180° BLOQUEO</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      HIP THRUST CON BARRA EN BANCO &bull; FOCO: <tspan fill="#0F969C" font-weight="700">GLÚTEO MAYOR (BLOQUEO HORIZONTAL 1s)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Banco Plano Horizontal -->
    <rect x="70" y="220" width="55" height="85" rx="5" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="82" y="305" width="8" height="25" fill="#1E293B"/>
    
    <!-- Torso Inclinado Hacia Abajo Sólido (Fase 1) -->
    <path d="M 115 210 Q 140 240 168 275 L 150 285 Q 120 245 105 220 Z" fill="#0F969C"/>
    <circle cx="96" cy="180" r="12" fill="#F5CBA7"/>
    <path d="M 90 170 C 100 167 108 174 108 184 C 108 192 100 195 92 193 Z" fill="#1C1917"/>
    
    <!-- Shorts Oscuros -->
    <path d="M 148 265 L 180 262 L 185 285 L 150 292 Z" fill="#05161A" stroke="#294D61" stroke-width="1"/>
    
    <!-- Muslo y Pantorrilla Flexionados -->
    <path d="M 178 268 Q 210 238 238 245 Q 248 285 250 320 L 238 320 Q 236 285 226 250 Q 200 245 174 272 Z" fill="#F5CBA7"/>
    <rect x="235" y="322" width="28" height="8" rx="2" fill="#1E293B"/>
    
    <!-- Barra Olímpica y Disco 20kg en Pelvis -->
    <rect x="164" y="215" width="6" height="100" rx="2" fill="#CBD5E1"/>
    <circle cx="168" cy="265" r="28" fill="#1E293B" stroke="#0F969C" stroke-width="2.5"/>
    <circle cx="168" cy="265" r="18" fill="#05161A"/>
    <circle cx="168" cy="265" r="10" fill="#1E293B"/>
    <text x="168" y="252" fill="#6DA5C0" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">20 KG</text>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Banco Plano Horizontal -->
    <rect x="445" y="220" width="55" height="85" rx="5" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="457" y="305" width="8" height="25" fill="#1E293B"/>
    
    <!-- Torso y Muslo en LÍNEA HORIZONTAL TOTAL A 180° SÓLIDO (Fase 2) -->
    <path d="M 485 204 L 575 204 L 570 226 L 482 224 Z" fill="#0F969C"/>
    <circle cx="452" cy="184" r="12" fill="#F5CBA7"/>
    <path d="M 446 174 C 456 171 464 178 464 188 C 464 196 456 200 448 198 Z" fill="#1C1917"/>
    
    <!-- FOCO NEUROMUSCULAR: GLÚTEO MAYOR EN BLOQUEO HORIZONTAL -->
    <ellipse cx="568" cy="214" rx="26" ry="18" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 552 214 Q 570 204 584 214" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Muslo Horizontal y Tibia Estrictamente Vertical a 90° -->
    <path d="M 570 205 L 655 205 L 655 322 L 642 322 L 642 220 L 570 220 Z" fill="#F5CBA7"/>
    <rect x="640" y="322" width="28" height="8" rx="2" fill="#1E293B"/>
    
    <!-- Barra Olímpica Elevada en Bloqueo con Resplandor -->
    <rect x="565" y="155" width="6" height="100" rx="2" fill="#CBD5E1"/>
    <circle cx="568" cy="208" r="28" fill="#1E293B" stroke="#0F969C" stroke-width="2.5" filter="url(#glow)"/>
    <circle cx="568" cy="208" r="18" fill="#05161A"/>
    <circle cx="568" cy="208" r="10" fill="#1E293B"/>
    <text x="568" y="195" fill="#0F969C" font-family="monospace" font-size="6" font-weight="700" text-anchor="middle">20 KG</text>
    
  </g>
</svg>`,
  "ex_3_2": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · INICIAL ERGUIDO</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · BISAGRA EXCÉNTRICA PICO</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      PESO MUERTO RUMANO UNILATERAL (RDL) &bull; FOCO: <tspan fill="#0F969C" font-weight="700">ISQUIOTIBIAL PROXIMAL &amp; CADENA POSTERIOR (BISAGRA PURA)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Atleta de Pie Erguido Sólido (Fase 1) -->
    <circle cx="195" cy="85" r="12" fill="#F5CBA7"/>
    <path d="M 189 75 C 197 73 205 79 205 88 C 205 95 197 98 190 96 Z" fill="#1C1917"/>
    <rect x="191" y="95" width="8" height="15" fill="#F5CBA7"/>
    
    <path d="M 185 110 L 205 110 L 202 185 L 188 185 Z" fill="#0F969C"/>
    <rect x="185" y="180" width="20" height="35" rx="3" fill="#05161A"/>
    
    <!-- Piernas Erguidas -->
    <path d="M 188 215 L 202 215 L 202 325 L 188 325 Z" fill="#F5CBA7"/>
    <rect x="186" y="322" width="24" height="8" rx="2" fill="#1E293B"/>
    
    <!-- Brazos con Mancuerna sostenida al frente -->
    <line x1="195" y1="125" x2="180" y2="200" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <rect x="170" y="200" width="18" height="18" rx="3" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Atleta en BISAGRA DE CADERA A 60° (Fase 2) -->
    <circle cx="608" cy="145" r="12" fill="#F5CBA7"/>
    <path d="M 602 135 C 610 133 618 139 618 148 C 618 155 610 158 603 156 Z" fill="#1C1917"/>
    
    <!-- Torso inclinado a 60° sólido -->
    <path d="M 535 205 L 595 160 L 602 170 L 542 215 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: ISQUIOTIBIAL PROXIMAL EN TENSIÓN EXCÉNTRICA MÁXIMA -->
    <ellipse cx="538" cy="245" rx="16" ry="34" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 535 225 C 542 245 542 265 536 280" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Pierna Delantera con Cadera Atrás -->
    <path d="M 532 205 L 544 265 L 544 325 L 532 325 L 532 265 Z" fill="#F5CBA7"/>
    <rect x="530" y="322" width="24" height="8" rx="2" fill="#1E293B"/>
    
    <!-- Pierna Trasera Staggered en punta -->
    <path d="M 535 205 L 505 265 L 490 325 L 498 325 L 512 265 Z" fill="#C6835F" opacity="0.5"/>
    <rect x="485" y="322" width="16" height="8" rx="2" fill="#1E293B" opacity="0.6"/>
    
    <!-- Brazos con Mancuerna Rozando la Espinilla -->
    <line x1="585" y1="165" x2="565" y2="265" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <rect x="555" y="265" width="18" height="22" rx="3" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    <line x1="564" y1="265" x2="564" y2="287" stroke="#94A3B8" stroke-width="3"/>
    
  </g>
</svg>`,
  "ex_3_3": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · DESCENSO EN ÁNGULO</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · EMPUJE DE TALONES</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      PRENSA 45° PIES ALTOS Y ANCHOS &bull; FOCO: <tspan fill="#0F969C" font-weight="700">GLÚTEOS &amp; ADUCTORES (DESCARGA ROTULIANA)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Prensa 45° -->
    <line x1="80" y1="320" x2="260" y2="140" stroke="#294D61" stroke-width="6" stroke-linecap="round"/>
    <rect x="110" y="240" width="70" height="20" rx="4" transform="rotate(-45 110 240)" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="190" y="160" width="16" height="50" rx="3" transform="rotate(-45 190 160)" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    <circle cx="215" cy="165" r="20" fill="#1E293B" stroke="#0F969C" stroke-width="2"/>
    
    <!-- Atleta con Pies Altos -->
    <path d="M 125 255 L 165 215 L 175 225 L 135 265 Z" fill="#0F969C"/>
    <circle cx="112" cy="270" r="12" fill="#F5CBA7"/>
    <path d="M 165 215 C 160 185, 175 165, 205 155 L 215 165 C 190 175, 178 195, 180 225 Z" fill="#F5CBA7"/>
    <path d="M 205 155 L 240 180 L 235 190 L 200 165 Z" fill="#F5CBA7"/>
    <rect x="235" y="170" width="22" height="10" rx="2" transform="rotate(-45 235 170)" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Prensa 45° -->
    <line x1="480" y1="320" x2="660" y2="140" stroke="#294D61" stroke-width="6" stroke-linecap="round"/>
    <rect x="510" y="240" width="70" height="20" rx="4" transform="rotate(-45 510 240)" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="635" y="105" width="16" height="50" rx="3" transform="rotate(-45 635 105)" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    <circle cx="655" cy="125" r="20" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    
    <!-- Atleta con Empuje de Talones Altos -->
    <path d="M 525 255 L 565 215 L 575 225 L 535 265 Z" fill="#0F969C"/>
    <circle cx="512" cy="270" r="12" fill="#F5CBA7"/>
    
    <!-- FOCO NEUROMUSCULAR: GLÚTEO MAYOR & ADUCTORES -->
    <ellipse cx="555" cy="225" rx="26" ry="18" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    
    <!-- Piernas extendidas arriba con pies altos -->
    <path d="M 565 215 L 650 135 L 658 143 L 575 225 Z" fill="#F5CBA7"/>
    <rect x="645" y="125" width="22" height="10" rx="2" transform="rotate(-45 645 125)" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_3_4": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · DORSIFLEXIÓN ESTIRADA</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · FLEXIÓN PLANTAR AISLADA</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      SÓLEO SENTADO EN MÁQUINA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">SÓLEO (AMORTIGUACIÓN DE IMPACTO 6-8x EN RUNNING)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Máquina de Sóleo Sentado -->
    <rect x="110" y="240" width="50" height="14" rx="3" fill="#0B1519"/>
    <rect x="175" y="235" width="30" height="14" rx="4" fill="#0B1519" stroke="#294D61" stroke-width="1.5"/>
    <rect x="185" y="315" width="40" height="15" rx="2" fill="#1E293B"/>
    
    <!-- Atleta Sentado a 90° (Fase 1: Talón Caído) -->
    <circle cx="125" cy="145" r="11" fill="#F5CBA7"/>
    <path d="M 120 160 L 135 160 L 135 240 L 120 240 Z" fill="#0F969C"/>
    
    <!-- Muslo horizontal bajo rodillera -->
    <path d="M 125 235 L 190 235 L 190 248 L 125 248 Z" fill="#F5CBA7"/>
    <!-- Tibia vertical y TALÓN BAJADO EN DORSIFLEXIÓN -->
    <path d="M 184 240 L 196 240 L 196 322 L 184 322 Z" fill="#F5CBA7"/>
    <path d="M 182 326 L 205 315 L 208 320 L 185 330 Z" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Máquina de Sóleo Sentado -->
    <rect x="510" y="240" width="50" height="14" rx="3" fill="#0B1519"/>
    <rect x="575" y="222" width="30" height="14" rx="4" fill="#0B1519" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    <rect x="585" y="315" width="40" height="15" rx="2" fill="#1E293B"/>
    
    <!-- Atleta Sentado -->
    <circle cx="525" cy="145" r="11" fill="#F5CBA7"/>
    <path d="M 520 160 L 535 160 L 535 240 L 520 240 Z" fill="#0F969C"/>
    
    <!-- Muslo elevado unos grados -->
    <path d="M 525 235 L 590 223 L 590 236 L 525 248 Z" fill="#F5CBA7"/>
    
    <!-- FOCO NEUROMUSCULAR: SÓLEO AISLADO EN FLEXIÓN PLANTAR -->
    <ellipse cx="590" cy="275" rx="16" ry="24" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 586 265 C 592 270 592 280 588 288" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Tibia y PUNTILLAS MÁXIMAS ELEVANDO LA CARGA -->
    <path d="M 584 228 L 596 228 L 596 305 L 584 305 Z" fill="#F5CBA7"/>
    <path d="M 590 305 L 590 315 L 602 318 L 598 324 Z" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_3_5": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · ESTIRAMIENTO PRONO</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · FLEXIÓN 90° TALONES A GLÚTEO</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      CURL FEMORAL TUMBADO (HSR) &bull; FOCO: <tspan fill="#0F969C" font-weight="700">ISQUIOTIBIALES &amp; BÍCEPS FEMORAL (SARCOMEROGÉNESIS)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Camilla de Curl Femoral -->
    <line x1="80" y1="260" x2="220" y2="260" stroke="#0B1519" stroke-width="14" stroke-linecap="round"/>
    <rect x="120" y="267" width="8" height="63" fill="#1E293B"/>
    <rect x="190" y="267" width="8" height="63" fill="#1E293B"/>
    
    <!-- Atleta Tumbado Boca Abajo con Piernas Extendidas (Fase 1) -->
    <circle cx="85" cy="245" r="10" fill="#F5CBA7"/>
    <path d="M 95 245 L 155 245 L 155 258 L 95 258 Z" fill="#0F969C"/>
    
    <!-- Piernas extendidas con rodillo en tendón de Aquiles -->
    <path d="M 155 246 L 235 246 L 235 258 L 155 258 Z" fill="#F5CBA7"/>
    <circle cx="230" cy="245" r="9" fill="#294D61" stroke="#0F969C" stroke-width="1.5"/>
    <rect x="235" y="248" width="16" height="8" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Camilla de Curl Femoral -->
    <line x1="480" y1="260" x2="620" y2="260" stroke="#0B1519" stroke-width="14" stroke-linecap="round"/>
    <rect x="520" y="267" width="8" height="63" fill="#1E293B"/>
    <rect x="590" y="267" width="8" height="63" fill="#1E293B"/>
    
    <!-- Atleta Tumbado Boca Abajo -->
    <circle cx="485" cy="245" r="10" fill="#F5CBA7"/>
    <path d="M 495 245 L 555 245 L 555 258 L 495 258 Z" fill="#0F969C"/>
    
    <!-- Muslo en la camilla -->
    <path d="M 555 246 L 595 246 L 595 258 L 555 258 Z" fill="#F5CBA7"/>
    
    <!-- FOCO NEUROMUSCULAR: BÍCEPS FEMORAL EN CONTRACCIÓN PICO -->
    <ellipse cx="585" cy="230" rx="18" ry="20" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 578 240 C 585 230 592 230 590 215" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Pierna FLEXIONADA LLEVANDO TALONES A GLÚTEOS (Fase 2) -->
    <path d="M 588 250 L 588 190 L 600 190 L 600 250 Z" fill="#F5CBA7"/>
    <circle cx="585" cy="190" r="9" fill="#294D61" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    <rect x="585" y="180" width="16" height="8" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_3_6": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · COLGADO EXTENDIDO</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · ELEVACIÓN EN L 90°</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      ELEVACIONES DE PIERNAS COLGADO &bull; FOCO: <tspan fill="#0F969C" font-weight="700">CORE INFERIOR, PSOAS &amp; FLEXORES (POSICIÓN EN L 90°)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Barra de Dominadas Alta -->
    <line x1="120" y1="50" x2="260" y2="50" stroke="#1E293B" stroke-width="6" stroke-linecap="round"/>
    <circle cx="190" cy="50" r="6" fill="#0F969C"/>
    
    <!-- Atleta Colgado en Extensión Vertical (Fase 1) -->
    <line x1="190" y1="50" x2="190" y2="110" stroke="#F5CBA7" stroke-width="7" stroke-linecap="round"/>
    <circle cx="190" cy="120" r="11" fill="#F5CBA7"/>
    <path d="M 183 130 L 197 130 L 197 215 L 183 215 Z" fill="#0F969C"/>
    
    <!-- Piernas juntas colgando verticalmente -->
    <path d="M 184 215 L 196 215 L 196 315 L 184 315 Z" fill="#F5CBA7"/>
    <rect x="184" y="315" width="16" height="10" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Barra de Dominadas Alta -->
    <line x1="520" y1="50" x2="660" y2="50" stroke="#1E293B" stroke-width="6" stroke-linecap="round"/>
    <circle cx="590" cy="50" r="6" fill="#0F969C"/>
    
    <!-- Atleta Colgado con RETROVERSIÓN PÉLVICA -->
    <line x1="590" y1="50" x2="590" y2="110" stroke="#F5CBA7" stroke-width="7" stroke-linecap="round"/>
    <circle cx="590" cy="120" r="11" fill="#F5CBA7"/>
    <path d="M 583 130 L 597 130 L 595 215 L 581 215 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: CORE INFERIOR EN COMPRESIÓN -->
    <ellipse cx="585" cy="205" rx="20" ry="16" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 578 200 C 585 195 592 205 585 212" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- PIERNAS ELEVADAS EN L HORIZONTAL A 90° (Fase 2) -->
    <path d="M 588 208 L 665 208 L 665 220 L 588 220 Z" fill="#F5CBA7"/>
    <rect x="660" y="208" width="16" height="12" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_4_1": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · BARRA EN ESTERNÓN</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · BLOQUEO VERTICAL ARRIBA</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      PRESS DE BANCA PLANO CON BARRA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">PECTORAL MAYOR &amp; TRÍCEPS (EMPUJE EXPLOSIVO)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Banco Plano Horizontal -->
    <rect x="75" y="240" width="130" height="15" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.2"/>
    <rect x="90" y="255" width="8" height="75" fill="#1E293B"/>
    <rect x="180" y="255" width="8" height="75" fill="#1E293B"/>
    <line x1="85" y1="160" x2="85" y2="255" stroke="#334155" stroke-width="4"/>
    
    <!-- Atleta Tumbado en el Banco (Fase 1: BARRA EN EL PECHO) -->
    <circle cx="95" cy="235" r="11" fill="#F5CBA7"/>
    <path d="M 105 228 L 175 228 L 175 242 L 105 242 Z" fill="#0F969C"/>
    
    <!-- Piernas plantadas -->
    <path d="M 170 235 L 185 270 L 185 328 L 175 328 L 175 275 L 165 240 Z" fill="#F5CBA7"/>
    <rect x="175" y="325" width="22" height="6" rx="2" fill="#1E293B"/>
    
    <!-- Brazos con Codos a 90° Abajo -->
    <path d="M 135 235 L 135 250 L 135 205" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="135" cy="205" r="4.5" fill="#DE9E78"/>
    
    <!-- Barra Olímpica y Disco 20kg en el Pecho -->
    <rect x="70" y="202" width="130" height="5" rx="2" fill="#CBD5E1"/>
    <circle cx="185" cy="204" r="26" fill="#1E293B" stroke="#0F969C" stroke-width="2.5"/>
    <circle cx="185" cy="204" r="12" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Banco Plano Horizontal -->
    <rect x="475" y="240" width="130" height="15" rx="3" fill="#0B1519" stroke="#294D61" stroke-width="1.2"/>
    <rect x="490" y="255" width="8" height="75" fill="#1E293B"/>
    <rect x="580" y="255" width="8" height="75" fill="#1E293B"/>
    <line x1="485" y1="160" x2="485" y2="255" stroke="#334155" stroke-width="4"/>
    
    <!-- Atleta Tumbado en el Banco (Fase 2: Bloqueo Vertical) -->
    <circle cx="495" cy="235" r="11" fill="#F5CBA7"/>
    <path d="M 505 228 L 575 228 L 575 242 L 505 242 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: PECTORAL MAYOR & TRÍCEPS EN BLOQUEO -->
    <ellipse cx="535" cy="230" rx="24" ry="12" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 525 228 C 535 224 545 224 550 230" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Piernas plantadas -->
    <path d="M 570 235 L 585 270 L 585 328 L 575 328 L 575 275 L 565 240 Z" fill="#F5CBA7"/>
    <rect x="575" y="325" width="22" height="6" rx="2" fill="#1E293B"/>
    
    <!-- Brazos TOTALMENTE EXTENDIDOS ARRIBA EN BLOQUEO -->
    <line x1="535" y1="230" x2="535" y2="155" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <circle cx="535" cy="155" r="4.5" fill="#DE9E78"/>
    
    <!-- Barra Olímpica Elevada Arriba -->
    <rect x="470" y="152" width="130" height="5" rx="2" fill="#CBD5E1"/>
    <circle cx="585" cy="154" r="26" fill="#1E293B" stroke="#0F969C" stroke-width="2.5" filter="url(#glow)"/>
    <circle cx="585" cy="154" r="12" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_4_2": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · DESCENSO EN ÁNGULO 30°</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · EMPUJE CONVERGENTE</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      PRESS INCLINADO CON MANCUERNAS 30° &bull; FOCO: <tspan fill="#0F969C" font-weight="700">PECTORAL CLAVICULAR SUPERIOR &amp; DELTOIDES ANTERIOR</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Banco Inclinado 30° -->
    <line x1="90" y1="285" x2="195" y2="200" stroke="#294D61" stroke-width="8" stroke-linecap="round"/>
    <rect x="130" y="260" width="8" height="70" fill="#1E293B"/>
    
    <!-- Atleta Recostado (Fase 1: Mancuernas al Pecho Alto) -->
    <circle cx="190" cy="195" r="11" fill="#F5CBA7"/>
    <path d="M 110 275 L 180 215 L 188 225 L 118 285 Z" fill="#0F969C"/>
    
    <!-- Brazos flexionados con codos a 60° -->
    <path d="M 165 225 L 165 240 L 165 205" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <rect x="155" y="198" width="20" height="14" rx="2" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    
    <!-- Piernas -->
    <path d="M 140 280 L 180 280 L 180 328 L 170 328 L 170 290 L 140 290 Z" fill="#F5CBA7"/>
    <rect x="170" y="325" width="22" height="6" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Banco Inclinado 30° -->
    <line x1="490" y1="285" x2="595" y2="200" stroke="#294D61" stroke-width="8" stroke-linecap="round"/>
    <rect x="530" y="260" width="8" height="70" fill="#1E293B"/>
    
    <!-- Atleta Recostado (Fase 2: Empuje Arriba) -->
    <circle cx="590" cy="195" r="11" fill="#F5CBA7"/>
    <path d="M 510 275 L 580 215 L 588 225 L 518 285 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: PECTORAL SUPERIOR CLAVICULAR -->
    <circle cx="570" cy="215" r="16" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 565 210 C 572 208 578 214 574 220" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Brazos EXTENDIDOS ARRIBA -->
    <line x1="565" y1="220" x2="565" y2="145" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <circle cx="565" cy="145" r="4.5" fill="#DE9E78"/>
    <rect x="555" y="138" width="20" height="14" rx="2" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    
    <!-- Piernas -->
    <path d="M 540 280 L 580 280 L 580 328 L 570 328 L 570 290 L 540 290 Z" fill="#F5CBA7"/>
    <rect x="570" y="325" width="22" height="6" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_4_3": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · APERTURA PROFUNDA</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · CIERRE AL ESTERNÓN</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      PEC DECK / CONTRACTOR EN MÁQUINA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">PECTORAL MAYOR (COMPRESIÓN ISOMÉTRICA FRONTAL)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Máquina Pec Deck -->
    <rect x="130" y="240" width="45" height="12" rx="3" fill="#0B1519"/>
    <rect x="150" y="140" width="10" height="100" rx="2" fill="#0B1519"/>
    <rect x="145" y="252" width="8" height="76" fill="#1E293B"/>
    
    <!-- Atleta Sentado Erguido con BRAZOS ABIERTOS EN CRUZ (Fase 1) -->
    <circle cx="152" cy="140" r="11" fill="#F5CBA7"/>
    <path d="M 145 160 L 160 160 L 160 240 L 145 240 Z" fill="#0F969C"/>
    
    <!-- Brazos abiertos lateralmente -->
    <path d="M 152 175 L 115 175 L 115 140" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <rect x="110" y="130" width="10" height="25" rx="3" fill="#1E293B" stroke="#0F969C" stroke-width="1.2"/>
    
    <!-- Piernas -->
    <path d="M 152 240 L 190 240 L 190 328 L 180 328 L 180 250 L 152 250 Z" fill="#F5CBA7"/>
    <rect x="180" y="325" width="20" height="6" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Máquina Pec Deck -->
    <rect x="530" y="240" width="45" height="12" rx="3" fill="#0B1519"/>
    <rect x="550" y="140" width="10" height="100" rx="2" fill="#0B1519"/>
    <rect x="545" y="252" width="8" height="76" fill="#1E293B"/>
    
    <!-- Atleta Sentado (Fase 2: Cierre al Esternón) -->
    <circle cx="552" cy="140" r="11" fill="#F5CBA7"/>
    <path d="M 545 160 L 560 160 L 560 240 L 545 240 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: PECTORAL MAYOR EN COMPRESIÓN ISOMÉTRICA -->
    <ellipse cx="570" cy="175" rx="16" ry="20" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 565 168 C 572 172 572 180 566 184" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Brazos CERRADOS AL FRENTE EN ARCO -->
    <path d="M 552 175 L 585 175 L 585 140" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <rect x="580" y="130" width="10" height="25" rx="3" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    
    <!-- Piernas -->
    <path d="M 552 240 L 590 240 L 590 328 L 580 328 L 580 250 L 552 250 Z" fill="#F5CBA7"/>
    <rect x="580" y="325" width="20" height="6" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_4_4": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · INICIAL A LOS COSTADOS</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · ELEVACIÓN EN T A HOMBROS</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      ELEVACIONES LATERALES CON MANCUERNAS &bull; FOCO: <tspan fill="#0F969C" font-weight="700">DELTOIDES LATERAL (AMPLITUD DE HOMBROS EN T)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Atleta de Pie Erguido Sólido (Fase 1: Brazos a los Costados) -->
    <circle cx="195" cy="85" r="12" fill="#F5CBA7"/>
    <path d="M 189 75 C 197 73 205 79 205 88 C 205 95 197 98 190 96 Z" fill="#1C1917"/>
    <rect x="191" y="95" width="8" height="15" fill="#F5CBA7"/>
    
    <path d="M 185 110 L 205 110 L 202 185 L 188 185 Z" fill="#0F969C"/>
    <rect x="185" y="180" width="20" height="35" rx="3" fill="#05161A"/>
    
    <!-- Piernas -->
    <path d="M 188 215 L 202 215 L 202 325 L 188 325 Z" fill="#F5CBA7"/>
    <rect x="186" y="322" width="24" height="8" rx="2" fill="#1E293B"/>
    
    <!-- Brazos colgando a los lados -->
    <line x1="185" y1="125" x2="170" y2="200" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <rect x="162" y="195" width="16" height="12" rx="2" fill="#1E293B" stroke="#0F969C" stroke-width="1.2"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Atleta de Pie (Fase 2: Brazos en T) -->
    <circle cx="595" cy="85" r="12" fill="#F5CBA7"/>
    <path d="M 589 75 C 597 73 605 79 605 88 C 605 95 597 98 590 96 Z" fill="#1C1917"/>
    <rect x="591" y="95" width="8" height="15" fill="#F5CBA7"/>
    
    <path d="M 585 110 L 605 110 L 602 185 L 588 185 Z" fill="#0F969C"/>
    <rect x="585" y="180" width="20" height="35" rx="3" fill="#05161A"/>
    
    <!-- FOCO NEUROMUSCULAR: DELTOIDES LATERAL EN CONTRACCIÓN PICO -->
    <circle cx="580" cy="122" r="14" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <circle cx="610" cy="122" r="14" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 575 118 C 580 115 586 118 584 125" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Brazos ELEVADOS EN FORMA DE T A LA ALTURA DE HOMBROS -->
    <line x1="585" y1="125" x2="530" y2="135" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <line x1="605" y1="125" x2="660" y2="135" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <rect x="518" y="130" width="14" height="18" rx="2" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    <rect x="658" y="130" width="14" height="18" rx="2" fill="#1E293B" stroke="#0F969C" stroke-width="2" filter="url(#glow)"/>
    
    <!-- Piernas -->
    <path d="M 588 215 L 602 215 L 602 325 L 588 325 Z" fill="#F5CBA7"/>
    <rect x="586" y="322" width="24" height="8" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_4_5": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · INICIAL FLEXIÓN 90°</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · EXTENSIÓN Y APERTURA PICO</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      TRÍCEPS EN POLEA CON CUERDA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">TRÍCEPS BRAQUIAL (BLOQUEO Y APERTURA FINAL)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <!-- Torre de Polea Alta -->
    <line x1="130" y1="50" x2="130" y2="120" stroke="#475569" stroke-width="3"/>
    <circle cx="130" cy="50" r="10" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    <line x1="130" y1="55" x2="175" y2="175" stroke="#6DA5C0" stroke-width="2"/>
    
    <!-- Atleta con Codos Pegados Flexionados a 90° (Fase 1) -->
    <circle cx="205" cy="115" r="11" fill="#F5CBA7"/>
    <path d="M 200 130 L 215 130 L 210 215 L 195 215 Z" fill="#0F969C"/>
    
    <!-- Brazo a 90° -->
    <path d="M 200 145 L 195 185 L 175 175" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="175" cy="175" r="4.5" fill="#DE9E78"/>
    <line x1="175" y1="170" x2="175" y2="190" stroke="#E2E8F0" stroke-width="3"/>
    
    <!-- Piernas -->
    <path d="M 200 215 L 195 325 L 205 325 L 210 215 Z" fill="#F5CBA7"/>
    <rect x="188" y="322" width="22" height="8" rx="2" fill="#1E293B"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <!-- Torre de Polea Alta -->
    <line x1="530" y1="50" x2="530" y2="120" stroke="#475569" stroke-width="3"/>
    <circle cx="530" cy="50" r="10" fill="#1E293B" stroke="#0F969C" stroke-width="1.5"/>
    <line x1="530" y1="55" x2="575" y2="235" stroke="#6DA5C0" stroke-width="2"/>
    
    <!-- Atleta (Fase 2: Extensión Completa) -->
    <circle cx="605" cy="115" r="11" fill="#F5CBA7"/>
    <path d="M 600 130 L 615 130 L 610 215 L 595 215 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: TRÍCEPS EN BLOQUEO TOTAL -->
    <ellipse cx="602" cy="165" rx="14" ry="18" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <path d="M 600 155 C 605 158 605 168 601 172" stroke="#6DA5C0" stroke-width="2.5" fill="none"/>
    
    <!-- Brazo TOTALMENTE EXTENDIDO VERTICAL HACIA ABAJO -->
    <path d="M 600 145 L 595 185 L 585 245" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    <circle cx="585" cy="245" r="4.5" fill="#DE9E78"/>
    <!-- Cuerda separada en la base -->
    <line x1="580" y1="235" x2="570" y2="255" stroke="#E2E8F0" stroke-width="3" filter="url(#glow)"/>
    <line x1="585" y1="235" x2="595" y2="255" stroke="#E2E8F0" stroke-width="3" filter="url(#glow)"/>
    
    <!-- Piernas -->
    <path d="M 600 215 L 595 325 L 605 325 L 610 215 Z" fill="#F5CBA7"/>
    <rect x="588" y="322" width="22" height="8" rx="2" fill="#1E293B"/>
    
  </g>
</svg>`,
  "ex_4_6": `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
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

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · PREPARACIÓN DE RODILLAS</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · PUENTE HORIZONTAL RÍGIDO</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      PLANCHA FRONTAL CORE ESTRICTA &bull; FOCO: <tspan fill="#0F969C" font-weight="700">CORE GLOBAL &amp; TRANSVERSO (PUENTE HORIZONTAL SUSPENDIDO)</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    
    <rect x="80" y="324" width="150" height="6" rx="2" fill="#0B1519" stroke="#294D61" stroke-width="1"/>
    
    <!-- Atleta en Preparación (Fase 1: Rodillas y Antebrazos) -->
    <circle cx="195" cy="265" r="10" fill="#F5CBA7"/>
    <path d="M 125 270 L 180 270 L 180 282 L 125 282 Z" fill="#0F969C"/>
    <path d="M 115 320 L 115 270 L 125 270 L 125 320 Z" fill="#F5CBA7"/>
    <path d="M 175 270 L 175 320 L 195 320" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    
    <rect x="480" y="324" width="150" height="6" rx="2" fill="#0B1519" stroke="#294D61" stroke-width="1"/>
    
    <!-- Atleta en PUENTE HORIZONTAL TOTAL CON RETROVERSIÓN PÉLVICA (Fase 2) -->
    <circle cx="625" cy="275" r="10" fill="#F5CBA7"/>
    <path d="M 505 315 L 545 285 L 550 293 L 510 323 Z" fill="#F5CBA7"/>
    <path d="M 545 285 L 610 278 L 610 290 L 545 297 Z" fill="#0F969C"/>
    
    <!-- FOCO NEUROMUSCULAR: CORE GLOBAL EN RETROVERSIÓN ILUMINADO -->
    <ellipse cx="570" cy="285" rx="35" ry="12" fill="#0F969C" fill-opacity="0.5" filter="url(#glow)"/>
    <line x1="545" y1="285" x2="595" y2="285" stroke="#6DA5C0" stroke-width="2.5" stroke-linecap="round"/>
    
    <!-- Punteras de pies y antebrazo a 90° -->
    <rect x="495" y="315" width="16" height="10" rx="2" fill="#1E293B"/>
    <path d="M 605 280 L 605 320 L 625 320" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    
  </g>
</svg>`,
};

/**
 * Obtiene el SVG correspondiente a una rutina y número de ejercicio.
 * Si no existe, devuelve el SVG de Sentadilla / Hip Thrust por defecto.
 */
export function getExerciseSvg(routineId: number, exerciseNum: number): string {
  const key = `ex_${routineId}_${exerciseNum}`;
  return EXERCISE_SVGS[key] || EXERCISE_SVGS["ex_1_1"] || "";
}

/**
 * Devuelve un Data URI base64 o utf-8 para usar en etiquetas <img> si fuera necesario.
 */
export function getExerciseSvgDataUri(routineId: number, exerciseNum: number): string {
  const svg = getExerciseSvg(routineId, exerciseNum);
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
}
