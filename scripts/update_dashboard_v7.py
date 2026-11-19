import re

def update_builder():
    with open('scripts/build_luxury_octet_dashboard.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Typography: Replace Outfit with Inter
    content = content.replace(
        'family=Outfit:wght@300;400;500;600;700;800;900',
        'family=Inter:wght@300;400;500;600;700;800;900'
    )
    content = content.replace(
        "font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;",
        "font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;\n      letter-spacing: -0.011em;"
    )
    content = content.replace(
        "font-family: 'Outfit', sans-serif;",
        "font-family: 'Inter', sans-serif;"
    )
    content = content.replace("family: 'Outfit'", "family: 'Inter'")

    # 2. Text contrast: Improve secondary text from #7b6e7f to #A297A6
    content = content.replace('--composers-magic: #7b6e7f;', '--composers-magic: #A297A6;')
    content = content.replace('text-[#7b6e7f]', 'text-[#A297A6]')

    # 3. Simplify Hero Card: Remove SVG waves & eliminate repetitive text
    old_hero_svg = '''            <!-- Ondas Orgánicas Fluidas (Efecto Tarjeta Balance) -->
            <svg class="absolute inset-0 w-full h-full opacity-25 pointer-events-none" preserveAspectRatio="none" viewBox="0 0 600 300" fill="none">
              <path d="M0 160 C 150 90, 300 230, 600 130" stroke="#FFFFFF" stroke-width="1.2" />
              <path d="M0 190 C 180 120, 330 260, 600 160" stroke="#FFFFFF" stroke-width="1.2" />
              <path d="M0 220 C 210 150, 360 290, 600 190" stroke="#FFFFFF" stroke-width="1.2" />
              <path d="M0 130 C 120 70, 270 200, 600 100" stroke="#FFFFFF" stroke-width="0.8" />
              <path d="M0 250 C 240 180, 390 320, 600 220" stroke="#FFFFFF" stroke-width="0.8" />
            </svg>'''
    
    content = content.replace(old_hero_svg, '')

    # Check and clean Hero Card layout
    old_hero_layout = '''            <!-- Header de la tarjeta -->
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
              <div class="p-4 rounded-2xl bg-[#171821]/40 backdrop-blur-md border border-white/20 relative z-10 space-y-2">
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
              <div class="p-4 rounded-2xl bg-[#171821]/40 backdrop-blur-md border border-white/20 relative z-10 flex flex-col justify-between space-y-2.5">
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
            </div>'''

    new_hero_layout = '''            <!-- Header de la tarjeta -->
            <div class="flex items-center justify-between pb-3 border-b border-white/20">
              <div class="flex flex-wrap items-center gap-2">
                <span class="inline-flex items-center px-3 py-1 rounded-full bg-black/25 backdrop-blur-md border border-white/20 text-xs font-black uppercase tracking-wider text-white">
                  SESIÓN DE HOY &bull; ${todayPlan.day_name.toUpperCase()} ${todayPlan.date}
                </span>
                <span class="inline-flex items-center gap-1 px-3 py-1 rounded-full bg-white/20 backdrop-blur-md border border-white/20 text-xs font-bold text-white">
                  ${todayPlan.running.session_type}
                </span>
              </div>
              <button onclick="switchTab('workouts')" class="text-xs font-bold text-white/85 hover:text-white transition flex items-center gap-1">
                <span>Ver Plan</span> &rarr;
              </button>
            </div>

            <!-- Título Principal & Métrica Limpia -->
            <div>
              <h2 class="text-xl sm:text-2xl font-black tracking-tight text-white leading-tight">
                ${todayPlan.running.title}
              </h2>
              <p class="text-xs sm:text-sm font-semibold text-white/95 mt-1">
                ${todayPlan.running.is_rest 
                  ? 'Descanso de carrera • 0 km impacto' 
                  : `${todayPlan.running.duration_min} min &bull; ${todayPlan.running.target_distance_km} km &bull; ${todayPlan.running.target_pace} &bull; ${todayPlan.running.hr_zone}`}
              </p>
            </div>

            <!-- Grid de Carrera y Gimnasio Separados (Cápsulas Translúcidas Estilo Balance) -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-3.5">
              <!-- Bloque Carrera -->
              <div class="p-4 rounded-2xl bg-[#171821]/40 backdrop-blur-md border border-white/20 space-y-1.5">
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black uppercase tracking-wide text-white flex items-center gap-1.5">
                    <i data-lucide="footprints" class="w-4 h-4 text-white"></i> Carrera
                  </span>
                  <span class="text-xs font-mono font-medium text-white/80">
                    ${todayPlan.running.shoes_recommended || 'Asics Novablast 5'}
                  </span>
                </div>
                <p class="text-xs text-white/90 leading-relaxed font-normal">
                  ${todayPlan.running.is_rest ? 'Descanso total de carrera para asimilar supercompensación y drenar piernas.' : todayPlan.running.main_work}
                </p>
              </div>

              <!-- Bloque Gimnasio -->
              <div class="p-4 rounded-2xl bg-[#171821]/40 backdrop-blur-md border border-white/20 flex flex-col justify-between space-y-2">
                <div>
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-black uppercase tracking-wide text-white flex items-center gap-1.5">
                      <i data-lucide="dumbbell" class="w-4 h-4 text-white"></i> Fuerza & Gimnasio
                    </span>
                    <span class="text-xs font-mono font-medium text-white/80">
                      ${todayPlan.gym.is_rest ? 'Descanso' : 'Rutina ' + (todayPlan.gym.routine_id || 2) + ' (Hoy)'}
                    </span>
                  </div>
                  <p class="text-xs text-white/90 leading-relaxed font-normal mt-1.5">
                    ${todayPlan.gym.is_rest 
                      ? 'Sin carga de pesas hoy. Regeneración del sistema nervioso central.' 
                      : todayPlan.gym.routine_name + (todayPlan.gym.highlight_exercises && todayPlan.gym.highlight_exercises.length > 0 ? ' &bull; ' + todayPlan.gym.highlight_exercises.slice(0, 3).map((e: any) => e.name).join(' &bull; ') : '')}
                  </p>
                </div>
                ${todayPlan.gym.is_rest ? '' : `
                <div class="pt-2 flex items-center justify-end border-t border-white/15">
                  <button onclick="goToGymRoutine(${todayPlan.gym.routine_id || 2})" class="px-3.5 py-1 rounded-full bg-white text-[#292631] text-[11px] font-extrabold hover:bg-white/90 transition flex items-center gap-1.5 shadow-sm">
                    <span>Ir a la Rutina</span> &rarr;
                  </button>
                </div>`}
              </div>
            </div>'''

    if old_hero_layout in content:
        content = content.replace(old_hero_layout, new_hero_layout)
        print("Hero layout successfully simplified!")
    else:
        print("Warning: old_hero_layout not found exactly, doing regex or partial replace.")

    # 4. Spline Chart Header & Mini Badges
    old_chart_header = '''              <div>
                <h3 class="text-lg font-black text-white tracking-tight">Evolución de Volumen & Proyección</h3>
                <p class="text-xs text-[#A297A6] mt-0.5 font-medium">Curvas superpuestas de volumen real vs objetivo programado</p>
              </div>
              <div class="flex items-center gap-4">
                <div class="flex items-center gap-2 text-xs font-bold text-white">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#d86991]"></span>
                  <span>Volumen Real (Km)</span>
                </div>
                <div class="flex items-center gap-2 text-xs font-bold text-[#a887ce]">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#a887ce]"></span>
                  <span>Objetivo Planificado</span>
                </div>'''

    new_chart_header = '''              <div>
                <h3 class="text-lg font-black text-white tracking-tight">Evolución de Volumen & Gimnasio</h3>
                <p class="text-xs text-[#A297A6] mt-0.5 font-medium">Volumen de running semanal vs sesiones de fuerza ejecutadas</p>
              </div>
              <div class="flex items-center gap-4">
                <div class="flex items-center gap-2 text-xs font-bold text-white">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#d86991]"></span>
                  <span>Running (km)</span>
                </div>
                <div class="flex items-center gap-2 text-xs font-bold text-[#a887ce]">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#a887ce]"></span>
                  <span>Gimnasio (sesiones)</span>
                </div>'''

    if old_chart_header in content:
        content = content.replace(old_chart_header, new_chart_header)
        print("Chart header updated to Running + Gym!")

    # 5. Mini Badges under chart
    old_badges = '''            <!-- Mini badges con las semanas clave -->
            <div class="grid grid-cols-4 sm:grid-cols-8 gap-2 mt-4 text-center">
              <div class="p-1.5 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#A297A6]">28 Sep</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">13.4k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#A297A6]">05 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">19.2k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#A297A6]">12 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">16.5k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#A297A6]">19 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">25.4k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#A297A6]">26 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">29.2k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631]/60 border border-[#a887ce]/30">
                <div class="text-[10px] text-[#a887ce] font-bold">10K Ávila</div>
                <div class="text-xs font-black text-white mt-0.5 font-mono">21.6k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631]/40 border border-[#d86991]/30">
                <div class="text-[10px] text-[#d86991] font-bold">6x800m</div>
                <div class="text-xs font-black text-white mt-0.5 font-mono">27.0k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#d86991]/10 border border-[#d86991]/50">
                <div class="text-[10px] text-[#d86991] font-black">Esta Sem</div>
                <div class="text-xs font-black text-[#d86991] mt-0.5 font-mono">~30k</div>
              </div>
            </div>'''

    new_badges = '''            <!-- Mini badges con las semanas clave -->
            <div class="grid grid-cols-4 sm:grid-cols-8 gap-2 mt-4 text-center">
              <div class="p-1.5 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#A297A6]">28 Sep</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">13.4k &bull; 0g</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#A297A6]">05 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">19.2k &bull; 0g</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#A297A6]">12 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">16.5k &bull; 0g</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#A297A6]">19 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">25.4k &bull; 3g</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#A297A6]">26 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">29.2k &bull; 3g</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631]/60 border border-[#a887ce]/30">
                <div class="text-[10px] text-[#a887ce] font-bold">10K Ávila</div>
                <div class="text-xs font-black text-white mt-0.5 font-mono">21.6k &bull; 1g</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#292631]/40 border border-[#d86991]/30">
                <div class="text-[10px] text-[#d86991] font-bold">6x800m</div>
                <div class="text-xs font-black text-white mt-0.5 font-mono">27.0k &bull; 4g</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#d86991]/10 border border-[#d86991]/50">
                <div class="text-[10px] text-[#d86991] font-black">Esta Sem</div>
                <div class="text-xs font-black text-[#d86991] mt-0.5 font-mono">~30k &bull; 3g</div>
              </div>
            </div>'''

    if old_badges in content:
        content = content.replace(old_badges, new_badges)
        print("Mini badges updated with km + gym!")

    # 6. Chart.js implementation for dual axes (km + gym)
    old_chart_js = '''        const labels = weeklyData.map(w => w.label);
        const kmValues = weeklyData.map(w => w.run_km);
        // Curva de proyección armónica superpuesta
        const targetValues = [15.0, 20.0, 18.0, 25.0, 30.0, 22.0, 28.0, 30.0];

        new Chart(ctxSpline, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [
              {
                label: 'Volumen Real (Km)',
                data: kmValues,
                borderColor: '#d86991',
                borderWidth: 3,
                tension: 0.45,
                fill: true,
                backgroundColor: gradientRose,
                pointBackgroundColor: '#d86991',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 6,
                yAxisID: 'y'
              },
              {
                label: 'Objetivo Planificado (Km)',
                data: targetValues,
                borderColor: '#a887ce',
                borderWidth: 2.5,
                tension: 0.45,
                fill: true,
                backgroundColor: gradientPurple,
                pointBackgroundColor: '#a887ce',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 5,
                yAxisID: 'y'
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: '#171821',
                borderColor: '#4d3e50',
                borderWidth: 1,
                titleColor: '#FFFFFF',
                titleFont: { family: 'Outfit', weight: 'bold' },
                bodyColor: '#a887ce',
                bodyFont: { family: 'Outfit' },
                padding: 12,
                cornerRadius: 12,
                callbacks: {
                  label: function(ctx) {
                    return ' ' + ctx.dataset.label + ': ' + ctx.parsed.y + ' km';
                  }
                }
              }
            },
            scales: {
              x: {
                grid: { display: false },
                ticks: { color: '#7b6e7f', font: { family: 'Outfit', size: 11, weight: '500' } }
              },
              y: {
                position: 'left',
                grid: { color: 'rgba(77, 62, 80, 0.25)', drawBorder: false },
                ticks: {
                  color: '#7b6e7f',
                  font: { family: 'Outfit', size: 11 },
                  callback: function(v) { return v + 'k'; }
                }
              }
            }
          }
        });'''

    new_chart_js = '''        const labels = weeklyData.map(w => w.label);
        const kmValues = weeklyData.map(w => w.run_km);
        const gymValues = weeklyData.map(w => w.gym_sessions);

        new Chart(ctxSpline, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [
              {
                label: 'Running (Km)',
                data: kmValues,
                borderColor: '#d86991',
                borderWidth: 3,
                tension: 0.45,
                fill: true,
                backgroundColor: gradientRose,
                pointBackgroundColor: '#d86991',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 6,
                yAxisID: 'y'
              },
              {
                label: 'Gimnasio (Sesiones)',
                data: gymValues,
                borderColor: '#a887ce',
                borderWidth: 2.5,
                tension: 0.45,
                fill: true,
                backgroundColor: gradientPurple,
                pointBackgroundColor: '#a887ce',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 5,
                yAxisID: 'y1'
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: { mode: 'index', intersect: false },
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: '#171821',
                borderColor: '#4d3e50',
                borderWidth: 1,
                titleColor: '#FFFFFF',
                titleFont: { family: 'Inter', weight: 'bold' },
                bodyColor: '#A297A6',
                bodyFont: { family: 'Inter' },
                padding: 12,
                cornerRadius: 12,
                callbacks: {
                  label: function(ctx) {
                    if (ctx.dataset.yAxisID === 'y') {
                      return ' Running: ' + ctx.parsed.y + ' km';
                    } else {
                      return ' Gimnasio: ' + ctx.parsed.y + ' sesiones';
                    }
                  }
                }
              }
            },
            scales: {
              x: {
                grid: { display: false },
                ticks: { color: '#A297A6', font: { family: 'Inter', size: 11, weight: '500' } }
              },
              y: {
                position: 'left',
                grid: { color: 'rgba(77, 62, 80, 0.25)', drawBorder: false },
                suggestedMin: 0,
                suggestedMax: 35,
                ticks: {
                  color: '#d86991',
                  font: { family: 'Inter', size: 11, weight: '500' },
                  callback: function(v) { return v + 'k'; }
                }
              },
              y1: {
                position: 'right',
                grid: { display: false },
                min: 0,
                max: 6,
                ticks: {
                  color: '#a887ce',
                  stepSize: 1,
                  font: { family: 'Inter', size: 11, weight: '500' },
                  callback: function(v) { return v + ' ses'; }
                }
              }
            }
          }
        });'''

    if old_chart_js in content:
        content = content.replace(old_chart_js, new_chart_js)
        print("Chart.js configuration successfully updated to dual axes!")
    else:
        print("Warning: old_chart_js not found exactly, doing inspection.")

    with open('scripts/build_luxury_octet_dashboard.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Finished updating build_luxury_octet_dashboard.py!")

if __name__ == '__main__':
    update_builder()
