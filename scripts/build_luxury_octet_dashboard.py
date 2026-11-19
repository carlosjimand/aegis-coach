import json
import os

print("Construyendo el nuevo index.ts v4 con Aero-Aegis, Subvistas de Calendario/Microciclo, Edición de Perfil y Chips actualizados...")

with open('cloudflare/plan.json', 'r', encoding='utf-8') as f:
    plan_json = json.load(f)

with open('data/weekly_evolution.json', 'r', encoding='utf-8') as f:
    weekly_evo = json.load(f)

display_weeks = [w for w in weekly_evo if w['run_km'] > 0 or w['week_start'] >= '2026-09-28']
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
        w['label'] = short_labels[w['week_start']]
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

# Calendario Multi-Mes Oficial (Septiembre a Diciembre 2026) con datos de Garmin/FIT
with open('data/full_multi_month_calendar.json', 'r', encoding='utf-8') as f:
    multi_month_calendar = json.load(f)

def make_aero_svg(prefix="aero"):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">
  <defs>
    <linearGradient id="{prefix}_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c5abde"/>
      <stop offset="50%" stop-color="#a887ce"/>
      <stop offset="100%" stop-color="#70559f"/>
    </linearGradient>
    <linearGradient id="{prefix}_coral" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e885a6"/>
      <stop offset="50%" stop-color="#d86991"/>
      <stop offset="100%" stop-color="#9c526d"/>
    </linearGradient>
    <linearGradient id="{prefix}_core" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#d86991"/>
      <stop offset="100%" stop-color="#a887ce"/>
    </linearGradient>
    <linearGradient id="{prefix}_wing" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#d86991"/>
    </linearGradient>
  </defs>
  <path d="M 50 14 C 38 12, 22 18, 16 32 C 11 48, 16 68, 32 82 C 40 88, 47 92, 50 93 C 44 86, 28 76, 25 61 C 22 47, 28 34, 40 26 C 44 23, 48 18, 50 14 Z" fill="url(#{prefix}_blue)"/>
  <path d="M 50 14 C 62 12, 78 18, 84 32 C 89 48, 84 68, 68 82 C 60 88, 53 92, 50 93 C 56 86, 72 76, 75 61 C 78 47, 72 34, 60 26 C 56 23, 52 18, 50 14 Z" fill="url(#{prefix}_coral)"/>
  <path d="M 50 26 C 52 26, 61 46, 65 62 C 66 66, 62 68, 57 67 C 54 62, 53 56, 50 56 C 47 56, 46 62, 43 67 C 38 68, 34 66, 35 62 C 39 46, 48 26, 50 26 Z" fill="url(#{prefix}_core)"/>
  <path d="M 22 57 C 35 53, 65 53, 78 57 C 68 61, 32 61, 22 57 Z" fill="url(#{prefix}_wing)"/>
