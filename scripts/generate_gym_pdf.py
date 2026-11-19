import os
from playwright.sync_api import sync_playwright

output_pdf = r"c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\Rutinas_Gimnasio_Carlos.pdf"
output_html = r"c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\scripts\gym_routines.html"

# SVG definitions for exercise illustrations
svg_icons = {
    "squat": """<svg viewBox="0 0 100 100" class="ex-svg">
        <circle cx="50" cy="20" r="7" fill="#38bdf8"/>
        <!-- Torso angled -->
        <line x1="50" y1="27" x2="42" y2="52" stroke="#38bdf8" stroke-width="4" stroke-linecap="round"/>
        <!-- Thigh -->
        <line x1="42" y1="52" x2="62" y2="68" stroke="#38bdf8" stroke-width="4.5" stroke-linecap="round"/>
        <!-- Shin -->
        <line x1="62" y1="68" x2="48" y2="88" stroke="#38bdf8" stroke-width="4.5" stroke-linecap="round"/>
        <!-- Foot -->
        <line x1="44" y1="88" x2="58" y2="88" stroke="#94a3b8" stroke-width="3" stroke-linecap="round"/>
        <!-- Arm to bar -->
        <line x1="48" y1="35" x2="46" y2="30" stroke="#38bdf8" stroke-width="3" stroke-linecap="round"/>
        <!-- Barbell -->
        <line x1="30" y1="30" x2="62" y2="30" stroke="#f59e0b" stroke-width="3.5" stroke-linecap="round"/>
        <!-- Weight plates -->
        <rect x="26" y="22" width="5" height="16" rx="1.5" fill="#f59e0b"/>
        <rect x="61" y="22" width="5" height="16" rx="1.5" fill="#f59e0b"/>
    </svg>""",

    "leg_press": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Machine 45 deg frame -->
        <line x1="20" y1="85" x2="80" y2="25" stroke="#475569" stroke-width="3" stroke-linecap="round"/>
        <!-- Sled platform -->
        <line x1="58" y1="40" x2="72" y2="54" stroke="#f59e0b" stroke-width="4" stroke-linecap="round"/>
        <rect x="64" y="32" width="14" height="6" transform="rotate(-45 64 32)" fill="#f59e0b" rx="1"/>
        <!-- Seat back -->
        <line x1="25" y1="65" x2="42" y2="82" stroke="#64748b" stroke-width="5" stroke-linecap="round"/>
        <!-- Head -->
        <circle cx="28" cy="58" r="6" fill="#38bdf8"/>
        <!-- Torso -->
        <line x1="32" y1="62" x2="44" y2="74" stroke="#38bdf8" stroke-width="4"/>
        <!-- Thigh -->
        <line x1="44" y1="74" x2="50" y2="58" stroke="#38bdf8" stroke-width="4"/>
        <!-- Shin extending to sled -->
        <line x1="50" y1="58" x2="64" y2="46" stroke="#38bdf8" stroke-width="4"/>
    </svg>""",

    "leg_curl": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Bench -->
        <line x1="15" y1="65" x2="85" y2="65" stroke="#475569" stroke-width="4" stroke-linecap="round"/>
        <line x1="30" y1="65" x2="30" y2="85" stroke="#475569" stroke-width="3"/>
        <line x1="70" y1="65" x2="70" y2="85" stroke="#475569" stroke-width="3"/>
        <!-- Athlete torso prone -->
        <circle cx="26" cy="54" r="6" fill="#38bdf8"/>
        <line x1="30" y1="58" x2="55" y2="60" stroke="#38bdf8" stroke-width="4"/>
        <!-- Thigh on bench -->
        <line x1="55" y1="60" x2="72" y2="60" stroke="#38bdf8" stroke-width="4"/>
        <!-- Shin curled up -->
        <line x1="72" y1="60" x2="64" y2="42" stroke="#38bdf8" stroke-width="4"/>
        <!-- Roller pad on back of ankle -->
        <circle cx="63" cy="40" r="4.5" fill="#f59e0b"/>
        <!-- Machine arm -->
        <line x1="75" y1="62" x2="63" y2="40" stroke="#f59e0b" stroke-width="2.5"/>
    </svg>""",

    "leg_extension": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Seat -->
        <line x1="30" y1="40" x2="30" y2="68" stroke="#475569" stroke-width="4"/>
        <line x1="30" y1="68" x2="58" y2="68" stroke="#475569" stroke-width="4"/>
        <!-- Head -->
        <circle cx="32" cy="30" r="6" fill="#38bdf8"/>
        <!-- Torso -->
        <line x1="32" y1="36" x2="35" y2="66" stroke="#38bdf8" stroke-width="4"/>
        <!-- Thigh -->
        <line x1="35" y1="66" x2="62" y2="66" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Shin extended horizontally -->
        <line x1="62" y1="66" x2="82" y2="62" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Roller pad on front of shin -->
        <circle cx="78" cy="60" r="4.5" fill="#f59e0b"/>
        <line x1="60" y1="72" x2="78" y2="60" stroke="#f59e0b" stroke-width="2.5"/>
    </svg>""",

    "standing_calves": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Elevated step -->
        <rect x="35" y="85" width="30" height="8" fill="#475569" rx="1"/>
        <!-- Head -->
        <circle cx="50" cy="18" r="6" fill="#38bdf8"/>
        <!-- Barbell on back -->
        <line x1="32" y1="26" x2="68" y2="26" stroke="#f59e0b" stroke-width="3"/>
        <rect x="28" y="20" width="5" height="12" fill="#f59e0b" rx="1"/>
        <rect x="67" y="20" width="5" height="12" fill="#f59e0b" rx="1"/>
        <!-- Body upright -->
        <line x1="50" y1="24" x2="50" y2="54" stroke="#38bdf8" stroke-width="4"/>
        <!-- Legs straight -->
        <line x1="50" y1="54" x2="48" y2="78" stroke="#38bdf8" stroke-width="4"/>
        <!-- Ankles plantarflexed high on toes -->
        <line x1="48" y1="78" x2="46" y2="84" stroke="#38bdf8" stroke-width="3.5"/>
        <circle cx="46" cy="85" r="2.5" fill="#10b981"/>
    </svg>""",

    "ab_wheel": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Floor -->
        <line x1="10" y1="85" x2="90" y2="85" stroke="#334155" stroke-width="2"/>
        <!-- Knees on floor -->
        <circle cx="25" cy="83" r="3.5" fill="#64748b"/>
        <!-- Body in rollout plank -->
        <line x1="25" y1="83" x2="45" y2="68" stroke="#38bdf8" stroke-width="4"/>
        <!-- Torso -->
        <line x1="45" y1="68" x2="65" y2="60" stroke="#38bdf8" stroke-width="4"/>
        <!-- Head -->
        <circle cx="68" cy="54" r="5" fill="#38bdf8"/>
        <!-- Arms extended to wheel -->
        <line x1="62" y1="62" x2="78" y2="75" stroke="#38bdf8" stroke-width="3.5"/>
        <!-- Wheel -->
        <circle cx="78" cy="77" r="8" stroke="#f59e0b" stroke-width="3" fill="none"/>
        <circle cx="78" cy="77" r="2" fill="#f59e0b"/>
    </svg>""",

    "v_pulldown": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Cable frame top -->
        <line x1="25" y1="12" x2="75" y2="12" stroke="#475569" stroke-width="4"/>
        <!-- Cable down -->
        <line x1="50" y1="12" x2="50" y2="28" stroke="#94a3b8" stroke-width="2"/>
        <!-- V-grip handle -->
        <path d="M 45 28 L 50 32 L 55 28" stroke="#f59e0b" stroke-width="3" fill="none"/>
        <!-- Head slightly leaned back -->
        <circle cx="48" cy="38" r="6" fill="#38bdf8"/>
        <!-- Torso angled 15 deg -->
        <line x1="48" y1="44" x2="44" y2="72" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Arms pulling down -->
        <line x1="47" y1="48" x2="49" y2="32" stroke="#38bdf8" stroke-width="3.5"/>
        <!-- Thighs locked under pad -->
        <line x1="44" y1="72" x2="64" y2="72" stroke="#38bdf8" stroke-width="4"/>
        <line x1="64" y1="72" x2="64" y2="88" stroke="#38bdf8" stroke-width="4"/>
        <rect x="52" y="68" width="12" height="4" fill="#64748b" rx="1"/>
    </svg>""",

    "dorian_row": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Chest support pad 45 deg -->
        <line x1="42" y1="40" x2="50" y2="65" stroke="#64748b" stroke-width="6" stroke-linecap="round"/>
        <!-- Athlete head -->
        <circle cx="38" cy="30" r="6" fill="#38bdf8"/>
        <!-- Torso supported against pad -->
        <line x1="39" y1="36" x2="46" y2="65" stroke="#38bdf8" stroke-width="4"/>
        <!-- Arm driving elbow back high -->
        <path d="M 42 45 L 60 48 L 48 38" stroke="#f59e0b" stroke-width="3.5" fill="none" stroke-linejoin="round"/>
        <!-- Handle -->
        <circle cx="60" cy="48" r="3" fill="#f59e0b"/>
        <!-- Legs seated -->
        <line x1="46" y1="65" x2="35" y2="85" stroke="#38bdf8" stroke-width="4"/>
    </svg>""",

    "gironda_row": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Low pulley machine line -->
        <line x1="85" y1="65" x2="85" y2="85" stroke="#475569" stroke-width="3"/>
        <circle cx="85" cy="65" r="4" fill="#f59e0b"/>
        <!-- Cable -->
        <line x1="85" y1="65" x2="60" y2="58" stroke="#94a3b8" stroke-width="2"/>
        <!-- Wide bar -->
        <line x1="58" y1="53" x2="62" y2="63" stroke="#f59e0b" stroke-width="3"/>
        <!-- Athlete seated upright -->
        <circle cx="35" cy="32" r="6" fill="#38bdf8"/>
        <line x1="35" y1="38" x2="38" y2="70" stroke="#38bdf8" stroke-width="4"/>
        <!-- Arms pulling wide to sternum -->
        <line x1="36" y1="46" x2="52" y2="52" stroke="#38bdf8" stroke-width="3.5"/>
        <line x1="52" y1="52" x2="60" y2="58" stroke="#38bdf8" stroke-width="3.5"/>
        <!-- Legs extended to footrests -->
        <line x1="38" y1="70" x2="65" y2="72" stroke="#38bdf8" stroke-width="4"/>
        <line x1="65" y1="72" x2="72" y2="76" stroke="#38bdf8" stroke-width="4"/>
    </svg>""",

    "face_pull": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- High cable -->
        <circle cx="85" cy="25" r="4" fill="#f59e0b"/>
        <line x1="85" y1="25" x2="58" y2="34" stroke="#94a3b8" stroke-width="2"/>
        <!-- Rope handles -->
        <path d="M 58 30 L 58 38" stroke="#f59e0b" stroke-width="3.5"/>
        <!-- Athlete standing athletic -->
        <circle cx="35" cy="28" r="6" fill="#38bdf8"/>
        <line x1="35" y1="34" x2="38" y2="65" stroke="#38bdf8" stroke-width="4"/>
        <!-- Elbows high flared out to ears -->
        <path d="M 37 42 L 50 32 L 58 34" stroke="#38bdf8" stroke-width="3.5" fill="none"/>
        <!-- Legs split stance -->
        <line x1="38" y1="65" x2="30" y2="88" stroke="#38bdf8" stroke-width="4"/>
        <line x1="38" y1="65" x2="48" y2="88" stroke="#38bdf8" stroke-width="4"/>
    </svg>""",

    "incline_curl": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Incline 45 bench -->
        <line x1="25" y1="85" x2="60" y2="40" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
        <!-- Head resting back -->
        <circle cx="58" cy="34" r="6" fill="#38bdf8"/>
        <!-- Torso on bench -->
        <line x1="55" y1="40" x2="38" y2="68" stroke="#38bdf8" stroke-width="4"/>
        <!-- Upper arm hanging vertically behind torso plane -->
        <line x1="50" y1="46" x2="50" y2="66" stroke="#38bdf8" stroke-width="3.5"/>
        <!-- Forearm curling forward -->
        <line x1="50" y1="66" x2="60" y2="56" stroke="#38bdf8" stroke-width="3.5"/>
        <!-- Dumbbell -->
        <circle cx="61" cy="54" r="4.5" fill="#f59e0b"/>
        <!-- Legs seated -->
        <line x1="38" y1="68" x2="45" y2="85" stroke="#38bdf8" stroke-width="4"/>
    </svg>""",

    "scott_curl": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Preacher pad angled forward -->
        <line x1="45" y1="50" x2="65" y2="58" stroke="#64748b" stroke-width="6" stroke-linecap="round"/>
        <!-- Athlete head -->
        <circle cx="35" cy="32" r="6" fill="#38bdf8"/>
        <line x1="36" y1="38" x2="40" y2="65" stroke="#38bdf8" stroke-width="4"/>
        <!-- Arms resting on pad curling up -->
        <line x1="40" y1="46" x2="55" y2="54" stroke="#38bdf8" stroke-width="3.5"/>
        <line x1="55" y1="54" x2="52" y2="40" stroke="#38bdf8" stroke-width="3.5"/>
        <circle cx="52" cy="38" r="4" fill="#f59e0b"/>
    </svg>""",

    "hip_thrust": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Bench support behind shoulders -->
        <rect x="20" y="55" width="16" height="25" fill="#475569" rx="2"/>
        <!-- Upper back resting on bench -->
        <circle cx="34" cy="46" r="6" fill="#38bdf8"/>
        <!-- Torso horizontal in full hip extension -->
        <line x1="35" y1="52" x2="58" y2="52" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Barbell across hip crease -->
        <circle cx="56" cy="50" r="5.5" fill="#f59e0b"/>
        <!-- Thigh horizontal -->
        <line x1="58" y1="52" x2="72" y2="52" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Shin vertical 90 deg -->
        <line x1="72" y1="52" x2="72" y2="80" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Foot flat -->
        <line x1="68" y1="80" x2="76" y2="80" stroke="#94a3b8" stroke-width="3"/>
    </svg>""",

    "single_leg_rdl": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Head -->
        <circle cx="28" cy="38" r="6" fill="#38bdf8"/>
        <!-- Torso horizontal in hinge -->
        <line x1="34" y1="42" x2="55" y2="48" stroke="#38bdf8" stroke-width="4"/>
        <!-- Back leg extended in line with torso -->
        <line x1="55" y1="48" x2="85" y2="42" stroke="#38bdf8" stroke-width="4"/>
        <!-- Supporting leg slightly soft knee -->
        <line x1="55" y1="48" x2="53" y2="70" stroke="#38bdf8" stroke-width="4.5"/>
        <line x1="53" y1="70" x2="52" y2="88" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Arm hanging with dumbbell -->
        <line x1="38" y1="44" x2="38" y2="70" stroke="#38bdf8" stroke-width="3"/>
        <rect x="34" y="68" width="8" height="6" fill="#f59e0b" rx="1.5"/>
    </svg>""",

    "high_press": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Incline sled line -->
        <line x1="20" y1="85" x2="80" y2="25" stroke="#475569" stroke-width="3"/>
        <!-- Feet high and wide at top of platform -->
        <line x1="70" y1="35" x2="78" y2="43" stroke="#f59e0b" stroke-width="4.5"/>
        <!-- Athlete in seat -->
        <circle cx="28" cy="58" r="6" fill="#38bdf8"/>
        <line x1="32" y1="62" x2="44" y2="74" stroke="#38bdf8" stroke-width="4"/>
        <!-- Glute/Hamstring dominant drive -->
        <line x1="44" y1="74" x2="54" y2="52" stroke="#38bdf8" stroke-width="4.5"/>
        <line x1="54" y1="52" x2="72" y2="38" stroke="#38bdf8" stroke-width="4.5"/>
    </svg>""",

    "seated_calves": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Seat & machine frame -->
        <line x1="25" y1="50" x2="25" y2="70" stroke="#475569" stroke-width="4"/>
        <line x1="25" y1="70" x2="50" y2="70" stroke="#475569" stroke-width="4"/>
        <circle cx="28" cy="40" r="6" fill="#38bdf8"/>
        <line x1="30" y1="46" x2="35" y2="68" stroke="#38bdf8" stroke-width="4"/>
        <!-- Thigh 90 deg horizontal -->
        <line x1="35" y1="68" x2="62" y2="68" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Knee pad with weights -->
        <rect x="54" y="60" width="14" height="6" fill="#f59e0b" rx="1"/>
        <!-- Shin vertical to foot block -->
        <line x1="62" y1="68" x2="62" y2="86" stroke="#38bdf8" stroke-width="4.5"/>
        <rect x="56" y="86" width="14" height="4" fill="#64748b"/>
    </svg>""",

    "pallof_press": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Cable origin on left -->
        <circle cx="15" cy="50" r="4" fill="#f59e0b"/>
        <!-- Cable line to chest -->
        <line x1="15" y1="50" x2="50" y2="50" stroke="#94a3b8" stroke-width="2"/>
        <!-- Hands pressing straight out -->
        <line x1="42" y1="46" x2="56" y2="50" stroke="#38bdf8" stroke-width="3"/>
        <circle cx="56" cy="50" r="3.5" fill="#f59e0b"/>
        <!-- Athlete standing athletic square to camera -->
        <circle cx="42" cy="24" r="6" fill="#38bdf8"/>
        <line x1="42" y1="30" x2="42" y2="62" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Athletic wide base legs -->
        <line x1="42" y1="62" x2="30" y2="88" stroke="#38bdf8" stroke-width="4"/>
        <line x1="42" y1="62" x2="54" y2="88" stroke="#38bdf8" stroke-width="4"/>
    </svg>""",

    "bench_press": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Flat bench -->
        <line x1="15" y1="65" x2="85" y2="65" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
        <!-- Athlete head -->
        <circle cx="28" cy="58" r="6" fill="#38bdf8"/>
        <!-- Torso lying flat with slight arch -->
        <path d="M 33 62 Q 48 58 65 62" stroke="#38bdf8" stroke-width="4.5" fill="none"/>
        <!-- Arms pressing straight up -->
        <line x1="50" y1="60" x2="50" y2="32" stroke="#38bdf8" stroke-width="3.5"/>
        <!-- Barbell -->
        <line x1="30" y1="30" x2="70" y2="30" stroke="#f59e0b" stroke-width="3.5"/>
        <rect x="25" y="22" width="6" height="16" fill="#f59e0b" rx="1.5"/>
        <rect x="69" y="22" width="6" height="16" fill="#f59e0b" rx="1.5"/>
        <!-- Legs down to floor -->
        <line x1="65" y1="62" x2="68" y2="80" stroke="#38bdf8" stroke-width="4"/>
    </svg>""",

    "incline_press": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Incline 30 bench -->
        <line x1="20" y1="80" x2="70" y2="45" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
        <circle cx="68" cy="38" r="6" fill="#38bdf8"/>
        <!-- Torso on incline -->
        <line x1="65" y1="44" x2="40" y2="66" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Arms pressing dumbbells up -->
        <line x1="55" y1="48" x2="65" y2="24" stroke="#38bdf8" stroke-width="3.5"/>
        <circle cx="66" cy="22" r="5" fill="#f59e0b"/>
        <!-- Legs seated -->
        <line x1="40" y1="66" x2="42" y2="84" stroke="#38bdf8" stroke-width="4"/>
    </svg>""",

    "pec_dec": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Seat upright -->
        <line x1="40" y1="35" x2="40" y2="75" stroke="#475569" stroke-width="4"/>
        <circle cx="40" cy="26" r="6" fill="#38bdf8"/>
        <line x1="40" y1="32" x2="42" y2="68" stroke="#38bdf8" stroke-width="4"/>
        <!-- Arms bringing levers together in front -->
        <path d="M 42 42 Q 62 42 58 54" stroke="#38bdf8" stroke-width="3.5" fill="none"/>
        <circle cx="58" cy="54" r="5" fill="#f59e0b"/>
        <rect x="55" y="44" width="6" height="18" fill="#f59e0b" rx="1.5"/>
        <line x1="42" y1="68" x2="48" y2="85" stroke="#38bdf8" stroke-width="4"/>
    </svg>""",

    "lateral_raise": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Head -->
        <circle cx="50" cy="22" r="6" fill="#38bdf8"/>
        <!-- Torso standing tall -->
        <line x1="50" y1="28" x2="50" y2="60" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Arms raised laterally to shoulder level -->
        <path d="M 22 42 L 50 34 L 78 42" stroke="#38bdf8" stroke-width="3.5" fill="none"/>
        <!-- Dumbbells in hands at 90 deg T-shape -->
        <circle cx="20" cy="42" r="4.5" fill="#f59e0b"/>
        <circle cx="80" cy="42" r="4.5" fill="#f59e0b"/>
        <!-- Legs standing -->
        <line x1="50" y1="60" x2="44" y2="88" stroke="#38bdf8" stroke-width="4"/>
        <line x1="50" y1="60" x2="56" y2="88" stroke="#38bdf8" stroke-width="4"/>
    </svg>""",

    "french_press": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- Bench -->
        <line x1="15" y1="68" x2="85" y2="68" stroke="#475569" stroke-width="5" stroke-linecap="round"/>
        <circle cx="30" cy="60" r="6" fill="#38bdf8"/>
        <line x1="35" y1="64" x2="65" y2="64" stroke="#38bdf8" stroke-width="4"/>
        <!-- Upper arm perpendicular to bench -->
        <line x1="46" y1="64" x2="46" y2="40" stroke="#38bdf8" stroke-width="3.5"/>
        <!-- Forearm bending back towards forehead -->
        <line x1="46" y1="40" x2="35" y2="48" stroke="#38bdf8" stroke-width="3.5"/>
        <!-- EZ curl bar at forehead -->
        <circle cx="33" cy="49" r="4.5" fill="#f59e0b"/>
    </svg>""",

    "tricep_rope": """<svg viewBox="0 0 100 100" class="ex-svg">
        <!-- High pulley -->
        <circle cx="65" cy="18" r="4" fill="#f59e0b"/>
        <line x1="65" y1="18" x2="52" y2="40" stroke="#94a3b8" stroke-width="2"/>
        <!-- Standing athlete -->
        <circle cx="36" cy="24" r="6" fill="#38bdf8"/>
        <line x1="36" y1="30" x2="38" y2="65" stroke="#38bdf8" stroke-width="4.5"/>
        <!-- Upper arms pinned to ribcage -->
        <line x1="38" y1="38" x2="42" y2="52" stroke="#38bdf8" stroke-width="3.5"/>
        <!-- Forearms extending down spreading rope -->
        <line x1="42" y1="52" x2="48" y2="68" stroke="#38bdf8" stroke-width="3.5"/>
        <circle cx="48" cy="70" r="3.5" fill="#f59e0b"/>
        <line x1="38" y1="65" x2="34" y2="88" stroke="#38bdf8" stroke-width="4"/>
        <line x1="38" y1="65" x2="44" y2="88" stroke="#38bdf8" stroke-width="4"/>
    </svg>"""
}

# Routines Data
routines = [
    {
        "title": "RUTINA 1 · PIERNA 1",
        "subtitle": "DOMINANCIA RODILLA · FUERZA NEURAL Y CUÁDRICEPS",
        "badge": "LUNES 18:00 · 45-50 MIN",
        "color": "#10b981", # green
        "exercises": [
            {
                "num": "01",
                "name": "Sentadilla Trasera con Barra (Back Squat)",
                "icon": "squat",
                "sets_reps": "4 × 4 – 6 reps",
                "weight": "85 kg",
                "tempo": "3-1-X-0 (3s bajada, 1s pausa, subida explosiva)",
                "rest": "3 min",
                "rir": "RIR 1-2 (a 1-2 reps del fallo)",
                "cue": "Profundidad rompiendo el paralelo. Empuja el suelo con todo el pie."
            },
            {
                "num": "02",
                "name": "Prensa de Piernas 45°",
                "icon": "leg_press",
                "sets_reps": "3 × 6 – 8 reps",
                "weight": "+40 kg / lado",
                "tempo": "3-0-1-0 (bajada controlada continua)",
                "rest": "2.5 min",
                "rir": "RIR 1",
                "cue": "Pies a anchura de caderas. Cero despegue lumbar del respaldo."
            },
            {
                "num": "03",
                "name": "Curl Femoral Tumbado en Máquina",
                "icon": "leg_curl",
                "sets_reps": "3 × 6 – 8 reps",
                "weight": "42 kg",
                "tempo": "3-1-1-0 (HSR: excéntrica en 3s)",
                "rest": "2 min",
                "rir": "RIR 1",
                "cue": "Frena la bajada. Estimula sarcómeros en serie del isquiotibial."
            },
            {
                "num": "04",
                "name": "Extensión de Cuádriceps en Máquina",
                "icon": "leg_extension",
                "sets_reps": "3 × 8 – 10 reps",
                "weight": "66 kg",
                "tempo": "2-0-1-1 (1s de bloqueo arriba)",
                "rest": "90 s",
                "rir": "RIR 1",
                "cue": "Aislamiento puro del recto femoral sin fatiga en columna."
            },
            {
                "num": "05",
                "name": "Elevación de Gemelos de Pie con Barra",
                "icon": "standing_calves",
                "sets_reps": "4 × 6 – 8 reps",
                "weight": "85 kg",
                "tempo": "3-2-X-0 (PAUSA DE 2s ABAJO)",
                "rest": "90 s",
                "rir": "RIR 1",
                "cue": "La pausa de 2s abajo anula el rebote tendinoso y carga el gastrocnemio."
            },
            {
                "num": "06",
                "name": "Core: Rueda Abdominal (Ab Wheel)",
                "icon": "ab_wheel",
                "sets_reps": "3 × 8 – 10 reps",
                "weight": "Autocarga",
                "tempo": "2-1-2-0 (control lumbo-pélvico)",
                "rest": "60 s",
                "rir": "Técnica estricta",
                "cue": "Anti-extensión pura. Retroversión pélvica activa: bloquea la pelvis neutra."
            }
        ]
    },
    {
        "title": "RUTINA 2 · TORSO TRACCIÓN",
        "subtitle": "DORSAL ANCHO · ESPALDA ALTA · BÍCEPS & DENSIDAD",
        "badge": "MIÉRCOLES 17:30 · 50 MIN",
        "color": "#06b6d4", # cyan
        "exercises": [
            {
                "num": "01",
                "name": "Jalón al Pecho Agarre Cerrado Neutro (V-Grip)",
                "icon": "v_pulldown",
                "sets_reps": "4 × 4 – 6 reps",
                "weight": "Pesado (progresivo)",
                "tempo": "3-0-X-1 (tirón explosivo, 1s abajo)",
                "rest": "2.5 min",
                "rir": "RIR 1",
                "cue": "Codos viajan pegados hacia las costillas. Máxima carga neural en dorsal."
            },
            {
                "num": "02",
                "name": "Remo Dorian en Máquina Unilateral",
                "icon": "dorian_row",
                "sets_reps": "3 × 6 – 8 reps / brazo",
                "weight": "Pesado",
                "tempo": "2-0-1-1 (1s de apriete en cadera)",
                "rest": "2 min",
                "rir": "RIR 1",
                "cue": "Apoyo esternal fijo. Conduce el codo directamente hacia el bolsillo trasero."
            },
            {
                "num": "03",
                "name": "Remo Gironda con Agarre Amplio",
                "icon": "gironda_row",
                "sets_reps": "3 × 8 – 10 reps",
                "weight": "Medio-Pesado",
                "tempo": "2-0-1-2 (2s de retracción escapular)",
                "rest": "90 s",
                "rir": "RIR 1",
                "cue": "Codos abiertos a 45°-60°. Junta escápulas para soporte postural de carrera."
            },
            {
                "num": "04",
                "name": "Face Pull en Polea Alta a la Frente",
                "icon": "face_pull",
                "sets_reps": "3 × 10 – 12 reps",
                "weight": "Medio",
                "tempo": "2-0-1-1 (rotación externa alta)",
                "rest": "75 s",
                "rir": "RIR 2",
                "cue": "Manos a la altura de los ojos separando la cuerda. Salud de manguito rotador."
            },
            {
                "num": "05",
                "name": "Curl con Mancuernas en Banco Inclinado (45°)",
                "icon": "incline_curl",
                "sets_reps": "3 × 6 – 8 reps",
                "weight": "Pesado",
                "tempo": "3-0-1-0 (estiramiento profundo)",
                "rest": "90 s",
                "rir": "RIR 1",
                "cue": "Brazos cuelgan atrás. Pone la cabeza larga del bíceps en tensión máxima."
            },
            {
                "num": "06",
                "name": "Curl en Máquina de Bíceps (o Banco Scott)",
                "icon": "scott_curl",
                "sets_reps": "2 × 8 – 10 reps",
                "weight": "Medio-Alto",
                "tempo": "2-0-1-1 (tensión continua)",
                "rest": "75 s",
                "rir": "RIR 0-1",
                "cue": "Codos firmes en el apoyo. Contracción pico para densidad de brazo."
            }
        ]
    },
    {
        "title": "RUTINA 3 · PIERNA 2",
        "subtitle": "DOMINANCIA CADERA · CADENA POSTERIOR & BLINDAJE ISQUIOS",
        "badge": "VIERNES 17:30 · 50 MIN",
        "color": "#f59e0b", # amber/gold
        "exercises": [
            {
                "num": "01",
                "name": "Hip Thrust con Barra o en Máquina",
                "icon": "hip_thrust",
                "sets_reps": "4 × 4 – 6 reps",
                "weight": "120 – 130 kg",
                "tempo": "2-1-X-1 (1s bloqueo arriba)",
                "rest": "3 min",
                "rir": "RIR 1",
                "cue": "Empuje con talones. Extensión total de cadera apretando glúteos arriba."
            },
            {
                "num": "02",
                "name": "Peso Muerto Rumano a 1 Pierna (Single-Leg RDL)",
                "icon": "single_leg_rdl",
                "sets_reps": "3 × 6 – 8 reps / pierna",
                "weight": "20 – 22 kg",
                "tempo": "3-1-1-0 (3s excéntrica lenta)",
                "rest": "2 min",
                "rir": "RIR 1-2",
                "cue": "El ejercicio rey de tu readaptación: bisagra de cadera con espalda neutra."
            },
            {
                "num": "03",
                "name": "Prensa 45° (Pies Altos y Anchos)",
                "icon": "high_press",
                "sets_reps": "3 × 6 – 8 reps",
                "weight": "+40-45 kg / lado",
                "tempo": "3-0-1-0 (freno excéntrico)",
                "rest": "2 min",
                "rir": "RIR 1",
                "cue": "Coloca los pies arriba y separados para activar glúteos e isquios."
            },
            {
                "num": "04",
                "name": "Curl Femoral Tumbado en Máquina",
                "icon": "leg_curl",
                "sets_reps": "3 × 6 – 8 reps",
                "weight": "42 kg",
                "tempo": "3-1-1-0 (control estricto)",
                "rest": "90 s",
                "rir": "RIR 1",
                "cue": "Sin balanceo de cadera. Carga excéntrica sin cizallamiento."
            },
            {
                "num": "05",
                "name": "Elevación de Sóleo Sentado en Máquina",
                "icon": "seated_calves",
                "sets_reps": "3 × 8 – 10 reps",
                "weight": "Pesado",
                "tempo": "3-2-1-0 (pausa 2s abajo)",
                "rest": "90 s",
                "rir": "RIR 1",
                "cue": "Rodilla a 90° aísla el sóleo (absorbe 6-8x tu peso en cada apoyo al correr)."
            },
            {
                "num": "06",
                "name": "Core: Pallof Press en Polea + Paseo de Granjero",
                "icon": "pallof_press",
                "sets_reps": "3 × 10 reps + 30m / lado",
                "weight": "Medio-Pesado",
                "tempo": "Isométrico",
                "rest": "60 s",
                "rir": "Estabilidad pura",
                "cue": "Anti-rotación y anti-flexión lateral. Evita el balanceo pélvico en carrera."
            }
        ]
    },
    {
        "title": "RUTINA 4 · TORSO EMPUJE",
        "subtitle": "PECTORAL · HOMBRO LATERAL · TRÍCEPS & DEFINICIÓN",
        "badge": "SÁBADO MAÑANA · 50 MIN",
        "color": "#ec4899", # pink/rose
        "exercises": [
            {
                "num": "01",
                "name": "Press de Banca Plano con Barra",
                "icon": "bench_press",
                "sets_reps": "4 × 4 – 6 reps",
                "weight": "Pesado (progresivo)",
                "tempo": "3-1-X-0 (pausa de 1s en pecho)",
                "rest": "2.5 min",
                "rir": "RIR 1-2",
                "cue": "Retracción escapular firme. Barra toca el pecho sin rebotar y subida explosiva."
            },
            {
                "num": "02",
                "name": "Press Inclinado con Mancuernas (30°)",
                "icon": "incline_press",
                "sets_reps": "3 × 6 – 8 reps",
                "weight": "Pesado",
                "tempo": "3-0-1-0 (bajada controlada)",
                "rest": "2 min",
                "rir": "RIR 1",
                "cue": "Ángulo a 30° para enfatizar la porción clavicular y deltoides anterior."
            },
            {
                "num": "03",
                "name": "Pec Dec / Aperturas en Máquina",
                "icon": "pec_dec",
                "sets_reps": "3 × 8 – 10 reps",
                "weight": "Medio",
                "tempo": "2-0-1-1 (1s contracción isométrica)",
                "rest": "90 s",
                "rir": "RIR 1",
                "cue": "Junta codos al frente y aprieta el pecho 1 segundo en máxima contracción."
            },
            {
                "num": "04",
                "name": "Elevaciones Laterales con Mancuerna o Polea",
                "icon": "lateral_raise",
                "sets_reps": "4 × 8 – 10 reps",
                "weight": "Pesado estricto",
                "tempo": "2-0-1-1 (sin inercia)",
                "rest": "75 s",
                "rir": "RIR 1",
                "cue": "Codos ligeramente flexionados. Clave para la amplitud y corte visual del hombro."
            },
            {
                "num": "05",
                "name": "Press Francés con Barra Z en Banco Plano",
                "icon": "french_press",
                "sets_reps": "3 × 6 – 8 reps",
                "weight": "Medio-Pesado",
                "tempo": "3-0-1-0 (hacia la coronilla)",
                "rest": "90 s",
                "rir": "RIR 1",
                "cue": "Codos fijos apuntando al techo. Estímulo directo a la cabeza larga del tríceps."
            },
            {
                "num": "06",
                "name": "Extensiones de Tríceps en Polea con Cuerda",
                "icon": "tricep_rope",
                "sets_reps": "3 × 8 – 10 reps",
                "weight": "Medio-Alto",
                "tempo": "2-0-1-1 (apertura abajo)",
                "rest": "75 s",
                "rir": "RIR 0-1",
                "cue": "Separa los extremos de la cuerda al final para acortar las cabezas lateral y medial."
            }
        ]
    }
]

# Generate HTML
html_content = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>AEGIS COACH · Cuaderno de Fuerza de Carlos</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
    
    * {{
        box-sizing: border-box;
        margin: 0;
        padding: 0;
    }}
    
    @page {{
        size: A4 portrait;
        margin: 0;
    }}
    
    body {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #090d16;
        color: #f1f5f9;
        -webkit-print-color-adjust: exact;
        print-color-adjust: exact;
    }}
    
    .page {{
        width: 210mm;
        height: 297mm;
        page-break-after: always;
        padding: 12mm 14mm;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        background: #090d16;
        position: relative;
        overflow: hidden;
    }}
    
    /* Header */
    .header {{
        border-bottom: 2px solid rgba(255,255,255,0.08);
        padding-bottom: 8px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
    }}
    
    .header-left h1 {{
        font-size: 20px;
        font-weight: 900;
        letter-spacing: -0.5px;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .header-left p {{
        font-size: 10px;
        color: #94a3b8;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-top: 2px;
    }}
    
    .badge {{
        font-size: 9px;
        font-weight: 800;
        padding: 4px 10px;
        border-radius: 999px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
    }}
    
    /* Grid of 6 exercises */
    .exercise-grid {{
        display: grid;
        grid-template-columns: 1fr;
        grid-template-rows: repeat(6, 1fr);
        gap: 8px;
        flex-grow: 1;
    }}
    
    .card {{
        background: #111827;
        border: 1px solid rgba(255,255,255,0.07);
        border-radius: 8px;
        padding: 8px 12px;
        display: grid;
        grid-template-columns: 36px 65px 1fr;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    }}
    
    .num-col {{
        font-size: 16px;
        font-weight: 900;
        color: #475569;
        text-align: center;
    }}
    
    .svg-container {{
        width: 65px;
        height: 65px;
        background: #0f172a;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 6px;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 4px;
    }}
    
    .ex-svg {{
        width: 100%;
        height: 100%;
    }}
    
    .info-col {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 3px;
    }}
    
    .ex-name {{
        font-size: 12.5px;
        font-weight: 800;
        color: #ffffff;
        letter-spacing: -0.2px;
    }}
    
    .metrics-row {{
        display: flex;
        flex-wrap: wrap;
        gap: 5px;
        align-items: center;
    }}
    
    .pill {{
        font-size: 9.5px;
        font-weight: 700;
        padding: 2px 7px;
        border-radius: 4px;
        background: #1e293b;
        color: #e2e8f0;
        border: 1px solid rgba(255,255,255,0.06);
    }}
    
    .pill-highlight {{
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border-color: rgba(16, 185, 129, 0.3);
        font-weight: 800;
    }}
    
    .pill-rest {{
        background: rgba(56, 189, 248, 0.12);
        color: #38bdf8;
        border-color: rgba(56, 189, 248, 0.25);
    }}
    
    .cue-text {{
        font-size: 9px;
        color: #94a3b8;
        line-height: 1.25;
        margin-top: 1px;
    }}
    
    .cue-text strong {{
        color: #cbd5e1;
    }}
    
    /* Footer */
    .footer {{
        border-top: 1px solid rgba(255,255,255,0.08);
        padding-top: 6px;
        margin-top: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 8.5px;
        color: #64748b;
        font-weight: 600;
    }}
    
    .footer span.brand {{
        color: #94a3b8;
        font-weight: 800;
        letter-spacing: 0.5px;
    }}
</style>
</head>
<body>
"""

for r in routines:
    color = r["color"]
    html_content += f"""
    <div class="page">
        <div class="header">
            <div class="header-left">
                <h1 style="color: {color};">{r["title"]}</h1>
                <p>{r["subtitle"]}</p>
            </div>
            <div class="badge" style="color: {color}; border-color: {color}44;">
                {r["badge"]}
            </div>
        </div>
        
        <div class="exercise-grid">
    """
    
    for ex in r["exercises"]:
        svg_code = svg_icons.get(ex["icon"], "")
        html_content += f"""
            <div class="card">
                <div class="num-col">{ex["num"]}</div>
                <div class="svg-container">
                    {svg_code}
                </div>
                <div class="info-col">
                    <div class="ex-name">{ex["name"]}</div>
                    <div class="metrics-row">
                        <span class="pill pill-highlight" style="background: {color}22; color: {color}; border-color: {color}55;">{ex["sets_reps"]}</span>
                        <span class="pill">Carga: <strong>{ex["weight"]}</strong></span>
                        <span class="pill pill-rest">Descanso: {ex["rest"]}</span>
                        <span class="pill">RIR: {ex["rir"]}</span>
                    </div>
                    <div class="cue-text">
                        <strong>Tempo:</strong> {ex["tempo"]} &bull; {ex["cue"]}
                    </div>
                </div>
            </div>
        """
        
    html_content += f"""
        </div>
        
        <div class="footer">
            <span class="brand">AEGIS COACH &bull; ATLETA: CARLOS GÓMEZ (63 KG)</span>
            <span>OBJETIVO: 10K ÁVILA (8 NOV) &bull; SAN SILVESTRE (31 DIC)</span>
            <span>SOBRECARGA PROGRESIVA: RIR 1-2 &bull; SUBIR +2.5 KG AL COMPLETAR EL RANGO</span>
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

# Compile to PDF using Playwright
print("Rendering PDF via Playwright...")
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(f"file:///{output_html.replace(os.sep, '/')}")
    page.pdf(
        path=output_pdf,
        format="A4",
        print_background=True,
        margin={"top": "0mm", "bottom": "0mm", "left": "0mm", "right": "0mm"}
    )
    browser.close()

print(f"SUCCESS: PDF created at {output_pdf} (Size: {os.path.getsize(output_pdf)} bytes)")
