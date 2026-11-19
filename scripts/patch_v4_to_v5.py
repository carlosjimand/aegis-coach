import re
import json

print("Leyendo build_final_v4_dashboard.py para aplicar las actualizaciones v5...")
with open('scripts/build_final_v4_dashboard.py', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Cargar multi_month_calendar
with open('data/full_multi_month_calendar.json', 'r', encoding='utf-8') as f:
    multi_month_json = json.load(f)

# Reemplazar carga de calendar_nov_2026 por CALENDAR_DATA_BY_MONTH
old_cal_def = """# Calendario de Noviembre 2026 (con datos de entrenos reales de Carlos)
calendar_nov_2026 = {"""
idx_cal_start = code.find('# Calendario de Noviembre 2026')
idx_cal_end = code.find('def make_aero_svg(prefix="aero"):')

new_cal_load = f'''# Calendario Multi-Mes Oficial (Septiembre a Diciembre 2026) con datos de Garmin/FIT
with open('data/full_multi_month_calendar.json', 'r', encoding='utf-8') as f:
    multi_month_calendar = json.load(f)

'''

code = code[:idx_cal_start] + new_cal_load + code[idx_cal_end:]

# Reemplazar const CALENDAR_DATA en worker
old_const = "const CALENDAR_DATA: any = ''' + json.dumps(calendar_nov_2026, indent=2, ensure_ascii=False) + ''';"
new_const = "const CALENDAR_DATA_BY_MONTH: any = ''' + json.dumps(multi_month_calendar, indent=2, ensure_ascii=False) + ''';"
code = code.replace(old_const, new_const)

# 2. Rutas del Worker: /manifest.json, /favicon.ico desde KV, iconos y no-cache
old_worker_fetch = """    // Favicon oficial y Logo Aero-Aegis SVG
    if (url.pathname === "/favicon.ico" || url.pathname === "/img/logo.svg") {
      return new Response(`''' + favicon_svg + '''`, {
        headers: {
          "Content-Type": "image/svg+xml",
          "Cache-Control": "public, max-age=86400"
        }
      });
    }

    // Servir imágenes (Vectoriales y Fotos) desde KV
    if (url.pathname.startsWith("/img/")) {
      const cleanPath = url.pathname.replace("/img/", "");
      let key = "";
      let contentType = "image/png";

      if (cleanPath.startsWith("vector_")) {
        key = cleanPath.replace(".png", "");
        contentType = "image/png";
      } else {
        key = "img_" + cleanPath.replace(".jpg", "").replace(".png", "");
        contentType = "image/jpeg";
      }

      try {
        const imgData = await env.AEGIS_KV.get(key, { type: "arrayBuffer" });
        if (imgData) {
          return new Response(imgData, {
            headers: {
              "Content-Type": contentType,
              "Cache-Control": "public, max-age=86400"
            }
          });
        }
      } catch (e) {
        console.error("Error leyendo imagen de KV:", e);
      }
      return new Response("Imagen no encontrada", { status: 404 });
    }"""

new_worker_fetch = """    // Web App Manifest para Android Chrome y PWA
    if (url.pathname === "/manifest.json") {
      const manifest = {
        name: "Aegis Coach",
        short_name: "Aegis",
        description: "Sistema de Inteligencia y Coaching de Carlos Jiménez Andrino",
        start_url: "/",
        display: "standalone",
        background_color: "#0d0e15",
        theme_color: "#0d0e15",
        icons: [
          {
            src: "/img/icon-192.png?v=6",
            sizes: "192x192",
            type: "image/png",
            purpose: "any maskable"
          },
          {
            src: "/img/icon-512.png?v=6",
            sizes: "512x512",
            type: "image/png",
            purpose: "any maskable"
          }
        ]
      };
      return new Response(JSON.stringify(manifest), {
        headers: {
          "Content-Type": "application/manifest+json; charset=utf-8",
          "Cache-Control": "no-cache, no-store, must-revalidate"
        }
      });
    }

    // Favicon oficial (.ico) servido desde KV con no-cache
    if (url.pathname === "/favicon.ico") {
      try {
        const icoData = await env.AEGIS_KV.get("img_favicon", { type: "arrayBuffer" });
        if (icoData) {
          return new Response(icoData, {
            headers: {
              "Content-Type": "image/x-icon",
              "Cache-Control": "no-cache, no-store, must-revalidate"
            }
          });
        }
      } catch (e) {}
    }

    // Logo Aero-Aegis SVG con no-cache
    if (url.pathname === "/img/logo.svg") {
      return new Response(`''' + favicon_svg + '''`, {
        headers: {
          "Content-Type": "image/svg+xml",
          "Cache-Control": "no-cache, no-store, must-revalidate"
        }
      });
    }

    // Servir imágenes (Vectoriales, Iconos y Fotos) desde KV con no-cache
    if (url.pathname.startsWith("/img/")) {
      const cleanPath = url.pathname.replace("/img/", "");
      let key = "";
      let contentType = "image/png";

      if (cleanPath.startsWith("vector_")) {
        key = cleanPath.replace(".png", "");
        contentType = "image/png";
      } else if (cleanPath.startsWith("icon-")) {
        key = "img_" + cleanPath.replace(".png", "");
        contentType = "image/png";
      } else {
        key = "img_" + cleanPath.replace(".jpg", "").replace(".png", "");
        contentType = "image/jpeg";
      }

      try {
        const imgData = await env.AEGIS_KV.get(key, { type: "arrayBuffer" });
        if (imgData) {
          return new Response(imgData, {
            headers: {
              "Content-Type": contentType,
              "Cache-Control": "no-cache, no-store, must-revalidate"
            }
          });
        }
      } catch (e) {
        console.error("Error leyendo imagen de KV:", e);
      }
      return new Response("Imagen no encontrada", { status: 404 });
    }"""

code = code.replace(old_worker_fetch, new_worker_fetch)

# 3. Encabezado HTML: Manifest, Iconos, Theme color
old_head_icon = '<link rel="icon" type="image/svg+xml" href="\' + favicon_data_uri + \'">'
new_head_icon = """<link rel="manifest" href="/manifest.json?v=6">
  <link rel="icon" type="image/png" sizes="192x192" href="/img/icon-192.png?v=6">
  <link rel="icon" type="image/svg+xml" href="' + favicon_data_uri + '">
  <link rel="apple-touch-icon" sizes="180x180" href="/img/icon-192.png?v=6">
  <link rel="shortcut icon" href="/favicon.ico?v=6">
  <meta name="theme-color" content="#141522">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Aegis Coach">"""

code = code.replace(old_head_icon, new_head_icon)

# 4. Estilo de Hero Card con degradado de alta gama en CSS
old_style_insert = """.luxury-card {
      background-color: var(--card-dark);
      border: 1px solid var(--card-border);
      border-radius: 1.5rem;
    }"""

new_style_insert = """.luxury-card {
      background-color: var(--card-dark);
      border: 1px solid var(--card-border);
      border-radius: 1.5rem;
    }
    .hero-gradient-card {
      background: linear-gradient(135deg, #FF3366 0%, #BA24D5 50%, #6366F1 100%);
      box-shadow: 0 14px 34px -6px rgba(255, 51, 102, 0.35);
      border-radius: 1.75rem;
    }"""

code = code.replace(old_style_insert, new_style_insert)

# 5. Reemplazar tarjeta de Sesión de Hoy (restaurar degradado, quitar En Curso, dos subbloques separados)
old_hero_card = """          <!-- 1. BLOQUE DE LA SESIÓN DE HOY (LIMPIO, RESPONSIVE & ELEGANTE) -->
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
                    ${todayPlan.gym.is_rest ? 'Descanso' : 'Rutina 2 · Torso Tracción (Hoy)'}
                  </span>
                  ${todayPlan.gym.is_rest ? '' : `<button onclick="goToGymRoutine(${todayPlan.gym.routine_id || 2})" class="px-4 py-2 rounded-xl bg-[#7B88FF] hover:bg-[#6875F5] text-white text-xs font-bold transition flex items-center gap-1.5">
                    <span>Ir a la Rutina</span> &rarr;
                  </button>`}
                </div>
              </div>
            </div>
          </div>"""

new_hero_card = """          <!-- 1. BLOQUE SESIÓN DE HOY (DEGRADADO DE ALTA GAMA RESTAURADO) -->
          <div class="hero-gradient-card p-5 sm:p-7 text-white space-y-4">
            <!-- Header de la tarjeta -->
            <div class="flex items-center justify-between pb-3 border-b border-white/20">
              <div class="flex flex-wrap items-center gap-2">
                <span class="inline-flex items-center px-3 py-1 rounded-full bg-black/25 backdrop-blur-md border border-white/20 text-xs font-black uppercase tracking-wider text-white">
                  HOY &bull; ${todayPlan.day_name.toUpperCase()} ${todayPlan.date}
                </span>
                <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-black/25 backdrop-blur-md border border-white/20 text-xs font-bold text-white/95">
                  ${todayPlan.running.session_type}
                  <i data-lucide="zap" class="w-3.5 h-3.5 text-yellow-300"></i>
                </span>
              </div>
              <button onclick="switchTab('workouts')" class="text-xs font-bold text-white/80 hover:text-white transition flex items-center gap-1">
                <span>Ver Plan</span> &rarr;
              </button>
            </div>

            <!-- Título Principal -->
            <div>
              <h2 class="text-xl sm:text-2xl font-black tracking-tight text-white leading-tight">
                ${todayPlan.running.is_rest ? todayPlan.running.title : todayPlan.running.title}
              </h2>
              <p class="text-xs sm:text-sm font-mono font-bold text-white/90 mt-1">
                ${todayPlan.running.is_rest 
                  ? 'Descanso de carrera • 0 km impacto' 
                  : `${todayPlan.running.duration_min} min • ${todayPlan.running.target_distance_km} km • Ritmo: ${todayPlan.running.target_pace} • ${todayPlan.running.hr_zone}`}
              </p>
            </div>

            <!-- Grid de Carrera y Gimnasio Separados (Translúcidos) -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-3.5">
              <!-- Bloque Carrera -->
              <div class="p-4 rounded-2xl bg-black/30 backdrop-blur-md border border-white/20 space-y-2">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black uppercase tracking-wide text-white flex items-center gap-1.5">
                    <i data-lucide="footprints" class="w-4 h-4 text-white"></i> Carrera
                  </span>
                  <span class="text-xs font-mono font-bold text-white/90">
                    ${todayPlan.running.is_rest ? 'Descanso' : `${todayPlan.running.duration_min} min • ${todayPlan.running.target_distance_km} km`}
                  </span>
                </div>
                <div class="text-sm font-extrabold text-white">
                  ${todayPlan.running.is_rest ? 'Recuperación Activa' : todayPlan.running.title}
                </div>
                <div class="flex flex-wrap gap-1.5 text-[11px] font-mono">
                  ${todayPlan.running.is_rest 
                    ? '<span class="px-2 py-0.5 rounded bg-black/40 text-white/80 border border-white/20">0 km impacto</span>' 
                    : `<span class="px-2 py-0.5 rounded bg-black/40 text-white border border-white/20">Ritmo: ${todayPlan.running.target_pace}</span>
                       <span class="px-2 py-0.5 rounded bg-black/40 text-white border border-white/20">${todayPlan.running.hr_zone}</span>
                       <span class="px-2 py-0.5 rounded bg-black/40 text-white/90 border border-white/20">${todayPlan.running.shoes_recommended || 'Asics Novablast 5'}</span>`}
                </div>
                <p class="text-xs text-white/85 leading-relaxed font-medium">
                  ${todayPlan.running.is_rest ? 'Descanso total de carrera para asimilar supercompensación y drenar piernas.' : todayPlan.running.main_work}
                </p>
              </div>

              <!-- Bloque Gimnasio -->
              <div class="p-4 rounded-2xl bg-black/30 backdrop-blur-md border border-white/20 flex flex-col justify-between space-y-2.5">
                <div class="space-y-1.5">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-black uppercase tracking-wide text-white flex items-center gap-1.5">
                      <i data-lucide="dumbbell" class="w-4 h-4 text-white"></i> Fuerza & Gimnasio
                    </span>
                    <span class="text-xs font-mono font-bold text-white/90">
                      ${todayPlan.gym.is_rest ? '0 fatiga' : 'RIR 1-2'}
                    </span>
                  </div>
                  <div class="text-sm font-extrabold text-white">
                    ${todayPlan.gym.is_rest ? 'Descanso Neuromuscular' : todayPlan.gym.routine_name}
                  </div>
                  <p class="text-xs text-white/85 leading-relaxed font-medium">
                    ${todayPlan.gym.is_rest 
                      ? 'Sin carga de pesas hoy. Regeneración del sistema nervioso central.' 
                      : (todayPlan.gym.highlight_exercises && todayPlan.gym.highlight_exercises.length > 0 
                          ? todayPlan.gym.highlight_exercises.slice(0, 3).map((e: any) => e.name).join(' • ') 
                          : 'Ejercicios de la rutina oficial')}
                  </p>
                </div>

                <div class="pt-2 flex items-center justify-between border-t border-white/20">
                  <span class="text-xs font-medium text-white/80">
                    ${todayPlan.gym.is_rest ? 'Descanso' : 'Rutina ' + (todayPlan.gym.routine_id || 2) + ' (Hoy)'}
                  </span>
                  ${todayPlan.gym.is_rest ? '' : `<button onclick="goToGymRoutine(${todayPlan.gym.routine_id || 2})" class="px-4 py-1.5 rounded-full bg-white text-black text-xs font-extrabold hover:bg-white/90 transition flex items-center gap-1.5 shadow-md">
                    <span>Ir a la Rutina</span> &rarr;
                  </button>`}
                </div>
              </div>
            </div>

            <!-- Botones Rápidos de la Tarjeta Hero -->
            <div class="flex flex-wrap items-center gap-3 pt-1">
              <button onclick="switchTab('workouts')" class="px-5 py-2.5 rounded-full bg-white text-black font-black text-xs hover:bg-white/90 transition shadow-lg flex items-center gap-2">
                <span>Ver Entrenos</span>
                <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
              </button>
              <button onclick="switchTab('gym')" class="px-5 py-2.5 rounded-full bg-black/40 hover:bg-black/60 text-white font-bold text-xs border border-white/30 backdrop-blur-md transition flex items-center gap-2">
                <i data-lucide="clipboard-pen" class="w-3.5 h-3.5"></i>
                <span>Registrar Gym</span>
              </button>
            </div>
          </div>"""

code = code.replace(old_hero_card, new_hero_card)

# 6. Añadir contenedores de vueltas y notas en el detalle del calendario
target_detail_end = '</p>\n              </div>\n            </div>'
replacement_detail_end = '</p>\n              </div>\n\n              <!-- Desglose de Vueltas Reales Garmin FIT -->\n              <div id="detail-laps-section" class="hidden"></div>\n\n              <!-- Notas de Carlos en Garmin -->\n              <div id="detail-notes-section" class="hidden"></div>\n            </div>'
code = code.replace(target_detail_end, replacement_detail_end)


# 7. Actualizar script cliente JS para usar calendarDataByMonth y selector de mes funcional
old_cal_js = """    const calendarData = ${JSON.stringify(CALENDAR_DATA)};"""
new_cal_js = """    const calendarDataByMonth = ${JSON.stringify(CALENDAR_DATA_BY_MONTH)};
    const monthKeys = ["2026-09", "2026-10", "2026-11", "2026-12"];
    let currentMonthIdx = 2; // Noviembre 2026 por defecto"""

code = code.replace(old_cal_js, new_cal_js)

# Actualizar URLs de imágenes con versionado ?v=6
code = code.replace('/img/vector_ex_', '/img/vector_ex_') # base
# Append ?v=6 to all vector_ex_X_Y.png in gymRoutinesData
code = re.sub(r'(/img/vector_ex_\d+_\d+\.png)(\?v=\d+)?', r'\1?v=6', code)

# Botones interactivos de mes de calendario
code = code.replace(
    '<span id="calendar-month-title">Noviembre 2026</span>',
    '<span id="calendar-month-label" class="min-w-[110px] text-center">Noviembre 2026</span>'
)
code = code.replace(
    '<button class="text-[#8E8FA3] hover:text-white transition px-1">&larr;</button>',
    '<button id="cal-btn-prev" onclick="changeCalendarMonth(-1)" class="text-[#8E8FA3] hover:text-white transition px-1 cursor-pointer">&larr;</button>'
)
code = code.replace(
    '<button class="text-[#8E8FA3] hover:text-white transition px-1">&rarr;</button>',
    '<button id="cal-btn-next" onclick="changeCalendarMonth(1)" class="text-[#8E8FA3] hover:text-white transition px-1 cursor-pointer">&rarr;</button>'
)

# Reemplazar funciones de calendario
old_cal_funcs = """    // ==========================================
    let currentMonthOffset = 0; // 0 = Nov 2026

    function changeCalendarMonth(delta) {
      currentMonthOffset += delta;
      renderCalendarMonth();
    }

    function renderCalendarMonth() {
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

    function onCalendarDayClick(el) {
      const dateKey = el.getAttribute('data-date');
      if (dateKey) selectCalendarDay(dateKey);
    }

    function selectCalendarDay(dateKey) {
      const act = calendarData.activities[dateKey];
      const detailContainer = document.getElementById('calendar-day-detail');
      if (!detailContainer) return;

      const dateObj = new Date(dateKey + 'T00:00:00Z');
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' };
      const formattedDate = dateObj.toLocaleDateString('es-ES', options);

      const dateBadge = document.getElementById('detail-date-badge');
      if (dateBadge) dateBadge.innerText = formattedDate;

      const titleEl = document.getElementById('detail-title');
      const kmEl = document.getElementById('detail-km') || document.getElementById('detail-dist');
      const timeEl = document.getElementById('detail-time');
      const paceEl = document.getElementById('detail-pace');
      const hrEl = document.getElementById('detail-hr');
      const aiEl = document.getElementById('detail-ai');

      if (act) {
        if (titleEl) titleEl.innerText = act.title;
        if (kmEl) kmEl.innerText = (act.km > 0 ? act.km + ' km' : '-');
        if (timeEl) timeEl.innerText = (act.time || '-');
        if (paceEl) paceEl.innerText = act.pace;
        if (hrEl) hrEl.innerText = act.hr;
        if (aiEl) aiEl.innerText = act.ai;
      } else {
        if (titleEl) titleEl.innerText = "Día de Descanso & Recuperación Celular";
        if (kmEl) kmEl.innerText = "-";
        if (timeEl) timeEl.innerText = "-";
        if (paceEl) paceEl.innerText = "-";
        if (hrEl) hrEl.innerText = "FCR 42 ppm";
        if (aiEl) aiEl.innerText = "Asimilación fisiológica de la carga previa. Reparación del tejido conjuntivo y supercompensación de glucógeno muscular.";
      }
    }"""

new_cal_funcs = """    // ==========================================
    // CALENDARIO MULTI-MES INTERACTIVO (SEP - DIC)
    // ==========================================
    function changeCalendarMonth(delta) {
      const newIdx = currentMonthIdx + delta;
      if (newIdx >= 0 && newIdx < monthKeys.length) {
        currentMonthIdx = newIdx;
        renderCalendarMonth();
      }
    }

    function renderCalendarMonth() {
      const container = document.getElementById('calendar-days-grid');
      if (!container) return;

      const mKey = monthKeys[currentMonthIdx];
      const mData = calendarDataByMonth[mKey];
      if (!mData) return;

      // Actualizar label del mes
      const monthLabel = document.getElementById('calendar-month-label');
      if (monthLabel) monthLabel.innerText = mData.month_name;

      // Actualizar opacidad de botones
      const prevBtn = document.getElementById('cal-btn-prev');
      const nextBtn = document.getElementById('cal-btn-next');
      if (prevBtn) {
        prevBtn.style.opacity = currentMonthIdx === 0 ? "0.3" : "1";
        prevBtn.style.pointerEvents = currentMonthIdx === 0 ? "none" : "auto";
      }
      if (nextBtn) {
        nextBtn.style.opacity = currentMonthIdx === monthKeys.length - 1 ? "0.3" : "1";
        nextBtn.style.pointerEvents = currentMonthIdx === monthKeys.length - 1 ? "none" : "auto";
      }

      const totalDays = mData.days_in_month;
      const firstWeekday = mData.first_day_weekday;

      let html = '';
      for (let i = 0; i < firstWeekday; i++) {
        html += '<div class="h-14 sm:h-16 rounded-xl bg-[#141522]/20 border border-transparent"></div>';
      }

      let firstActiveDate = null;
      for (let d = 1; d <= totalDays; d++) {
        const dayStr = d < 10 ? '0' + d : '' + d;
        const dateKey = mKey + '-' + dayStr;
        const activity = mData.activities[dateKey] || { dots: [] };
        const isToday = dateKey === todayISO;

        if (activity.title && !firstActiveDate) {
          firstActiveDate = dateKey;
        }

        const borderClass = isToday 
          ? 'border-2 border-[#FF5E80] shadow-md shadow-[#FF5E80]/20 bg-[#1D1E2C]' 
          : 'border border-[#2D2F45] bg-[#141522] hover:border-[#7B88FF]/60 hover:bg-[#1D1E2C]/60';

        let dayNumberHtml = '';
        if (isToday) {
          dayNumberHtml = '<div class="w-6 h-6 sm:w-7 sm:h-7 rounded-full bg-[#FF5E80] text-white font-black flex items-center justify-center mx-auto text-xs sm:text-sm shadow-md">' + d + '</div>';
        } else {
          dayNumberHtml = '<div class="w-6 h-6 sm:w-7 sm:h-7 flex items-center justify-center mx-auto text-xs sm:text-sm font-bold text-white/90">' + d + '</div>';
        }

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

      // Auto-seleccionar día de hoy si estamos en noviembre, o primer día con entreno
      const dateToSelect = (mKey === '2026-11' && mData.activities[todayISO]) ? todayISO : (firstActiveDate || (mKey + '-01'));
      selectCalendarDay(dateToSelect);
    }

    function onCalendarDayClick(el) {
      const dateKey = el.getAttribute('data-date');
      if (dateKey) selectCalendarDay(dateKey);
    }

    function selectCalendarDay(dateKey) {
      const mKey = dateKey.substring(0, 7);
      const mData = calendarDataByMonth[mKey] || calendarDataByMonth['2026-11'];
      const act = mData.activities[dateKey];
      const detailContainer = document.getElementById('calendar-day-detail');
      if (!detailContainer) return;

      // Resaltar celda seleccionada
      document.querySelectorAll('#calendar-days-grid > div[data-date]').forEach(function(c) {
        const isT = c.getAttribute('data-date') === todayISO;
        c.className = (isT 
          ? 'border-2 border-[#FF5E80] shadow-md shadow-[#FF5E80]/20 bg-[#1D1E2C]' 
          : 'border border-[#2D2F45] bg-[#141522] hover:border-[#7B88FF]/60 hover:bg-[#1D1E2C]/60') + 
          ' h-14 sm:h-16 p-1 sm:p-1.5 rounded-xl flex flex-col justify-between cursor-pointer transition select-none';
      });
      const selectedEl = document.querySelector('#calendar-days-grid > div[data-date="' + dateKey + '"]');
      if (selectedEl) {
        selectedEl.className = 'border-2 border-[#7B88FF] shadow-lg shadow-[#7B88FF]/30 bg-[#25283D] h-14 sm:h-16 p-1 sm:p-1.5 rounded-xl flex flex-col justify-between cursor-pointer transition select-none scale-[1.02]';
      }

      const dateObj = new Date(dateKey + 'T00:00:00Z');
      const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric', timeZone: 'UTC' };
      const formattedDate = dateObj.toLocaleDateString('es-ES', options);

      const dateBadge = document.getElementById('detail-date-badge');
      if (dateBadge) dateBadge.innerText = formattedDate;

      const titleEl = document.getElementById('detail-title');
      const kmEl = document.getElementById('detail-km') || document.getElementById('detail-dist');
      const timeEl = document.getElementById('detail-time');
      const paceEl = document.getElementById('detail-pace');
      const hrEl = document.getElementById('detail-hr');
      const aiEl = document.getElementById('detail-ai');
      const typeBadge = document.getElementById('detail-type-badge');

      if (act) {
        if (titleEl) titleEl.innerText = act.title;
        if (kmEl) kmEl.innerText = (act.km > 0 ? act.km + ' km' : '-');
        if (timeEl) timeEl.innerText = (act.time || '-');
        if (paceEl) paceEl.innerText = act.pace;
        if (hrEl) hrEl.innerText = act.hr;
        if (aiEl) aiEl.innerText = act.ai;
        if (typeBadge) {
          typeBadge.innerText = act.type;
          typeBadge.className = 'px-3 py-1 rounded-full text-xs font-bold ' + 
            (act.type.includes('Running') ? 'bg-[#FF5E80]/20 text-[#FF5E80] border border-[#FF5E80]/30' : 
            (act.type.includes('Gym') ? 'bg-[#7B88FF]/20 text-[#7B88FF] border border-[#7B88FF]/30' : 'bg-[#20D994]/20 text-[#20D994] border border-[#20D994]/30'));
        }
      } else {
        if (titleEl) titleEl.innerText = "Día de Descanso & Recuperación Celular";
        if (kmEl) kmEl.innerText = "-";
        if (timeEl) timeEl.innerText = "-";
        if (paceEl) paceEl.innerText = "-";
        if (hrEl) hrEl.innerText = "FCR 42 ppm";
        if (aiEl) aiEl.innerText = "Asimilación fisiológica de la carga previa. Reparación del tejido conjuntivo y supercompensación de glucógeno muscular.";
        if (typeBadge) {
          typeBadge.innerText = "Descanso";
          typeBadge.className = "px-3 py-1 rounded-full text-xs font-bold bg-[#20D994]/20 text-[#20D994] border border-[#20D994]/30";
        }
      }

      // Sección de Vueltas Reales
      const lapsContainer = document.getElementById('detail-laps-section');
      if (lapsContainer) {
        if (act && act.laps && act.laps.length > 0) {
          let lHtml = '<div class="mt-4 pt-4 border-t border-[#2D2F45]/60 space-y-2">' +
            '<div class="flex items-center justify-between">' +
              '<span class="text-xs font-bold text-white flex items-center gap-1.5"><i data-lucide="timer" class="w-3.5 h-3.5 text-[#FF5E80]"></i> Desglose de Vueltas / Parciales Oficiales Garmin</span>' +
              '<span class="text-[11px] font-mono text-[#8E8FA3]">' + act.laps.length + ' vueltas</span>' +
            '</div>' +
            '<div class="overflow-x-auto rounded-xl border border-[#2D2F45]/70 bg-[#1D1E2C]/50">' +
              '<table class="w-full text-left text-xs font-mono">' +
                '<thead>' +
                  '<tr class="bg-[#141522] text-[#8E8FA3] border-b border-[#2D2F45] text-[10px] uppercase">' +
                    '<th class="py-2 px-3">Lap</th>' +
                    '<th class="py-2 px-3">Distancia</th>' +
                    '<th class="py-2 px-3">Tiempo</th>' +
                    '<th class="py-2 px-3">Ritmo</th>' +
                    '<th class="py-2 px-3">FC Media</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody class="divide-y divide-[#2D2F45]/40 text-white/90">';
          act.laps.forEach(function(l) {
            const paceColor = l.pace.startsWith('3:') ? 'text-[#FF5E80]' : 'text-white';
            lHtml += '<tr class="hover:bg-white/5 transition">' +
              '<td class="py-1.5 px-3 font-bold text-[#7B88FF]">' + l.lap + '</td>' +
              '<td class="py-1.5 px-3">' + l.dist_m + ' m</td>' +
              '<td class="py-1.5 px-3">' + l.time_str + '</td>' +
              '<td class="py-1.5 px-3 font-bold ' + paceColor + '">' + l.pace + '</td>' +
              '<td class="py-1.5 px-3">' + (l.hr_avg || '-') + ' ppm</td>' +
            '</tr>';
          });
          lHtml += '</tbody></table></div></div>';
          lapsContainer.innerHTML = lHtml;
          lapsContainer.classList.remove('hidden');
        } else {
          lapsContainer.innerHTML = '';
          lapsContainer.classList.add('hidden');
        }
      }

      // Sección de Notas de Carlos
      const notesContainer = document.getElementById('detail-notes-section');
      if (notesContainer) {
        if (act && act.notes) {
          notesContainer.innerHTML = '<div class="mt-3 p-3.5 rounded-xl bg-[#1D1E2C] border border-[#2D2F45] text-xs text-[#8E8FA3] leading-relaxed">' +
            '<span class="font-bold text-white block mb-1">📝 Notas de Carlos (Garmin):</span>' +
            '<div class="whitespace-pre-line text-white/90">' + act.notes + '</div>' +
          '</div>';
          notesContainer.classList.remove('hidden');
        } else {
          notesContainer.innerHTML = '';
          notesContainer.classList.add('hidden');
        }
      }

      if (window.lucide) window.lucide.createIcons();
    }"""

code = code.replace(old_cal_funcs, new_cal_funcs)

with open('scripts/build_final_v5_dashboard.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("¡build_final_v5_dashboard.py guardado con todas las mejoras!")
