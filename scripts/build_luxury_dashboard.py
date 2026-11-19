import json
import re

print("Generando index.ts con diseño de lujo idéntico a la referencia...")

# Cargar plan maestro
with open('cloudflare/plan.json', 'r', encoding='utf-8') as f:
    plan_json = json.load(f)

# Cargar semanas reales
with open('data/weekly_evolution.json', 'r', encoding='utf-8') as f:
    weekly_evo = json.load(f)

# 8 semanas más relevantes
display_weeks = [w for w in weekly_evo if w['run_km'] > 0 or w['week_start'] >= '2026-09-28']
# añadir proyección semana actual (16 Nov) y semana cross (23 Nov)
display_weeks.append({
    "week_start": "2026-11-16",
    "week_end": "2026-11-22",
    "label": "16 Nov (Hoy)",
    "run_km": 30.0,
    "runs": 4,
    "pace_avg": "4:45/km",
    "gym_sessions": 3,
    "ctl": 16.5,
    "atl": 26.0,
    "tsb": -9.5,
    "is_projected": True
})
display_weeks.append({
    "week_start": "2026-11-23",
    "week_end": "2026-11-29",
    "label": "23 Nov (Cross)",
    "run_km": 20.0,
    "runs": 4,
    "pace_avg": "4:15/km",
    "gym_sessions": 2,
    "ctl": 17.0,
    "atl": 18.0,
    "tsb": -1.0,
    "is_projected": True
})

print(f"Total semanas para el gráfico dinámico: {len(display_weeks)}")

# Construir index.ts completo
daysJsonStr = json.dumps(plan_json['days'], ensure_ascii=False)
weeklyEvoStr = json.dumps(display_weeks, ensure_ascii=False)

