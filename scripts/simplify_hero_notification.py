def update_hero():
    with open('scripts/build_luxury_octet_dashboard.py', 'r', encoding='utf-8') as f:
        content = f.read()

    old_hero = '''          <!-- 1. BLOQUE SESIÓN DE HOY (DEGRADADO DE ALTA GAMA RESTAURADO) -->
          <div class="hero-gradient-card p-5 sm:p-7 text-white space-y-4 relative overflow-hidden">

            <!-- Header de la tarjeta -->
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
            </div>

            <!-- Botones Rápidos de la Tarjeta Hero -->
            <div class="flex flex-wrap items-center gap-3 pt-1 relative z-10">
              <button onclick="switchTab('workouts')" class="px-5 py-2.5 rounded-full bg-white text-[#292631] font-black text-xs hover:bg-white/90 transition shadow-lg flex items-center gap-2">
                <span>Ver Entrenos</span>
                <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
              </button>
              <button onclick="switchTab('gym')" class="px-5 py-2.5 rounded-full bg-[#171821]/45 hover:bg-[#171821]/65 text-white font-bold text-xs border border-white/25 backdrop-blur-md transition flex items-center gap-2">
                <i data-lucide="clipboard-pen" class="w-3.5 h-3.5"></i>
                <span>Registrar Gym</span>
              </button>
            </div>
          </div>'''

    new_hero = '''          <!-- 1. BLOQUE SESIÓN DE HOY (NOTIFICACIÓN MINIMALISTA & IMPACTANTE) -->
          <div class="hero-gradient-card p-4 sm:p-5 text-white relative overflow-hidden">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
              
              <!-- Contenido Conciso: Qué toca entrenar hoy -->
              <div class="space-y-2.5">
                <!-- Tag Hoy + Nombre Sesión Principal -->
                <div class="flex flex-wrap items-center gap-2">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full bg-black/30 backdrop-blur-md border border-white/20 text-[11px] font-black uppercase tracking-wider text-white">
                    HOY &bull; ${todayPlan.day_name.toUpperCase()} ${todayPlan.date}
                  </span>
                  <span class="text-sm sm:text-base font-black text-white tracking-tight">
                    ${todayPlan.running.title}
                  </span>
                </div>

                <!-- Detalle Rápido con Iconos: Carrera + Fuerza -->
                <div class="flex flex-wrap items-center gap-2.5 sm:gap-3 text-xs sm:text-sm font-semibold text-white/95">
                  <!-- Carrera -->
                  <div class="flex items-center gap-2 bg-black/25 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/10 shadow-sm">
                    <i data-lucide="footprints" class="w-4 h-4 text-white"></i>
                    <span>
                      ${todayPlan.running.is_rest 
                        ? 'Descanso de carrera' 
                        : `${todayPlan.running.duration_min} min &bull; ${todayPlan.running.target_pace} &bull; ${todayPlan.running.hr_zone}`}
                    </span>
                  </div>

                  <!-- Separador sutil -->
                  <span class="hidden sm:inline text-white/40 font-bold">&bull;</span>

                  <!-- Fuerza -->
                  <div class="flex items-center gap-2 bg-black/25 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/10 shadow-sm">
                    <i data-lucide="dumbbell" class="w-4 h-4 text-white"></i>
                    <span>
                      ${todayPlan.gym.is_rest 
                        ? 'Descanso de fuerza' 
                        : 'Fuerza: ' + (todayPlan.gym.routine_name ? (todayPlan.gym.routine_name.includes('·') ? todayPlan.gym.routine_name.split('·')[1].split('(')[0].trim() : todayPlan.gym.routine_name) : 'Torso Tracción')}
                    </span>
                  </div>
                </div>
              </div>

              <!-- Botón Único de Acción: Lleva al entreno detallado -->
              <div class="flex items-center shrink-0 pt-1 md:pt-0">
                <button onclick="goToTodayWorkout()" class="w-full md:w-auto px-5 py-2.5 rounded-full bg-white text-[#171821] font-black text-xs hover:bg-white/90 transition shadow-lg flex items-center justify-center gap-2">
                  <span>Ver Entreno</span>
                  <i data-lucide="arrow-right" class="w-3.5 h-3.5"></i>
                </button>
              </div>

            </div>
          </div>'''

    if old_hero in content:
        content = content.replace(old_hero, new_hero)
        print("Hero card successfully replaced with minimalist notification block!")
    else:
        print("Error: old_hero not found exactly!")
        return False

    # Add goToTodayWorkout function if not present
    if 'function goToTodayWorkout' not in content:
        content = content.replace(
            'function goToGymRoutine(routineId) {',
            '''function goToTodayWorkout() {
      switchTab('workouts');
      if (typeof selectCalendarDay === 'function') {
        selectCalendarDay(todayISO || '2026-11-16');
      }
      setTimeout(() => {
        const detailEl = document.getElementById('calendar-day-detail');
        if (detailEl) {
          detailEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 150);
    }

    function goToGymRoutine(routineId) {'''
        )
        print("goToTodayWorkout function added!")

    with open('scripts/build_luxury_octet_dashboard.py', 'w', encoding='utf-8') as f:
        f.write(content)
    return True

if __name__ == '__main__':
    update_hero()
