def finish_updates():
    with open('scripts/build_luxury_octet_dashboard.py', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update CSS
    old_css_block = '''    /* Tarjetas de lujo con degradado vertical sutil de Jaguar a sombra oscura */
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

    new_css_block = '''    /* Tarjetas de lujo con degradado ambiental y resplandor superior (Estilo Referencia Octet / Dribbble) */
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

    if old_css_block in content:
        content = content.replace(old_css_block, new_css_block)
        print("CSS block updated successfully!")
    else:
        print("Error: old_css_block not found!")

    # 2. Update body background image
    old_body_bg = '''    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      letter-spacing: -0.011em;
      background-color: #171821;
      color: #FFFFFF;
      -webkit-font-smoothing: antialiased;
    }'''

    new_body_bg = '''    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      letter-spacing: -0.011em;
      background-color: #171821;
      background-image: 
        radial-gradient(circle at 85% 5%, rgba(156, 82, 109, 0.16) 0%, transparent 45%),
        radial-gradient(circle at 15% 45%, rgba(168, 135, 206, 0.10) 0%, transparent 45%);
      color: #FFFFFF;
      -webkit-font-smoothing: antialiased;
    }'''

    if old_body_bg in content:
        content = content.replace(old_body_bg, new_body_bg)
        print("Body background updated with ambient lights!")
    else:
        print("Error: old_body_bg not found!")

    # 3. Update Chart.js code
    old_chart_js = '''      // Gráfico Spline con Áreas Superpuestas Rellenas (Estilo Octet Interactive Dashboards)
      const ctxSpline = document.getElementById('weeklySplineChart')?.getContext('2d');
      if (ctxSpline) {
        // Degradado leve Rosa/Mulberry para Volumen Real
        const gradientRose = ctxSpline.createLinearGradient(0, 0, 0, 260);
        gradientRose.addColorStop(0, 'rgba(216, 105, 145, 0.50)');
        gradientRose.addColorStop(0.5, 'rgba(216, 105, 145, 0.16)');
        gradientRose.addColorStop(1, 'rgba(216, 105, 145, 0.0)');

        // Degradado leve Púrpura/Lavanda para Objetivo/Proyección
        const gradientPurple = ctxSpline.createLinearGradient(0, 0, 0, 260);
        gradientPurple.addColorStop(0, 'rgba(168, 135, 206, 0.42)');
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

    new_chart_js = '''      // Gráfico Spline con Áreas Superpuestas Rellenas con Colores Potentes (Estilo Referencia media_1794822984640_6116ce9d.png)
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

    if old_chart_js in content:
        content = content.replace(old_chart_js, new_chart_js)
        print("Chart.js upgraded with vivid colors, exact areas and syncDynamicMetrics!")
    else:
        print("Error: old_chart_js not found!")

    with open('scripts/build_luxury_octet_dashboard.py', 'w', encoding='utf-8') as f:
        f.write(content)

    print("Finished finish_v8_design.py!")

if __name__ == '__main__':
    finish_updates()