worker_ts_content = '''/**
 * Aegis Coach — Sistema de Inteligencia y Coaching de Carlos Jiménez Andrino
 * Cloudflare Worker + Dynamic PWA Dashboard
 * Diseño de Lujo: Dark Slate Obsidian + Neon Coral Pink & Periwinkle Gradients
 */

export interface Env {
  AEGIS_KV: KVNamespace;
  ATHLETE_ID: string;
  INTERVALS_API_KEY: string;
  TELEGRAM_BOT_TOKEN: string;
  TELEGRAM_CHAT_ID: string;
}

function getTodayMadridISO(): string {
  const now = new Date();
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Madrid',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  });
  return formatter.format(now);
}

function calculateDaysRemaining(targetDateISO: string, todayISO: string): number {
  const target = new Date(targetDateISO + 'T00:00:00Z').getTime();
  const today = new Date(todayISO + 'T00:00:00Z').getTime();
  const diffMs = target - today;
  return Math.max(0, Math.ceil(diffMs / (1000 * 60 * 60 * 24)));
}

const DEFAULT_PLAN: any = ''' + json.dumps(plan_json, indent=2, ensure_ascii=False) + ''';

const WEEKLY_EVO_DATA: any = ''' + json.dumps(display_weeks, indent=2, ensure_ascii=False) + ''';

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Servir imágenes de gimnasio desde KV
    if (url.pathname.startsWith("/img/")) {
      const key = "img_" + url.pathname.replace("/img/", "").replace(".jpg", "");
      try {
        const imgData = await env.AEGIS_KV.get(key, { type: "arrayBuffer" });
        if (imgData) {
          return new Response(imgData, {
            headers: {
              "Content-Type": "image/jpeg",
              "Cache-Control": "public, max-age=86400"
            }
          });
        }
      } catch (e) {
        console.error("Error leyendo imagen de KV:", e);
      }
      return new Response("Imagen no encontrada", { status: 404 });
    }

    // API de actualización manual
    if (url.pathname === "/api/set_day_status" && request.method === "POST") {
      try {
        const body: any = await request.json();
        const date = body.date;
        const status = body.status;
        if (!date || !status) {
          return new Response(JSON.stringify({ error: "Faltan parámetros date o status" }), { status: 400 });
        }
        let currentPlan: any = await env.AEGIS_KV.get("current_plan", { type: "json" });
        if (!currentPlan) currentPlan = DEFAULT_PLAN;
        for (const d of currentPlan.days) {
          if (d.date === date) {
            d.manual_status = status;
            break;
          }
        }
        await env.AEGIS_KV.put("current_plan", JSON.stringify(currentPlan));
        return new Response(JSON.stringify({ success: true, date, status }), {
          headers: { "Content-Type": "application/json" }
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500 });
      }
    }

    // Webhook de Telegram
    if (url.pathname === "/telegram-webhook" && request.method === "POST") {
      try {
        const update: any = await request.json();
        if (update && update.message) {
          await handleTelegramMessage(update.message, env);
        }
        return new Response("OK", { status: 200 });
      } catch (err: any) {
        console.error("Error Telegram Webhook:", err);
        return new Response("Error", { status: 500 });
      }
    }

    // Cargar plan desde KV o fallback maestro
    let planData: any = null;
    try {
      planData = await env.AEGIS_KV.get("current_plan", { type: "json" });
    } catch (e) {
      console.error("Error cargando current_plan de KV:", e);
    }
    if (!planData) {
      planData = DEFAULT_PLAN;
    }

    const html = getLuxuryDashboardHtml(planData);
    return new Response(html, {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-cache"
      }
    });
  },

  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    console.log("Cron ejecutado en Cloudflare Workers:", event.cron);
  }
};

async function handleTelegramMessage(message: any, env: Env) {
  const chatId = message.chat.id;
  const text = (message.text || "").trim();
  const todayISO = getTodayMadridISO();

  let plan: any = null;
  try {
    plan = await env.AEGIS_KV.get("current_plan", { type: "json" });
  } catch (e) {}
  if (!plan) plan = DEFAULT_PLAN;

  const days: any[] = plan.days || [];
  const todayPlan = days.find((d: any) => d.date === todayISO) || days[0];

  let reply = "";
  if (text === "/start" || text === "/ayuda") {
    reply = "👋 *Aegis Coach — Carlos Jiménez Andrino*\\n\\n" +
      "Comandos rápidos:\\n" +
      "• `/hoy` — Plan de hoy (" + todayPlan.display_date + ")\\n" +
      "• `/semana` — Resumen del microciclo\\n" +
      "• `/rodilla` — Protocolo preventivo VMO\\n" +
      "• `/app` — Acceso al Dashboard Web";
  } else if (text === "/hoy") {
    reply = "📅 *PLAN DE HOY (" + todayPlan.display_date + " — " + todayPlan.day_name + ")*\\n\\n";
    if (todayPlan.running.is_rest) {
      reply += "🏃 *Running:* Descanso de carrera\\n";
    } else {
      reply += "🏃 *Running:* " + todayPlan.running.title + "\\n" +
        "• *Distancia:* " + todayPlan.running.target_distance_km + " km (" + todayPlan.running.duration_min + " min)\\n" +
        "• *Ritmo:* `" + todayPlan.running.target_pace + "` (" + todayPlan.running.hr_zone + ")\\n" +
        "• *Zapatillas:* " + todayPlan.running.shoes_recommended + "\\n\\n";
    }
    if (todayPlan.gym.is_rest) {
      reply += "🏋️ *Gym:* Descanso de fuerza\\n";
    } else {
      reply += "🏋️ *Gym:* " + todayPlan.gym.routine_name + "\\n" +
        "Abre la web app para ver fotos de ejecución y registrar cargas.";
    }
  } else if (text === "/app") {
    reply = "🌐 *Aegis Coach PWA:*\\nhttps://aegis-intervals-sync.uranuslabs.workers.dev";
  } else {
    reply = "Comando no reconocido. Escribe `/hoy` para ver tu sesión actual.";
  }

  const url = "https://api.telegram.org/bot" + env.TELEGRAM_BOT_TOKEN + "/sendMessage";
  await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: chatId,
      text: reply,
      parse_mode: "Markdown"
    })
  });
}

function getLuxuryDashboardHtml(planData: any): string {
  const todayISO = getTodayMadridISO();
  const primaryObj = planData.macrocycle.primary_objective;
  const daysRemaining = calculateDaysRemaining(primaryObj.date, todayISO);
  const weeksRemaining = (daysRemaining / 7).toFixed(1);

  const days: any[] = planData.days || [];
  const daysJsonStr = JSON.stringify(days);
  const weeklyEvoStr = JSON.stringify(WEEKLY_EVO_DATA);

  return `<!DOCTYPE html>
<html lang="es" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
  <title>Aegis Coach — Carlos Jiménez Andrino</title>
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23FF5E80' stroke-width='2'%3E%3Cpath d='M13 2L3 14h9l-1 8 10-12h-9l1-8z'/%3E%3C/svg%3E">
  
  <!-- Tipografía de Lujo: Plus Jakarta Sans & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <!-- Tailwind CSS & Lucide Icons -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: {
            app: {
              bg: '#141522',
              sidebar: '#13141F',
              card: '#1D1E2C',
              subcard: '#242638',
              border: '#2D2F45',
              hover: '#292B3E'
            },
            neon: {
              pink: '#FF5E80',
              pinkDark: '#FF4B72',
              blue: '#7B88FF',
              indigo: '#6C5DD3',
              purple: '#C471ED',
              green: '#20D994'
            },
            slateText: {
              primary: '#FFFFFF',
              secondary: '#9D9EA7',
              muted: '#5D5F76'
            }
          },
          fontFamily: {
            sans: ['"Plus Jakarta Sans"', 'sans-serif'],
            mono: ['"JetBrains Mono"', 'monospace']
          }
        }
      }
    };
  </script>

  <style>
    body {
      background-color: #141522;
      color: #FFFFFF;
      font-family: 'Plus Jakarta Sans', sans-serif;
      -webkit-font-smoothing: antialiased;
      -moz-osx-font-smoothing: grayscale;
    }
    
    /* Scrollbar estilizada */
    ::-webkit-scrollbar {
      width: 6px;
      height: 6px;
    }
    ::-webkit-scrollbar-track {
      background: #141522;
    }
    ::-webkit-scrollbar-thumb {
      background: #2D2F45;
      border-radius: 9999px;
    }
    ::-webkit-scrollbar-thumb:hover {
      background: #7B88FF;
    }

    /* Tarjetas de lujo con bordes y gradientes tenues */
    .luxury-card {
      background-color: #1D1E2C;
      border: 1px solid #2D2F45;
      border-radius: 24px;
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
    .luxury-card:hover {
      border-color: rgba(123, 136, 255, 0.3);
    }

    .luxury-subcard {
      background-color: #242638;
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 18px;
    }

    /* Glows y degradados */
    .glow-pink {
      box-shadow: 0 8px 24px -6px rgba(255, 94, 128, 0.35);
    }
    .glow-blue {
      box-shadow: 0 8px 24px -6px rgba(123, 136, 255, 0.35);
    }

    /* Gradiente suave estilo referencia */
    .bg-gradient-hero {
      background: linear-gradient(135deg, #7B88FF 0%, #A08BFE 40%, #FF5E80 100%);
    }

    .active-nav-link {
      color: #FF5E80 !important;
      position: relative;
    }
    .active-nav-link::before {
      content: '';
      position: absolute;
      left: 0;
      top: 50%;
      transform: translateY(-50%);
      width: 4px;
      height: 24px;
      background: #FF5E80;
      border-radius: 0 4px 4px 0;
      box-shadow: 0 0 12px #FF5E80;
    }
    
    /* Radial gauge SVG */
    .gauge-circle-bg {
      stroke: #2D2F45;
      stroke-width: 5;
      fill: none;
    }
    .gauge-circle-val {
      stroke-width: 5;
      stroke-linecap: round;
      fill: none;
      transition: stroke-dasharray 0.8s ease;
    }
  </style>
</head>

<body class="min-h-screen bg-[#141522] text-white flex flex-col antialiased selection:bg-[#FF5E80] selection:text-white pb-24 lg:pb-8">

  <div class="flex-1 flex w-full max-w-[1600px] mx-auto">

    <!-- SIDEBAR VERTICAL (Desktop: >= 1024px) -->
    <aside class="hidden lg:flex flex-col items-center justify-between w-24 py-8 bg-[#13141F] border-r border-[#2D2F45] fixed h-full z-30">
      <div class="flex flex-col items-center gap-10 w-full">
        <!-- Logo -->
        <div class="w-12 h-12 rounded-2xl bg-gradient-to-tr from-[#6C5DD3] to-[#FF5E80] flex items-center justify-center glow-pink cursor-pointer" onclick="switchTab('dashboard')">
          <i data-lucide="zap" class="w-6 h-6 text-white stroke-[2.5]"></i>
        </div>

        <!-- Menú de Iconos con Indicador Activo Vertical -->
        <nav class="flex flex-col gap-6 w-full">
          <button onclick="switchTab('dashboard')" id="nav-desktop-dashboard" class="relative w-full py-3 flex items-center justify-center text-[#FF5E80] active-nav-link transition-colors">
            <i data-lucide="layout-grid" class="w-6 h-6 stroke-[2]"></i>
          </button>
          <button onclick="switchTab('workouts')" id="nav-desktop-workouts" class="relative w-full py-3 flex items-center justify-center text-[#8E8FA3] hover:text-white transition-colors">
            <i data-lucide="calendar" class="w-6 h-6 stroke-[2]"></i>
          </button>
          <button onclick="switchTab('gym')" id="nav-desktop-gym" class="relative w-full py-3 flex items-center justify-center text-[#8E8FA3] hover:text-white transition-colors">
            <i data-lucide="dumbbell" class="w-6 h-6 stroke-[2]"></i>
          </button>
          <button onclick="switchTab('goals')" id="nav-desktop-goals" class="relative w-full py-3 flex items-center justify-center text-[#8E8FA3] hover:text-white transition-colors">
            <i data-lucide="target" class="w-6 h-6 stroke-[2]"></i>
          </button>
        </nav>
      </div>

      <!-- Botón Telegram en Sidebar -->
      <a href="https://t.me/aegis_coach_chatbot" target="_blank" title="Abrir Bot de Telegram" class="w-11 h-11 rounded-xl bg-[#1D1E2C] border border-[#2D2F45] flex items-center justify-center text-[#7B88FF] hover:border-[#7B88FF] hover:scale-105 transition">
        <i data-lucide="send" class="w-5 h-5"></i>
      </a>
    </aside>

    <!-- CONTENEDOR PRINCIPAL -->
    <main class="flex-1 flex flex-col lg:pl-24 w-full">

      <!-- TOP BAR HEADER -->
      <header class="w-full px-5 lg:px-10 py-5 lg:py-6 flex items-center justify-between border-b border-[#2D2F45]/60 bg-[#141522]/90 backdrop-blur sticky top-0 z-20">
        <div class="flex items-center gap-4">
          <!-- Logo Móvil -->
          <div class="lg:hidden w-10 h-10 rounded-xl bg-gradient-to-tr from-[#6C5DD3] to-[#FF5E80] flex items-center justify-center shadow-lg shadow-[#FF5E80]/20">
            <i data-lucide="zap" class="w-5 h-5 text-white stroke-[2.5]"></i>
          </div>
          <div>
            <h1 id="header-title" class="text-xl lg:text-2xl font-extrabold tracking-tight text-white flex items-center gap-2">
              Dashboard
            </h1>
            <p class="text-xs text-[#8E8FA3] hidden sm:block">Aegis Coach &bull; Fisiología del Rendimiento & Fuerza</p>
          </div>
        </div>

        <!-- Buscador & Perfil (Estilo Referencia) -->
        <div class="flex items-center gap-3 sm:gap-4">
          <!-- Input Buscador (Desktop) -->
          <div class="hidden md:flex items-center gap-2 px-4 py-2 rounded-2xl bg-[#1D1E2C] border border-[#2D2F45] text-xs text-[#8E8FA3] w-64 focus-within:border-[#7B88FF] transition">
            <i data-lucide="search" class="w-4 h-4 text-[#8E8FA3]"></i>
            <input type="text" placeholder="Buscar sesión, ritmo, ejercicio..." class="bg-transparent border-none outline-none text-white w-full placeholder-[#5D5F76]">
          </div>

          <!-- Telegram Bot Pill -->
          <a href="https://t.me/aegis_coach_chatbot" target="_blank" class="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-[#1D1E2C] border border-[#7B88FF]/40 text-[#7B88FF] text-xs font-bold hover:bg-[#7B88FF]/10 transition shadow-sm">
            <i data-lucide="send" class="w-3.5 h-3.5"></i>
            <span class="hidden sm:inline">Bot</span> Telegram
          </a>

          <!-- Perfil Atleta -->
          <div class="flex items-center gap-3 pl-2 sm:border-l sm:border-[#2D2F45]">
            <div class="relative w-10 h-10 rounded-2xl bg-gradient-to-tr from-[#FF5E80] to-[#7B88FF] p-0.5">
              <div class="w-full h-full bg-[#1D1E2C] rounded-[14px] flex items-center justify-center text-xs font-black text-white">
                CJ
              </div>
              <span class="absolute bottom-0 right-0 w-2.5 h-2.5 rounded-full bg-[#20D994] ring-2 ring-[#141522]"></span>
            </div>
            <div class="hidden xl:block text-left">
              <div class="text-xs font-bold text-white leading-tight">Carlos Jiménez</div>
              <div class="text-[10px] text-[#8E8FA3]">63 kg &bull; 1.73 m</div>
            </div>
          </div>
        </div>
      </header>

      <!-- BARRA DE PESTAÑAS MÓVIL (Pills superiores en móvil) -->
      <div class="lg:hidden px-5 pt-4 pb-2 flex gap-2 overflow-x-auto no-scrollbar">
        <button onclick="switchTab('dashboard')" id="nav-mobile-dashboard" class="px-4 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap bg-[#FF5E80] text-white glow-pink">
          Dashboard
        </button>
        <button onclick="switchTab('workouts')" id="nav-mobile-workouts" class="px-4 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap bg-[#1D1E2C] text-[#8E8FA3] border border-[#2D2F45]">
          Entrenos (14D)
        </button>
        <button onclick="switchTab('gym')" id="nav-mobile-gym" class="px-4 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap bg-[#1D1E2C] text-[#8E8FA3] border border-[#2D2F45]">
          Gimnasio & Registro
        </button>
        <button onclick="switchTab('goals')" id="nav-mobile-goals" class="px-4 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap bg-[#1D1E2C] text-[#8E8FA3] border border-[#2D2F45]">
          Objetivos & Ritmos
        </button>
      </div>

      <!-- CONTENIDO DE LAS PESTAÑAS -->
      <div class="p-5 lg:p-10 flex-1">

        <!-- ========================================== -->
        <!-- PESTAÑA 1: DASHBOARD DE LUJO (REFERENCIA) -->
        <!-- ========================================== -->
        <section id="tab-dashboard" class="space-y-6">

          <!-- TIRA DE 3 GAUGES CIRCULARES (Exacto como Total Income, Expense, Bonus) -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-5">

            <!-- Card 1: Volumen Esta Semana -->
            <div class="luxury-card p-6 flex items-center justify-between">
              <div>
                <p class="text-xs font-semibold text-[#8E8FA3]">Volumen Semanal (Run)</p>
                <h3 class="text-2xl lg:text-3xl font-black text-white mt-1">27.0 <span class="text-sm font-semibold text-[#8E8FA3]">km</span></h3>
                <p class="text-[11px] text-[#20D994] font-medium mt-1.5 flex items-center gap-1">
                  <i data-lucide="trending-up" class="w-3.5 h-3.5"></i>
                  <span>90% del objetivo (30 km)</span>
                </p>
              </div>
              <!-- Radial Gauge Rosa -->
              <div class="relative w-18 h-18 flex items-center justify-center">
                <svg class="w-18 h-18 -rotate-90" viewBox="0 0 64 64">
                  <circle cx="32" cy="32" r="26" class="gauge-circle-bg"></circle>
                  <circle cx="32" cy="32" r="26" class="gauge-circle-val" stroke="#FF5E80" stroke-dasharray="163.36" stroke-dashoffset="16.3"></circle>
                </svg>
                <span class="absolute text-xs font-extrabold text-white">90%</span>
              </div>
            </div>

            <!-- Card 2: Fuerza & Gimnasio -->
            <div class="luxury-card p-6 flex items-center justify-between">
              <div>
                <p class="text-xs font-semibold text-[#8E8FA3]">Sesiones de Fuerza</p>
                <h3 class="text-2xl lg:text-3xl font-black text-white mt-1">4 <span class="text-sm font-semibold text-[#8E8FA3]">sesiones</span></h3>
                <p class="text-[11px] text-[#7B88FF] font-medium mt-1.5 flex items-center gap-1">
                  <i data-lucide="check-circle" class="w-3.5 h-3.5"></i>
                  <span>100% cumplido (4 de 4)</span>
                </p>
              </div>
              <!-- Radial Gauge Azul/Indigo -->
              <div class="relative w-18 h-18 flex items-center justify-center">
                <svg class="w-18 h-18 -rotate-90" viewBox="0 0 64 64">
                  <circle cx="32" cy="32" r="26" class="gauge-circle-bg"></circle>
                  <circle cx="32" cy="32" r="26" class="gauge-circle-val" stroke="#7B88FF" stroke-dasharray="163.36" stroke-dashoffset="0"></circle>
                </svg>
                <span class="absolute text-xs font-extrabold text-white">100%</span>
              </div>
            </div>

            <!-- Card 3: Estado de Forma TSB -->
            <div class="luxury-card p-6 flex items-center justify-between">
              <div>
                <p class="text-xs font-semibold text-[#8E8FA3]">Estado Forma (TSB / CTL)</p>
                <h3 class="text-2xl lg:text-3xl font-black text-white mt-1">TSB -9.5 <span class="text-sm font-semibold text-[#8E8FA3]">/ 16.1</span></h3>
                <p class="text-[11px] text-[#C471ED] font-medium mt-1.5 flex items-center gap-1">
                  <i data-lucide="activity" class="w-3.5 h-3.5"></i>
                  <span>Fatiga asimilable (ATL 25.7)</span>
                </p>
              </div>
              <!-- Radial Gauge Lila -->
              <div class="relative w-18 h-18 flex items-center justify-center">
                <svg class="w-18 h-18 -rotate-90" viewBox="0 0 64 64">
                  <circle cx="32" cy="32" r="26" class="gauge-circle-bg"></circle>
                  <circle cx="32" cy="32" r="26" class="gauge-circle-val" stroke="#C471ED" stroke-dasharray="163.36" stroke-dashoffset="40.8"></circle>
                </svg>
                <span class="absolute text-xs font-extrabold text-white">75%</span>
              </div>
            </div>

          </div>

          <!-- FILA CENTRAL: GRÁFICO DINÁMICO DEGRADADO + TARJETA DE PRÓXIMA SESIÓN -->
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

            <!-- GRÁFICO DE EVOLUCIÓN SEMANAL EN KM (2 Columnas en Desktop) -->
            <div class="lg:col-span-2 luxury-card p-6 flex flex-col justify-between">
              <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-6">
                <div>
                  <h3 class="text-lg font-extrabold text-white">Evolución de Volumen Semanal (KM)</h3>
                  <p class="text-xs text-[#8E8FA3] mt-0.5">Kilómetros reales rodados semana a semana &bull; Tendencia de carga</p>
                </div>

                <div class="flex items-center gap-4 text-xs font-semibold">
                  <div class="flex items-center gap-1.5">
                    <span class="w-3 h-3 rounded-full bg-[#FF5E80] glow-pink"></span>
                    <span class="text-white">Run (km)</span>
                  </div>
                  <div class="flex items-center gap-1.5">
                    <span class="w-3 h-3 rounded-full bg-[#7B88FF] glow-blue"></span>
                    <span class="text-[#8E8FA3]">Gym (sesiones)</span>
                  </div>
                  <span class="px-3 py-1 rounded-xl bg-[#242638] border border-[#2D2F45] text-[11px] text-[#8E8FA3]">
                    8 Semanas
                  </span>
                </div>
              </div>

              <!-- Canvas Chart.js con Monotone Spline y Degradado Tenue -->
              <div class="w-full h-64 sm:h-72 relative">
                <canvas id="weeklySplineChart"></canvas>
              </div>

              <!-- Desglose numérico rápido por semana -->
              <div class="grid grid-cols-4 sm:grid-cols-8 gap-2 pt-4 mt-4 border-t border-[#2D2F45]/60 text-center">
                <div class="p-1.5 rounded-xl bg-[#242638]/40">
                  <div class="text-[10px] text-[#8E8FA3]">28 Sep</div>
                  <div class="text-xs font-black text-white mt-0.5 font-mono">13.4k</div>
                </div>
                <div class="p-1.5 rounded-xl bg-[#242638]/40">
                  <div class="text-[10px] text-[#8E8FA3]">05 Oct</div>
                  <div class="text-xs font-black text-white mt-0.5 font-mono">19.2k</div>
                </div>
                <div class="p-1.5 rounded-xl bg-[#242638]/40">
                  <div class="text-[10px] text-[#8E8FA3]">12 Oct</div>
                  <div class="text-xs font-black text-white mt-0.5 font-mono">16.5k</div>
                </div>
                <div class="p-1.5 rounded-xl bg-[#242638]/40">
                  <div class="text-[10px] text-[#8E8FA3]">19 Oct</div>
                  <div class="text-xs font-black text-white mt-0.5 font-mono">25.4k</div>
                </div>
                <div class="p-1.5 rounded-xl bg-[#242638]/40">
                  <div class="text-[10px] text-[#8E8FA3]">26 Oct</div>
                  <div class="text-xs font-black text-white mt-0.5 font-mono">29.2k</div>
                </div>
                <div class="p-1.5 rounded-xl bg-[#242638]/40 border border-[#7B88FF]/30">
                  <div class="text-[10px] text-[#7B88FF] font-bold">10K Ávila</div>
                  <div class="text-xs font-black text-white mt-0.5 font-mono">21.6k</div>
                </div>
                <div class="p-1.5 rounded-xl bg-[#242638]/40 border border-[#FF5E80]/30">
                  <div class="text-[10px] text-[#FF5E80] font-bold">6x800m</div>
                  <div class="text-xs font-black text-white mt-0.5 font-mono">27.0k</div>
                </div>
                <div class="p-1.5 rounded-xl bg-[#FF5E80]/10 border border-[#FF5E80]/50">
                  <div class="text-[10px] text-[#FF5E80] font-black">Esta Sem</div>
                  <div class="text-xs font-black text-[#FF5E80] mt-0.5 font-mono">~30k</div>
                </div>
              </div>
            </div>

            <!-- COLUMNA DERECHA: TARJETA GLOWING DE ENTRENAMIENTO DE HOY (Estilo "My Cards") -->
            <div class="space-y-6">

              <!-- Tarjeta Gradiente Rosa-Púrpura -->
              <div class="rounded-3xl p-6 bg-gradient-hero text-white shadow-xl glow-pink flex flex-col justify-between h-56 relative overflow-hidden">
                <!-- Efecto visual curvado de fondo -->
                <div class="absolute -right-8 -bottom-8 w-40 h-40 bg-white/10 rounded-full blur-2xl pointer-events-none"></div>

                <div class="flex items-center justify-between relative z-10">
                  <span class="text-xs uppercase font-extrabold tracking-wider bg-black/20 px-3 py-1 rounded-full backdrop-blur">
                    SESIÓN DE HOY &bull; LUNES 16 NOV
                  </span>
                  <i data-lucide="zap" class="w-5 h-5 text-white"></i>
                </div>

                <div class="my-auto relative z-10">
                  <div class="text-2xl font-black tracking-tight leading-tight">
                    35' Rodaje Regenerativo
                  </div>
                  <div class="text-xs text-white/90 font-mono mt-1 font-semibold">
                    Ritmo 4:55 - 5:10/km &bull; Z1 (&lt;145 ppm)
                  </div>
                </div>

                <div class="flex items-center justify-between pt-3 border-t border-white/20 relative z-10">
                  <div class="text-xs font-bold text-white/90">
                    + Rutina 2: Torso Tracción
                  </div>
                  <button onclick="switchTab('workouts')" class="px-3 py-1.5 rounded-xl bg-white text-[#141522] text-xs font-black hover:bg-white/90 transition flex items-center gap-1">
                    <span>Ver</span> &rarr;
                  </button>
                </div>
              </div>

              <!-- LISTADO DE ÚLTIMAS ACTIVIDADES (Estilo "Recent Transactions") -->
              <div class="luxury-card p-6">
                <div class="flex items-center justify-between mb-4">
                  <h4 class="text-sm font-extrabold text-white">Últimas Sesiones Clave</h4>
                  <span class="text-[11px] text-[#8E8FA3]">Intervals.icu</span>
                </div>

                <div class="space-y-3">
                  <!-- Item 1: 6x800m -->
                  <div class="flex items-center justify-between p-2.5 rounded-xl bg-[#242638] border border-[#2D2F45]">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-xl bg-[#FF5E80]/15 text-[#FF5E80] flex items-center justify-center font-bold">
                        <i data-lucide="flame" class="w-4 h-4"></i>
                      </div>
                      <div>
                        <div class="text-xs font-bold text-white">6x800m Parque del Soto</div>
                        <div class="text-[10px] text-[#8E8FA3]">14 Nov &bull; Clavos 6mm &bull; 90" rec</div>
                      </div>
                    </div>
                    <div class="text-right">
                      <div class="text-xs font-black text-white font-mono">3:00.0 avg</div>
                      <div class="text-[10px] text-[#FF5E80]">3:45/km real</div>
                    </div>
                  </div>

                  <!-- Item 2: Rutina 3 Pierna 2 -->
                  <div class="flex items-center justify-between p-2.5 rounded-xl bg-[#242638] border border-[#2D2F45]">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-xl bg-[#7B88FF]/15 text-[#7B88FF] flex items-center justify-center font-bold">
                        <i data-lucide="dumbbell" class="w-4 h-4"></i>
                      </div>
                      <div>
                        <div class="text-xs font-bold text-white">Rutina 3 &bull; Pierna 2</div>
                        <div class="text-[10px] text-[#8E8FA3]">13 Nov &bull; RDL Unilateral</div>
                      </div>
                    </div>
                    <div class="text-right">
                      <div class="text-xs font-black text-white font-mono">140 kg</div>
                      <div class="text-[10px] text-[#7B88FF]">Hip Thrust</div>
                    </div>
                  </div>

                  <!-- Item 3: 10K Ávila -->
                  <div class="flex items-center justify-between p-2.5 rounded-xl bg-[#242638] border border-[#2D2F45]">
                    <div class="flex items-center gap-3">
                      <div class="w-9 h-9 rounded-xl bg-[#20D994]/15 text-[#20D994] flex items-center justify-center font-bold">
                        <i data-lucide="trophy" class="w-4 h-4"></i>
                      </div>
                      <div>
                        <div class="text-xs font-bold text-white">10K Ávila Monumental</div>
                        <div class="text-[10px] text-[#8E8FA3]">08 Nov &bull; 1.070m altitud</div>
                      </div>
                    </div>
                    <div class="text-right">
                      <div class="text-xs font-black text-white font-mono">38:26</div>
                      <div class="text-[10px] text-[#20D994]">3:50/km</div>
                    </div>
                  </div>
                </div>
              </div>

            </div>

          </div>

          <!-- FILA INFERIOR: PRÓXIMOS HITOS (Estilo Investment & Deposit) -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

            <!-- Hito 1: Cross del Soto -->
            <div class="luxury-card p-6 flex flex-col justify-between">
              <div class="flex items-center justify-between">
                <div>
                  <span class="text-[10px] uppercase font-extrabold px-2.5 py-1 rounded-lg bg-[#FF5E80]/15 text-[#FF5E80] border border-[#FF5E80]/30">
                    PRÓXIMA COMPETICIÓN &bull; 28 NOV
                  </span>
                  <h4 class="text-xl font-extrabold text-white mt-2">Cross Popular Parque del Soto</h4>
                  <p class="text-xs text-[#8E8FA3] mt-0.5">5.0 km hierba / tierra &bull; 1.060m altitud &bull; Clavos 6 mm</p>
                </div>
                <div class="text-right">
                  <div class="text-2xl font-black text-[#FF5E80] font-mono">${daysRemaining} Días</div>
                  <div class="text-xs text-[#8E8FA3]">${weeksRemaining} semanas</div>
                </div>
              </div>

              <div class="mt-4">
                <div class="flex justify-between text-xs font-semibold mb-1.5">
                  <span class="text-[#8E8FA3]">Ritmo Objetivo: sub 3:35/km (~17:45)</span>
                  <span class="text-[#FF5E80]">78% Afinamiento</span>
                </div>
                <div class="w-full h-2.5 rounded-full bg-[#242638] overflow-hidden">
                  <div class="h-full rounded-full bg-gradient-to-r from-[#7B88FF] to-[#FF5E80] glow-pink" style="width: 78%"></div>
                </div>
              </div>
            </div>

            <!-- Hito 2: San Silvestre -->
            <div class="luxury-card p-6 flex flex-col justify-between">
              <div class="flex items-center justify-between">
                <div>
                  <span class="text-[10px] uppercase font-extrabold px-2.5 py-1 rounded-lg bg-[#7B88FF]/15 text-[#7B88FF] border border-[#7B88FF]/30">
                    OBJETIVO FIN DE AÑO &bull; 31 DIC
                  </span>
                  <h4 class="text-xl font-extrabold text-white mt-2">San Silvestre (6.5 km)</h4>
                  <p class="text-xs text-[#8E8FA3] mt-0.5">Asfalto urbano &bull; Ritmo objetivo: sub 3:35/km (sub 23:15)</p>
                </div>
                <div class="text-right">
                  <div class="text-2xl font-black text-[#7B88FF] font-mono">46 Días</div>
                  <div class="text-xs text-[#8E8FA3]">6.5 semanas</div>
                </div>
              </div>

              <div class="mt-4">
                <div class="flex justify-between text-xs font-semibold mb-1.5">
                  <span class="text-[#8E8FA3]">Base de Ritmo 10K: 3:50/km consolidada</span>
                  <span class="text-[#7B88FF]">Fase de Carga</span>
                </div>
                <div class="w-full h-2.5 rounded-full bg-[#242638] overflow-hidden">
                  <div class="h-full rounded-full bg-gradient-to-r from-[#6C5DD3] to-[#7B88FF] glow-blue" style="width: 55%"></div>
                </div>
              </div>
            </div>

          </div>

        </section>

        <!-- ========================================== -->
        <!-- PESTAÑA 2: ENTRENOS (CALENDARIO 14 DÍAS) -->
        <!-- ========================================== -->
        <section id="tab-workouts" class="space-y-4 hidden">
          <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-2">
            <div>
              <h2 class="text-xl font-extrabold text-white">Microciclo Bi-Semanal (14 Días)</h2>
              <p class="text-xs text-[#8E8FA3]">Toca cualquier día para desplegar o colapsar el detalle técnico y directrices</p>
            </div>
            <div class="flex items-center gap-2">
              <span class="text-xs px-3 py-1.5 rounded-xl bg-[#242638] border border-[#2D2F45] text-[#8E8FA3]">
                Hoy: <strong class="text-white">${todayISO}</strong>
              </span>
            </div>
          </div>

          <div id="workout-days-accordion" class="space-y-3">
            <!-- Inyectado dinámicamente con JavaScript -->
          </div>
        </section>

        <!-- ========================================== -->
        <!-- PESTAÑA 3: GIMNASIO & REGISTRO DE CARGAS -->
        <!-- ========================================== -->
        <section id="tab-gym" class="space-y-6 hidden">

          <!-- Selector de las 4 Rutinas Oficiales -->
          <div class="luxury-card p-5">
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4">
              <div>
                <span class="text-[10px] uppercase font-extrabold px-2 py-0.5 rounded bg-[#FF5E80]/20 text-[#FF5E80]">
                  RUTINAS OFICIALES MAESTRAS (PDF PÁGS 1-4)
                </span>
                <h3 class="text-lg font-extrabold text-white mt-1">Selecciona la Rutina de Gimnasio</h3>
                <p class="text-xs text-[#8E8FA3]">4 sesiones estables para sobrecarga progresiva y rigidez miotendinosa</p>
              </div>
              <div class="text-xs text-[#20D994] font-semibold flex items-center gap-1">
                <i data-lucide="shield-check" class="w-4 h-4"></i>
                <span>Sobrecarga: +2.5 kg al completar reps</span>
              </div>
            </div>

            <!-- Botones de las 4 Rutinas -->
            <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
              <button onclick="selectGymRoutine(1)" id="gym-chip-1" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#242638] border-[#2D2F45] text-[#8E8FA3] hover:border-[#FF5E80]">
                <span class="text-[10px] uppercase font-bold text-[#8E8FA3]">LUNES 18:00</span>
                <span class="text-xs font-extrabold text-white mt-1">Pierna 1</span>
                <span class="text-[10px] text-[#8E8FA3] mt-0.5">Cuádriceps & VMO</span>
              </button>

              <button onclick="selectGymRoutine(2)" id="gym-chip-2" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#242638] border-[#2D2F45] text-[#8E8FA3] hover:border-[#FF5E80]">
                <span class="text-[10px] uppercase font-bold text-[#8E8FA3]">MIÉRCOLES 17:30</span>
                <span class="text-xs font-extrabold text-white mt-1">Torso Tracción</span>
                <span class="text-[10px] text-[#8E8FA3] mt-0.5">Dorsal, Remo & Bíceps</span>
              </button>

              <button onclick="selectGymRoutine(3)" id="gym-chip-3" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#FF5E80] text-white border-[#FF5E80] font-semibold glow-pink">
                <span class="text-[10px] uppercase font-extrabold text-white/80">JUEVES/VIERNES</span>
                <span class="text-xs font-extrabold text-white mt-1">Pierna 2 (Hoy)</span>
                <span class="text-[10px] text-white/80 mt-0.5">Hip Thrust & Isquios</span>
              </button>

              <button onclick="selectGymRoutine(4)" id="gym-chip-4" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#242638] border-[#2D2F45] text-[#8E8FA3] hover:border-[#FF5E80]">
                <span class="text-[10px] uppercase font-bold text-[#8E8FA3]">SÁBADO 11:00</span>
                <span class="text-xs font-extrabold text-white mt-1">Torso Empuje</span>
                <span class="text-[10px] text-[#8E8FA3] mt-0.5">Pectoral & Deltoides</span>
              </button>
            </div>
          </div>

          <!-- Blindaje Rodilla Izquierda (Activo) -->
          <div class="luxury-card p-5 border border-[#20D994]/30 bg-[#20D994]/5 flex items-start gap-4">
            <div class="w-10 h-10 rounded-xl bg-[#20D994]/20 text-[#20D994] flex items-center justify-center shrink-0">
              <i data-lucide="shield-check" class="w-5 h-5"></i>
            </div>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <h4 class="text-sm font-extrabold text-white">Blindaje VMO & Rodilla Izquierda (Activo)</h4>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-[#20D994]/20 text-[#20D994]">0/10 Dolor</span>
              </div>
              <p class="text-xs text-[#8E8FA3] mt-1 leading-relaxed">
                <strong>Spanish Squat Isométrica con Banda:</strong> 4 series &times; 35-40s de retención a 70°-80° de flexión. Tibias verticales. Recluta masivamente el vasto medial sin compresión patelofemoral.
              </p>
            </div>
          </div>

          <!-- Contenedor de Ejercicios de la Rutina Seleccionada -->
          <div id="gym-exercises-container" class="space-y-4">
            <!-- Renderizado con fotos reales de ejecución técnica e inputs interactivos -->
          </div>

          <!-- Botón de Copiado Global -->
          <div class="luxury-card p-6 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>
              <h4 class="text-sm font-extrabold text-white">¿Has terminado el entrenamiento?</h4>
              <p class="text-xs text-[#8E8FA3] mt-0.5">Los pesos quedan guardados en tu móvil. Cópialos con 1 toque para enviar al chat.</p>
            </div>
            <button onclick="copyGymSessionToClipboard()" id="copy-gym-btn" class="w-full sm:w-auto px-6 py-3 rounded-2xl bg-gradient-to-r from-[#FF5E80] to-[#FF4B72] text-white font-extrabold text-xs glow-pink hover:scale-[1.02] active:scale-[0.98] transition flex items-center justify-center gap-2">
              <i data-lucide="clipboard-copy" class="w-4 h-4"></i>
              <span>Copiar Registro de Hoy</span>
            </button>
          </div>

        </section>

        <!-- ========================================== -->
        <!-- PESTAÑA 4: OBJETIVOS & CALCULADORA RITMOS -->
        <!-- ========================================== -->
        <section id="tab-goals" class="space-y-6 hidden">

          <div class="luxury-card p-6">
            <h3 class="text-lg font-extrabold text-white">Matriz de Objetivos & Ritmos de Carrera</h3>
            <p class="text-xs text-[#8E8FA3] mt-1">Calibrado con tus datos de 10K Ávila (38:26 @ 3:50/km) y perfil anaeróbico</p>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mt-6">
              
              <!-- Objetivo 1: Cross del Soto -->
              <div class="luxury-subcard p-5 border-t-4 border-t-[#FF5E80]">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-[10px] font-bold text-[#FF5E80] uppercase">28 Noviembre</span>
                  <span class="text-xs font-black font-mono text-white">5.0 km</span>
                </div>
                <h4 class="text-base font-extrabold text-white">Cross Parque del Soto</h4>
                <div class="mt-4 space-y-1.5 text-xs">
                  <div class="flex justify-between text-[#8E8FA3]">
                    <span>Ritmo Objetivo:</span>
                    <strong class="text-white font-mono">3:35 - 3:40/km</strong>
                  </div>
                  <div class="flex justify-between text-[#8E8FA3]">
                    <span>Tiempo Meta:</span>
                    <strong class="text-[#FF5E80] font-mono">17:45 - 18:00</strong>
                  </div>
                  <div class="flex justify-between text-[#8E8FA3]">
                    <span>Superficie:</span>
                    <span class="text-white">Hierba/Tierra (Clavos 6mm)</span>
                  </div>
                </div>
              </div>

              <!-- Objetivo 2: San Silvestre -->
              <div class="luxury-subcard p-5 border-t-4 border-t-[#7B88FF]">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-[10px] font-bold text-[#7B88FF] uppercase">31 Diciembre</span>
                  <span class="text-xs font-black font-mono text-white">6.5 km</span>
                </div>
                <h4 class="text-base font-extrabold text-white">San Silvestre</h4>
                <div class="mt-4 space-y-1.5 text-xs">
                  <div class="flex justify-between text-[#8E8FA3]">
                    <span>Ritmo Objetivo:</span>
                    <strong class="text-white font-mono">sub 3:35/km</strong>
                  </div>
                  <div class="flex justify-between text-[#8E8FA3]">
                    <span>Tiempo Meta:</span>
                    <strong class="text-[#7B88FF] font-mono">sub 23:15</strong>
                  </div>
                  <div class="flex justify-between text-[#8E8FA3]">
                    <span>Superficie:</span>
                    <span class="text-white">Asfalto Urbano</span>
                  </div>
                </div>
              </div>

              <!-- Benchmark: 10K Ávila -->
              <div class="luxury-subcard p-5 border-t-4 border-t-[#20D994]">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-[10px] font-bold text-[#20D994] uppercase">08 Noviembre</span>
                  <span class="text-xs font-black font-mono text-white">10.0 km</span>
                </div>
                <h4 class="text-base font-extrabold text-white">10K Ávila Monumental</h4>
                <div class="mt-4 space-y-1.5 text-xs">
                  <div class="flex justify-between text-[#8E8FA3]">
                    <span>Marca Oficial:</span>
                    <strong class="text-[#20D994] font-mono">38:26 (3:50/km)</strong>
                  </div>
                  <div class="flex justify-between text-[#8E8FA3]">
                    <span>Altitud:</span>
                    <span class="text-white">1.070 m (D+ 95m)</span>
                  </div>
                  <div class="flex justify-between text-[#8E8FA3]">
                    <span>Equivalente Nivel Mar:</span>
                    <strong class="text-white font-mono">~37:10 (3:43/km)</strong>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <!-- Criterios Tácticos del Coach -->
          <div class="luxury-card p-6">
            <h4 class="text-sm font-extrabold text-white flex items-center gap-2">
              <i data-lucide="shield-alert" class="w-4 h-4 text-[#FF5E80]"></i>
              <span>Directrices de Rendimiento & Biomecánica</span>
            </h4>
            
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4 text-xs">
              <div class="luxury-subcard p-4">
                <strong class="text-white block mb-1">🚫 Veto de Pista de 200m sin Peralte:</strong>
                <p class="text-[#8E8FA3] leading-relaxed">
                  Series a 3:30/km en 200m planos implican 20 curvas cerradas de radio &lt;25m. La fuerza centrífuga genera cizallamiento severo sobre la cintilla iliotibial y rodilla izquierda (post-derrame). Todas las series de VO2max se hacen en asfalto recto y llano.
                </p>
              </div>

              <div class="luxury-subcard p-4">
                <strong class="text-white block mb-1">👟 Rotación de Zapatillas Estratégica:</strong>
                <p class="text-[#8E8FA3] leading-relaxed">
                  • <strong>Novablast 5:</strong> Rodajes Z1/Z2 regenerativos (cero estrés articular).<br>
                  • <strong>Nike Streakfly 2:</strong> Series de 1.000m en asfalto llano.<br>
                  • <strong>Clavos 6 mm:</strong> Cross del Soto en hierba/tierra compacta.
                </p>
              </div>
            </div>
          </div>

        </section>

      </div>

    </main>

  </div>

  <!-- BARRA DE NAVEGACIÓN INFERIOR FLOTANTE (Móvil: < 1024px) -->
  <nav class="lg:hidden fixed bottom-3 left-4 right-4 h-16 bg-[#1D1E2C]/95 backdrop-blur-md border border-[#2D2F45] rounded-2xl flex items-center justify-around z-40 px-2 shadow-2xl">
    <button onclick="switchTab('dashboard')" id="dock-btn-dashboard" class="flex flex-col items-center justify-center text-[#FF5E80] flex-1 py-1">
      <i data-lucide="layout-grid" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[10px] font-bold mt-1">Dashboard</span>
    </button>
    <button onclick="switchTab('workouts')" id="dock-btn-workouts" class="flex flex-col items-center justify-center text-[#8E8FA3] flex-1 py-1">
      <i data-lucide="calendar" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[10px] font-bold mt-1">Entrenos</span>
    </button>
    <button onclick="switchTab('gym')" id="dock-btn-gym" class="flex flex-col items-center justify-center text-[#8E8FA3] flex-1 py-1">
      <i data-lucide="dumbbell" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[10px] font-bold mt-1">Gimnasio</span>
    </button>
    <button onclick="switchTab('goals')" id="dock-btn-goals" class="flex flex-col items-center justify-center text-[#8E8FA3] flex-1 py-1">
      <i data-lucide="target" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[10px] font-bold mt-1">Objetivos</span>
    </button>
  </nav>

  <!-- JAVASCRIPT DEL CLIENTE -->
  <script>
    const daysData = ${daysJsonStr};
    const weeklyData = ${weeklyEvoStr};
    const todayISO = "${todayISO}";

    const gymRoutinesData = {
      1: {
        title: "Rutina 1 · Pierna 1 (Dominancia Rodilla & Cuádriceps)",
        day: "Lunes 18:00 • 45-50 min • RIR 1-2",
        exercises: [
          { num: 1, name: "Sentadilla con Barra / Box Squat", sub: "Back Squat a cajón paralelo", img: "/img/ex_1_1.jpg", muscle: "Cuádriceps & Glúteos", series: "4 series × 4-6 reps", weight: "65 - 70 kg", rest: "3.0 min", rir: "RIR 1-2", cue: "Rompe el paralelo al cajón. Empuja con todo el pie sin valgo de rodilla." },
          { num: 2, name: "Prensa de Piernas 45°", sub: "Incline Leg Press", img: "/img/ex_1_2.jpg", muscle: "Cuádriceps & Aductores", series: "3 series × 6-8 reps", weight: "+40 kg / lado", rest: "2.5 min", rir: "RIR 1", cue: "Pies anchura caderas. Cero despegue lumbar del respaldo." },
          { num: 3, name: "Extensión de Cuádriceps", sub: "Leg Extension en Máquina", img: "/img/ex_1_3.jpg", muscle: "Recto Femoral & VMO", series: "3 series × 8-10 reps", weight: "66 kg", rest: "90 seg", rir: "RIR 1", cue: "Aislamiento puro del recto femoral sin fatiga en columna." },
          { num: 4, name: "Gemelos de Pie con Barra", sub: "Standing Calf Raise", img: "/img/ex_1_4.jpg", muscle: "Gastrocnemio", series: "4 series × 6-8 reps", weight: "85 kg", rest: "90 seg", rir: "RIR 1", cue: "Pausa de 2s abajo para anular rebote tendinoso." },
          { num: 5, name: "Spanish Squat Isométrica con Banda", sub: "Blindaje VMO", img: "/img/ex_1_5.jpg", muscle: "Vasto Medial", series: "4 series × 35-40s", weight: "Banda Pesada", rest: "60 seg", rir: "RIR 0", cue: "Tibias verticales a 70°-80°. Reclutamiento máximo del vasto medial." },
          { num: 6, name: "Rueda Abdominal (Core)", sub: "Ab Wheel Rollout", img: "/img/ex_1_6.jpg", muscle: "Core & Anti-extensión", series: "3 series × 8-10 reps", weight: "Autocarga", rest: "60 seg", rir: "RIR 1", cue: "Retroversión pélvica activa en todo el recorrido." }
        ]
      },
      2: {
        title: "Rutina 2 · Torso Tracción (Dorsal, Espalda Alta & Bíceps)",
        day: "Miércoles 17:30 • 50 min • RIR 1",
        exercises: [
          { num: 1, name: "Jalón Agarre Cerrado V", sub: "Close-Grip Lat Pulldown", img: "/img/ex_2_1.jpg", muscle: "Dorsal Ancho", series: "4 series × 4-6 reps", weight: "54 - 59 kg", rest: "2.5 min", rir: "RIR 1", cue: "Codos hacia abajo y adentro apretando el dorsal." },
          { num: 2, name: "Remo Dorian Unilateral", sub: "One-Arm Dumbbell Row", img: "/img/ex_2_2.jpg", muscle: "Dorsal & Espalda Media", series: "3 series × 6-8 reps", weight: "28 - 30 kg", rest: "2.0 min", rir: "RIR 1", cue: "Tracción hacia el bolsillo trasero, codo pegado al costado." },
          { num: 3, name: "Remo Gironda con Agarre Amplio", sub: "Seated Cable Row", img: "/img/ex_2_3.jpg", muscle: "Espalda Alta & Romboides", series: "3 series × 8-10 reps", weight: "36 kg", rest: "90 seg", rir: "RIR 1", cue: "Retracción escapular máxima en el punto de contracción." },
          { num: 4, name: "Face Pull en Polea Alta", sub: "Cable Face Pull", img: "/img/ex_2_4.jpg", muscle: "Deltoides Post. & Manguito", series: "3 series × 10-12 reps", weight: "23 - 27 kg", rest: "60 seg", rir: "RIR 2", cue: "Cuerda a la frente con rotación externa de hombro." },
          { num: 5, name: "Curl Bíceps Mancuernas Inclinado", sub: "Incline Dumbbell Curl", img: "/img/ex_2_5.jpg", muscle: "Bíceps (Cabeza Larga)", series: "3 series × 8-10 reps", weight: "12 kg / mano", rest: "90 seg", rir: "RIR 1", cue: "Estiramiento máximo con los codos perpendiculares al suelo." },
          { num: 6, name: "Curl en Banco Scott / Predicador", sub: "Preacher Curl", img: "/img/ex_2_6.jpg", muscle: "Braquial & Bíceps", series: "3 series × 8-10 reps", weight: "25 kg", rest: "90 seg", rir: "RIR 1", cue: "Aislamiento estricto sin balanceo del torso." }
        ]
      },
      3: {
        title: "Rutina 3 · Pierna 2 (Cadena Posterior & Blindaje Isquios)",
        day: "Jueves/Viernes 17:30 • 50 min • RIR 1",
        exercises: [
          { num: 1, name: "Hip Thrust con Barra", sub: "Barbell Hip Thrust en Banco", img: "/img/ex_3_1.jpg", muscle: "Glúteo Mayor (Blindaje Carrera)", series: "4 series × 4-6 reps", weight: "130 - 140 kg", rest: "3.0 min", rir: "RIR 1", cue: "Parada de 1s arriba con retroversión pélvica y mentón pegado." },
          { num: 2, name: "Peso Muerto Rumano Unilateral / Staggered", sub: "Single-Leg / Staggered RDL", img: "/img/ex_3_2.jpg", muscle: "Isquiotibiales (MTJ proximal)", series: "3 series × 6-8 reps", weight: "20 - 24 kg / mano", rest: "2.0 min", rir: "RIR 1-2", cue: "Bisagra de cadera pura con espalda neutra y tensión excéntrica." },
          { num: 3, name: "Prensa Pies Altos y Anchos", sub: "High Foot Stance Leg Press", img: "/img/ex_3_3.jpg", muscle: "Glúteos & Aductores", series: "3 series × 6-8 reps", weight: "+40 - 45 kg / lado", rest: "2.5 min", rir: "RIR 1", cue: "Empuje de talones reduciendo el estrés en el tendón rotuliano." },
          { num: 4, name: "Sóleo Sentado en Máquina", sub: "Seated Calf Raise", img: "/img/ex_3_4.jpg", muscle: "Sóleo (Amortiguación de Carrera)", series: "4 series × 8-10 reps", weight: "40 kg", rest: "90 seg", rir: "RIR 1", cue: "El sóleo absorbe hasta 8x el peso corporal en cada zancada." },
          { num: 5, name: "Curl Femoral Tumbado", sub: "Lying Leg Curl (HSR)", img: "/img/ex_3_5.jpg", muscle: "Isquiotibiales (Bíceps Femoral)", series: "3 series × 6-8 reps", weight: "42 kg", rest: "2.0 min", rir: "RIR 1", cue: "Frena la fase excéntrica en 3s para blindar la unión miotendinosa." },
          { num: 6, name: "Elevaciones de Piernas Colgado", sub: "Hanging Leg Raise", img: "/img/ex_3_6.jpg", muscle: "Core & Flexores de Cadera", series: "3 series × 10-12 reps", weight: "Autocarga", rest: "60 seg", rir: "RIR 1", cue: "Sube las piernas en L a 90° flexionando la pelvis sin balanceo." }
        ]
      },
      4: {
        title: "Rutina 4 · Torso Empuje (Pectoral, Hombro & Tríceps)",
        day: "Sábado 11:00 • 50 min • RIR 1-2",
        exercises: [
          { num: 1, name: "Press de Banca Plano", sub: "Barbell Bench Press", img: "/img/ex_4_1.jpg", muscle: "Pectoral Mayor & Tríceps", series: "4 series × 4-6 reps", weight: "60 - 65 kg", rest: "2.5 min", rir: "RIR 1-2", cue: "Escápulas retraídas, barra al esternón y empuje firme." },
          { num: 2, name: "Press Inclinado con Mancuernas 30°", sub: "Incline Dumbbell Press", img: "/img/ex_4_2.jpg", muscle: "Pectoral Clavicular & Deltoides Ant.", series: "3 series × 6-8 reps", weight: "22 kg / mano", rest: "2.0 min", rir: "RIR 1", cue: "Banca a 30° para activación máxima de la porción superior." },
          { num: 3, name: "Pec Deck / Contractor", sub: "Machine Flyes", img: "/img/ex_4_3.jpg", muscle: "Pectoral (Aislamiento)", series: "3 series × 8-10 reps", weight: "50 kg", rest: "90 seg", rir: "RIR 1", cue: "Cierre al esternón con compresión isométrica de 1s." },
          { num: 4, name: "Elevaciones Laterales con Mancuernas", sub: "Dumbbell Lateral Raise", img: "/img/ex_4_4.jpg", muscle: "Deltoides Lateral", series: "4 series × 10-12 reps", weight: "10 kg / mano", rest: "60 seg", rir: "RIR 1", cue: "Eleva en el plano escapular liderando con los codos." },
          { num: 5, name: "Tríceps en Polea con Cuerda", sub: "Triceps Rope Pushdown", img: "/img/ex_4_5.jpg", muscle: "Tríceps (Cabeza Lateral)", series: "3 series × 8-10 reps", weight: "25 kg", rest: "60 seg", rir: "RIR 1", cue: "Abre la cuerda al final bloqueando el tríceps abajo." },
          { num: 6, name: "Plancha Frontal Core Estricta", sub: "RKC Plank", img: "/img/ex_4_6.jpg", muscle: "Core & Anti-extensión", series: "3 series × 40-45s", weight: "Autocarga", rest: "60 seg", rir: "RIR 0", cue: "Tensión de glúteos y abdomen como una tabla de piedra." }
        ]
      }
    };

    function handleImgError(img) {
      img.onerror = null;
      img.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200"><rect width="400" height="200" fill="%231D1E2C"/><text x="50%" y="50%" fill="%238E8FA3" font-family="sans-serif" font-size="14" text-anchor="middle" dominant-baseline="middle">Ejercicio Visual (PDF)</text></svg>';
    }

    function switchTab(tabId) {
      const tabs = ['dashboard', 'workouts', 'gym', 'goals'];
      tabs.forEach(t => {
        const el = document.getElementById('tab-' + t);
        if (el) el.classList.toggle('hidden', t !== tabId);

        // Sidebar Desktop
        const deskBtn = document.getElementById('nav-desktop-' + t);
        if (deskBtn) {
          deskBtn.classList.toggle('active-nav-link', t === tabId);
          deskBtn.classList.toggle('text-[#FF5E80]', t === tabId);
          deskBtn.classList.toggle('text-[#8E8FA3]', t !== tabId);
        }

        // Mobile Pills
        const mobBtn = document.getElementById('nav-mobile-' + t);
        if (mobBtn) {
          mobBtn.className = t === tabId 
            ? "px-4 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap bg-[#FF5E80] text-white glow-pink"
            : "px-4 py-2 rounded-xl text-xs font-bold transition whitespace-nowrap bg-[#1D1E2C] text-[#8E8FA3] border border-[#2D2F45]";
        }

        // Mobile Dock
        const dockBtn = document.getElementById('dock-btn-' + t);
        if (dockBtn) {
          dockBtn.classList.toggle('text-[#FF5E80]', t === tabId);
          dockBtn.classList.toggle('text-[#8E8FA3]', t !== tabId);
        }
      });

      const headerTitle = document.getElementById('header-title');
      if (headerTitle) {
        if (tabId === 'dashboard') headerTitle.innerText = 'Dashboard';
        else if (tabId === 'workouts') headerTitle.innerText = 'Entrenamientos';
        else if (tabId === 'gym') headerTitle.innerText = 'Gimnasio & Registro';
        else if (tabId === 'goals') headerTitle.innerText = 'Objetivos & Ritmos';
      }

      if (tabId === 'gym') {
        selectGymRoutine(3);
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function toggleDayAccordion(idx) {
      const body = document.getElementById('day-body-' + idx);
      const icon = document.getElementById('day-icon-' + idx);
      if (!body) return;
      const isHidden = body.classList.contains('hidden');
      body.classList.toggle('hidden', !isHidden);
      if (icon) {
        icon.style.transform = isHidden ? 'rotate(180deg)' : 'rotate(0deg)';
      }
    }

    function goToGymRoutine(routineId) {
      switchTab('gym');
      selectGymRoutine(routineId);
    }

    function selectGymRoutine(routineId) {
      for (let i = 1; i <= 4; i++) {
        const btn = document.getElementById('gym-chip-' + i);
        if (!btn) continue;
        if (i === routineId) {
          btn.className = "p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#FF5E80] text-white border-[#FF5E80] font-semibold glow-pink";
          btn.querySelectorAll('span')[0].className = "text-[10px] uppercase font-extrabold text-white/80";
          btn.querySelectorAll('span')[1].className = "text-xs font-extrabold text-white mt-1";
          btn.querySelectorAll('span')[2].className = "text-[10px] text-white/80 mt-0.5";
        } else {
          btn.className = "p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#242638] border-[#2D2F45] text-[#8E8FA3] hover:border-[#FF5E80]";
          btn.querySelectorAll('span')[0].className = "text-[10px] uppercase font-bold text-[#8E8FA3]";
          btn.querySelectorAll('span')[1].className = "text-xs font-extrabold text-white mt-1";
          btn.querySelectorAll('span')[2].className = "text-[10px] text-[#8E8FA3] mt-0.5";
        }
      }

      const routine = gymRoutinesData[routineId];
      if (!routine) return;

      const container = document.getElementById('gym-exercises-container');
      let html = '<div class="luxury-card p-4 sm:p-5 flex items-center justify-between border-b border-[#2D2F45]">' +
        '<div>' +
          '<h3 class="text-base font-extrabold text-white">' + routine.title + '</h3>' +
          '<p class="text-xs text-[#FF5E80] font-medium mt-0.5">' + routine.day + '</p>' +
        '</div>' +
        '<span class="text-xs font-extrabold px-3 py-1 rounded-xl bg-[#242638] text-[#8E8FA3] border border-[#2D2F45]">' +
          routine.exercises.length + ' Ejercicios' +
        '</span>' +
      '</div>';

      routine.exercises.forEach(function(ex) {
        html += '<div class="luxury-card overflow-hidden shadow-xl">' +
          '<div class="relative w-full bg-[#141522] border-b border-[#2D2F45] flex items-center justify-center p-2">' +
            '<img src="' + ex.img + '" alt="' + ex.name + '" class="w-full max-h-56 sm:max-h-64 object-contain rounded-xl" loading="lazy" onerror="handleImgError(this)">' +
            '<span class="absolute top-4 left-4 px-2.5 py-1 rounded-lg bg-[#141522]/90 border border-[#2D2F45] text-[10px] font-extrabold text-[#7B88FF] uppercase tracking-wider backdrop-blur">' +
              ex.muscle +
            '</span>' +
          '</div>' +

          '<div class="p-5">' +
            '<div class="flex items-start justify-between gap-2">' +
              '<div>' +
                '<h4 class="text-base font-extrabold text-white leading-snug">' + ex.name + '</h4>' +
                '<p class="text-xs text-[#8E8FA3] mt-0.5">' + ex.sub + '</p>' +
              '</div>' +
            '</div>' +

            '<div class="grid grid-cols-2 sm:grid-cols-4 gap-2 my-4 text-center">' +
              '<div class="luxury-subcard p-2.5">' +
                '<div class="text-[10px] text-[#8E8FA3] uppercase font-bold">Series & Reps</div>' +
                '<div class="text-xs font-black text-white mt-0.5 font-mono">' + ex.series + '</div>' +
              '</div>' +
              '<div class="luxury-subcard p-2.5">' +
                '<div class="text-[10px] text-[#8E8FA3] uppercase font-bold">Carga Objetivo</div>' +
                '<div class="text-xs font-black text-[#FF5E80] mt-0.5 font-mono">' + ex.weight + '</div>' +
              '</div>' +
              '<div class="luxury-subcard p-2.5">' +
                '<div class="text-[10px] text-[#8E8FA3] uppercase font-bold">Descanso</div>' +
                '<div class="text-xs font-black text-white mt-0.5 font-mono">' + ex.rest + '</div>' +
              '</div>' +
              '<div class="luxury-subcard p-2.5">' +
                '<div class="text-[10px] text-[#8E8FA3] uppercase font-bold">Esfuerzo</div>' +
                '<div class="text-xs font-black text-[#7B88FF] mt-0.5 font-mono">' + ex.rir + '</div>' +
              '</div>' +
            '</div>' +

            '<div class="p-3 rounded-xl bg-[#242638] border border-[#2D2F45] text-xs text-[#8E8FA3] mb-4">' +
              '<strong class="text-white">Clave técnica:</strong> ' + ex.cue +
            '</div>' +

            '<!-- REGISTRO INTERACTIVO DE CARGAS -->' +
            '<div class="p-3.5 rounded-2xl bg-[#141522] border border-[#2D2F45] space-y-2.5">' +
              '<div class="flex items-center justify-between text-xs">' +
                '<span class="font-extrabold text-white flex items-center gap-1.5">' +
                  '<i data-lucide="edit-3" class="w-3.5 h-3.5 text-[#FF5E80]"></i> Tu Registro Real de Hoy' +
                '</span>' +
                '<span class="text-[10px] text-[#8E8FA3]">Auto-guardado local</span>' +
              '</div>' +
              '<div class="grid grid-cols-2 gap-2">' +
                '<div>' +
                  '<label class="text-[10px] text-[#8E8FA3] block mb-1 font-bold">CARGA USADA</label>' +
                  '<input type="text" id="log_weight_' + routineId + '_' + ex.num + '" placeholder="' + ex.weight + '" onchange="saveGymLog(' + routineId + ')" class="w-full bg-[#1D1E2C] border border-[#2D2F45] rounded-xl px-3 py-2 text-xs font-mono font-bold text-white focus:outline-none focus:border-[#FF5E80] transition">' +
                '</div>' +
                '<div>' +
                  '<label class="text-[10px] text-[#8E8FA3] block mb-1 font-bold">SERIES × REPS</label>' +
                  '<input type="text" id="log_reps_' + routineId + '_' + ex.num + '" placeholder="' + ex.series.replace(' series × ', 'x').replace(' reps', '') + '" onchange="saveGymLog(' + routineId + ')" class="w-full bg-[#1D1E2C] border border-[#2D2F45] rounded-xl px-3 py-2 text-xs font-mono font-bold text-white focus:outline-none focus:border-[#FF5E80] transition">' +
                '</div>' +
              '</div>' +
              '<div>' +
                '<input type="text" id="log_notes_' + routineId + '_' + ex.num + '" placeholder="Notas / RIR / Sensaciones..." onchange="saveGymLog(' + routineId + ')" class="w-full bg-[#1D1E2C] border border-[#2D2F45] rounded-xl px-3 py-2 text-xs text-white placeholder-[#5D5F76] focus:outline-none focus:border-[#FF5E80] transition">' +
              '</div>' +
            '</div>' +

          '</div>' +
        '</div>';
      });

      container.innerHTML = html;
      loadGymLog(routineId);
      lucide.createIcons();
    }

    function saveGymLog(routineId) {
      const routine = gymRoutinesData[routineId];
      if (!routine) return;
      const log = {};
      routine.exercises.forEach(function(ex) {
        const w = document.getElementById('log_weight_' + routineId + '_' + ex.num);
        const r = document.getElementById('log_reps_' + routineId + '_' + ex.num);
        const n = document.getElementById('log_notes_' + routineId + '_' + ex.num);
        log[ex.num] = {
          weight: w ? w.value : '',
          reps: r ? r.value : '',
          notes: n ? n.value : ''
        };
      });
      localStorage.setItem('aegis_gym_log_' + routineId, JSON.stringify(log));
    }

    function loadGymLog(routineId) {
      const raw = localStorage.getItem('aegis_gym_log_' + routineId);
      if (!raw) return;
      try {
        const log = JSON.parse(raw);
        for (const num in log) {
          const item = log[num];
          const w = document.getElementById('log_weight_' + routineId + '_' + num);
          const r = document.getElementById('log_reps_' + routineId + '_' + num);
          const n = document.getElementById('log_notes_' + routineId + '_' + num);
          if (w && item.weight) w.value = item.weight;
          if (r && item.reps) r.value = item.reps;
          if (n && item.notes) n.value = item.notes;
        }
      } catch (e) {}
    }

    function copyGymSessionToClipboard() {
      const activeBtn = document.querySelector('.gym-chip-active') || document.getElementById('gym-chip-3');
      let routineId = 3;
      for (let i = 1; i <= 4; i++) {
        const b = document.getElementById('gym-chip-' + i);
        if (b && b.classList.contains('bg-[#FF5E80]')) {
          routineId = i;
          break;
        }
      }

      saveGymLog(routineId);
      const routine = gymRoutinesData[routineId];
      const now = new Date();
      const dateStr = now.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
      
      const lines = [];
      lines.push('🏋️ REGISTRO DE GIMNASIO — ' + routine.title + ' (' + dateStr + ')');
      lines.push('Atleta: Carlos Jiménez Andrino');
      lines.push('----------------------------------------');

      routine.exercises.forEach(function(ex) {
        const w = document.getElementById('log_weight_' + routineId + '_' + ex.num);
        const r = document.getElementById('log_reps_' + routineId + '_' + ex.num);
        const n = document.getElementById('log_notes_' + routineId + '_' + ex.num);
        const weightVal = (w && w.value) ? w.value : ex.weight;
        const repsVal = (r && r.value) ? r.value : ex.series;
        const notesVal = (n && n.value) ? (' (' + n.value + ')') : '';
        lines.push('• ' + ex.name + ': ' + weightVal + ' | ' + repsVal + notesVal);
      });

      lines.push('----------------------------------------');
      lines.push('Blindaje Rodilla Izquierda: 0/10 Dolor (VMO activo)');

      const textToCopy = lines.join(String.fromCharCode(10));
      navigator.clipboard.writeText(textToCopy).then(function() {
        const btn = document.getElementById('copy-gym-btn');
        if (btn) {
          const original = btn.innerHTML;
          btn.innerHTML = '<i data-lucide="check" class="w-4 h-4"></i> ¡Copiado al Portapapeles!';
          btn.classList.add('bg-[#20D994]');
          lucide.createIcons();
          setTimeout(function() {
            btn.innerHTML = original;
            btn.classList.remove('bg-[#20D994]');
            lucide.createIcons();
          }, 2500);
        }
      });
    }

    // Inicialización del Calendario de 14 Días
    function renderWorkoutsAccordion() {
      const container = document.getElementById('workout-days-accordion');
      if (!container) return;

      let html = '';
      daysData.forEach(function(day, idx) {
        const isToday = day.date === todayISO;
        const isPast = day.date < todayISO;
        const isKey = day.is_key_session;

        let badgeHtml = '';
        if (isToday) {
          badgeHtml = '<span class="px-2.5 py-1 rounded-xl bg-[#FF5E80] text-white text-[10px] font-black uppercase tracking-wider glow-pink">HOY</span>';
        } else if (isPast) {
          badgeHtml = '<span class="px-2 py-0.5 rounded-lg bg-[#20D994]/20 text-[#20D994] border border-[#20D994]/30 text-[10px] font-bold">OK</span>';
        } else if (isKey) {
          badgeHtml = '<span class="px-2 py-0.5 rounded-lg bg-[#FF5E80]/20 text-[#FF5E80] border border-[#FF5E80]/30 text-[10px] font-bold">CLAVE</span>';
        } else {
          badgeHtml = '<span class="px-2 py-0.5 rounded-lg bg-[#242638] text-[#8E8FA3] text-[10px] font-bold">PEND</span>';
        }

        const borderClass = isToday ? 'border-[#FF5E80] glow-pink' : 'border-[#2D2F45]';
        const startOpen = isToday || (!daysData.some(d => d.date === todayISO) && idx === 0);

        html += '<div class="luxury-card ' + borderClass + ' overflow-hidden transition-all">' +
          '<div onclick="toggleDayAccordion(' + idx + ')" class="p-4 sm:p-5 flex items-center justify-between cursor-pointer hover:bg-[#242638]/40 transition select-none">' +
            '<div class="flex items-center gap-3">' +
              badgeHtml +
              '<div>' +
                '<div class="text-sm sm:text-base font-extrabold text-white">' + day.day_name + ' ' + day.display_date + '</div>' +
                '<div class="text-xs text-[#8E8FA3] mt-0.5 truncate max-w-[200px] sm:max-w-md">' +
                  (day.running.is_rest ? 'Descanso carrera' : day.running.title) + ' &bull; ' +
                  (day.gym.is_rest ? 'Descanso fuerza' : day.gym.routine_name.split('·')[0]) +
                '</div>' +
              '</div>' +
            '</div>' +
            '<div class="flex items-center gap-2">' +
              '<i data-lucide="chevron-down" id="day-icon-' + idx + '" class="w-5 h-5 text-[#8E8FA3] transition-transform duration-200" style="transform: ' + (startOpen ? 'rotate(180deg)' : 'rotate(0deg)') + '"></i>' +
            '</div>' +
          '</div>' +

          '<div id="day-body-' + idx + '" class="' + (startOpen ? '' : 'hidden') + ' px-4 pb-5 sm:px-5 sm:pb-6 pt-2 border-t border-[#2D2F45]/60 space-y-4">' +
            '<!-- Running -->' +
            (day.running.is_rest ? 
              '<div class="p-3.5 rounded-2xl bg-[#242638] text-xs text-[#8E8FA3]">🏃 Descanso de carrera</div>' :
              '<div class="luxury-subcard p-4 space-y-3">' +
                '<div class="flex items-center justify-between">' +
                  '<span class="text-xs font-extrabold text-[#FF5E80] flex items-center gap-1.5">' +
                    '<i data-lucide="footprints" class="w-4 h-4"></i> ' + day.running.title +
                  '</span>' +
                  '<span class="text-xs font-mono font-black text-white">' + day.running.duration_min + ' min &bull; ' + day.running.target_distance_km + ' km</span>' +
                '</div>' +
                '<p class="text-xs text-white/90 leading-relaxed">' + day.running.main_work + '</p>' +
                '<div class="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs pt-1">' +
                  '<div class="p-2 rounded-xl bg-[#141522]"><span class="text-[#8E8FA3] block text-[10px]">RITMO:</span><strong class="text-white font-mono">' + day.running.target_pace + '</strong></div>' +
                  '<div class="p-2 rounded-xl bg-[#141522]"><span class="text-[#8E8FA3] block text-[10px]">ZONA FC:</span><strong class="text-[#FF5E80] font-mono">' + day.running.hr_zone + '</strong></div>' +
                  '<div class="p-2 rounded-xl bg-[#141522] col-span-2 sm:col-span-1"><span class="text-[#8E8FA3] block text-[10px]">ZAPATILLA:</span><strong class="text-white">' + day.running.shoes_recommended + '</strong></div>' +
                '</div>' +
              '</div>'
            ) +

            '<!-- Gym -->' +
            (day.gym.is_rest ? 
              '<div class="p-3.5 rounded-2xl bg-[#242638] text-xs text-[#8E8FA3]">🏋️ Descanso de gimnasio</div>' :
              '<div class="luxury-subcard p-4 space-y-3">' +
                '<div class="flex items-center justify-between">' +
                  '<span class="text-xs font-extrabold text-[#7B88FF] flex items-center gap-1.5">' +
                    '<i data-lucide="dumbbell" class="w-4 h-4"></i> ' + day.gym.routine_name +
                  '</span>' +
                  '<span class="text-[10px] font-bold px-2 py-0.5 rounded bg-[#7B88FF]/20 text-[#7B88FF]">RUTINA ' + day.gym.routine_id + '</span>' +
                '</div>' +
                '<div class="space-y-1.5">' +
                  day.gym.highlight_exercises.map(function(ex) {
                    return '<div class="flex items-center justify-between p-2 rounded-xl bg-[#141522] text-xs">' +
                      '<span class="text-white font-medium">' + ex.name + '</span>' +
                      '<span class="font-mono text-[#7B88FF] font-bold">' + ex.load + ' (' + ex.rir + ')</span>' +
                    '</div>';
                  }).join('') +
                '</div>' +
                '<button onclick="goToGymRoutine(' + day.gym.routine_id + ')" class="w-full py-2.5 rounded-xl bg-[#7B88FF]/15 border border-[#7B88FF]/30 text-[#7B88FF] text-xs font-extrabold hover:bg-[#7B88FF]/25 transition flex items-center justify-center gap-1.5">' +
                  '<i data-lucide="external-link" class="w-3.5 h-3.5"></i> Abrir Rutina ' + day.gym.routine_id + ' con Fotos Técnicas' +
                '</button>' +
              '</div>'
            ) +
          '</div>' +
        '</div>';
      });

      container.innerHTML = html;
      lucide.createIcons();
    }

    // Inicializar Gráficos Spline Area Dinámicos
    document.addEventListener("DOMContentLoaded", function() {
      lucide.createIcons();
      renderWorkoutsAccordion();
      selectGymRoutine(3);

      const ctxSpline = document.getElementById('weeklySplineChart')?.getContext('2d');
      if (ctxSpline) {
        // Crear gradientes tenues verticales
        const gradientPink = ctxSpline.createLinearGradient(0, 0, 0, 260);
        gradientPink.addColorStop(0, 'rgba(255, 94, 128, 0.45)');
        gradientPink.addColorStop(0.6, 'rgba(255, 94, 128, 0.1)');
        gradientPink.addColorStop(1, 'rgba(255, 94, 128, 0.0)');

        const gradientBlue = ctxSpline.createLinearGradient(0, 0, 0, 260);
        gradientBlue.addColorStop(0, 'rgba(123, 136, 255, 0.35)');
        gradientBlue.addColorStop(0.6, 'rgba(123, 136, 255, 0.08)');
        gradientBlue.addColorStop(1, 'rgba(123, 136, 255, 0.0)');

        const labels = weeklyData.map(w => w.label);
        const kmValues = weeklyData.map(w => w.run_km);
        const gymValues = weeklyData.map(w => w.gym_sessions);

        new Chart(ctxSpline, {
          type: 'line',
          data: {
            labels: labels,
            datasets: [
              {
                label: 'Volumen Run (km)',
                data: kmValues,
                borderColor: '#FF5E80',
                borderWidth: 3.5,
                backgroundColor: gradientPink,
                fill: true,
                tension: 0.4,
                cubicInterpolationMode: 'monotone',
                pointBackgroundColor: '#FF5E80',
                pointBorderColor: '#141522',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 7,
                yAxisID: 'y'
              },
              {
                label: 'Sesiones Gym',
                data: gymValues,
                borderColor: '#7B88FF',
                borderWidth: 2.5,
                backgroundColor: gradientBlue,
                fill: true,
                tension: 0.4,
                cubicInterpolationMode: 'monotone',
                pointBackgroundColor: '#7B88FF',
                pointBorderColor: '#141522',
                pointBorderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 6,
                yAxisID: 'y1'
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
              mode: 'index',
              intersect: false
            },
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: '#1D1E2C',
                titleColor: '#FFFFFF',
                bodyColor: '#9D9EA7',
                borderColor: '#2D2F45',
                borderWidth: 1,
                padding: 12,
                cornerRadius: 14,
                bodyFont: { family: 'Plus Jakarta Sans', size: 12 }
              }
            },
            scales: {
              x: {
                grid: { display: false },
                ticks: { color: '#8E8FA3', font: { family: 'Plus Jakarta Sans', size: 11, weight: '600' } }
              },
              y: {
                type: 'linear',
                display: true,
                position: 'left',
                grid: { color: 'rgba(255, 255, 255, 0.04)' },
                ticks: {
                  color: '#FF5E80',
                  font: { family: 'JetBrains Mono', size: 11 },
                  callback: function(v) { return v + ' km'; }
                }
              },
              y1: {
                type: 'linear',
                display: false,
                position: 'right',
                min: 0,
                max: 6,
                grid: { drawOnChartArea: false }
              }
            }
          }
        });
      }
    });
  </script>
</body>
</html>`;
}
'''

with open('cloudflare/src/index.ts', 'w', encoding='utf-8') as f:
    f.write(worker_ts_content)

print(f"Generado exitosamente cloudflare/src/index.ts (Tamaño: {len(worker_ts_content)} bytes)")
