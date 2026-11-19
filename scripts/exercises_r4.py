# Rutina 4: Torso Empuje (Pectoral, Hombro & Tríceps)
# Anatomía 2D Atlética Sólida de Alta Fidelidad
from scripts.svg_base_helper import get_svg_wrapper

def get_r4_exercises():
    exercises = {}

    # ----------------------------------------------------
    # EX 4.1: PRESS DE BANCA PLANO CON BARRA
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_4_1'] = get_svg_wrapper(
        title="PRESS DE BANCA PLANO CON BARRA",
        muscle_target="PECTORAL MAYOR &amp; TRÍCEPS (EMPUJE EXPLOSIVO)",
        phase1_name="BARRA EN ESTERNÓN",
        phase2_name="BLOQUEO VERTICAL ARRIBA",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 4.2: PRESS INCLINADO CON MANCUERNAS 30°
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_4_2'] = get_svg_wrapper(
        title="PRESS INCLINADO CON MANCUERNAS 30°",
        muscle_target="PECTORAL CLAVICULAR SUPERIOR &amp; DELTOIDES ANTERIOR",
        phase1_name="DESCENSO EN ÁNGULO 30°",
        phase2_name="EMPUJE CONVERGENTE",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 4.3: PEC DECK / CONTRACTOR EN MÁQUINA
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_4_3'] = get_svg_wrapper(
        title="PEC DECK / CONTRACTOR EN MÁQUINA",
        muscle_target="PECTORAL MAYOR (COMPRESIÓN ISOMÉTRICA FRONTAL)",
        phase1_name="APERTURA PROFUNDA",
        phase2_name="CIERRE AL ESTERNÓN",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 4.4: ELEVACIONES LATERALES CON MANCUERNAS
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_4_4'] = get_svg_wrapper(
        title="ELEVACIONES LATERALES CON MANCUERNAS",
        muscle_target="DELTOIDES LATERAL (AMPLITUD DE HOMBROS EN T)",
        phase1_name="INICIAL A LOS COSTADOS",
        phase2_name="ELEVACIÓN EN T A HOMBROS",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 4.5: TRÍCEPS EN POLEA CON CUERDA
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_4_5'] = get_svg_wrapper(
        title="TRÍCEPS EN POLEA CON CUERDA",
        muscle_target="TRÍCEPS BRAQUIAL (BLOQUEO Y APERTURA FINAL)",
        phase1_name="INICIAL FLEXIÓN 90°",
        phase2_name="EXTENSIÓN Y APERTURA PICO",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 4.6: PLANCHA FRONTAL CORE ESTRICTA
    # ----------------------------------------------------
    p1 = '''
    <rect x="80" y="324" width="150" height="6" rx="2" fill="#0B1519" stroke="#294D61" stroke-width="1"/>
    
    <!-- Atleta en Preparación (Fase 1: Rodillas y Antebrazos) -->
    <circle cx="195" cy="265" r="10" fill="#F5CBA7"/>
    <path d="M 125 270 L 180 270 L 180 282 L 125 282 Z" fill="#0F969C"/>
    <path d="M 115 320 L 115 270 L 125 270 L 125 320 Z" fill="#F5CBA7"/>
    <path d="M 175 270 L 175 320 L 195 320" stroke="#F5CBA7" stroke-width="6" stroke-linecap="round" fill="none"/>
    '''

    p2 = '''
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
    '''
    exercises['ex_4_6'] = get_svg_wrapper(
        title="PLANCHA FRONTAL CORE ESTRICTA",
        muscle_target="CORE GLOBAL &amp; TRANSVERSO (PUENTE HORIZONTAL SUSPENDIDO)",
        phase1_name="PREPARACIÓN DE RODILLAS",
        phase2_name="PUENTE HORIZONTAL RÍGIDO",
        content_phase1=p1,
        content_phase2=p2
    )

    return exercises
