# Rutina 2: Torso Tracción (Dorsal, Espalda Alta & Bíceps)
# Anatomía 2D Atlética Sólida de Alta Fidelidad
from scripts.svg_base_helper import get_svg_wrapper

def get_r2_exercises():
    exercises = {}

    # ----------------------------------------------------
    # EX 2.1: JALÓN AL PECHO AGARRE CERRADO V (V-GRIP)
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_2_1'] = get_svg_wrapper(
        title="JALÓN AL PECHO AGARRE CERRADO V",
        muscle_target="DORSAL ANCHO &amp; REDONDO MAYOR (TRACCIÓN VERTICAL)",
        phase1_name="ESTIRAMIENTO SUPERIOR",
        phase2_name="COMPRESIÓN AL PECHO",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 2.2: REMO DORIAN UNILATERAL CON MANCUERNA
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_2_2'] = get_svg_wrapper(
        title="REMO DORIAN UNILATERAL MANCUERNA",
        muscle_target="DORSAL ANCHO INFERIOR &amp; TRAPECIO MEDIO",
        phase1_name="ESTIRAMIENTO INFERIOR",
        phase2_name="CODO AL BOLSILLO TRASERO",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 2.3: REMO GIRONDA CON AGARRE AMPLIO
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_2_3'] = get_svg_wrapper(
        title="REMO GIRONDA CON AGARRE AMPLIO",
        muscle_target="ESPALDA ALTA, ROMBOIDES &amp; TRAPECIO (RETRACCIÓN ESCAPULAR)",
        phase1_name="ESTIRAMIENTO FRONTAL",
        phase2_name="TRACCIÓN AL ESTERNÓN",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 2.4: FACE PULL EN POLEA ALTA CON CUERDA
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_2_4'] = get_svg_wrapper(
        title="FACE PULL EN POLEA ALTA CON CUERDA",
        muscle_target="DELTOIDES POSTERIOR &amp; MANGUITO ROTADOR (SALUD ARTICULAR)",
        phase1_name="ESTIRAMIENTO HACIA POLEA",
        phase2_name="ROTACIÓN EXTERNA A SIENES",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 2.5: CURL DE BÍCEPS EN BANCO INCLINADO 45°
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_2_5'] = get_svg_wrapper(
        title="CURL DE BÍCEPS EN BANCO INCLINADO 45°",
        muscle_target="CABEZA LARGA DEL BÍCEPS (TENSIÓN EXCÉNTRICA EN ESTIRAMIENTO)",
        phase1_name="ESTIRAMIENTO VERTICAL ATRÁS",
        phase2_name="FLEXIÓN CON SUPINACIÓN",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 2.6: CURL EN BANCO SCOTT / PREDICADOR
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_2_6'] = get_svg_wrapper(
        title="CURL EN BANCO SCOTT / PREDICADOR",
        muscle_target="BRAQUIAL ANTERIOR &amp; BÍCEPS (AISLAMIENTO ESTRICTO)",
        phase1_name="APOYO EXTENDIDO EN PAD",
        phase2_name="FLEXIÓN A LA BARBILLA",
        content_phase1=p1,
        content_phase2=p2
    )

    return exercises
