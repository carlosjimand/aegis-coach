# Build and Export All 24 2D Athletic Anatomical Exercises for Aegis Coach
import os
import sys
sys.path.insert(0, os.path.abspath('.'))
import json
from scripts.exercises_r1 import get_r1_exercises
from scripts.exercises_r2 import get_r2_exercises
from scripts.exercises_r3 import get_r3_exercises
from scripts.exercises_r4 import get_r4_exercises

os.makedirs('docs/svg', exist_ok=True)
os.makedirs('cloudflare/src', exist_ok=True)

all_exercises = {}
all_exercises.update(get_r1_exercises())
all_exercises.update(get_r2_exercises())
all_exercises.update(get_r3_exercises())
all_exercises.update(get_r4_exercises())

print(f"Loaded {len(all_exercises)} exercises.")

# 1. Guardar cada archivo SVG individual en docs/svg/
for ex_id, svg_code in all_exercises.items():
    svg_path = f"docs/svg/{ex_id}.svg"
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_code.strip())
print(f"Exported {len(all_exercises)} SVG files to docs/svg/")

# 2. Generar el archivo TypeScript para Cloudflare Workers: cloudflare/src/exercise_illustrations.ts
ts_code = '''// Sistema Visual Anatómico Deportivo 2D para Aegis Coach
// 24 Ejercicios Oficiales en SVG Puro Vectorial de Alta Fidelidad
// Paleta: #05161A (Canvas), #072E33 (Spruce), #0C7075 (Teal Profundo), #0F969C (Luminoso), #6DA5C0 (Cielo), #294D61 (Pizarra)

export const EXERCISE_SVGS: Record<string, string> = {
'''

for ex_id, svg_code in all_exercises.items():
    # Sanitizar y comprimir espacios para TypeScript
    clean_svg = svg_code.strip().replace('\\', '\\\\').replace('`', '\\`').replace('${', '\\${')
    ts_code += f'  "{ex_id}": `{clean_svg}`,\n'

ts_code += '''};

/**
 * Obtiene el SVG correspondiente a una rutina y número de ejercicio.
 * Si no existe, devuelve el SVG de Sentadilla / Hip Thrust por defecto.
 */
export function getExerciseSvg(routineId: number, exerciseNum: number): string {
  const key = `ex_${routineId}_${exerciseNum}`;
  return EXERCISE_SVGS[key] || EXERCISE_SVGS["ex_1_1"] || "";
}

/**
 * Devuelve un Data URI base64 o utf-8 para usar en etiquetas <img> si fuera necesario.
 */
export function getExerciseSvgDataUri(routineId: number, exerciseNum: number): string {
  const svg = getExerciseSvg(routineId, exerciseNum);
  return `data:image/svg+xml;utf8,${encodeURIComponent(svg)}`;
}
'''

with open('cloudflare/src/exercise_illustrations.ts', 'w', encoding='utf-8') as f:
    f.write(ts_code)
print("Generated cloudflare/src/exercise_illustrations.ts successfully!")