</svg>'''

header_logo_svg = make_aero_svg("hdr")
aside_logo_svg = make_aero_svg("aside")
profile_logo_svg = make_aero_svg("prof")
favicon_svg = make_aero_svg("fav")

# Encode for favicon data uri
import urllib.parse
favicon_data_uri = "data:image/svg+xml," + urllib.parse.quote(favicon_svg)
worker_ts = '''/**
 * Aegis Coach — Sistema de Inteligencia y Coaching de Carlos Jiménez Andrino
 * Cloudflare Worker + Dynamic PWA Dashboard v3
 * Versión de Alto Rendimiento:
 * - Logo Fluido Monograma 'A' (Aero Wing)
 * - Calendario Mensual con Puntos de Color & Análisis IA
 * - Registro Serie a Serie (Orden: Serie - Reps - Carga - Acción)
 * - Perfil de Usuario con Calculadora e Indicador de IMC
 * - Reorganización de Dashboard (Sesión de Hoy arriba del todo)
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
const CALENDAR_DATA_BY_MONTH: any = ''' + json.dumps(multi_month_calendar, indent=2, ensure_ascii=False) + ''';

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Web App Manifest para Android Chrome y PWA
    if (url.pathname === "/manifest.json") {
      const manifest = {
        name: "Aegis Coach",
        short_name: "Aegis",
        description: "Sistema de Inteligencia y Coaching de Carlos Jiménez Andrino",
        start_url: "/",
        display: "standalone",
        background_color: "#171821",
        theme_color: "#171821",
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
    }

    // Endpoint: Guardar Sesión de Gimnasio
    if (url.pathname === "/api/save_gym_session" && request.method === "POST") {
      try {
        const body: any = await request.json();
        const date = body.date || getTodayMadridISO();
        const key = "gym_session_" + date;
        await env.AEGIS_KV.put(key, JSON.stringify(body));
        return new Response(JSON.stringify({ ok: true, key }), {
          headers: { "Content-Type": "application/json" }
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { "Content-Type": "application/json" } });
      }
    }

    // Endpoint: Guardar Perfil de Usuario (Peso, Altura, etc.)
    if (url.pathname === "/api/save_profile" && request.method === "POST") {
      try {
        const body: any = await request.json();
        await env.AEGIS_KV.put("user_profile", JSON.stringify(body));
        return new Response(JSON.stringify({ ok: true }), {
          headers: { "Content-Type": "application/json" }
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { "Content-Type": "application/json" } });
      }
    }

    // Webhook de Telegram
    if (url.pathname === "/webhook" && request.method === "POST") {
      try {
        const update: any = await request.json();
        if (update && update.message) {
          await handleTelegramMessage(update.message, env);
        }
        return new Response("OK", { status: 200 });
      } catch (err: any) {
        return new Response("Error", { status: 500 });
      }
    }

    // Cargar plan desde KV o fallback maestro
    let planData: any = null;
    try {
      planData = await env.AEGIS_KV.get("current_plan", { type: "json" });
    } catch (e) {}
    if (!planData) planData = DEFAULT_PLAN;

    const html = getLuxuryDashboardHtml(planData);
    return new Response(html, {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-cache, no-store, must-revalidate"
      }
    });
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
    reply = "👋 *Aegis Coach Bot*\\n\\nComandos disponibles:\\n• `/hoy` - Entrenamiento programado para el día actual.\\n• `/semana` - Resumen del microciclo completo.\\n• `/rodilla` - Estado de salud y prevención articular.\\n• `/web` - Abrir la Web App Dashboard.";
  } else if (text === "/hoy") {
    const r = todayPlan.running;
    const g = todayPlan.gym;
    reply = `🏃 *ENTRENAMIENTO DE HOY* (${todayPlan.day_name} ${todayPlan.date}):\\n\\n` +
      `• *Running:* ${r.is_rest ? "Descanso" : `${r.title} (${r.duration_min} min, ${r.target_distance_km} km @ ${r.target_pace}, ${r.hr_zone})`}\\n` +
      `• *Fuerza:* ${g.is_rest ? "Descanso" : `${g.routine_name} (${g.focus})`}\\n\\n` +
      `🌐 [Ver Dashboard y Series](https://aegis-intervals-sync.uranuslabs.workers.dev)`;
  } else if (text === "/semana") {
    reply = `📅 *PLAN SEMANAL EN CURSO* (Semana del ${days[0]?.date || ""}):\\n\\n` +
      days.map((d: any) => `• *${d.day_name.substring(0, 3)} ${d.date.substring(5)}:* ${d.running.is_rest ? "Descanso run" : d.running.session_type} | ${d.gym.is_rest ? "Descanso gym" : d.gym.routine_name.split("·")[0]}`).join("\\n") +
      `\\n\\n🌐 [Abrir Web App](https://aegis-intervals-sync.uranuslabs.workers.dev)`;
  } else if (text === "/rodilla") {
    reply = "🛡️ *BLINDAJE ARTICULAR & ISQUIOS*\\n\\n• *Rodilla Izquierda:* 0/10 Dolor (Derrame reactivo totalmente reabsorbido).\\n• *Isquiotibial MTJ:* 0/10 Dolor. Asintomático y blindado con Hip Thrust y RDL unilateral.";
  } else if (text === "/web") {
    reply = "🌐 Accede a tu Web App Dashboard aquí:\\nhttps://aegis-intervals-sync.uranuslabs.workers.dev";
  } else {
    reply = "Comando no reconocido. Escribe `/hoy` para ver tu sesión actual o `/ayuda`.";
  }

  await fetch(`https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`, {
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

  // Sesión de hoy dinámica
  const days: any[] = planData.days || [];
  const todayPlan = days.find((d: any) => d.date === todayISO) || days[0];

  return `<!DOCTYPE html>
<html lang="es" class="h-full">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover">
  <title>Aegis Coach — Carlos Jiménez Andrino</title>
  <link rel="manifest" href="/manifest.json?v=6">
  <link rel="icon" type="image/png" sizes="192x192" href="/img/icon-192.png?v=6">
  <link rel="icon" type="image/svg+xml" href="' + favicon_data_uri + '">
  <link rel="apple-touch-icon" sizes="180x180" href="/img/icon-192.png?v=6">
  <link rel="shortcut icon" href="/favicon.ico?v=6">
  <meta name="theme-color" content="#171821">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Aegis Coach">
  
  <!-- Tipografía: Plus Jakarta Sans & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    :root {
      /* Paleta Oficial Octet Interactive Dashboards */
      --river-styx: #171821;        /* Fondo base */
      --jaguar: #292631;            /* Superficie de tarjetas */
      --stone-violet: #4d3e50;      /* Bordes y divisores */
      --composers-magic: #A297A6;   /* Texto secundario / muteado */
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
    }
    .glow-pink {
      box-shadow: 0 8px 30px -4px rgba(216, 105, 145, 0.30);
    }
    .glow-purple {
      box-shadow: 0 8px 30px -4px rgba(168, 135, 206, 0.30);
    }
    .bg-gradient-hero {
      background: linear-gradient(135deg, #a887ce 0%, #a272a4 40%, #9c526d 100%);
    }
    .active-nav-link {
      color: #d86991 !important;
      background-color: rgba(216, 105, 145, 0.12);
      border: 1px solid rgba(216, 105, 145, 0.25);
    }
    .scrollbar-none::-webkit-scrollbar {
      display: none;
    }
    .scrollbar-none {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
  </style>
</head>
<body class="h-full flex flex-col bg-[#171821] text-white">

  <!-- =================================================== -->
  <!-- LAYOUT PRINCIPAL -->
  <!-- =================================================== -->
  <div class="flex-1 flex flex-col lg:flex-row min-h-screen">

    <!-- SIDEBAR ESCRITORIO -->
    <aside class="hidden lg:flex w-24 flex-col items-center py-6 border-r border-[#4d3e50] bg-[#171821] fixed top-0 bottom-0 left-0 z-30">
      <!-- Monograma Logo SVG -->
      <div onclick="switchTab('dashboard')" class="w-12 h-12 rounded-2xl flex items-center justify-center cursor-pointer transition hover:scale-105 mb-8">
        ''' + aside_logo_svg + '''
      </div>

      <!-- Iconos de Navegación Vertical -->
      <div class="flex flex-col gap-6 items-center flex-1">
        <button onclick="switchTab('dashboard')" id="nav-desktop-dashboard" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#d86991] active-nav-link transition hover:text-white" title="Dashboard">
          <i data-lucide="layout-grid" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('workouts')" id="nav-desktop-workouts" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#A297A6] transition hover:text-white" title="Entrenos & Calendario">
          <i data-lucide="calendar" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('gym')" id="nav-desktop-gym" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#A297A6] transition hover:text-white" title="Gimnasio & Series">
          <i data-lucide="dumbbell" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('goals')" id="nav-desktop-goals" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#A297A6] transition hover:text-white" title="Objetivos">
          <i data-lucide="target" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('profile')" id="nav-desktop-profile" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#A297A6] transition hover:text-white" title="Perfil & IMC">
          <i data-lucide="user" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Botón Telegram en Sidebar -->
      <a href="https://t.me/aegis_coach_chatbot" target="_blank" class="w-11 h-11 rounded-2xl bg-[#292631] border border-[#4d3e50] text-[#a887ce] flex items-center justify-center hover:border-[#a887ce] transition" title="Bot de Telegram">
        <i data-lucide="send" class="w-4 h-4"></i>
      </a>
    </aside>

    <!-- CONTENEDOR CENTRAL -->
    <main class="flex-1 lg:pl-24 pb-28 lg:pb-12 flex flex-col min-w-0">
      
      <!-- TOPBAR / HEADER LIMPIO (Sin Buscador, Sin PRO, Sin Kilos Fijos) -->
      <header class="h-20 border-b border-[#4d3e50] px-4 sm:px-8 flex items-center justify-between bg-[#171821]/90 backdrop-blur sticky top-0 z-20">
        <div class="flex items-center gap-3 sm:gap-4">
          <!-- Monograma Logo -->
          <div onclick="switchTab('dashboard')" class="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl flex items-center justify-center cursor-pointer transition hover:scale-105 flex-shrink-0">
            ''' + header_logo_svg + '''
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-base sm:text-lg font-black tracking-tight text-white">AEGIS COACH</span>
            </div>
            <p class="text-[11px] sm:text-xs text-[#A297A6] font-medium leading-none mt-0.5">
              Carlos Jiménez Andrino &bull; Fisiología & Rendimiento
            </p>
          </div>
        </div>

        <div class="flex items-center gap-2 sm:gap-3">
          <!-- Acceso Perfil Rápido -->
          <button onclick="switchTab('profile')" class="px-3 py-1.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-white hover:border-[#a887ce] text-xs font-bold transition flex items-center gap-1.5">
            <i data-lucide="user" class="w-3.5 h-3.5 text-[#a887ce]"></i>
            <span class="hidden sm:inline">Perfil & IMC</span>
          </button>
          
          <!-- Botón Telegram -->
          <a href="https://t.me/aegis_coach_chatbot" target="_blank" class="px-3.5 py-1.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-[#A297A6] hover:text-white hover:border-[#a887ce] text-xs font-bold transition flex items-center gap-1.5">
            <i data-lucide="send" class="w-3.5 h-3.5 text-[#a887ce]"></i>
            <span class="hidden sm:inline">Bot Telegram</span>
          </a>
        </div>
      </header>

      <!-- CONTENIDO DE PESTAÑAS -->
      <div class="p-4 sm:p-8 max-w-7xl w-full mx-auto space-y-6">

        <!-- ========================================== -->
        <!-- PESTAÑA 1: DASHBOARD -->
        <!-- ========================================== -->
        <section id="tab-dashboard" class="space-y-6">

          <!-- 1. BLOQUE SESIÓN DE HOY (NOTIFICACIÓN MINIMALISTA & IMPACTANTE) -->
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
          </div>

          <!-- 2. TRES KPIS PRINCIPALES (ESTILO REFERENCIA INVESTMENT & DEPOSIT CON BARRA HORIZONTAL) -->
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
          </div>

          <!-- 3. GRÁFICO SPLINE DE EVOLUCIÓN DE VOLUMEN SEMANAL (KM REALES & GIMNASIO - ESTILO REFERENCIA EXACTO) -->
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
            </div>

            <!-- Canvas del Spline Chart -->
            <div class="h-64 sm:h-72 w-full relative">
              <canvas id="weeklySplineChart"></canvas>
            </div>

            <!-- Mini badges con las semanas clave -->
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
            </div>
          </div>

          <!-- 4. SESIONES CLAVE & PRÓXIMOS OBJETIVOS (DOS COLUMNAS) -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Columna Izquierda: 3 Sesiones Clave de Referencia -->
            <div class="luxury-card p-6">
              <div class="flex items-center justify-between mb-4">
                <h4 class="text-sm font-extrabold text-white flex items-center gap-2">
                  <i data-lucide="flame" class="w-4 h-4 text-[#d86991]"></i>
                  <span>3 Sesiones Clave de Referencia</span>
                </h4>
                <span class="text-[11px] text-[#A297A6]">Memoria Cuantitativa</span>
              </div>

              <div class="space-y-3">
                <div class="flex items-center justify-between p-3 rounded-2xl bg-[#292631] border border-[#4d3e50]">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-[#d86991]/20 text-[#d86991] flex items-center justify-center">
                      <i data-lucide="trophy" class="w-4 h-4"></i>
                    </div>
                    <div>
                      <div class="text-xs font-bold text-white">10K Ávila Monumental</div>
                      <div class="text-[11px] text-[#A297A6]">08 Nov &bull; 1.070m altitud, viento y cuestas</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-sm font-extrabold text-white font-mono">38:26</div>
                    <div class="text-[10px] text-[#20D994] font-bold">3:50/km</div>
                  </div>
                </div>

                <div class="flex items-center justify-between p-3 rounded-2xl bg-[#292631] border border-[#4d3e50]">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-[#a887ce]/20 text-[#a887ce] flex items-center justify-center">
                      <i data-lucide="timer" class="w-4 h-4"></i>
                    </div>
                    <div>
                      <div class="text-xs font-bold text-white">6&times;800m Parque del Soto</div>
                      <div class="text-[11px] text-[#A297A6]">14 Nov &bull; Clavos 6mm en hierba/tierra &bull; rec 90"</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-sm font-extrabold text-white font-mono">3:00.0 avg</div>
                    <div class="text-[10px] text-[#d86991] font-bold">3:45/km real</div>
                  </div>
                </div>

                <div class="flex items-center justify-between p-3 rounded-2xl bg-[#292631] border border-[#4d3e50]">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-[#20D994]/20 text-[#20D994] flex items-center justify-center">
                      <i data-lucide="dumbbell" class="w-4 h-4"></i>
                    </div>
                    <div>
                      <div class="text-xs font-bold text-white">Rutina 3 &bull; Pierna 2 (Fuerza)</div>
                      <div class="text-[11px] text-[#A297A6]">13 Nov &bull; Hip Thrust + RDL Unilateral</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-sm font-extrabold text-white font-mono">140 kg</div>
                    <div class="text-[10px] text-[#a887ce] font-bold">RIR 1 &bull; 4 reps</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Columna Derecha: Próximos Objetivos & Cuenta Atrás -->
            <div class="luxury-card p-6">
              <div class="flex items-center justify-between mb-4">
                <h4 class="text-sm font-extrabold text-white flex items-center gap-2">
                  <i data-lucide="target" class="w-4 h-4 text-[#a887ce]"></i>
                  <span>Próximas Competiciones</span>
                </h4>
                <span class="text-[11px] text-[#A297A6]">Cuenta Atrás</span>
              </div>

              <div class="space-y-3">
                <!-- Objetivo 1: Cross del Soto -->
                <div class="p-3.5 rounded-2xl bg-[#292631] border border-[#d86991]/40 relative overflow-hidden">
                  <div class="flex items-center justify-between">
                    <div>
                      <span class="text-[10px] font-extrabold px-2 py-0.5 rounded bg-[#d86991]/20 text-[#d86991] uppercase">
                        28 Noviembre 2026
                      </span>
                      <h5 class="text-sm font-extrabold text-white mt-1">Cross Popular Parque del Soto</h5>
                      <p class="text-xs text-[#A297A6]">5 km en tierra/hierba @ 3:30/km (~17:30) &bull; Clavos 6mm</p>
                    </div>
                    <div class="text-right pl-3">
                      <div class="text-2xl font-black text-[#d86991] font-mono leading-none">${daysRemaining}</div>
                      <div class="text-[10px] text-[#A297A6] mt-1 font-semibold">días</div>
                    </div>
                  </div>
                </div>

                <!-- Objetivo 2: San Silvestre -->
                <div class="p-3.5 rounded-2xl bg-[#292631] border border-[#4d3e50]">
                  <div class="flex items-center justify-between">
                    <div>
                      <span class="text-[10px] font-extrabold px-2 py-0.5 rounded bg-[#a887ce]/20 text-[#a887ce] uppercase">
                        31 Diciembre 2026
                      </span>
                      <h5 class="text-sm font-extrabold text-white mt-1">San Silvestre</h5>
                      <p class="text-xs text-[#A297A6]">6.5 km @ sub 3:35/km &bull; Asfalto &bull; Zapatilla voladora</p>
                    </div>
                    <div class="text-right pl-3">
                      <div class="text-2xl font-black text-white font-mono leading-none">45</div>
                      <div class="text-[10px] text-[#A297A6] mt-1 font-semibold">días</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </section>

        <!-- ========================================== -->
        <!-- PESTAÑA 2: ENTRENAMIENTOS & CALENDARIO -->
        <!-- ========================================== -->
        <section id="tab-workouts" class="space-y-6 hidden">
          
          <!-- Segmented Control de Vista: Calendario vs Microciclo -->
          <div class="flex p-1 rounded-2xl bg-[#171821] border border-[#4d3e50] max-w-sm sm:max-w-md mx-auto">
            <button onclick="switchWorkoutSubView('calendar')" id="subview-btn-calendar" class="flex-1 py-2 px-3 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 bg-[#d86991] text-white shadow-lg">
              <i data-lucide="calendar" class="w-4 h-4"></i>
              <span>Calendario Mensual</span>
            </button>
            <button onclick="switchWorkoutSubView('microcycle')" id="subview-btn-microcycle" class="flex-1 py-2 px-3 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 text-[#A297A6] hover:text-white">
              <i data-lucide="list-checks" class="w-4 h-4"></i>
              <span>Próximos Entrenos</span>
            </button>
          </div>

          <!-- SUB-VISTA 1: CALENDARIO MENSUAL MINIMALISTA (ESTILO GOOGLE CALENDAR) -->
          <div id="workout-subview-calendar" class="space-y-6">
            <div class="luxury-card p-5 sm:p-7 space-y-4">
              <!-- Cabecera del Mes y Navegación -->
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-[#4d3e50]/60">
                <div>
                  <h3 class="text-lg font-black text-white flex items-center gap-2">
                    <i data-lucide="calendar" class="w-5 h-5 text-[#d86991]"></i>
                    <span>Calendario de Entrenamientos</span>
                  </h3>
                  <div class="flex items-center gap-3 text-xs text-[#A297A6] mt-1">
                    <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#d86991]"></span> Carrera</span>
                    <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#a887ce]"></span> Gimnasio</span>
                    <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#20D994]"></span> Evento / Descanso</span>
                  </div>
                </div>

                <div class="flex items-center gap-2 bg-[#292631] border border-[#4d3e50] rounded-xl px-3 py-1.5 text-xs font-bold text-white self-start sm:self-auto">
                  <button id="cal-btn-prev" onclick="changeCalendarMonth(-1)" class="text-[#A297A6] hover:text-white transition px-1 cursor-pointer">&larr;</button>
                  <span id="calendar-month-label" class="min-w-[110px] text-center">Noviembre 2026</span>
                  <button id="cal-btn-next" onclick="changeCalendarMonth(1)" class="text-[#A297A6] hover:text-white transition px-1 cursor-pointer">&rarr;</button>
                </div>
              </div>

              <!-- Días de la semana -->
              <div class="grid grid-cols-7 gap-1 sm:gap-2 text-center text-[10px] font-bold text-[#A297A6] uppercase tracking-wider py-1">
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
            <div id="calendar-day-detail" class="luxury-card p-6 border-l-4 border-l-[#d86991] space-y-3">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-2 border-b border-[#4d3e50]/60">
                <div class="flex items-center gap-2.5">
                  <span id="detail-date-badge" class="px-2.5 py-1 rounded-lg bg-[#d86991]/20 text-[#d86991] text-xs font-mono font-bold">16 NOV</span>
                  <h4 id="detail-title" class="text-base font-extrabold text-white">35 min Drenaje Z1 + Rutina 2</h4>
                </div>
                <span id="detail-type-badge" class="text-xs font-bold text-[#A297A6] font-mono">Sesión de Hoy</span>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono pt-1">
                <div class="p-2.5 rounded-xl bg-[#171821] border border-[#4d3e50]">
                  <span class="text-[10px] text-[#A297A6] uppercase block">Distancia</span>
                  <strong id="detail-km" class="text-white text-sm">7.0 km</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-[#171821] border border-[#4d3e50]">
                  <span class="text-[10px] text-[#A297A6] uppercase block">Duración</span>
                  <strong id="detail-time" class="text-white text-sm">35:00</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-[#171821] border border-[#4d3e50]">
                  <span class="text-[10px] text-[#A297A6] uppercase block">Ritmo</span>
                  <strong id="detail-pace" class="text-[#d86991] text-sm">4:55-5:10/km</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-[#171821] border border-[#4d3e50]">
                  <span class="text-[10px] text-[#A297A6] uppercase block">Zona / FC</span>
                  <strong id="detail-hr" class="text-[#20D994] text-sm">Z1 (&lt;145 ppm)</strong>
                </div>
              </div>

              <!-- Fisiología & Análisis IA del Coach -->
              <div class="p-3.5 rounded-xl bg-[#171821] border border-[#4d3e50] text-xs space-y-1">
                <span class="font-extrabold text-[#a887ce] text-[10px] uppercase tracking-wider block">Análisis Fisiológico del Coach:</span>
                <p id="detail-ai" class="text-white/90 leading-relaxed font-sans">
                  Sesión activa de hoy: Rodaje suave en asfalto llano + Rutina 2 (Espalda y Bíceps).
                </p>
              </div>

              <!-- Desglose de Vueltas Reales Garmin FIT -->
              <div id="detail-laps-section" class="hidden"></div>

              <!-- Notas de Carlos en Garmin -->
              <div id="detail-notes-section" class="hidden"></div>
            </div>
          </div>

          <!-- SUB-VISTA 2: PRÓXIMOS ENTRENOS (MICROCICLO ACORDEÓN) -->
          <div id="workout-subview-microcycle" class="space-y-4 hidden">
            <div id="workouts-accordion-container" class="space-y-4"></div>
          </div>

        </section>

        <!-- ========================================== -->
        <!-- PESTAÑA 3: GIMNASIO & REGISTRO SERIE A SERIE -->
        <!-- ========================================== -->
        <section id="tab-gym" class="space-y-6 hidden">

          <!-- Selector de las 4 Rutinas Oficiales -->
          <div class="luxury-card p-6">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 mb-4">
              <div>
                <span class="text-[10px] uppercase font-extrabold text-[#d86991] tracking-wider">
                  RUTINAS OFICIALES MAESTRAS (PDF PÁGS 1-4)
                </span>
                <h3 class="text-lg font-black text-white mt-0.5">Selecciona la Rutina de Gimnasio</h3>
                <p class="text-xs text-[#A297A6]">Sobrecarga progresiva: registra tus kilos y repeticiones serie a serie</p>
              </div>
              <div class="flex items-center gap-2 text-xs font-bold text-[#20D994]">
                <i data-lucide="check-circle" class="w-4 h-4"></i>
                <span>Sobrecarga: +2.5 kg al completar reps</span>
              </div>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <button onclick="selectGymRoutine(1)" id="gym-chip-1" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#292631] border-[#4d3e50] text-[#A297A6] hover:border-[#d86991]">
                <span class="text-[10px] uppercase font-bold text-[#A297A6]">Lunes 18:00</span>
                <span class="text-xs font-extrabold text-white mt-1">Pierna 1</span>
                <span class="text-[10px] text-[#A297A6] mt-0.5">Cuádriceps, Gemelos & Core</span>
              </button>

              <button onclick="selectGymRoutine(2)" id="gym-chip-2" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#d86991] text-white border-[#d86991] font-semibold glow-pink">
                <span class="text-[10px] uppercase font-bold text-[#A297A6]">Miércoles 17:30</span>
                <span class="text-xs font-extrabold text-white mt-1">Torso Tracción (Hoy)</span>
                <span class="text-[10px] text-[#A297A6] mt-0.5">Espalda & Bíceps</span>
              </button>

              <button onclick="selectGymRoutine(3)" id="gym-chip-3" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#292631] border-[#4d3e50] text-[#A297A6] hover:border-[#d86991]">
                <span class="text-[10px] uppercase font-extrabold text-white/80">Jueves/Viernes</span>
                <span class="text-xs font-extrabold text-white mt-1">Pierna 2</span>
                <span class="text-[10px] text-white/80 mt-0.5">Glúteo, Femoral & Sóleo</span>
              </button>

              <button onclick="selectGymRoutine(4)" id="gym-chip-4" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#292631] border-[#4d3e50] text-[#A297A6] hover:border-[#d86991]">
                <span class="text-[10px] uppercase font-bold text-[#A297A6]">Sábado 11:00</span>
                <span class="text-xs font-extrabold text-white mt-1">Torso Empuje</span>
                <span class="text-[10px] text-[#A297A6] mt-0.5">Pecho, Hombro & Tríceps</span>
              </button>
            </div>
          </div>

          <!-- Contenedor de Ejercicios con Tarjetas Vectoriales y Registro Serie a Serie -->
          <div id="gym-exercises-container" class="space-y-6"></div>

          <!-- Resumen Markdown para Garmin / Intervals -->
          <div class="luxury-card p-6 space-y-4">
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <h4 class="text-base font-extrabold text-white flex items-center gap-2">
                  <i data-lucide="file-text" class="w-5 h-5 text-[#d86991]"></i>
                  <span>Resumen Markdown para Notas de Garmin & Coach</span>
                </h4>
                <p class="text-xs text-[#A297A6] mt-0.5">Generado en tiempo real con las repeticiones y kilos anotados hoy.</p>
              </div>

              <button onclick="copyGymSessionToClipboard()" id="copy-gym-btn" class="px-5 py-2.5 rounded-xl bg-[#d86991] text-white font-extrabold text-xs transition hover:brightness-110 glow-pink flex items-center gap-2">
                <i data-lucide="copy" class="w-4 h-4"></i>
                <span id="copy-btn-text">Copiar para Notas de Garmin</span>
              </button>
            </div>

            <!-- Previsualización Markdown -->
            <div class="relative">
              <textarea id="markdown-summary-preview" readonly class="w-full h-40 bg-[#171821] border border-[#4d3e50] rounded-2xl p-4 font-mono text-xs text-[#9D9EA7] resize-none focus:outline-none"></textarea>
            </div>
          </div>

        </section>

        <!-- ========================================== -->
        <!-- PESTAÑA 4: OBJETIVOS & RITMOS RENOVADA -->
        <!-- ========================================== -->
        <section id="tab-goals" class="space-y-6 hidden">

          <!-- HERO CARDS DE COMPETICIONES -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Objetivo 1: Cross del Soto -->
            <div class="luxury-card p-6 border-t-4 border-t-[#d86991] flex flex-col justify-between space-y-4">
              <div>
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black px-3 py-1 rounded-full bg-[#d86991]/20 text-[#d86991]">
                    OBJETIVO INMEDIATO &bull; 28 NOV 2026
                  </span>
                  <span class="text-xs font-mono font-bold text-[#A297A6]">${daysRemaining} días restantes</span>
                </div>
                <h3 class="text-xl font-black text-white mt-3">Cross Popular Parque del Soto (Ávila)</h3>
                <p class="text-xs text-[#A297A6] mt-1 leading-relaxed">5 km en terreno deformable (hierba y tierra). Exige máxima rigidez miotendinosa y clavos de 6mm para compensar las curvas sin peralte.</p>
              </div>

              <div class="grid grid-cols-3 gap-2 text-center pt-2 border-t border-[#4d3e50]">
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#A297A6]">Distancia</div>
                  <div class="text-sm font-extrabold text-white font-mono">5.0 km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#A297A6]">Ritmo Meta</div>
                  <div class="text-sm font-extrabold text-[#d86991] font-mono">3:30/km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#A297A6]">Tiempo Obj</div>
                  <div class="text-sm font-extrabold text-[#20D994] font-mono">~17:30</div>
                </div>
              </div>
            </div>

            <!-- Objetivo 2: San Silvestre -->
            <div class="luxury-card p-6 border-t-4 border-t-[#a887ce] flex flex-col justify-between space-y-4">
              <div>
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black px-3 py-1 rounded-full bg-[#a887ce]/20 text-[#a887ce]">
                    OBJETIVO FIN DE AÑO &bull; 31 DIC 2026
                  </span>
                  <span class="text-xs font-mono font-bold text-[#A297A6]">45 días restantes</span>
                </div>
                <h3 class="text-xl font-black text-white mt-3">San Silvestre</h3>
                <p class="text-xs text-[#A297A6] mt-1 leading-relaxed">6.5 km sobre asfalto urbano frío. Reactividad pura y zapatilla voladora con placa de carbono para exprimir el umbral submáximo.</p>
              </div>

              <div class="grid grid-cols-3 gap-2 text-center pt-2 border-t border-[#4d3e50]">
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#A297A6]">Distancia</div>
                  <div class="text-sm font-extrabold text-white font-mono">6.5 km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#A297A6]">Ritmo Meta</div>
                  <div class="text-sm font-extrabold text-[#a887ce] font-mono">sub 3:35/km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#A297A6]">Tiempo Obj</div>
                  <div class="text-sm font-extrabold text-[#20D994] font-mono">~23:15</div>
                </div>
              </div>
            </div>
          </div>

          <!-- TABLA VISUAL DE RITMOS DE COMPETICIÓN VS ZONAS DE ENTRENAMIENTO -->
          <div class="luxury-card p-6 sm:p-8">
            <h4 class="text-base font-extrabold text-white flex items-center gap-2 mb-4">
              <i data-lucide="gauge" class="w-5 h-5 text-[#d86991]"></i>
              <span>Matriz Fisiológica de Ritmos de Carrera</span>
            </h4>

            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs font-mono">
                <thead>
                  <tr class="border-b border-[#4d3e50] text-[10px] text-[#A297A6] uppercase tracking-wider">
                    <th class="pb-3">Distancia / Zona</th>
                    <th class="pb-3">Ritmo Exigible</th>
                    <th class="pb-3">Sustrato Energético</th>
                    <th class="pb-3">Foco Fisiológico</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-[#4d3e50]/50">
                  <tr>
                    <td class="py-3 font-bold text-white">1.500m / Milla</td>
                    <td class="py-3 text-[#d86991] font-bold">3:05 - 3:15/km</td>
                    <td class="py-3 text-[#A297A6]">Glucólisis Rápida / Lactato</td>
                    <td class="py-3 text-white">Potencia Anaeróbica & Frecuencia</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">5K Cross (El Soto)</td>
                    <td class="py-3 text-[#d86991] font-bold">3:30/km</td>
                    <td class="py-3 text-[#A297A6]">VO2max Puro (100%)</td>
                    <td class="py-3 text-white">Tolerancia a la fatiga en terreno blando</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">10K Ruta (Hito Ávila)</td>
                    <td class="py-3 text-[#a887ce] font-bold">3:45 - 3:50/km</td>
                    <td class="py-3 text-[#A297A6]">Umbral Anaeróbico (LT2)</td>
                    <td class="py-3 text-white">Capacidad de aclaramiento de lactato</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">Media Maratón</td>
                    <td class="py-3 text-[#a887ce] font-bold">3:55 - 4:00/km</td>
                    <td class="py-3 text-[#A297A6]">Glucógeno Mixto / Umbral LT1-LT2</td>
                    <td class="py-3 text-white">Ritmo crucero submáximo sostenido</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">Rodaje Z2 Base</td>
                    <td class="py-3 text-[#20D994] font-bold">4:35 - 4:55/km</td>
                    <td class="py-3 text-[#A297A6]">Oxidación Lipídica</td>
                    <td class="py-3 text-white">Capilarización & Biogénesis Mitocondrial</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">Rodaje Regenerativo Z1</td>
                    <td class="py-3 text-[#20D994] font-bold">5:00 - 5:20/km</td>
                    <td class="py-3 text-[#A297A6]">Grasas Puras / Flujo Sanguíneo</td>
                    <td class="py-3 text-white">Drenaje de piernas y recuperación articular</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

        </section>

        <!-- ========================================== -->
        <!-- PESTAÑA 5: PERFIL DE USUARIO & IMC (NUEVA) -->
        <!-- ========================================== -->
        <section id="tab-profile" class="space-y-6 hidden">

          <!-- Tarjeta de Datos del Atleta Editable -->
          <div class="luxury-card p-6 sm:p-8">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-[#4d3e50]">
              <div class="flex items-center gap-4">
                <div class="w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0">
                  ''' + profile_logo_svg + '''
                </div>
                <div>
                  <h3 class="text-xl font-black text-white">Carlos Jiménez Andrino</h3>
                  <p class="text-xs text-[#A297A6] mt-0.5">Atleta Medio Fondo & Fondo &bull; Categoría Senior</p>
                </div>
              </div>

              <button onclick="toggleProfileEdit()" id="profile-edit-btn" class="px-4 py-2.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-[#a887ce] hover:border-[#a887ce] font-extrabold text-xs transition flex items-center gap-2">
                <i data-lucide="edit-3" class="w-4 h-4"></i>
                <span id="profile-edit-text">Editar Perfil</span>
              </button>
            </div>

            <!-- Inputs de Parámetros Antropométricos -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-6">
              <div>
                <label class="text-[10px] uppercase font-bold text-[#A297A6]">Peso Actual (kg)</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-weight" step="0.1" value="63.0" oninput="calculateBMI()" disabled class="w-full bg-[#171821]/50 border border-[#4d3e50] rounded-xl px-3 py-2 text-white/90 font-mono font-bold text-sm focus:outline-none focus:border-[#d86991] opacity-80 cursor-default transition">
                </div>
                <span class="text-[10px] text-[#A297A6] mt-1 block">Varía según hidratación</span>
              </div>

              <div>
                <label class="text-[10px] uppercase font-bold text-[#A297A6]">Altura (cm)</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-height" value="173" oninput="calculateBMI()" class="w-full bg-[#171821] border border-[#4d3e50] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#d86991]">
                </div>
                <span class="text-[10px] text-[#A297A6] mt-1 block">1.73 metros</span>
              </div>

              <div>
                <label class="text-[10px] uppercase font-bold text-[#A297A6]">Edad</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-age" value="23" class="w-full bg-[#171821] border border-[#4d3e50] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#d86991]">
                </div>
                <span class="text-[10px] text-[#A297A6] mt-1 block">Años cumplidos</span>
              </div>

              <div>
                <label class="text-[10px] uppercase font-bold text-[#A297A6]">FC Reposo (FCR)</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-fcr" value="42" class="w-full bg-[#171821] border border-[#4d3e50] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#d86991]">
                </div>
                <span class="text-[10px] text-[#20D994] mt-1 block font-bold">Bradicardia atlética</span>
              </div>
            </div>
          </div>

          <!-- CALCULADORA AUTOMÁTICA DE IMC & GRÁFICO VISUAL -->
          <div class="luxury-card p-6 sm:p-8 space-y-6">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <h4 class="text-base font-extrabold text-white flex items-center gap-2">
                  <i data-lucide="scale" class="w-5 h-5 text-[#20D994]"></i>
                  <span>Índice de Masa Corporal (IMC)</span>
                </h4>
                <p class="text-xs text-[#A297A6]">Calculado automáticamente a partir de tu peso y altura en tiempo real</p>
              </div>

              <div class="flex items-baseline gap-2">
                <span id="bmi-display-value" class="text-3xl sm:text-4xl font-black text-white font-mono">21.05</span>
                <span class="text-xs text-[#A297A6] font-mono font-bold">kg/m&sup2;</span>
              </div>
            </div>

            <!-- Barra Segmentada Visual de IMC -->
            <div class="space-y-2">
              <div class="relative h-4 rounded-full overflow-hidden bg-[#292631] flex">
                <!-- Bajo peso (<18.5) -->
                <div style="width: 23%;" class="bg-[#38BDF8] h-full" title="Bajo peso (<18.5)"></div>
                <!-- Normal / Rango Óptimo Corredor (18.5 - 24.9) -->
                <div style="width: 43%;" class="bg-gradient-to-r from-[#20D994] to-[#a887ce] h-full" title="Normopeso / Óptimo Atleta"></div>
                <!-- Sobrepeso (>25.0) -->
                <div style="width: 34%;" class="bg-[#d86991] h-full" title="Sobrepeso (>25.0)"></div>
              </div>

              <!-- Marcador Visual de Posición del IMC -->
              <div class="relative h-6">
                <div id="bmi-marker-pin" class="absolute -top-1 transform -translate-x-1/2 flex flex-col items-center transition-all duration-300" style="left: 40.3%;">
                  <div class="w-3 h-3 rounded-full bg-white ring-4 ring-[#20D994] shadow-lg"></div>
                  <span id="bmi-marker-text" class="text-[10px] font-extrabold text-[#20D994] mt-0.5 font-mono">21.05</span>
                </div>
              </div>

              <!-- Leyenda de rangos -->
              <div class="flex items-center justify-between text-[10px] font-mono text-[#A297A6] pt-1">
                <span>&lt; 18.5 (Bajo Peso)</span>
                <span class="text-[#20D994] font-bold">18.5 - 24.9 (Rango Óptimo Atleta: 20.5 - 21.5)</span>
                <span>&gt; 25.0 (Sobrepeso)</span>
              </div>
            </div>

            <!-- Veredicto Fisiológico del IMC -->
            <div class="p-4 rounded-2xl bg-[#171821] border border-[#4d3e50] space-y-2">
              <div class="flex items-center gap-2">
                <i data-lucide="check-circle-2" class="w-4 h-4 text-[#20D994]"></i>
                <span id="bmi-status-title" class="text-xs font-black text-[#20D994] uppercase tracking-wider">
                  Clasificación: Rango Óptimo de Rendimiento en Fondo
                </span>
              </div>
              <p id="bmi-status-desc" class="text-xs text-[#A297A6] leading-relaxed">
                Tu IMC actual de <strong>21.05 kg/m&sup2;</strong> sitúa tu relación potencia:peso en el rango de máxima eficiencia para 5K, 10K y Maratón. Permite minimizar el coste de transporte de oxígeno por zancada sin sacrificar masa muscular funcional ni rigidez del tendón de Aquiles.
              </p>
            </div>
          </div>

        </section>

      </div>
    </main>

  </div>

  <!-- =================================================== -->
  <!-- NAVEGACIÓN INFERIOR FLOTANTE MÓVIL (5 BOTONES) -->
  <!-- =================================================== -->
  <nav class="lg:hidden fixed bottom-3 left-3 right-3 h-16 bg-[#292631]/95 backdrop-blur-md border border-[#4d3e50] rounded-2xl flex items-center justify-around z-40 px-1 shadow-2xl">
    <button onclick="switchTab('dashboard')" id="dock-btn-dashboard" class="flex flex-col items-center justify-center text-[#d86991] flex-1 py-1">
      <i data-lucide="layout-grid" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Dashboard</span>
    </button>
    <button onclick="switchTab('workouts')" id="dock-btn-workouts" class="flex flex-col items-center justify-center text-[#A297A6] flex-1 py-1">
      <i data-lucide="calendar" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Entrenos</span>
    </button>
    <button onclick="switchTab('gym')" id="dock-btn-gym" class="flex flex-col items-center justify-center text-[#A297A6] flex-1 py-1">
      <i data-lucide="dumbbell" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Gimnasio</span>
    </button>
    <button onclick="switchTab('goals')" id="dock-btn-goals" class="flex flex-col items-center justify-center text-[#A297A6] flex-1 py-1">
      <i data-lucide="target" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Objetivos</span>
    </button>
    <button onclick="switchTab('profile')" id="dock-btn-profile" class="flex flex-col items-center justify-center text-[#A297A6] flex-1 py-1">
      <i data-lucide="user" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Perfil</span>
    </button>
  </nav>

  <!-- =================================================== -->
  <!-- JAVASCRIPT DEL CLIENTE -->
  <!-- =================================================== -->
  <script>
    const daysData = ${JSON.stringify(planData.days || [])};
    const weeklyData = ${JSON.stringify(WEEKLY_EVO_DATA)};
    const calendarDataByMonth = ${JSON.stringify(CALENDAR_DATA_BY_MONTH)};
    const monthKeys = ["2026-09", "2026-10", "2026-11", "2026-12"];
    let currentMonthIdx = 2; // Noviembre 2026 por defecto
    const todayISO = "${todayISO}";

    const gymRoutinesData = {
      1: {
        title: "Rutina 1 · Pierna 1 (Dominancia Rodilla & Cuádriceps)",
        day: "Lunes 18:00 • 45-50 min • RIR 1-2",
        exercises: [
          { num: 1, name: "Sentadilla con Barra / Box Squat", vector: "/img/vector_ex_1_1.png?v=6", muscle: "Cuádriceps", target_sets: 4, target_reps: "4-6", target_weight: "65-70 kg", rir: "RIR 1-2", cue: "Rompe el paralelo al cajón. Empuja con todo el pie sin valgo de rodilla." },
          { num: 2, name: "Prensa de Piernas 45°", vector: "/img/vector_ex_1_2.png?v=6", muscle: "Cuádriceps & Aductores", target_sets: 3, target_reps: "6-8", target_weight: "+40 kg/lado", rir: "RIR 1", cue: "Pies anchura caderas. Cero despegue lumbar del respaldo." },
          { num: 3, name: "Extensión de Cuádriceps", vector: "/img/vector_ex_1_3.png?v=6", muscle: "Recto Femoral", target_sets: 3, target_reps: "8-10", target_weight: "66 kg", rir: "RIR 1", cue: "Aislamiento puro del recto femoral sin fatiga en columna." },
          { num: 4, name: "Gemelos de Pie con Barra", vector: "/img/vector_ex_1_4.png?v=6", muscle: "Gastrocnemio", target_sets: 4, target_reps: "6-8", target_weight: "85 kg", rir: "RIR 1", cue: "Pausa de 2s abajo para anular rebote tendinoso." },
          { num: 5, name: "Sentadilla Búlgara con Mancuernas", vector: "/img/vector_ex_1_5.png?v=6", muscle: "Estabilidad & Glúteo Medio", target_sets: 3, target_reps: "8-10", target_weight: "14-16 kg/mano", rir: "RIR 1", cue: "Fuerza unilateral de zancada. Apoyo firme del empeine trasero." },
          { num: 6, name: "Rueda Abdominal (Core)", vector: "/img/vector_ex_1_6.png?v=6", muscle: "Core & Abdomen", target_sets: 3, target_reps: "8-10", target_weight: "Autocarga", rir: "RIR 1", cue: "Retroversión pélvica activa en todo el recorrido." }
        ]
      },
      2: {
        title: "Rutina 2 · Torso Tracción (Hoy) (Dorsal, Espalda Alta & Bíceps)",
        day: "Miércoles 17:30 • 50 min • RIR 1",
        exercises: [
          { num: 1, name: "Jalón Agarre Cerrado V", vector: "/img/vector_ex_2_1.png?v=6", muscle: "Dorsal Ancho", target_sets: 4, target_reps: "4-6", target_weight: "54-59 kg", rir: "RIR 1", cue: "Codos hacia abajo y adentro apretando el dorsal." },
          { num: 2, name: "Remo Dorian Unilateral", vector: "/img/vector_ex_2_2.png?v=6", muscle: "Dorsal & Espalda Media", target_sets: 3, target_reps: "6-8", target_weight: "28-30 kg", rir: "RIR 1", cue: "Tracción hacia el bolsillo trasero, codo pegado al costado." },
          { num: 3, name: "Remo Gironda con Agarre Amplio", vector: "/img/vector_ex_2_3.png?v=6", muscle: "Espalda Alta", target_sets: 3, target_reps: "8-10", target_weight: "36 kg", rir: "RIR 1", cue: "Retracción escapular máxima en el punto de contracción." },
          { num: 4, name: "Face Pull en Polea Alta", vector: "/img/vector_ex_2_4.png?v=6", muscle: "Deltoides Posterior", target_sets: 3, target_reps: "10-12", target_weight: "23-27 kg", rir: "RIR 2", cue: "Cuerda a la frente con rotación externa de hombro." },
          { num: 5, name: "Curl Bíceps Mancuernas Inclinado", vector: "/img/vector_ex_2_5.png?v=6", muscle: "Bíceps", target_sets: 3, target_reps: "8-10", target_weight: "12 kg/mano", rir: "RIR 1", cue: "Estiramiento máximo con los codos perpendiculares al suelo." },
          { num: 6, name: "Curl en Banco Scott / Predicador", vector: "/img/vector_ex_2_6.png?v=6", muscle: "Braquial & Bíceps", target_sets: 3, target_reps: "8-10", target_weight: "25 kg", rir: "RIR 1", cue: "Aislamiento estricto sin balanceo del torso." }
        ]
      },
      3: {
        title: "Rutina 3 · Pierna 2 (Cadena Posterior & Blindaje Isquios)",
        day: "Jueves/Viernes 17:30 • 50 min • RIR 1",
        exercises: [
          { num: 1, name: "Hip Thrust con Barra", vector: "/img/vector_ex_3_1.png?v=6", muscle: "Glúteo Mayor", target_sets: 4, target_reps: "4-6", target_weight: "130-140 kg", rir: "RIR 1", cue: "Parada de 1s arriba con retroversión pélvica y mentón pegado." },
          { num: 2, name: "Peso Muerto Rumano Unilateral", vector: "/img/vector_ex_3_2.png?v=6", muscle: "Isquiotibiales", target_sets: 3, target_reps: "6-8", target_weight: "20-24 kg/mano", rir: "RIR 1-2", cue: "Bisagra de cadera unipodal pura con espalda neutra y pierna retrasada." },
          { num: 3, name: "Prensa Pies Altos y Anchos", vector: "/img/vector_ex_3_3.png?v=6", muscle: "Glúteos & Aductores", target_sets: 3, target_reps: "6-8", target_weight: "+40-45 kg/lado", rir: "RIR 1", cue: "Empuje de talones reduciendo el estrés en el tendón rotuliano." },
          { num: 4, name: "Sóleo Sentado en Máquina", vector: "/img/vector_ex_3_4.png?v=6", muscle: "Sóleo", target_sets: 4, target_reps: "8-10", target_weight: "40 kg", rir: "RIR 1", cue: "El sóleo absorbe hasta 8x el peso corporal en cada zancada." },
          { num: 5, name: "Curl Femoral Tumbado", vector: "/img/vector_ex_3_5.png?v=6", muscle: "Isquiotibiales", target_sets: 3, target_reps: "6-8", target_weight: "42 kg", rir: "RIR 1", cue: "Frena la fase excéntrica en 3s para blindar la unión miotendinosa." },
          { num: 6, name: "Elevaciones de Piernas Colgado", vector: "/img/vector_ex_3_6.png?v=6", muscle: "Core & Abdomen", target_sets: 3, target_reps: "10-12", target_weight: "Autocarga", rir: "RIR 1", cue: "Sube las piernas en L a 90° flexionando la pelvis sin balanceo." }
        ]
      },
      4: {
        title: "Rutina 4 · Torso Empuje (Pectoral, Deltoides & Tríceps)",
        day: "Sábado 11:00 • 45 min • RIR 1-2",
        exercises: [
          { num: 1, name: "Press de Banca Plano", vector: "/img/vector_ex_4_1.png?v=6", muscle: "Pectoral Mayor", target_sets: 4, target_reps: "4-6", target_weight: "60-65 kg", rir: "RIR 1-2", cue: "Escápulas retraídas, barra al esternón y empuje firme." },
          { num: 2, name: "Press Inclinado con Mancuernas 30°", vector: "/img/vector_ex_4_2.png?v=6", muscle: "Pectoral Superior", target_sets: 3, target_reps: "6-8", target_weight: "22 kg/mano", rir: "RIR 1", cue: "Banca a 30° para activación máxima de la porción clavicular." },
          { num: 3, name: "Pec Deck / Contractor", vector: "/img/vector_ex_4_3.png?v=6", muscle: "Pectoral (Aislamiento)", target_sets: 3, target_reps: "8-10", target_weight: "50 kg", rir: "RIR 1", cue: "Cierre al esternón con compresión isométrica de 1s." },
          { num: 4, name: "Elevaciones Laterales con Mancuernas", vector: "/img/vector_ex_4_4.png?v=6", muscle: "Deltoides Lateral", target_sets: 4, target_reps: "10-12", target_weight: "10 kg/mano", rir: "RIR 1", cue: "Eleva en el plano escapular liderando con los codos." },
          { num: 5, name: "Tríceps en Polea Unilateral", vector: "/img/vector_ex_4_5.png?v=6", muscle: "Tríceps", target_sets: 3, target_reps: "8-10", target_weight: "12-15 kg", rir: "RIR 1", cue: "Extensión unilateral estricta bloqueando abajo sin balancear el hombro." },
          { num: 6, name: "Plancha Frontal Core Estricta", vector: "/img/vector_ex_4_6.png?v=6", muscle: "Core & Abdomen", target_sets: 3, target_reps: "40-45s", target_weight: "Autocarga", rir: "RIR 0", cue: "Tensión de glúteos y abdomen como una tabla de piedra." }
        ]
      }
    };

    function handleImgError(img) {
      img.onerror = null;
      img.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200"><rect width="400" height="200" fill="%231D1E2C"/><text x="50%" y="50%" fill="%238E8FA3" font-family="sans-serif" font-size="14" text-anchor="middle" dominant-baseline="middle">Ilustración Vectorial</text></svg>';
    }

    
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
        calBtn.classList.add('bg-[#d86991]', 'text-white', 'shadow-lg');
        calBtn.classList.remove('text-[#A297A6]');
        micBtn.classList.remove('bg-[#d86991]', 'text-white', 'shadow-lg');
        micBtn.classList.add('text-[#A297A6]');
      } else {
        calView.classList.add('hidden');
        micView.classList.remove('hidden');
        micBtn.classList.add('bg-[#d86991]', 'text-white', 'shadow-lg');
        micBtn.classList.remove('text-[#A297A6]');
        calBtn.classList.remove('bg-[#d86991]', 'text-white', 'shadow-lg');
        calBtn.classList.add('text-[#A297A6]');
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
        weightInput.classList.remove('opacity-80', 'cursor-default', 'bg-[#171821]/50');
        weightInput.classList.add('bg-[#292631]', 'border-[#a887ce]', 'ring-1', 'ring-[#a887ce]/30');
        heightInput.classList.remove('opacity-80', 'cursor-default', 'bg-[#171821]/50');
        heightInput.classList.add('bg-[#292631]', 'border-[#a887ce]');

        editBtn.classList.remove('bg-[#292631]', 'text-[#a887ce]');
        editBtn.classList.add('bg-[#a887ce]', 'text-white');
        editBtnText.innerText = "Guardar Cambios";
        weightInput.focus();
      } else {
        // Guardar cambios
        saveUserProfile();
        isProfileEditing = false;
        weightInput.disabled = true;
        heightInput.disabled = true;
        weightInput.classList.add('opacity-80', 'cursor-default', 'bg-[#171821]/50');
        weightInput.classList.remove('bg-[#292631]', 'border-[#a887ce]', 'ring-1', 'ring-[#a887ce]/30');
        heightInput.classList.add('opacity-80', 'cursor-default', 'bg-[#171821]/50');
        heightInput.classList.remove('bg-[#292631]', 'border-[#a887ce]');

        editBtnText.innerText = "¡Guardado!";
        editBtn.classList.remove('bg-[#a887ce]');
        editBtn.classList.add('bg-[#20D994]');
        setTimeout(() => {
          editBtnText.innerText = "Editar Perfil";
          editBtn.classList.remove('bg-[#20D994]', 'text-white');
          editBtn.classList.add('bg-[#292631]', 'text-[#a887ce]');
        }, 2000);
      }
    }

    function switchTab(tabId) {
      const tabs = ['dashboard', 'workouts', 'gym', 'goals', 'profile'];
      tabs.forEach(t => {
        const el = document.getElementById('tab-' + t);
        if (el) el.classList.toggle('hidden', t !== tabId);

        const deskBtn = document.getElementById('nav-desktop-' + t);
        if (deskBtn) {
          deskBtn.classList.toggle('active-nav-link', t === tabId);
          deskBtn.classList.toggle('text-[#d86991]', t === tabId);
          deskBtn.classList.toggle('text-[#A297A6]', t !== tabId);
        }

        const dockBtn = document.getElementById('dock-btn-' + t);
        if (dockBtn) {
          dockBtn.classList.toggle('text-[#d86991]', t === tabId);
          dockBtn.classList.toggle('text-[#A297A6]', t !== tabId);
        }
      });

      if (tabId === 'gym') {
        selectGymRoutine(2);
      }
      if (tabId === 'profile') {
        calculateBMI();
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    function goToTodayWorkout() {
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

    function goToGymRoutine(routineId) {
      switchTab('gym');
      selectGymRoutine(routineId);
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

    // ==========================================
    // ESTADO DEL LOGGER SERIE A SERIE
    // ==========================================
    let currentGymState = {};

    function selectGymRoutine(routineId) {
      for (let i = 1; i <= 4; i++) {
        const btn = document.getElementById('gym-chip-' + i);
        if (!btn) continue;
        if (i === routineId) {
          btn.className = "p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#d86991] text-white border-[#d86991] font-semibold glow-pink";
          btn.querySelectorAll('span')[0].className = "text-[10px] uppercase font-extrabold text-white/80";
          btn.querySelectorAll('span')[1].className = "text-xs font-extrabold text-white mt-1";
          btn.querySelectorAll('span')[2].className = "text-[10px] text-white/80 mt-0.5";
        } else {
          btn.className = "p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#292631] border-[#4d3e50] text-[#A297A6] hover:border-[#d86991]";
          btn.querySelectorAll('span')[0].className = "text-[10px] uppercase font-bold text-[#A297A6]";
          btn.querySelectorAll('span')[1].className = "text-xs font-extrabold text-white mt-1";
          btn.querySelectorAll('span')[2].className = "text-[10px] text-[#A297A6] mt-0.5";
        }
      }

      const routine = gymRoutinesData[routineId];
      if (!routine) return;

      const savedKey = 'aegis_workout_v3_' + todayISO + '_r' + routineId;
      const raw = localStorage.getItem(savedKey);
      if (raw) {
        try { currentGymState = JSON.parse(raw); } catch(e) { currentGymState = {}; }
      } else {
        currentGymState = {};
      }

      const container = document.getElementById('gym-exercises-container');
      let html = '<div class="luxury-card p-4 sm:p-5 flex items-center justify-between border-b border-[#4d3e50]">' +
        '<div>' +
          '<h3 class="text-base font-extrabold text-white">' + routine.title + '</h3>' +
          '<p class="text-xs text-[#d86991] font-medium mt-0.5">' + routine.day + '</p>' +
        '</div>' +
        '<span class="text-xs font-extrabold px-3 py-1 rounded-xl bg-[#292631] text-[#A297A6] border border-[#4d3e50]">' +
          routine.exercises.length + ' Ejercicios' +
        '</span>' +
      '</div>';

      routine.exercises.forEach(function(ex) {
        if (!currentGymState[ex.num]) {
          currentGymState[ex.num] = {
            sets: [],
            notes: ''
          };
          for (let s = 1; s <= ex.target_sets; s++) {
            currentGymState[ex.num].sets.push({
              set_num: s,
              reps: ex.target_reps.split('-')[0],
              weight: ex.target_weight.split(' ')[0].replace('kg', ''),
              completed: true
            });
          }
        }

        html += '<div class="luxury-card overflow-hidden space-y-4 p-5 sm:p-6">' +
          '<div class="flex flex-col md:flex-row gap-5 items-center">' +
            '<!-- Tarjeta Vectorial Dual-Fase -->' +
            '<div class="w-full md:w-80 h-36 rounded-2xl overflow-hidden bg-[#171821] border border-[#4d3e50] flex items-center justify-center p-2 relative flex-shrink-0">' +
              '<img src="' + ex.vector + '" alt="' + ex.name + '" class="max-h-full max-w-full object-contain" onerror="handleImgError(this)">' +
              '<span class="absolute top-2 left-2 text-[10px] font-extrabold px-2 py-0.5 rounded-lg bg-[#292631] text-[#a887ce] border border-[#4d3e50] uppercase tracking-wider">' +
                ex.muscle +
              '</span>' +
            '</div>' +

            '<!-- Detalle del Ejercicio -->' +
            '<div class="flex-1 w-full space-y-3">' +
              '<div>' +
                '<h4 class="text-base font-extrabold text-white">' + ex.name + '</h4>' +
                '<p class="text-xs text-[#A297A6] mt-0.5 font-medium">Objetivo: <strong class="text-white">' + ex.target_sets + ' series &times; ' + ex.target_reps + ' reps</strong> @ <strong class="text-[#d86991] font-mono">' + ex.target_weight + '</strong> (' + ex.rir + ')</p>' +
              '</div>' +

              '<!-- Tabla de Series (ORDEN: Serie - Reps - Carga - Acción) -->' +
              '<div class="overflow-x-auto">' +
                '<div class="min-w-[320px] space-y-2" id="sets-container-' + ex.num + '">' +
                  renderExerciseSetsHtml(routineId, ex.num) +
                '</div>' +
              '</div>' +

              '<!-- Botón Añadir Serie -->' +
              '<div class="flex items-center justify-between pt-1">' +
                '<button onclick="addSetRow(' + routineId + ', ' + ex.num + ')" id="add-set-btn-' + ex.num + '" class="px-3 py-1.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-[#A297A6] hover:text-white text-xs font-bold transition flex items-center gap-1.5">' +
                  '<i data-lucide="plus" class="w-3.5 h-3.5 text-[#d86991]"></i> + Añadir Serie' +
                '</button>' +
                '<div class="text-[11px] text-[#A297A6] italic">' + ex.cue + '</div>' +
              '</div>' +

              '<!-- Notas del Ejercicio -->' +
              '<div class="pt-1">' +
                '<input type="text" value="' + (currentGymState[ex.num].notes || '') + '" oninput="updateExerciseNotes(' + routineId + ', ' + ex.num + ', this.value)" placeholder="Sensaciones, RIR o apuntes del ejercicio..." class="w-full bg-[#171821] border border-[#4d3e50] rounded-xl px-3 py-1.5 text-xs text-[#A297A6] focus:text-white focus:outline-none focus:border-[#a887ce] transition">' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>';
      });

      container.innerHTML = html;
      updateMarkdownPreview(routineId);
      lucide.createIcons();
    }

    function renderExerciseSetsHtml(routineId, exNum) {
      const exState = currentGymState[exNum];
      if (!exState || !exState.sets) return '';

      // ORDEN REQUERIDO: Serie - Reps - Carga (KG) - Acción
      let out = '<div class="grid grid-cols-12 gap-2 text-[10px] text-[#A297A6] font-bold uppercase tracking-wider px-2 pb-1 border-b border-[#4d3e50]/60">' +
        '<div class="col-span-2">Serie</div>' +
        '<div class="col-span-4">Reps</div>' +
        '<div class="col-span-4">Carga (kg)</div>' +
        '<div class="col-span-2 text-center">Acción</div>' +
      '</div>';

      exState.sets.forEach((s, idx) => {
        out += '<div class="grid grid-cols-12 gap-2 items-center p-2 rounded-xl bg-[#171821] border border-[#4d3e50] text-xs font-mono">' +
          '<div class="col-span-2 font-bold text-[#A297A6] flex items-center gap-1">' +
            '<span class="w-5 h-5 rounded-lg bg-[#292631] text-white flex items-center justify-center text-[10px]">' + s.set_num + '</span>' +
          '</div>' +
          '<div class="col-span-4">' +
            '<input type="text" value="' + (s.reps || '') + '" oninput="updateSetReps(' + routineId + ', ' + exNum + ', ' + idx + ', this.value)" placeholder="reps" class="w-full bg-[#292631] border border-[#4d3e50] rounded-lg px-2.5 py-1 text-white font-bold text-xs focus:outline-none focus:border-[#d86991] transition">' +
          '</div>' +
          '<div class="col-span-4">' +
            '<input type="text" value="' + (s.weight || '') + '" oninput="updateSetWeight(' + routineId + ', ' + exNum + ', ' + idx + ', this.value)" placeholder="kg" class="w-full bg-[#292631] border border-[#4d3e50] rounded-lg px-2.5 py-1 text-white font-bold text-xs focus:outline-none focus:border-[#d86991] transition">' +
          '</div>' +
          '<div class="col-span-2 flex items-center justify-center gap-1">' +
            (exState.sets.length > 1 ? '<button onclick="removeSetRow(' + routineId + ', ' + exNum + ', ' + idx + ')" class="w-6 h-6 rounded-lg bg-[#292631] hover:bg-rose-500/20 text-[#A297A6] hover:text-[#d86991] flex items-center justify-center transition" title="Eliminar serie">&times;</button>' : '<span class="text-[#20D994] font-bold text-xs">✓</span>') +
          '</div>' +
        '</div>';
      });

      return out;
    }

    function addSetRow(routineId, exNum) {
      if (!currentGymState[exNum]) return;
      const nextNum = currentGymState[exNum].sets.length + 1;
      const lastReps = nextNum > 1 ? currentGymState[exNum].sets[nextNum - 2].reps : '';
      const lastWeight = nextNum > 1 ? currentGymState[exNum].sets[nextNum - 2].weight : '';
      currentGymState[exNum].sets.push({
        set_num: nextNum,
        reps: lastReps,
        weight: lastWeight,
        completed: true
      });
      persistGymState(routineId);
      document.getElementById('sets-container-' + exNum).innerHTML = renderExerciseSetsHtml(routineId, exNum);
      updateMarkdownPreview(routineId);
      lucide.createIcons();
    }

    function removeSetRow(routineId, exNum, idx) {
      if (!currentGymState[exNum] || currentGymState[exNum].sets.length <= 1) return;
      currentGymState[exNum].sets.splice(idx, 1);
      currentGymState[exNum].sets.forEach((s, i) => s.set_num = i + 1);
      persistGymState(routineId);
      document.getElementById('sets-container-' + exNum).innerHTML = renderExerciseSetsHtml(routineId, exNum);
      updateMarkdownPreview(routineId);
      lucide.createIcons();
    }

    function updateSetReps(routineId, exNum, idx, val) {
      if (!currentGymState[exNum] || !currentGymState[exNum].sets[idx]) return;
      currentGymState[exNum].sets[idx].reps = val;
      persistGymState(routineId);
      updateMarkdownPreview(routineId);
    }

    function updateSetWeight(routineId, exNum, idx, val) {
      if (!currentGymState[exNum] || !currentGymState[exNum].sets[idx]) return;
      currentGymState[exNum].sets[idx].weight = val;
      persistGymState(routineId);
      updateMarkdownPreview(routineId);
    }

    function updateExerciseNotes(routineId, exNum, val) {
      if (!currentGymState[exNum]) return;
      currentGymState[exNum].notes = val;
      persistGymState(routineId);
      updateMarkdownPreview(routineId);
    }

    function persistGymState(routineId) {
      const savedKey = 'aegis_workout_v3_' + todayISO + '_r' + routineId;
      localStorage.setItem(savedKey, JSON.stringify(currentGymState));

      fetch('/api/save_gym_session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          date: todayISO,
          routine_id: routineId,
          routine_name: gymRoutinesData[routineId].title,
          state: currentGymState
        })
      }).catch(e => console.log('KV sync error (offline fallback active)'));
    }

    function generateMarkdownText(routineId) {
      const routine = gymRoutinesData[routineId];
      const now = new Date();
      const dateStr = now.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
      
      const lines = [
        '🏋️ AEGIS COACH — ' + routine.title.toUpperCase() + ' (' + dateStr + ')',
        'Atleta: Carlos Jiménez Andrino',
        '----------------------------------------'
      ];

      routine.exercises.forEach(ex => {
        const state = currentGymState[ex.num];
        if (!state || !state.sets || state.sets.length === 0) return;
        
        const setStrings = state.sets.map(s => {
          const w = (s.weight || '0').replace('kg', '');
          const r = s.reps || '0';
          return r + 'r@' + w + 'kg';
        });

        let line = '• ' + ex.name + ': ' + setStrings.join(', ');
        if (state.notes && state.notes.trim()) {
          line += ' [' + state.notes.trim() + ']';
        }
        lines.push(line);
      });

      return lines.join(String.fromCharCode(10));
    }

    function updateMarkdownPreview(routineId) {
      const textarea = document.getElementById('markdown-summary-preview');
      if (textarea) {
        textarea.value = generateMarkdownText(routineId);
      }
    }

    function copyGymSessionToClipboard() {
      let routineId = 3;
      for (let i = 1; i <= 4; i++) {
        const btn = document.getElementById('gym-chip-' + i);
        if (btn && btn.classList.contains('bg-[#d86991]')) {
          routineId = i;
          break;
        }
      }

      const textToCopy = generateMarkdownText(routineId);

      function onSuccess() {
        const btnText = document.getElementById('copy-btn-text');
        const btn = document.getElementById('copy-gym-btn');
        if (btnText && btn) {
          const original = btnText.innerText;
          btnText.innerText = "¡Copiado al Portapapeles!";
          btn.classList.add('bg-[#20D994]');
          btn.classList.remove('bg-[#d86991]');
          setTimeout(() => {
            btnText.innerText = original;
            btn.classList.remove('bg-[#20D994]');
            btn.classList.add('bg-[#d86991]');
          }, 2000);
        }
      }

      function fallbackCopy() {
        try {
          const t = document.createElement("textarea");
          t.value = textToCopy;
          t.style.position = "fixed";
          t.style.left = "-9999px";
          t.style.top = "-9999px";
          document.body.appendChild(t);
          t.focus();
          t.select();
          document.execCommand('copy');
          document.body.removeChild(t);
          onSuccess();
        } catch(e) {
          console.warn('Fallback copy error:', e);
        }
      }

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(textToCopy).then(onSuccess).catch(fallbackCopy);
      } else {
        fallbackCopy();
      }
    }

    // ==========================================
    // CALENDARIO MENSUAL MINIMALISTA
    // ==========================================
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
        html += '<div class="h-14 sm:h-16 rounded-xl bg-[#171821]/20 border border-transparent"></div>';
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
          ? 'border-2 border-[#d86991] shadow-md shadow-[#d86991]/20 bg-[#292631]' 
          : 'border border-[#4d3e50] bg-[#171821] hover:border-[#a887ce]/60 hover:bg-[#292631]/60';

        let dayNumberHtml = '';
        if (isToday) {
          dayNumberHtml = '<div class="w-6 h-6 sm:w-7 sm:h-7 rounded-full bg-[#d86991] text-white font-black flex items-center justify-center mx-auto text-xs sm:text-sm shadow-md">' + d + '</div>';
        } else {
          dayNumberHtml = '<div class="w-6 h-6 sm:w-7 sm:h-7 flex items-center justify-center mx-auto text-xs sm:text-sm font-bold text-white/90">' + d + '</div>';
        }

        const dotsHtml = '<div class="flex items-center justify-center gap-1 mt-1 sm:mt-1.5">' +
          (activity.dots || []).map(function(dot) {
            const color = dot === 'run' ? '#d86991' : (dot === 'gym' ? '#a887ce' : '#20D994');
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
          ? 'border-2 border-[#d86991] shadow-md shadow-[#d86991]/20 bg-[#292631]' 
          : 'border border-[#4d3e50] bg-[#171821] hover:border-[#a887ce]/60 hover:bg-[#292631]/60') + 
          ' h-14 sm:h-16 p-1 sm:p-1.5 rounded-xl flex flex-col justify-between cursor-pointer transition select-none';
      });
      const selectedEl = document.querySelector('#calendar-days-grid > div[data-date="' + dateKey + '"]');
      if (selectedEl) {
        selectedEl.className = 'border-2 border-[#a887ce] shadow-lg shadow-[#a887ce]/30 bg-[#25283D] h-14 sm:h-16 p-1 sm:p-1.5 rounded-xl flex flex-col justify-between cursor-pointer transition select-none scale-[1.02]';
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
            (act.type.includes('Running') ? 'bg-[#d86991]/20 text-[#d86991] border border-[#d86991]/30' : 
            (act.type.includes('Gym') ? 'bg-[#a887ce]/20 text-[#a887ce] border border-[#a887ce]/30' : 'bg-[#20D994]/20 text-[#20D994] border border-[#20D994]/30'));
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
          let lHtml = '<div class="mt-4 pt-4 border-t border-[#4d3e50]/60 space-y-2">' +
            '<div class="flex items-center justify-between">' +
              '<span class="text-xs font-bold text-white flex items-center gap-1.5"><i data-lucide="timer" class="w-3.5 h-3.5 text-[#d86991]"></i> Desglose de Vueltas / Parciales Oficiales Garmin</span>' +
              '<span class="text-[11px] font-mono text-[#A297A6]">' + act.laps.length + ' vueltas</span>' +
            '</div>' +
            '<div class="overflow-x-auto rounded-xl border border-[#4d3e50]/70 bg-[#292631]/50">' +
              '<table class="w-full text-left text-xs font-mono">' +
                '<thead>' +
                  '<tr class="bg-[#171821] text-[#A297A6] border-b border-[#4d3e50] text-[10px] uppercase">' +
                    '<th class="py-2 px-3">Lap</th>' +
                    '<th class="py-2 px-3">Distancia</th>' +
                    '<th class="py-2 px-3">Tiempo</th>' +
                    '<th class="py-2 px-3">Ritmo</th>' +
                    '<th class="py-2 px-3">FC Media</th>' +
                  '</tr>' +
                '</thead>' +
                '<tbody class="divide-y divide-[#4d3e50]/40 text-white/90">';
          act.laps.forEach(function(l) {
            const paceColor = l.pace.startsWith('3:') ? 'text-[#d86991]' : 'text-white';
            lHtml += '<tr class="hover:bg-white/5 transition">' +
              '<td class="py-1.5 px-3 font-bold text-[#a887ce]">' + l.lap + '</td>' +
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
          notesContainer.innerHTML = '<div class="mt-3 p-3.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-xs text-[#A297A6] leading-relaxed">' +
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
    }

    // ==========================================
    // ACORDEÓN DE MICROCICLO DE 14 DÍAS
    // ==========================================
    function renderWorkoutsAccordion() {
      const container = document.getElementById('workouts-accordion-container');
      if (!container) return;

      let html = '';
      daysData.forEach(function(day, idx) {
        const isToday = day.date === todayISO;
        const isPast = day.date < todayISO;
        const isKey = day.is_key_session;

        let badgeHtml = '';
        if (isToday) {
          badgeHtml = '<span class="text-[10px] font-black uppercase px-2.5 py-1 rounded-full bg-[#d86991] text-white glow-pink">HOY</span>';
        } else if (isPast) {
          badgeHtml = '<span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-[#20D994]/20 text-[#20D994] flex items-center gap-1"><i data-lucide="check" class="w-3 h-3"></i> Completado</span>';
        } else if (isKey) {
          badgeHtml = '<span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-[#a887ce]/20 text-[#a887ce]">Sesión Clave</span>';
        }

        const borderClass = isToday ? 'border-[#d86991] glow-pink' : 'border-[#4d3e50]';
        const startOpen = isToday || (!daysData.some(d => d.date === todayISO) && idx === 0);

        html += '<div class="luxury-card ' + borderClass + ' overflow-hidden transition-all">' +
          '<div onclick="toggleDayAccordion(' + idx + ')" class="p-4 sm:p-5 flex items-center justify-between cursor-pointer hover:bg-[#292631]/40 transition select-none">' +
            '<div class="flex items-center gap-3">' +
              badgeHtml +
              '<div>' +
                '<span class="text-sm sm:text-base font-extrabold text-white">' + day.day_name + ' ' + day.date.substring(8) + ' ' + (day.date.substring(5, 7) === '11' ? 'Nov' : 'Dic') + '</span>' +
                '<div class="text-xs text-[#A297A6] font-medium mt-0.5">' +
                  (day.running.is_rest ? 'Descanso carrera' : day.running.title) + ' &bull; ' +
                  (day.gym.is_rest ? 'Descanso fuerza' : day.gym.routine_name.split('·')[0]) +
                '</div>' +
              '</div>' +
            '</div>' +
            '<i id="day-icon-' + idx + '" data-lucide="chevron-down" class="w-5 h-5 text-[#A297A6] transition-transform duration-200" style="transform: ' + (startOpen ? 'rotate(180deg)' : 'rotate(0deg)') + ';"></i>' +
          '</div>' +

          '<div id="day-body-' + idx + '" class="px-4 pb-4 sm:px-6 sm:pb-6 pt-1 space-y-4 border-t border-[#4d3e50]/50 ' + (startOpen ? '' : 'hidden') + '">' +
            '<!-- Running -->' +
            (day.running.is_rest 
              ? '<div class="p-3.5 rounded-xl bg-[#171821] border border-[#4d3e50]/60 text-xs text-[#A297A6] flex items-center gap-2"><i data-lucide="moon" class="w-4 h-4 text-[#a887ce]"></i> Descanso de running: Recuperación activa y regeneración celular.</div>'
              : '<div class="p-4 rounded-xl bg-[#171821] border border-[#4d3e50] space-y-2">' +
                '<div class="flex items-center justify-between text-xs font-bold text-[#d86991]">' +
                  '<span class="flex items-center gap-1.5">' +
                    '<i data-lucide="footprints" class="w-4 h-4"></i> ' + day.running.title +
                  '</span>' +
                  '<span class="text-xs font-mono font-black text-white">' + day.running.duration_min + ' min &bull; ' + day.running.target_distance_km + ' km</span>' +
                '</div>' +
                '<p class="text-xs text-white/90 leading-relaxed">' + day.running.main_work + '</p>' +
                '<div class="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-1 text-[11px] font-mono">' +
                  '<div class="p-2 rounded-lg bg-[#292631] border border-[#4d3e50] text-[#A297A6]">' +
                    'RITMO: <strong class="text-white">' + day.running.target_pace + '</strong>' +
                  '</div>' +
                  '<div class="p-2 rounded-lg bg-[#292631] border border-[#4d3e50] text-[#A297A6]">' +
                    'ZONA FC: <strong class="text-[#d86991]">' + day.running.hr_zone + '</strong>' +
                  '</div>' +
                  '<div class="p-2 rounded-lg bg-[#292631] border border-[#4d3e50] text-[#A297A6] col-span-2 sm:col-span-1">' +
                    'ZAPATILLA: <strong class="text-white">' + (day.running.shoe || 'Asics Novablast') + '</strong>' +
                  '</div>' +
                '</div>' +
              '</div>'
            ) +

            '<!-- Fuerza Gym -->' +
            (day.gym.is_rest
              ? '<div class="p-3.5 rounded-xl bg-[#171821] border border-[#4d3e50]/60 text-xs text-[#A297A6] flex items-center gap-2"><i data-lucide="coffee" class="w-4 h-4 text-[#20D994]"></i> Descanso de gimnasio: 0 fatiga neuromuscular.</div>'
              : '<div class="p-4 rounded-xl bg-[#171821] border border-[#4d3e50] space-y-3">' +
                '<div class="flex items-center justify-between text-xs font-bold text-[#a887ce]">' +
                  '<span class="flex items-center gap-1.5">' +
                    '<i data-lucide="dumbbell" class="w-4 h-4"></i> ' + day.gym.routine_name +
                  '</span>' +
                  '<button onclick="goToGymRoutine(' + (day.gym.routine_id || 1) + ')" class="px-2.5 py-1 rounded-lg bg-[#a887ce] text-white text-[11px] font-bold hover:brightness-110 transition">' +
                    'Ir a la Rutina &rarr;' +
                  '</button>' +
                '</div>' +
                '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">' +
                  (day.gym.highlight_exercises || day.gym.exercises || []).map(function(ex) {
                    return '<div class="p-2 rounded-lg bg-[#292631] border border-[#4d3e50] flex items-center justify-between text-[11px]">' +
                      '<span class="text-white font-medium">' + ex.name + '</span>' +
                      '<span class="font-mono text-[#a887ce] font-bold">' + ex.load + ' (' + ex.rir + ')</span>' +
                    '</div>';
                  }).join('') +
                '</div>' +
              '</div>'
            ) +
          '</div>' +
        '</div>';
      });

      container.innerHTML = html;
      lucide.createIcons();
    }

    // ==========================================
    // PERFIL DE ATLETA & CALCULADORA DE IMC
    // ==========================================
    function calculateBMI() {
      const weightInput = document.getElementById('profile-weight');
      const heightInput = document.getElementById('profile-height');
      if (!weightInput || !heightInput) return;

      const weight = parseFloat(weightInput.value) || 63.0;
      const heightCm = parseFloat(heightInput.value) || 173.0;
      const heightM = heightCm / 100.0;
      const bmi = weight / (heightM * heightM);
      const bmiRounded = bmi.toFixed(2);

      const valDisplay = document.getElementById('bmi-display-value');
      const markerText = document.getElementById('bmi-marker-text');
      const markerPin = document.getElementById('bmi-marker-pin');
      const statusTitle = document.getElementById('bmi-status-title');
      const statusDesc = document.getElementById('bmi-status-desc');

      if (valDisplay) valDisplay.innerText = bmiRounded;
      if (markerText) markerText.innerText = bmiRounded;

      // Escala: 15 (0%) a 30 (100%)
      const minBmi = 15.0;
      const maxBmi = 30.0;
      let pct = ((bmi - minBmi) / (maxBmi - minBmi)) * 100;
      pct = Math.max(2, Math.min(98, pct));

      if (markerPin) {
        markerPin.style.left = pct.toFixed(1) + '%';
      }

      if (statusTitle && statusDesc) {
        if (bmi < 18.5) {
          statusTitle.innerText = "Clasificación: Bajo Peso Funcional";
          statusTitle.className = "text-xs font-black text-[#38BDF8] uppercase tracking-wider";
          statusDesc.innerHTML = "Tu IMC de <strong>" + bmiRounded + " kg/m²</strong> indica bajo peso. Asegurar superávit calórico y densidad proteica para proteger masa muscular.";
        } else if (bmi <= 24.9) {
          statusTitle.innerText = "Clasificación: Rango Óptimo de Rendimiento en Fondo";
          statusTitle.className = "text-xs font-black text-[#20D994] uppercase tracking-wider";
          statusDesc.innerHTML = "Tu IMC actual de <strong>" + bmiRounded + " kg/m²</strong> sitúa tu relación potencia:peso en el rango de máxima eficiencia para 5K, 10K y Maratón. Permite minimizar el coste de transporte de oxígeno por zancada sin sacrificar masa muscular funcional ni rigidez del tendón de Aquiles.";
        } else {
          statusTitle.innerText = "Clasificación: Ligero Sobrepeso para Fondista";
          statusTitle.className = "text-xs font-black text-[#d86991] uppercase tracking-wider";
          statusDesc.innerHTML = "Tu IMC de <strong>" + bmiRounded + " kg/m²</strong> incrementa el coste metabólico por zancada. Ajuste de composición corporal recomendado.";
        }
      }
    }

    function saveUserProfile() {
      const weight = parseFloat(document.getElementById('profile-weight')?.value) || 63.0;
      const height = parseFloat(document.getElementById('profile-height')?.value) || 173.0;
      const age = parseInt(document.getElementById('profile-age')?.value) || 23;
      const fcr = parseInt(document.getElementById('profile-fcr')?.value) || 42;

      const profile = { weight, height, age, fcr, updatedAt: new Date().toISOString() };
      localStorage.setItem('aegis_athlete_profile', JSON.stringify(profile));

      fetch('/api/save_profile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(profile)
      }).then(() => {
        const btnText = document.getElementById('save-profile-text');
        if (btnText) {
          const orig = btnText.innerText;
          btnText.innerText = "¡Guardado!";
          setTimeout(() => btnText.innerText = orig, 2000);
        }
      }).catch(e => console.log('Error saving profile'));
    }

    // ==========================================
    // INICIALIZACIÓN AL CARGAR LA PÁGINA
    // ==========================================
    document.addEventListener("DOMContentLoaded", function() {
      lucide.createIcons();
      renderWorkoutsAccordion();
      renderCalendarMonth();
      selectCalendarDay('2026-11-16');
      selectGymRoutine(2);
      calculateBMI();

      // Cargar perfil guardado si existe
      const savedProfile = localStorage.getItem('aegis_athlete_profile');
      if (savedProfile) {
        try {
          const p = JSON.parse(savedProfile);
          if (p.weight && document.getElementById('profile-weight')) document.getElementById('profile-weight').value = p.weight;
          if (p.height && document.getElementById('profile-height')) document.getElementById('profile-height').value = p.height;
          calculateBMI();
        } catch(e) {}
      }

      // Gráfico Spline con Áreas Superpuestas Rellenas con Colores Potentes (Estilo Referencia media_1794822984640_6116ce9d.png)
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
      syncDynamicMetrics();
    });
  </script>
</body>
</html>`;
}
'''

with open('cloudflare/src/index.ts', 'w', encoding='utf-8') as f:
    f.write(worker_ts)

print(f"Index.ts v3 actualizado exitosamente ({len(worker_ts)} bytes)")
