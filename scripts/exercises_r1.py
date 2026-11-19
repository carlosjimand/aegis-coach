# Rutina 1: Pierna 1 (Dominancia Rodilla & Cuádriceps)
# Anatomía 2D Atlética Sólida de Alta Fidelidad
from scripts.svg_base_helper import get_svg_wrapper

def get_r1_exercises():
    exercises = {}

    # ----------------------------------------------------
    # EX 1.1: SENTADILLA CON BARRA / BOX SQUAT
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_1_1'] = get_svg_wrapper(
        title="SENTADILLA CON BARRA / BOX SQUAT",
        muscle_target="CUÁDRICEPS &amp; GLÚTEO MAYOR (PARALELO)",
        phase1_name="INICIAL ERGUIDA",
        phase2_name="FONDO PARALELO",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 1.2: PRENSA DE PIERNAS 45°
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_1_2'] = get_svg_wrapper(
        title="PRENSA DE PIERNAS 45°",
        muscle_target="CUÁDRICEPS &amp; VASTOS (EMPUJE 45°)",
        phase1_name="DESCENSO CONTROLADO",
        phase2_name="EXTENSIÓN COMPLETA",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 1.3: EXTENSIÓN DE CUÁDRICEPS EN MÁQUINA
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_1_3'] = get_svg_wrapper(
        title="EXTENSIÓN DE CUÁDRICEPS EN MÁQUINA",
        muscle_target="RECTO FEMORAL &amp; VASTO MEDIAL (BLOQUEO ISOMÉTRICO)",
        phase1_name="INICIAL FLEXIONADA",
        phase2_name="EXTENSIÓN 180° PICO",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 1.4: GEMELOS DE PIE CON BARRA
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_1_4'] = get_svg_wrapper(
        title="GEMELOS DE PIE CON BARRA",
        muscle_target="GASTROCNEMIO / GEMELOS (FLEXIÓN PLANTAR PICO)",
        phase1_name="TALONES ABAJO (ESTIRAMIENTO)",
        phase2_name="PUNTILLAS MÁXIMA ALTURA",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 1.5: SPANISH SQUAT CON BANDA ISOMÉTRICA
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_1_5'] = get_svg_wrapper(
        title="SPANISH SQUAT CON BANDA ISOMÉTRICA",
        muscle_target="CUÁDRICEPS &amp; BLINDAJE ROTULIANO (TIBIA 90°)",
        phase1_name="INICIAL ERGUIDO",
        phase2_name="ISOMETRÍA 90° VERTICAL",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 1.6: RUEDA ABDOMINAL CORE (AB WHEEL ROLLOUT)
    # ----------------------------------------------------
    p1 = '''
    <rect x="80" y="324" width="70" height="6" rx="2" fill="#0B1519" stroke="#294D61" stroke-width="1"/>
    
    <!-- Atleta de Rodillas Compacto -->
    <path d="M 115 320 L 115 260 L 128 260 L 128 320 Z" fill="#F5CBA7"/>
    <path d="M 125 255 L 180 245 L 182 260 L 127 270 Z" fill="#0F969C"/>
    <circle cx="195" cy="230" r="12" fill="#F5CBA7"/>
    
    <!-- Brazos verticales apoyados en rueda -->
    <line x1="180" y1="245" x2="180" y2="305" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round"/>
    <circle cx="180" cy="315" r="15" fill="#1E293B" stroke="#0F969C" stroke-width="2"/>
    <circle cx="180" cy="315" r="5" fill="#E2E8F0"/>
    '''

    p2 = '''
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
    '''
    exercises['ex_1_6'] = get_svg_wrapper(
        title="RUEDA ABDOMINAL CORE (AB WHEEL)",
        muscle_target="RECTO ABDOMINAL &amp; ANTI-EXTENSIÓN LUMBAR",
        phase1_name="INICIAL DE RODILLAS",
        phase2_name="ROLLOUT EXTENDIDO PICO",
        content_phase1=p1,
        content_phase2=p2
    )

    return exercises
