import re

def update_chart():
    with open('scripts/build_luxury_octet_dashboard.py', 'r', encoding='utf-8') as f:
        content = f.read()

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
                titleFont: { family: 'Inter', weight: 'bold' },
                bodyColor: '#a887ce',
                bodyFont: { family: 'Inter' },
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
                ticks: { color: '#7b6e7f', font: { family: 'Inter', size: 11, weight: '500' } }
              },
              y: {
                position: 'left',
                grid: { color: 'rgba(77, 62, 80, 0.25)', drawBorder: false },
                ticks: {
                  color: '#7b6e7f',
                  font: { family: 'Inter', size: 11 },
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
        print("Chart.js successfully updated to dual axes!")
    else:
        print("Error: old_chart_js not matched!")
        return False

    with open('scripts/build_luxury_octet_dashboard.py', 'w', encoding='utf-8') as f:
        f.write(content)
    return True

if __name__ == '__main__':
    update_chart()
