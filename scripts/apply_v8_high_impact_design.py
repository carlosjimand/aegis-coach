import re

def update_all():
    with open('scripts/build_luxury_octet_dashboard.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS in :root and body
    old_css_root = ''':root {
      /* Paleta Oficial Octet Interactive Dashboards */
      --river-styx: #171821;        /* Fondo base */
      --jaguar: #292631;            /* Superficie de tarjetas */
      --stone-violet: #4d3e50;      /* Bordes y divisores */
      --composers-magic: #A297A6;   /* Texto secundario / legible (>5:1 contraste) */
      --mulberry-mix: #9c526d;      /* Acento primario magenta / rosa */
      --middys-purple: #a887ce;     /* Acento lavanda / púrpura brillante */
      --vibrant-rose: #d86991;      /* Acento rosa vibrante curvas */

      --bg-dark: var(--river-styx);
      --card-dark: var(--jaguar);
      --card-border: var(--stone-violet);
      --accent-pink: var(--vibrant-rose);
      --accent-blue: var(--middys-purple);
      --accent-green: #62a87c;
      --text-muted: var(--composers-magic);
    }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      letter-spacing: -0.011em;
      background-color: #171821;
      color: #FFFFFF;
      -webkit-font-smoothing: antialiased;
    }
    h1, h2, h3, h4, h5, h6, p, span, button, input, div {
      font-family: 'Inter', sans-serif;
    }
    .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }
    /* Tarjetas de lujo con degradado vertical sutil de Jaguar a sombra oscura */
    .luxury-card {
      background: linear-gradient(180deg, #2b2735 0%, #22202a 100%);
      border: 1px solid rgba(77, 62, 80, 0.45);
      border-radius: 1.5rem;
      position: relative;
    }
    .luxury-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent 0%, rgba(168, 135, 206, 0.20) 50%, transparent 100%);
      pointer-events: none;
    }
    /* Hero Card Estilo "Balance" (Degradado Suave Lavanda-Mulberry con Ondas Guilloche) */
    .hero-gradient-card {
      background: linear-gradient(135deg, #a887ce 0%, #a272a4 40%, #9c526d 100%);
      box-shadow: 0 18px 38px -10px rgba(168, 135, 206, 0.38);
      border-radius: 1.75rem;
      position: relative;
      overflow: hidden;
    }'''

    new_css_root = ''':root {
      /* Paleta Oficial Octet Interactive Dashboards & Luxury Fintech */
      --river-styx: #171821;        /* Fondo base ultra oscuro */
      --jaguar: #21222d;            /* Superficie de tarjetas luxury */
      --stone-violet: #4d3e50;      /* Bordes y divisores */
      --composers-magic: #A297A6;   /* Texto secundario / legible */
      --mulberry-mix: #9c526d;      /* Acento primario magenta / rosa */
      --middys-purple: #a887ce;     /* Acento lavanda / púrpura brillante */
      --vibrant-rose: #fa769e;      /* Acento rosa eléctrico idéntico a referencia */
      --periwinkle-blue: #9ca8f3;   /* Acento azul lavanda Investment */

      --bg-dark: var(--river-styx);
      --card-dark: var(--jaguar);
      --card-border: var(--stone-violet);
      --accent-pink: var(--vibrant-rose);
      --accent-blue: var(--periwinkle-blue);
      --accent-green: #54D68A;
      --text-muted: var(--composers-magic);
    }
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      letter-spacing: -0.011em;
      background-color: #171821;
      background-image: 
        radial-gradient(circle at 85% 5%, rgba(156, 82, 109, 0.16) 0%, transparent 45%),
        radial-gradient(circle at 15% 45%, rgba(168, 135, 206, 0.10) 0%, transparent 45%);
      color: #FFFFFF;
      -webkit-font-smoothing: antialiased;
    }
    h1, h2, h3, h4, h5, h6, p, span, button, input, div {
      font-family: 'Inter', sans-serif;
    }
    .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }
    /* Tarjetas de lujo con degradado ambiental y resplandor superior (Estilo Referencia Octet / Dribbble) */
    .luxury-card {
      background: radial-gradient(circle at 88% 15%, rgba(156, 82, 109, 0.20) 0%, rgba(33, 34, 45, 0) 58%), #21222d;
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 1.75rem;
      box-shadow: 0 16px 36px -12px rgba(0, 0, 0, 0.45);
      position: relative;
      overflow: hidden;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .luxury-card:hover {
      border-color: rgba(168, 135, 206, 0.28);
      transform: translateY(-2px);
    }
    .luxury-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.12) 50%, transparent 100%);
      pointer-events: none;
    }
    /* Tarjeta KPI Estilo "Investment" (Resplandor Azul Periwinkle / Lavanda) */
    .luxury-card-glow-blue {
      background: radial-gradient(circle at 88% 15%, rgba(151, 168, 255, 0.18) 0%, rgba(33, 34, 45, 0) 55%), #21222d;
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 1.75rem;
      box-shadow: 0 16px 36px -12px rgba(0, 0, 0, 0.45);
      position: relative;
      overflow: hidden;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .luxury-card-glow-blue:hover {
      border-color: rgba(151, 168, 255, 0.35);
      transform: translateY(-2px);
    }
    .luxury-card-glow-blue::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent 0%, rgba(151, 168, 255, 0.30) 50%, transparent 100%);
      pointer-events: none;
    }
    /* Tarjeta KPI Estilo "Deposit" (Resplandor Rosa / Mulberry) */
    .luxury-card-glow-pink {
      background: radial-gradient(circle at 88% 15%, rgba(250, 118, 158, 0.22) 0%, rgba(33, 34, 45, 0) 55%), #21222d;
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 1.75rem;
      box-shadow: 0 16px 36px -12px rgba(0, 0, 0, 0.45);
      position: relative;
      overflow: hidden;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .luxury-card-glow-pink:hover {
      border-color: rgba(250, 118, 158, 0.35);
      transform: translateY(-2px);
    }
    .luxury-card-glow-pink::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent 0%, rgba(250, 118, 158, 0.35) 50%, transparent 100%);
      pointer-events: none;
    }
    /* Hero Card Estilo "Balance" Lujoso */
    .hero-gradient-card {
      background: linear-gradient(135deg, #a887ce 0%, #b86fa2 45%, #fa769e 100%);
      box-shadow: 0 20px 45px -10px rgba(250, 118, 158, 0.35), 0 10px 25px -8px rgba(168, 135, 206, 0.35);
      border-radius: 1.75rem;
      position: relative;
      overflow: hidden;
    }
    .hero-gradient-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      right: 0;
      height: 1px;
      background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.40) 50%, transparent 100%);
      pointer-events: none;
    }'''

    if old_css_root in content:
        content = content.replace(old_css_root, new_css_root)
        print("CSS classes successfully upgraded with ambient lighting & glow!")
    else:
        print("Warning: old_css_root not matched exactly!")

    # 2. Replace 3 KPI cards with Investment & Deposit styles (Horizontal bars)
    old_kpi_section = '''          <!-- 2. TRES KPIS PRINCIPALES (CON ANILLOS RADIALES ESTILO OCTET) -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
            <!-- KPI 1: Volumen Semanal Run -->
            <div class="luxury-card p-6 flex flex-col justify-between">
              <div class="flex items-center justify-between">
                <div>
                  <span class="text-xs font-bold text-[#A297A6] uppercase tracking-wider">Volumen Semanal</span>
                  <div class="flex items-baseline gap-1.5 mt-2">
                    <span class="text-3xl sm:text-4xl font-extrabold text-white font-mono">27.0</span>
                    <span class="text-xs text-[#A297A6] font-bold">km</span>
                  </div>
                </div>
                <!-- Anillo Radial 90% Rosa/Mulberry -->
                <div class="relative w-12 h-12 flex items-center justify-center shrink-0">
                  <svg class="w-12 h-12 transform -rotate-90" viewBox="0 0 36 36">
                    <path class="text-[#4d3e50]/40" stroke-width="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                    <path class="text-[#d86991]" stroke-dasharray="90, 100" stroke-width="3.2" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                  </svg>
                  <span class="absolute text-[10px] font-black text-white font-mono">90%</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-[#4d3e50]/40 flex items-center justify-between text-xs">
                <span class="text-[#A297A6]">Meta Semanal: 30 km</span>
                <span class="text-[#d86991] font-bold flex items-center gap-1">
                  <i data-lucide="trending-up" class="w-3.5 h-3.5"></i> +5.4 km vs sem ant
                </span>
              </div>
            </div>

            <!-- KPI 2: Sesiones de Fuerza -->
            <div class="luxury-card p-6 flex flex-col justify-between">
              <div class="flex items-center justify-between">
                <div>
                  <span class="text-xs font-bold text-[#A297A6] uppercase tracking-wider">Sesiones de Fuerza</span>
                  <div class="flex items-baseline gap-1.5 mt-2">
                    <span class="text-3xl sm:text-4xl font-extrabold text-white font-mono">4</span>
                    <span class="text-xs text-[#A297A6] font-bold">/ 4 días</span>
                  </div>
                </div>
                <!-- Anillo Radial 100% Púrpura -->
                <div class="relative w-12 h-12 flex items-center justify-center shrink-0">
                  <svg class="w-12 h-12 transform -rotate-90" viewBox="0 0 36 36">
                    <path class="text-[#4d3e50]/40" stroke-width="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                    <path class="text-[#a887ce]" stroke-dasharray="100, 100" stroke-width="3.2" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                  </svg>
                  <span class="absolute text-[10px] font-black text-white font-mono">100%</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-[#4d3e50]/40 flex items-center justify-between text-xs">
                <span class="text-[#A297A6]">Planificación PDF</span>
                <span class="text-[#a887ce] font-bold flex items-center gap-1">
                  <i data-lucide="check-circle" class="w-3.5 h-3.5"></i> Blindaje Activo
                </span>
              </div>
            </div>

            <!-- KPI 3: Estado de Forma TSB / CTL -->
            <div class="luxury-card p-6 flex flex-col justify-between">
              <div class="flex items-center justify-between">
                <div>
                  <span class="text-xs font-bold text-[#A297A6] uppercase tracking-wider">Estado de Forma (TSB)</span>
                  <div class="flex items-baseline gap-1.5 mt-2">
                    <span class="text-3xl sm:text-4xl font-extrabold text-white font-mono">-9.5</span>
                    <span class="text-xs text-[#A297A6] font-mono font-bold">CTL 16.1</span>
                  </div>
                </div>
                <!-- Anillo Radial 75% Mulberry Mix -->
                <div class="relative w-12 h-12 flex items-center justify-center shrink-0">
                  <svg class="w-12 h-12 transform -rotate-90" viewBox="0 0 36 36">
                    <path class="text-[#4d3e50]/40" stroke-width="3" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                    <path class="text-[#9c526d]" stroke-dasharray="75, 100" stroke-width="3.2" stroke-linecap="round" stroke="currentColor" fill="none" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" />
                  </svg>
                  <span class="absolute text-[10px] font-black text-white font-mono">ATL 25</span>
                </div>
              </div>
              <div class="mt-4 pt-3 border-t border-[#4d3e50]/40 flex items-center justify-between text-xs">
                <span class="text-[#A297A6]">Carga Aguda Controlada</span>
                <span class="text-[#9c526d] font-bold flex items-center gap-1">
                  <i data-lucide="activity" class="w-3.5 h-3.5"></i> Tapering Cross
                </span>
              </div>
            </div>
          </div>'''

    new_kpi_section = '''          <!-- 2. TRES KPIS PRINCIPALES (ESTILO REFERENCIA INVESTMENT & DEPOSIT CON BARRA HORIZONTAL) -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
            <!-- KPI 1: Volumen Semanal (Estilo Investment: Periwinkle Blue #9ca8f3) -->
            <div class="luxury-card-glow-blue p-5 sm:p-6 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between">
                  <span class="text-xs sm:text-sm font-semibold text-[#A297A6] tracking-tight">Volumen Semanal</span>
                  <i data-lucide="trending-up" class="w-4 h-4 text-[#7A7585]"></i>
                </div>
                <div class="flex items-baseline justify-between mt-3">
                  <div class="flex items-baseline gap-1.5">
                    <span id="kpi-run-km" class="text-3xl sm:text-4xl font-black text-white tracking-tight font-mono">27.0</span>
                    <span class="text-xs font-bold text-[#A297A6]">km</span>
                  </div>
                  <span id="kpi-run-badge" class="text-xs font-bold text-[#54D68A]">+5.4k (90%)</span>
                </div>
              </div>
              <div class="mt-4 pt-1">
                <!-- Barra de progreso horizontal idéntica a Investment -->
                <div class="h-2 w-full rounded-full bg-[#181622] overflow-hidden">
                  <div id="kpi-run-bar" class="h-full rounded-full bg-[#9ca8f3] shadow-[0_0_12px_rgba(156,168,243,0.5)] transition-all duration-500" style="width: 90%;"></div>
                </div>
              </div>
            </div>

            <!-- KPI 2: Sesiones de Fuerza (Estilo Deposit: Candy Rose #fa769e) -->
            <div class="luxury-card-glow-pink p-5 sm:p-6 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between">
                  <span class="text-xs sm:text-sm font-semibold text-[#A297A6] tracking-tight">Sesiones de Fuerza</span>
                  <i data-lucide="trending-up" class="w-4 h-4 text-[#7A7585]"></i>
                </div>
                <div class="flex items-baseline justify-between mt-3">
                  <div class="flex items-baseline gap-1.5">
                    <span id="kpi-gym-sessions" class="text-3xl sm:text-4xl font-black text-white tracking-tight font-mono">4</span>
                    <span class="text-xs font-bold text-[#A297A6]">/ 4 días</span>
                  </div>
                  <span id="kpi-gym-badge" class="text-xs font-bold text-[#54D68A]">100% (Blindaje)</span>
                </div>
              </div>
              <div class="mt-4 pt-1">
                <!-- Barra de progreso horizontal idéntica a Deposit -->
                <div class="h-2 w-full rounded-full bg-[#181622] overflow-hidden">
                  <div id="kpi-gym-bar" class="h-full rounded-full bg-[#fa769e] shadow-[0_0_12px_rgba(250,118,158,0.5)] transition-all duration-500" style="width: 100%;"></div>
                </div>
              </div>
            </div>

            <!-- KPI 3: Estado de Forma TSB (Estilo Gradiente Lavanda-Mulberry) -->
            <div class="luxury-card p-5 sm:p-6 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between">
                  <span class="text-xs sm:text-sm font-semibold text-[#A297A6] tracking-tight">Estado de Forma (TSB)</span>
                  <i data-lucide="trending-up" class="w-4 h-4 text-[#7A7585]"></i>
                </div>
                <div class="flex items-baseline justify-between mt-3">
                  <div class="flex items-baseline gap-1.5">
                    <span id="kpi-tsb-val" class="text-3xl sm:text-4xl font-black text-white tracking-tight font-mono">-9.5</span>
                    <span class="text-xs font-bold text-[#A297A6]">TSB</span>
                  </div>
                  <span id="kpi-tsb-badge" class="text-xs font-bold text-[#a887ce]">CTL 16.1 (ATL 25)</span>
                </div>
              </div>
              <div class="mt-4 pt-1">
                <!-- Barra de progreso horizontal degradada -->
                <div class="h-2 w-full rounded-full bg-[#181622] overflow-hidden">
                  <div id="kpi-tsb-bar" class="h-full rounded-full bg-gradient-to-r from-[#a887ce] to-[#fa769e] shadow-[0_0_12px_rgba(168,135,206,0.4)] transition-all duration-500" style="width: 75%;"></div>
                </div>
              </div>
            </div>
          </div>'''

    if old_kpi_section in content:
        content = content.replace(old_kpi_section, new_kpi_section)
        print("KPI section successfully replaced with Investment & Deposit horizontal bar cards!")
    else:
        print("Warning: old_kpi_section not matched!")

    # 3. Spline Chart Card Container & Header (styled like reference image media_1794822984640_6116ce9d.png)
    old_chart_card_start = '''          <!-- 3. GRÁFICO SPLINE DE EVOLUCIÓN DE VOLUMEN SEMANAL (KM REALES) -->
          <div class="luxury-card p-6 sm:p-8">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
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
                </div>
                <span class="hidden sm:inline-block px-3 py-1 rounded-xl bg-[#171821] border border-[#4d3e50]/50 text-xs text-[#A297A6] font-mono">
                  Últimas 8 semanas
                </span>
              </div>
            </div>'''

    new_chart_card_start = '''          <!-- 3. GRÁFICO SPLINE DE EVOLUCIÓN DE VOLUMEN SEMANAL (KM REALES & GIMNASIO - ESTILO REFERENCIA EXACTO) -->
          <div class="luxury-card-glow-pink p-6 sm:p-8">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-5">
              <div class="flex items-center gap-5">
                <div class="flex items-center gap-2 text-xs sm:text-sm font-semibold text-white">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#fa769e] shadow-[0_0_8px_#fa769e]"></span>
                  <span>Running (km)</span>
                </div>
                <div class="flex items-center gap-2 text-xs sm:text-sm font-semibold text-[#97a8ff]">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#97a8ff] shadow-[0_0_8px_#97a8ff]"></span>
                  <span>Gimnasio (sesiones)</span>
                </div>
              </div>
              <!-- Botón selector idéntico al 'Last week ∨' de la referencia -->
              <div class="flex items-center gap-2">
                <div class="px-3.5 py-1.5 rounded-xl bg-[#171821]/80 border border-white/10 text-xs font-semibold text-[#A297A6] flex items-center gap-1.5 shadow-sm">
                  <span>Últimas 8 semanas</span>
                  <i data-lucide="chevron-down" class="w-3.5 h-3.5 text-[#A297A6]"></i>
                </div>
              </div>
            </div>'''

    if old_chart_card_start in content:
        content = content.replace(old_chart_card_start, new_chart_card_start)
        print("Chart card header replaced with exact reference layout!")
    else:
        print("Warning: old_chart_card_start not matched!")

    # 4. Chart.js colors: Vibrant Rose #fa769e and Glowing Blue #97a8ff with intense filled areas
    old_chart_js_snippet = '''      // Gráfico Spline con Áreas Superpuestas Rellenas (Estilo Octet Interactive Dashboards)
      const ctxSpline = document.getElementById('weeklySplineChart')?.getContext('2d');
      if (ctxSpline) {
        // Degradado leve Rosa/Mulberry para Running (Km)
        const gradientRose = ctxSpline.createLinearGradient(0, 0, 0, 260);
        gradientRose.addColorStop(0, 'rgba(216, 105, 145, 0.48)');
        gradientRose.addColorStop(0.5, 'rgba(216, 105, 145, 0.16)');
        gradientRose.addColorStop(1, 'rgba(216, 105, 145, 0.0)');

        // Degradado leve Púrpura/Lavanda para Gimnasio (Sesiones)
        const gradientPurple = ctxSpline.createLinearGradient(0, 0, 0, 260);
        gradientPurple.addColorStop(0, 'rgba(168, 135, 206, 0.40)');
        gradientPurple.addColorStop(0.5, 'rgba(168, 135, 206, 0.12)');
        gradientPurple.addColorStop(1, 'rgba(168, 135, 206, 0.0)');

        const labels = weeklyData.map(w => w.label);
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
        });
      }'''

    new_chart_js_snippet = '''      // Gráfico Spline con Áreas Superpuestas Rellenas con Colores Potentes (Estilo Referencia media_1794822984640_6116ce9d.png)
      const ctxSpline = document.getElementById('weeklySplineChart')?.getContext('2d');
      let weeklySplineChartInstance = null;
      if (ctxSpline) {
        // Degradado Potente Rosa / Candy Rose #fa769e idéntico a la curva "Income" de la referencia
        const gradientRose = ctxSpline.createLinearGradient(0, 0, 0, 280);
        gradientRose.addColorStop(0, 'rgba(250, 118, 158, 0.82)');
        gradientRose.addColorStop(0.35, 'rgba(235, 90, 138, 0.48)');
        gradientRose.addColorStop(0.7, 'rgba(180, 70, 120, 0.18)');
        gradientRose.addColorStop(1, 'rgba(33, 34, 45, 0.0)');

        // Degradado Potente Periwinkle Blue #97a8ff idéntico a la curva "Expense" de la referencia
        const gradientBlue = ctxSpline.createLinearGradient(0, 0, 0, 280);
        gradientBlue.addColorStop(0, 'rgba(151, 168, 255, 0.72)');
        gradientBlue.addColorStop(0.4, 'rgba(130, 145, 235, 0.32)');
        gradientBlue.addColorStop(0.8, 'rgba(90, 105, 190, 0.08)');
        gradientBlue.addColorStop(1, 'rgba(33, 34, 45, 0.0)');

        const labels = weeklyData.map(w => w.label);
        const kmValues = weeklyData.map(w => w.run_km);
        const gymValues = weeklyData.map(w => w.gym_sessions);

        weeklySplineChartInstance = new Chart(ctxSpline, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [
              {
                label: 'Running (Km)',
                data: kmValues,
                borderColor: '#fa769e',
                borderWidth: 3.5,
                tension: 0.45,
                fill: true,
                backgroundColor: gradientRose,
                pointBackgroundColor: '#fa769e',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointRadius: 0,
                pointHoverRadius: 6,
                yAxisID: 'y'
              },
              {
                label: 'Gimnasio (Sesiones)',
                data: gymValues,
                borderColor: '#97a8ff',
                borderWidth: 3.0,
                tension: 0.45,
                fill: true,
                backgroundColor: gradientBlue,
                pointBackgroundColor: '#97a8ff',
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
                borderColor: 'rgba(255, 255, 255, 0.1)',
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
                ticks: { color: '#7A7585', font: { family: 'Inter', size: 11, weight: '500' } }
              },
              y: {
                position: 'left',
                grid: { color: 'rgba(255, 255, 255, 0.04)', drawBorder: false },
                suggestedMin: 0,
                suggestedMax: 35,
                ticks: {
                  color: '#fa769e',
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
                  color: '#97a8ff',
                  stepSize: 1,
                  font: { family: 'Inter', size: 11, weight: '500' },
                  callback: function(v) { return v + ' ses'; }
                }
              }
            }
          }
        });
      }

      // Sincronización Dinámica Reactiva de Métricas de Garmin y Gym
      function syncDynamicMetrics() {
        const curW = weeklyData.find(w => w.week_start === '2026-11-16') || weeklyData[weeklyData.length - 2];
        if (curW) {
          const runKmEl = document.getElementById('kpi-run-km');
          const runBarEl = document.getElementById('kpi-run-bar');
          const runBadgeEl = document.getElementById('kpi-run-badge');
          if (runKmEl) runKmEl.textContent = (curW.run_km || 0).toFixed(1);
          const runPct = Math.min(100, Math.round(((curW.run_km || 0) / 30.0) * 100));
          if (runBarEl) runBarEl.style.width = runPct + '%';
          if (runBadgeEl) runBadgeEl.textContent = '+' + (curW.run_km > 21.6 ? (curW.run_km - 21.6).toFixed(1) + 'k' : '0k') + ' (' + runPct + '%)';

          const gymEl = document.getElementById('kpi-gym-sessions');
          const gymBarEl = document.getElementById('kpi-gym-bar');
          const gymBadgeEl = document.getElementById('kpi-gym-badge');
          if (gymEl) gymEl.textContent = curW.gym_sessions || 0;
          const gymPct = Math.min(100, Math.round(((curW.gym_sessions || 0) / 4.0) * 100));
          if (gymBarEl) gymBarEl.style.width = gymPct + '%';
          if (gymBadgeEl) gymBadgeEl.textContent = gymPct + '% (Blindaje)';

          const tsbEl = document.getElementById('kpi-tsb-val');
          const tsbBarEl = document.getElementById('kpi-tsb-bar');
          const tsbBadgeEl = document.getElementById('kpi-tsb-badge');
          if (tsbEl && curW.tsb !== undefined) tsbEl.textContent = curW.tsb;
          if (tsbBadgeEl && curW.ctl !== undefined) tsbBadgeEl.textContent = 'CTL ' + curW.ctl + ' (ATL ' + (curW.atl || 25) + ')';
          if (tsbBarEl) tsbBarEl.style.width = '75%';
        }
      }
      syncDynamicMetrics();'''

    if old_chart_js_snippet in content:
        content = content.replace(old_chart_js_snippet, new_chart_js_snippet)
        print("Chart.js upgraded with vivid colors, exact areas and syncDynamicMetrics!")
    else:
        print("Warning: old_chart_js_snippet not matched!")

    with open('scripts/build_luxury_octet_dashboard.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Completed v8 high impact updates in build_luxury_octet_dashboard.py!")

if __name__ == '__main__':
    update_all()
