import os
import re

with open('scripts/build_final_v3_dashboard.py', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update title/banner print
text = text.replace(
    'Construyendo el nuevo index.ts v3 con Calendario Mensual, Perfil de Usuario con IMC, Logo Fluido y Reordenación de Columnas...',
    'Construyendo el nuevo index.ts v4 con Aero-Aegis, Subvistas de Calendario/Microciclo, Edición de Perfil y Chips actualizados...'
)

# 2. Add short label mappings for mobile volume chart
text = re.sub(
    r'display_weeks = \[w for w in weekly_evo if w\[\'run_km\'\] > 0 or w\[\'week_start\'\] >= \'2026-09-28\'\]',
    '''display_weeks = [w for w in weekly_evo if w['run_km'] > 0 or w['week_start'] >= '2026-09-28']
short_labels = {
    "2026-09-28": "28 Sep",
    "2026-10-05": "5 Oct",
    "2026-10-12": "12 Oct",
    "2026-10-19": "19 Oct",
    "2026-10-26": "26 Oct",
    "2026-11-02": "2 Nov",
    "2026-11-09": "9 Nov",
    "2026-11-16": "16 Nov"
}
for w in display_weeks:
    if w['week_start'] in short_labels:
        w['label'] = short_labels[w['week_start']]''',
    text
)

# 3. Update calendar_nov_2026 to reflect real training history
cal_start = text.find('calendar_nov_2026 = {')
cal_end = text.find('svg_logo = \'\'\'<svg', cal_start)

real_calendar = '''calendar_nov_2026 = {
    "year": 2026,
    "month": 11,
    "month_name": "Noviembre 2026",
    "days_in_month": 30,
    "first_day_weekday": 6, # 0=Lunes, 6=Domingo (1 Nov 2026 fue Domingo)
    "activities": {
        "2026-11-01": {"dots": ["run"], "title": "Rodaje Pre-10K Ávila (10.7 km)", "type": "Running", "km": 10.7, "time": "52:10", "pace": "4:52/km", "hr": "151 ppm", "ai": "Rodaje sostenido de calibración aeróbica previa al 10K."},
        "2026-11-04": {"dots": ["run"], "title": "Series / Intervalos (7.5 km)", "type": "Running", "km": 7.5, "time": "36:40", "pace": "4:40/km", "hr": "166 ppm", "ai": "Cambios de ritmo previos al derrame sinovial reactivo detectado al día siguiente."},
        "2026-11-07": {"dots": ["run"], "title": "Activación Pre-Competición (4.1 km)", "type": "Running", "km": 4.1, "time": "20:30", "pace": "4:58/km", "hr": "140 ppm", "ai": "Puesta a punto neural previa al 10K. Rodilla respondiendo 0/10 dolor."},
        "2026-11-08": {"dots": ["run", "gym"], "title": "10K Ávila Monumental (38:26) + Gym Descarga", "type": "Competición", "km": 10.0, "time": "38:26", "pace": "3:50/km", "hr": "174 ppm", "ai": "HITO DE RENDIMIENTO: 38:26 oficial (3:50/km) a 1.070m de altitud con viento y cuestas. Tarde de movilidad en gimnasio."},
        "2026-11-10": {"dots": ["run"], "title": "Rodaje Regenerativo Suave (5.6 km)", "type": "Running", "km": 5.6, "time": "29:15", "pace": "5:13/km", "hr": "142 ppm", "ai": "Retorno a la carrera tras el 10K. Drenaje linfático y descarga sin inflamación articular."},
        "2026-11-11": {"dots": ["run", "gym"], "title": "Rodaje 8.1 km + Gym Rutina 2 (Torso Tracción)", "type": "Running + Gym", "km": 8.1, "time": "39:50", "pace": "4:54/km", "hr": "150 ppm", "ai": "Doble sesión: Jalón V a 59 kg + Remo Dorian a 30 kg, seguido de rodaje Z2 fluido."},
        "2026-11-12": {"dots": ["gym"], "title": "Gym Rutina 3 · Hip Thrust 140 kg & Isquios", "type": "Gimnasio", "km": 0, "time": "50 min", "pace": "-", "hr": "122 ppm", "ai": "Hito de fuerza: Hip Thrust pesado (140 kg × 4 reps @ RIR 1) blindando el isquiotibial proximal."},
        "2026-11-13": {"dots": ["run", "gym"], "title": "Cinta VirtualRun 5.2 km + Gym Torso Empuje", "type": "Running + Gym", "km": 5.2, "time": "26:00", "pace": "5:00/km", "hr": "145 ppm", "ai": "Mantenimiento neural de pectoral y hombro con rodaje regenerativo en tapiz."},
        "2026-11-14": {"dots": ["run", "mountain"], "title": "6×800m Parque del Soto + Paintball 2h", "type": "Series Cross", "km": 8.05, "time": "41:30", "pace": "3:45/km avg", "hr": "164 ppm", "ai": "Series en hierba/tierra con clavos de 6mm. Media clavada de 3:00.0 con pausas exactas de 90s. Paintball 2h posterior."},
        "2026-11-15": {"dots": ["gym"], "title": "Gym Rutina 1 · Pierna 1 (Box Squat & Prensa)", "type": "Gimnasio", "km": 0, "time": "45 min", "pace": "-", "hr": "120 ppm", "ai": "Fuerza de cuádriceps completada tras noche de fiesta. Descanso total de carrera para descargar isquios."},
        "2026-11-16": {"dots": ["run", "gym"], "title": "35 min Drenaje Z1 (<145 ppm) + Rutina 2 (Torso)", "type": "Hoy", "km": 7.0, "time": "35:00", "pace": "4:55-5:10/km", "hr": "Z1", "ai": "Sesión activa de hoy: Rodaje suave en asfalto llano + Rutina 2 (Espalda y Bíceps)."},
        "2026-11-17": {"dots": ["run"], "title": "Rodaje 50 min Z2 con 6 Progresiones", "type": "Planificado", "km": 10.0, "time": "50:00", "pace": "4:45/km", "hr": "Z2", "ai": "Volumen aeróbico base de la semana con reactividad neuromuscular en los últimos 2 km."},
        "2026-11-18": {"dots": ["run", "gym"], "title": "8×500m @ 1:40 (3:20/km) + Rutina 3 (Isquios)", "type": "Planificado", "km": 9.5, "time": "46:00", "pace": "3:20/km", "hr": "VO2max", "ai": "Sesión clave de VO2max en asfalto llano + último estímulo pesado de cadena posterior."},
        "2026-11-19": {"dots": ["gym"], "title": "Descanso Carrera + Movilidad & Core", "type": "Planificado", "km": 0, "time": "35 min", "pace": "-", "hr": "Baja", "ai": "Asimilación del trabajo de series y prevención articular."},
        "2026-11-20": {"dots": ["run"], "title": "Rodaje Suave 30 min Pre-Viaje + 4 Rectas", "type": "Planificado", "km": 6.0, "time": "30:00", "pace": "5:05/km", "hr": "Z1", "ai": "Oxigenación antes de salir de viaje. Zapatillas rodadoras blandas."},
        "2026-11-21": {"dots": ["run", "gym"], "title": "Test 5K Ritmo Controlado + Rutina 4", "type": "Planificado", "km": 8.0, "time": "38:00", "pace": "4:10/km", "hr": "Tempo", "ai": "Comprobación de sensaciones a ritmo vivo antes de la semana de afinamiento."},
        "2026-11-22": {"dots": ["run"], "title": "Tirada Larga Continua 60 min Z2", "type": "Planificado", "km": 13.0, "time": "60:00", "pace": "4:45/km", "hr": "Z2", "ai": "Cierre de la Semana 1 Pre-Milán con 33 km completados."},
        "2026-11-24": {"dots": ["run"], "title": "12×200m @ 37s (3:05/km) rec 45s", "type": "Semana Cross", "km": 7.0, "time": "36:00", "pace": "3:05/km", "hr": "Neural", "ai": "Afinamiento neuromuscular: frecuencia de zancada sin acumulación de lactato residual."},
        "2026-11-26": {"dots": ["run"], "title": "20 min Trote + 4 Rectas Clavos 6mm en El Soto", "type": "Semana Cross", "km": 4.5, "time": "22:00", "pace": "5:00/km", "hr": "Z1", "ai": "Reconocimiento de curvas y terreno deformable con clavos de 6mm."},
        "2026-11-28": {"dots": ["run"], "title": "CROSS POPULAR PARQUE DEL SOTO (5 KM)", "type": "COMPETICIÓN", "km": 5.0, "time": "17:30 obj", "pace": "3:30/km", "hr": "Máxima", "ai": "OBJETIVO PRIMARIO: 5 km en tierra/hierba @ 3:30/km (~17:30). Clavos 6mm obligatorios."}
    }
}
'''
text = text[:cal_start] + real_calendar + text[cal_end:]

# 4. Replace svg_logo with Aero-Aegis (Concept 1) and make_aero_svg function
svg_def_old = text[text.find('svg_logo = \'\'\'<svg'):text.find('worker_ts = \'\'\'/**')]
svg_def_new = '''def make_aero_svg(prefix="aero"):
    return f\'\'\'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">
  <defs>
    <linearGradient id="{prefix}_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#7B88FF"/>
      <stop offset="100%" stop-color="#4F46E5"/>
    </linearGradient>
    <linearGradient id="{prefix}_coral" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF758C"/>
      <stop offset="50%" stop-color="#FF5E80"/>
      <stop offset="100%" stop-color="#D946EF"/>
    </linearGradient>
    <linearGradient id="{prefix}_core" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#FF5E80"/>
      <stop offset="100%" stop-color="#7B88FF"/>
    </linearGradient>
    <linearGradient id="{prefix}_wing" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FF5E80"/>
    </linearGradient>
  </defs>
  <path d="M 50 14 C 38 12, 22 18, 16 32 C 11 48, 16 68, 32 82 C 40 88, 47 92, 50 93 C 44 86, 28 76, 25 61 C 22 47, 28 34, 40 26 C 44 23, 48 18, 50 14 Z" fill="url(#{prefix}_blue)"/>
  <path d="M 50 14 C 62 12, 78 18, 84 32 C 89 48, 84 68, 68 82 C 60 88, 53 92, 50 93 C 56 86, 72 76, 75 61 C 78 47, 72 34, 60 26 C 56 23, 52 18, 50 14 Z" fill="url(#{prefix}_coral)"/>
  <path d="M 50 26 C 52 26, 61 46, 65 62 C 66 66, 62 68, 57 67 C 54 62, 53 56, 50 56 C 47 56, 46 62, 43 67 C 38 68, 34 66, 35 62 C 39 46, 48 26, 50 26 Z" fill="url(#{prefix}_core)"/>
  <path d="M 22 57 C 35 53, 65 53, 78 57 C 68 61, 32 61, 22 57 Z" fill="url(#{prefix}_wing)"/>
</svg>\'\'\'

header_logo_svg = make_aero_svg("hdr")
aside_logo_svg = make_aero_svg("aside")
profile_logo_svg = make_aero_svg("prof")
favicon_svg = make_aero_svg("fav")

# Encode for favicon data uri
import urllib.parse
favicon_data_uri = "data:image/svg+xml," + urllib.parse.quote(favicon_svg)
'''
text = text.replace(svg_def_old, svg_def_new)

# 5. Add /favicon.ico and /img/logo.svg endpoints in Worker fetch
worker_fav_code = """    // Favicon oficial y Logo Aero-Aegis SVG
    if (url.pathname === "/favicon.ico" || url.pathname === "/img/logo.svg") {
      return new Response(''' + favicon_svg + ''', {
        headers: {
          "Content-Type": "image/svg+xml",
          "Cache-Control": "public, max-age=86400"
        }
      });
    }

    // Servir imágenes (Vectoriales y Fotos) desde KV
    if (url.pathname.startsWith("/img/")) {"""

text = text.replace(
    '    // Servir imágenes (Vectoriales y Fotos) desde KV\n    if (url.pathname.startsWith("/img/")) {',
    worker_fav_code
)

# 6. Replace favicon <link> in HTML <head>
text = re.sub(
    r'<link rel="icon" type="image/svg\+xml" href="data:image/svg\+xml,[^"]+">',
    '<link rel="icon" type="image/svg+xml" href="\' + favicon_data_uri + \'">',
    text
)

# 7. Replace svg_logo references with respective specific instances
text = text.replace("''' + svg_logo + '''", "''' + aside_logo_svg + '''", 1) # First is aside
text = text.replace("''' + svg_logo + '''", "''' + header_logo_svg + '''", 1) # Second is header
text = text.replace("''' + svg_logo + '''", "''' + profile_logo_svg + '''", 1) # Third is profile

# 8. Redesign Dashboard Hero Card (Sesión de Hoy)
hero_old = text[text.find('<!-- 1. BLOQUE DE LA SESIÓN DE HOY (ARRIBA DEL TODO) -->'):text.find('<!-- 2. TRES KPIS PRINCIPALES')]
hero_new = '''<!-- 1. BLOQUE DE LA SESIÓN DE HOY (LIMPIO, RESPONSIVE & ELEGANTE) -->
          <div class="luxury-card p-5 sm:p-7 border border-[#2D2F45] bg-[#141522] space-y-4">
            <!-- Header de la tarjeta -->
            <div class="flex items-center justify-between pb-3 border-b border-[#2D2F45]/60">
              <div class="flex items-center gap-2">
                <span class="text-xs font-black uppercase tracking-wider text-[#FF5E80]">
                  HOY &bull; ${todayPlan.day_name.toUpperCase()} ${todayPlan.date}
                </span>
                <span class="text-[10px] font-extrabold px-2.5 py-0.5 rounded-lg bg-[#20D994]/20 text-[#20D994] border border-[#20D994]/40">
                  En Curso
                </span>
              </div>
              <button onclick="switchTab('workouts')" class="text-xs font-bold text-[#8E8FA3] hover:text-white transition flex items-center gap-1">
                <span>Ver Plan Completo</span> &rarr;
              </button>
            </div>

            <!-- Grid de Carrera y Gimnasio Separados -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
              <!-- Bloque Carrera -->
              <div class="p-4 rounded-xl bg-[#1D1E2C] border border-[#2D2F45] space-y-2.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-extrabold text-[#FF5E80] flex items-center gap-1.5 uppercase tracking-wide">
                    <i data-lucide="footprints" class="w-4 h-4"></i> Carrera
                  </span>
                  <span class="text-xs font-mono font-bold text-white">
                    ${todayPlan.running.is_rest ? 'Descanso' : `${todayPlan.running.duration_min} min &bull; ${todayPlan.running.target_distance_km} km`}
                  </span>
                </div>
                <div class="text-base font-extrabold text-white">
                  ${todayPlan.running.is_rest ? 'Recuperación Activa' : todayPlan.running.title}
                </div>
                <div class="flex flex-wrap gap-1.5 text-[11px] font-mono">
                  ${todayPlan.running.is_rest 
                    ? '<span class="px-2 py-0.5 rounded bg-[#141522] text-[#8E8FA3] border border-[#2D2F45]">0 km impacto</span>' 
                    : `<span class="px-2 py-0.5 rounded bg-[#141522] text-white border border-[#2D2F45]">Ritmo: ${todayPlan.running.target_pace}</span>
                       <span class="px-2 py-0.5 rounded bg-[#141522] text-[#FF5E80] border border-[#2D2F45]">${todayPlan.running.hr_zone}</span>
                       <span class="px-2 py-0.5 rounded bg-[#141522] text-[#8E8FA3] border border-[#2D2F45]">${todayPlan.running.shoes_recommended || 'Asics Novablast'}</span>`}
                </div>
                <p class="text-xs text-[#8E8FA3] leading-relaxed">
                  ${todayPlan.running.is_rest ? 'Descanso total de carrera para asimilar supercompensación y drenar piernas.' : todayPlan.running.main_work}
                </p>
              </div>

              <!-- Bloque Gimnasio -->
              <div class="p-4 rounded-xl bg-[#1D1E2C] border border-[#2D2F45] flex flex-col justify-between space-y-3">
                <div class="space-y-2">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-extrabold text-[#7B88FF] flex items-center gap-1.5 uppercase tracking-wide">
                      <i data-lucide="dumbbell" class="w-4 h-4"></i> Fuerza & Gimnasio
                    </span>
                    <span class="text-xs font-mono font-bold text-white">
                      ${todayPlan.gym.is_rest ? '0 fatiga' : 'RIR 1-2'}
                    </span>
                  </div>
                  <div class="text-base font-extrabold text-white">
                    ${todayPlan.gym.is_rest ? 'Descanso Neuromuscular' : todayPlan.gym.routine_name}
                  </div>
                  <p class="text-xs text-[#8E8FA3] leading-relaxed">
                    ${todayPlan.gym.is_rest 
                      ? 'Sin carga de pesas hoy. Regeneración del sistema nervioso central.' 
                      : 'Sobrecarga progresiva en jalón, remos y bíceps. Espalda compacta para soporte postural de carrera.'}
                  </p>
                </div>

                <div class="pt-2 flex items-center justify-between border-t border-[#2D2F45]/60">
                  <span class="text-xs font-medium text-[#8E8FA3]">
                    ${todayPlan.gym.is_rest ? 'Descanso' : 'Rutina 2 · Torso Tracción'}
                  </span>
                  ${todayPlan.gym.is_rest ? '' : `<button onclick="goToGymRoutine(${todayPlan.gym.routine_id || 2})" class="px-4 py-2 rounded-xl bg-[#7B88FF] hover:bg-[#6875F5] text-white text-xs font-bold transition flex items-center gap-1.5">
                    <span>Ir a la Rutina</span> &rarr;
                  </button>`}
                </div>
              </div>
            </div>
          </div>

          '''
text = text.replace(hero_old, hero_new)

# 9. In Gimnasio: Remove Blindaje Articular card and update Routine subtitles
blindaje_start = text.find('<!-- Blindaje Articular (Rodilla & Isquiotibial) -->')
blindaje_end = text.find('<!-- Contenedor de Ejercicios', blindaje_start)
if blindaje_start != -1 and blindaje_end != -1:
    text = text[:blindaje_start] + text[blindaje_end:]

# Update Routine Subtitles on Chips
text = text.replace('Cuádriceps & Búlgaras', 'Cuádriceps, Gemelos & Core')
text = text.replace('Dorsal, Remo & Bíceps', 'Espalda & Bíceps')
text = text.replace('Hip Thrust & Isquios', 'Glúteo, Femoral & Sóleo')
text = text.replace('Pectoral & Deltoides', 'Pecho, Hombro & Tríceps')

# Highlight Routine 2 by default on Monday
text = text.replace(
    'id="gym-chip-2" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#242638] border-[#2D2F45] text-[#8E8FA3] hover:border-[#FF5E80]">',
    'id="gym-chip-2" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#FF5E80] text-white border-[#FF5E80] font-semibold glow-pink">'
)
text = text.replace(
    'id="gym-chip-3" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#FF5E80] text-white border-[#FF5E80] font-semibold glow-pink">',
    'id="gym-chip-3" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#242638] border-[#2D2F45] text-[#8E8FA3] hover:border-[#FF5E80]">'
)
text = text.replace('Pierna 2 (Hoy)', 'Pierna 2')
text = text.replace('Torso Tracción', 'Torso Tracción (Hoy)')

# 10. Update Tab Entrenos to have Subview Segmented Control (Calendario vs Microciclo)
workouts_old_start = text.find('<!-- PESTAÑA 2: ENTRENOS & CALENDARIO MENSUAL -->')
if workouts_old_start != -1:
    workouts_old_start = text.rfind('<!-- ===', 0, workouts_old_start)

workouts_old_end = text.find('<!-- PESTAÑA 3: GIMNASIO', workouts_old_start)
if workouts_old_end != -1:
    workouts_old_end = text.rfind('<!-- ===', 0, workouts_old_end)

print(f"workouts_old_start: {workouts_old_start}, workouts_old_end: {workouts_old_end}")

workouts_new = '''<!-- ========================================== -->
        <!-- PESTAÑA 2: ENTRENAMIENTOS & CALENDARIO -->
        <!-- ========================================== -->
        <section id="tab-workouts" class="space-y-6 hidden">
          
          <!-- Segmented Control de Vista: Calendario vs Microciclo -->
          <div class="flex p-1 rounded-2xl bg-[#141522] border border-[#2D2F45] max-w-sm sm:max-w-md mx-auto">
            <button onclick="switchWorkoutSubView('calendar')" id="subview-btn-calendar" class="flex-1 py-2 px-3 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 bg-[#FF5E80] text-white shadow-lg">
              <i data-lucide="calendar" class="w-4 h-4"></i>
              <span>Calendario Mensual</span>
            </button>
            <button onclick="switchWorkoutSubView('microcycle')" id="subview-btn-microcycle" class="flex-1 py-2 px-3 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 text-[#8E8FA3] hover:text-white">
              <i data-lucide="list-checks" class="w-4 h-4"></i>
              <span>Próximos Entrenos</span>
            </button>
          </div>

          <!-- SUB-VISTA 1: CALENDARIO MENSUAL MINIMALISTA (ESTILO GOOGLE CALENDAR) -->
          <div id="workout-subview-calendar" class="space-y-6">
            <div class="luxury-card p-5 sm:p-7 space-y-4">
              <!-- Cabecera del Mes y Navegación -->
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#2D2F45]/60">
                <div>
                  <h3 class="text-lg font-black text-white flex items-center gap-2">
                    <i data-lucide="calendar" class="w-5 h-5 text-[#FF5E80]"></i>
                    <span>Calendario de Entrenamientos</span>
                  </h3>
                  <div class="flex items-center gap-3 text-xs text-[#8E8FA3] mt-1">
                    <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#FF5E80]"></span> Carrera</span>
                    <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#7B88FF]"></span> Gimnasio</span>
                    <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#20D994]"></span> Evento / Descanso</span>
                  </div>
                </div>

                <div class="flex items-center gap-2 bg-[#1D1E2C] border border-[#2D2F45] rounded-xl px-3 py-1.5 text-xs font-bold text-white self-start sm:self-auto">
                  <button class="text-[#8E8FA3] hover:text-white transition px-1">&larr;</button>
                  <span id="calendar-month-title">Noviembre 2026</span>
                  <button class="text-[#8E8FA3] hover:text-white transition px-1">&rarr;</button>
                </div>
              </div>

              <!-- Días de la semana -->
              <div class="grid grid-cols-7 gap-1 sm:gap-2 text-center text-[10px] font-bold text-[#8E8FA3] uppercase tracking-wider py-1">
                <div>Lun</div>
                <div>Mar</div>
                <div>Mié</div>
                <div>Jue</div>
                <div>Vie</div>
                <div>Sáb</div>
                <div>Dom</div>
              </div>

              <!-- Cuadrícula de Días -->
              <div id="calendar-days-grid" class="grid grid-cols-7 gap-1 sm:gap-2"></div>
            </div>

            <!-- Detalle del Día Seleccionado (Card Dinámica) -->
            <div id="calendar-day-detail" class="luxury-card p-6 border-l-4 border-l-[#FF5E80] space-y-3">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-[#2D2F45]/60">
                <div class="flex items-center gap-2.5">
                  <span id="detail-date-badge" class="px-2.5 py-1 rounded-lg bg-[#FF5E80]/20 text-[#FF5E80] text-xs font-mono font-bold">16 NOV</span>
                  <h4 id="detail-title" class="text-base font-extrabold text-white">35 min Drenaje Z1 + Rutina 2</h4>
                </div>
                <span id="detail-type-badge" class="text-xs font-bold text-[#8E8FA3] font-mono">Sesión de Hoy</span>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono pt-1">
                <div class="p-2.5 rounded-xl bg-[#141522] border border-[#2D2F45]">
                  <span class="text-[10px] text-[#8E8FA3] uppercase block">Distancia</span>
                  <strong id="detail-km" class="text-white text-sm">7.0 km</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-[#141522] border border-[#2D2F45]">
                  <span class="text-[10px] text-[#8E8FA3] uppercase block">Duración</span>
                  <strong id="detail-time" class="text-white text-sm">35:00</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-[#141522] border border-[#2D2F45]">
                  <span class="text-[10px] text-[#8E8FA3] uppercase block">Ritmo</span>
                  <strong id="detail-pace" class="text-[#FF5E80] text-sm">4:55-5:10/km</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-[#141522] border border-[#2D2F45]">
                  <span class="text-[10px] text-[#8E8FA3] uppercase block">Zona / FC</span>
                  <strong id="detail-hr" class="text-[#20D994] text-sm">Z1 (&lt;145 ppm)</strong>
                </div>
              </div>

              <!-- Fisiología & Análisis IA del Coach -->
              <div class="p-3.5 rounded-xl bg-[#141522] border border-[#2D2F45] text-xs space-y-1">
                <span class="font-extrabold text-[#7B88FF] text-[10px] uppercase tracking-wider block">Análisis Fisiológico del Coach:</span>
                <p id="detail-ai" class="text-white/90 leading-relaxed font-sans">
                  Sesión activa de hoy: Rodaje suave en asfalto llano + Rutina 2 (Espalda y Bíceps).
                </p>
              </div>
            </div>
          </div>

          <!-- SUB-VISTA 2: PRÓXIMOS ENTRENOS (MICROCICLO ACORDEÓN) -->
          <div id="workout-subview-microcycle" class="space-y-4 hidden">
            <div id="workouts-accordion-container" class="space-y-4"></div>
          </div>

        </section>

        '''

text = text[:workouts_old_start] + workouts_new + text[workouts_old_end:]

# 11. In Perfil Tab: Add toggle edit mode button and disabled inputs by default
profile_old_header = text.find('<button onclick="saveUserProfile()" id="save-profile-btn"')
profile_old_end = text.find('</button>', profile_old_header) + 9

profile_new_btn = '''<button onclick="toggleProfileEdit()" id="profile-edit-btn" class="px-4 py-2.5 rounded-xl bg-[#242638] border border-[#2D2F45] text-[#7B88FF] hover:border-[#7B88FF] font-extrabold text-xs transition flex items-center gap-2">
                <i data-lucide="edit-3" class="w-4 h-4"></i>
                <span id="profile-edit-text">Editar Perfil</span>
              </button>'''

text = text[:profile_old_header] + profile_new_btn + text[profile_old_end:]

# Set profile inputs to disabled/readonly initially with clean styling
text = text.replace(
    'id="profile-weight" step="0.1" value="63.0" oninput="calculateBMI()" class="w-full bg-[#141522] border border-[#2D2F45] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#FF5E80]">',
    'id="profile-weight" step="0.1" value="63.0" oninput="calculateBMI()" disabled class="w-full bg-[#141522]/50 border border-[#2D2F45] rounded-xl px-3 py-2 text-white/90 font-mono font-bold text-sm focus:outline-none focus:border-[#FF5E80] opacity-80 cursor-default transition">'
)
text = text.replace(
    'id="profile-height" step="1" value="173" oninput="calculateBMI()" class="w-full bg-[#141522] border border-[#2D2F45] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#FF5E80]">',
    'id="profile-height" step="1" value="173" oninput="calculateBMI()" disabled class="w-full bg-[#141522]/50 border border-[#2D2F45] rounded-xl px-3 py-2 text-white/90 font-mono font-bold text-sm focus:outline-none focus:border-[#FF5E80] opacity-80 cursor-default transition">'
)

# 12. Client JavaScript: Add switchWorkoutSubView and toggleProfileEdit
js_hooks = '''
    // Sub-vistas en Entrenos (Calendario vs Microciclo)
    function switchWorkoutSubView(view) {
      const calView = document.getElementById('workout-subview-calendar');
      const micView = document.getElementById('workout-subview-microcycle');
      const calBtn = document.getElementById('subview-btn-calendar');
      const micBtn = document.getElementById('subview-btn-microcycle');

      if (!calView || !micView) return;

      if (view === 'calendar') {
        calView.classList.remove('hidden');
        micView.classList.add('hidden');
        calBtn.classList.add('bg-[#FF5E80]', 'text-white', 'shadow-lg');
        calBtn.classList.remove('text-[#8E8FA3]');
        micBtn.classList.remove('bg-[#FF5E80]', 'text-white', 'shadow-lg');
        micBtn.classList.add('text-[#8E8FA3]');
      } else {
        calView.classList.add('hidden');
        micView.classList.remove('hidden');
        micBtn.classList.add('bg-[#FF5E80]', 'text-white', 'shadow-lg');
        micBtn.classList.remove('text-[#8E8FA3]');
        calBtn.classList.remove('bg-[#FF5E80]', 'text-white', 'shadow-lg');
        calBtn.classList.add('text-[#8E8FA3]');
      }
      lucide.createIcons();
    }

    // Modo Edición / Guardado de Perfil
    let isProfileEditing = false;
    function toggleProfileEdit() {
      const weightInput = document.getElementById('profile-weight');
      const heightInput = document.getElementById('profile-height');
      const editBtn = document.getElementById('profile-edit-btn');
      const editBtnText = document.getElementById('profile-edit-text');
      if (!weightInput || !heightInput || !editBtn || !editBtnText) return;

      if (!isProfileEditing) {
        // Entrar en modo edición
        isProfileEditing = true;
        weightInput.disabled = false;
        heightInput.disabled = false;
        weightInput.classList.remove('opacity-80', 'cursor-default', 'bg-[#141522]/50');
        weightInput.classList.add('bg-[#1D1E2C]', 'border-[#7B88FF]', 'ring-1', 'ring-[#7B88FF]/30');
        heightInput.classList.remove('opacity-80', 'cursor-default', 'bg-[#141522]/50');
        heightInput.classList.add('bg-[#1D1E2C]', 'border-[#7B88FF]');

        editBtn.classList.remove('bg-[#242638]', 'text-[#7B88FF]');
        editBtn.classList.add('bg-[#7B88FF]', 'text-white');
        editBtnText.innerText = "Guardar Cambios";
        weightInput.focus();
      } else {
        // Guardar cambios
        saveUserProfile();
        isProfileEditing = false;
        weightInput.disabled = true;
        heightInput.disabled = true;
        weightInput.classList.add('opacity-80', 'cursor-default', 'bg-[#141522]/50');
        weightInput.classList.remove('bg-[#1D1E2C]', 'border-[#7B88FF]', 'ring-1', 'ring-[#7B88FF]/30');
        heightInput.classList.add('opacity-80', 'cursor-default', 'bg-[#141522]/50');
        heightInput.classList.remove('bg-[#1D1E2C]', 'border-[#7B88FF]');

        editBtnText.innerText = "¡Guardado!";
        editBtn.classList.remove('bg-[#7B88FF]');
        editBtn.classList.add('bg-[#20D994]');
        setTimeout(() => {
          editBtnText.innerText = "Editar Perfil";
          editBtn.classList.remove('bg-[#20D994]', 'text-white');
          editBtn.classList.add('bg-[#242638]', 'text-[#7B88FF]');
        }, 2000);
      }
    }
'''

text = text.replace('function switchTab(tabId) {', js_hooks + '\n    function switchTab(tabId) {')

# 13. Update renderCalendarMonth to use Google Calendar style today circle (no overlapping badge!)
old_cal_render_start = text.find('function renderCalendarMonth() {')
old_cal_render_end = text.find('function onCalendarDayClick(el) {', old_cal_render_start)

new_cal_render = '''function renderCalendarMonth() {
      const container = document.getElementById('calendar-days-grid');
      if (!container) return;

      const totalDays = calendarData.days_in_month;
      const firstWeekday = calendarData.first_day_weekday; // 6 para domingo

      let html = '';

      // Días vacíos previos (Lunes=0..Domingo=6)
      const emptyPrev = firstWeekday === 0 ? 0 : firstWeekday;
      for (let i = 0; i < emptyPrev; i++) {
        html += '<div class="h-14 sm:h-16 rounded-xl bg-[#141522]/20 border border-transparent"></div>';
      }

      // Días del mes (1 a 30)
      for (let d = 1; d <= totalDays; d++) {
        const dateKey = "2026-11-" + (d < 10 ? '0' + d : d);
        const activity = calendarData.activities[dateKey] || { dots: [] };
        const isToday = dateKey === todayISO;

        const borderClass = isToday 
          ? 'border-2 border-[#FF5E80] shadow-md shadow-[#FF5E80]/20 bg-[#1D1E2C]' 
          : 'border border-[#2D2F45] bg-[#141522] hover:border-[#7B88FF]/60 hover:bg-[#1D1E2C]/60';

        // Estilo Google Calendar para HOY: número dentro de un círculo coral sólido centrado
        let dayNumberHtml = '';
        if (isToday) {
          dayNumberHtml = '<div class="w-6 h-6 sm:w-7 sm:h-7 rounded-full bg-[#FF5E80] text-white font-black flex items-center justify-center mx-auto text-xs sm:text-sm shadow-md">' + d + '</div>';
        } else {
          dayNumberHtml = '<div class="w-6 h-6 sm:w-7 sm:h-7 flex items-center justify-center mx-auto text-xs sm:text-sm font-bold text-white/90">' + d + '</div>';
        }

        // Puntos de color discretos
        const dotsHtml = '<div class="flex items-center justify-center gap-1 mt-1 sm:mt-1.5">' +
          (activity.dots || []).map(function(dot) {
            const color = dot === 'run' ? '#FF5E80' : (dot === 'gym' ? '#7B88FF' : '#20D994');
            return '<span class="w-1.5 h-1.5 rounded-full" style="background-color: ' + color + ';"></span>';
          }).join('') +
        '</div>';

        html += '<div data-date="' + dateKey + '" onclick="onCalendarDayClick(this)" class="' + borderClass + ' h-14 sm:h-16 p-1 sm:p-1.5 rounded-xl flex flex-col justify-between cursor-pointer transition select-none">' +
          dayNumberHtml +
          dotsHtml +
        '</div>';
      }

      container.innerHTML = html;
    }

    '''

text = text[:old_cal_render_start] + new_cal_render + text[old_cal_render_end:]

# 14. In DOMContentLoaded, make sure selectGymRoutine(2) is called for Monday
text = text.replace("selectGymRoutine(3);", "selectGymRoutine(2);")
text = text.replace("selectCalendarDay('2026-11-14');", "selectCalendarDay('2026-11-16');")

# Save as scripts/build_final_v4_dashboard.py
with open('scripts/build_final_v4_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("scripts/build_final_v4_dashboard.py creado exitosamente! Longitud:", len(text))