# 3. Generar la Galería Interactiva HTML en docs/ejercicios_anatomicos_2d.html
html_gallery = '''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Aegis Coach — Sistema Visual Anatómico Deportivo 2D</title>
<script src="https://cdn.tailwindcss.com"></script>
<style>
  body {
    background-color: #05161A;
    color: #F8FAFC;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
  }
  .card-container {
    background: linear-gradient(135deg, rgba(7, 46, 51, 0.4) 0%, rgba(5, 22, 26, 0.9) 100%);
    border: 1px solid rgba(41, 77, 97, 0.35);
    backdrop-filter: blur(12px);
    transition: all 0.25s ease;
  }
  .card-container:hover {
    border-color: #0F969C;
    box-shadow: 0 10px 30px -10px rgba(15, 150, 156, 0.3);
    transform: translateY(-2px);
  }
  .tab-btn.active {
    background-color: #0F969C;
    color: #05161A;
    font-weight: 700;
  }
</style>
</head>
<body class="p-4 sm:p-8 min-h-screen">
  <div class="max-w-7xl mx-auto">
    <!-- Header -->
    <header class="mb-8 border-b border-[#294D61]/40 pb-6 flex flex-col md:flex-row md:items-center md:justify-between gap-4">
      <div>
        <div class="flex items-center gap-2 mb-2">
          <span class="w-3 h-3 rounded-full bg-[#0F969C] shadow-lg shadow-[#0F969C]/50 animate-pulse"></span>
          <span class="text-xs font-mono font-bold tracking-widest uppercase text-[#6DA5C0]">Aegis Coach &bull; Visual Engine 2D</span>
        </div>
        <h1 class="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">Sistema Visual de Ejercicios Anatómicos 2D</h1>
        <p class="text-sm text-slate-400 mt-1">24 ejercicios oficiales en SVG vectorial de alto rendimiento &bull; Fase Inicial &bull; Contracción &bull; Foco Neuromuscular</p>
      </div>
      <div class="flex items-center gap-3">
        <span class="px-3 py-1.5 rounded-lg bg-[#072E33] border border-[#0F969C]/40 text-[#0F969C] text-xs font-mono font-bold">24 Vectores SVG</span>
        <span class="px-3 py-1.5 rounded-lg bg-[#072E33] border border-[#294D61] text-[#6DA5C0] text-xs font-mono font-bold">Retina Ready</span>
      </div>
    </header>

    <!-- Selector de Rutinas -->
    <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-8">
      <button onclick="filterRoutine(1)" id="tab-1" class="tab-btn active py-3 px-4 rounded-xl text-left border border-[#294D61]/50 bg-[#072E33]/40 text-slate-300 transition">
        <div class="text-[10px] uppercase font-bold text-slate-400">Rutina 1 &bull; Lunes</div>
        <div class="text-xs sm:text-sm font-bold text-white mt-0.5">Pierna 1: Cuádriceps</div>
      </button>
      <button onclick="filterRoutine(2)" id="tab-2" class="tab-btn py-3 px-4 rounded-xl text-left border border-[#294D61]/50 bg-[#072E33]/40 text-slate-300 transition">
        <div class="text-[10px] uppercase font-bold text-slate-400">Rutina 2 &bull; Miércoles</div>
        <div class="text-xs sm:text-sm font-bold text-white mt-0.5">Torso Tracción: Dorsal</div>
      </button>
      <button onclick="filterRoutine(3)" id="tab-3" class="tab-btn py-3 px-4 rounded-xl text-left border border-[#294D61]/50 bg-[#072E33]/40 text-slate-300 transition">
        <div class="text-[10px] uppercase font-bold text-slate-400">Rutina 3 &bull; Jueves/Viernes</div>
        <div class="text-xs sm:text-sm font-bold text-white mt-0.5">Pierna 2: Cadena Posterior</div>
      </button>
      <button onclick="filterRoutine(4)" id="tab-4" class="tab-btn py-3 px-4 rounded-xl text-left border border-[#294D61]/50 bg-[#072E33]/40 text-slate-300 transition">
        <div class="text-[10px] uppercase font-bold text-slate-400">Rutina 4 &bull; Sábado</div>
        <div class="text-xs sm:text-sm font-bold text-white mt-0.5">Torso Empuje: Pecho/Hombro</div>
      </button>
    </div>

    <!-- Grid de Ejercicios -->
    <div id="exercise-grid" class="grid grid-cols-1 md:grid-cols-2 gap-6">
'''

# Añadir las tarjetas con el SVG embebido directamente
for r in range(1, 5):
    for e in range(1, 7):
        ex_id = f"ex_{r}_{e}"
        svg_code = all_exercises.get(ex_id, "")
        html_gallery += f'''
      <div class="exercise-card card-container rounded-2xl p-4 overflow-hidden" data-routine="{r}">
        <div class="flex items-center justify-between mb-3">
          <span class="text-xs font-mono font-bold px-2 py-0.5 rounded bg-[#0F969C]/10 text-[#0F969C] border border-[#0F969C]/30">Rutina {r} &bull; Ejercicio {e}</span>
          <span class="text-xs font-mono text-slate-400">ID: {ex_id}</span>
        </div>
        <div class="w-full rounded-xl overflow-hidden shadow-2xl bg-[#05161A]">
          {svg_code}
        </div>
      </div>
'''

html_gallery += '''
    </div>
  </div>

  <script>
    function filterRoutine(routineId) {
      document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
      document.getElementById('tab-' + routineId)?.classList.add('active');

      document.querySelectorAll('.exercise-card').forEach(card => {
        if (card.getAttribute('data-routine') === String(routineId)) {
          card.classList.remove('hidden');
        } else {
          card.classList.add('hidden');
        }
      });
    }

    // Inicializar mostrando la Rutina 1
    filterRoutine(1);
  </script>
</body>
</html>'''

with open('docs/ejercicios_anatomicos_2d.html', 'w', encoding='utf-8') as f:
    f.write(html_gallery)
print("Generated docs/ejercicios_anatomicos_2d.html successfully!")
