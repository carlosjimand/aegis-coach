# Rutina 3: Pierna 2 (Cadena Posterior & Blindaje Isquios)
# Anatomía 2D Atlética Sólida de Alta Fidelidad
from scripts.svg_base_helper import get_svg_wrapper

def get_r3_exercises():
    exercises = {}

    # ----------------------------------------------------
    # EX 3.1: HIP THRUST CON BARRA EN BANCO
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_3_1'] = get_svg_wrapper(
        title="HIP THRUST CON BARRA EN BANCO",
        muscle_target="GLÚTEO MAYOR (BLOQUEO HORIZONTAL 1s)",
        phase1_name="DESCENSO PÉLVICO",
        phase2_name="EXTENSIÓN 180° BLOQUEO",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 3.2: PESO MUERTO RUMANO UNILATERAL (RDL)
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_3_2'] = get_svg_wrapper(
        title="PESO MUERTO RUMANO UNILATERAL (RDL)",
        muscle_target="ISQUIOTIBIAL PROXIMAL &amp; CADENA POSTERIOR (BISAGRA PURA)",
        phase1_name="INICIAL ERGUIDO",
        phase2_name="BISAGRA EXCÉNTRICA PICO",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 3.3: PRENSA 45° PIES ALTOS Y ANCHOS
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_3_3'] = get_svg_wrapper(
        title="PRENSA 45° PIES ALTOS Y ANCHOS",
        muscle_target="GLÚTEOS &amp; ADUCTORES (DESCARGA ROTULIANA)",
        phase1_name="DESCENSO EN ÁNGULO",
        phase2_name="EMPUJE DE TALONES",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 3.4: SÓLEO SENTADO EN MÁQUINA
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_3_4'] = get_svg_wrapper(
        title="SÓLEO SENTADO EN MÁQUINA",
        muscle_target="SÓLEO (AMORTIGUACIÓN DE IMPACTO 6-8x EN RUNNING)",
        phase1_name="DORSIFLEXIÓN ESTIRADA",
        phase2_name="FLEXIÓN PLANTAR AISLADA",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 3.5: CURL FEMORAL TUMBADO (HSR)
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_3_5'] = get_svg_wrapper(
        title="CURL FEMORAL TUMBADO (HSR)",
        muscle_target="ISQUIOTIBIALES &amp; BÍCEPS FEMORAL (SARCOMEROGÉNESIS)",
        phase1_name="ESTIRAMIENTO PRONO",
        phase2_name="FLEXIÓN 90° TALONES A GLÚTEO",
        content_phase1=p1,
        content_phase2=p2
    )

    # ----------------------------------------------------
    # EX 3.6: ELEVACIONES DE PIERNAS COLGADO (HANGING LEG RAISE)
    # ----------------------------------------------------
    p1 = '''
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
    '''

    p2 = '''
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
    '''
    exercises['ex_3_6'] = get_svg_wrapper(
        title="ELEVACIONES DE PIERNAS COLGADO",
        muscle_target="CORE INFERIOR, PSOAS &amp; FLEXORES (POSICIÓN EN L 90°)",
        phase1_name="COLGADO EXTENDIDO",
        phase2_name="ELEVACIÓN EN L 90°",
        content_phase1=p1,
        content_phase2=p2
    )

    return exercises
