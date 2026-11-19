import json
import os

print("Construyendo el nuevo index.ts v3 con Calendario Mensual, Perfil de Usuario con IMC, Logo Fluido y Reordenación de Columnas...")

with open('cloudflare/plan.json', 'r', encoding='utf-8') as f:
    plan_json = json.load(f)

with open('data/weekly_evolution.json', 'r', encoding='utf-8') as f:
    weekly_evo = json.load(f)

display_weeks = [w for w in weekly_evo if w['run_km'] > 0 or w['week_start'] >= '2026-09-28']
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

# Calendario de Noviembre 2026 (con datos de entrenos reales de Carlos)
calendar_nov_2026 = {
    "year": 2026,
    "month": 11,
    "month_name": "Noviembre 2026",
    "days_in_month": 30,
    "first_day_weekday": 6, # 0=Lunes, 6=Domingo (1 Nov 2026 fue Domingo)
    "activities": {
        "2026-11-01": {"dots": ["run"], "title": "Rodaje Regenerativo Z1", "type": "Running", "km": 6.0, "time": "32:10", "pace": "5:21/km", "hr": "138 ppm", "ai": "Drenaje capilar y soltura suave previa a la semana de competición."},
        "2026-11-03": {"dots": ["run"], "title": "Rodaje Progresivo Z2", "type": "Running", "km": 8.0, "time": "38:40", "pace": "4:50/km", "hr": "146 ppm", "ai": "Economía lipolítica y activación neuromuscular sin fatiga de glucógeno."},
        "2026-11-05": {"dots": ["gym"], "title": "Rutina 1 · Pierna & VMO", "type": "Gimnasio", "km": 0, "time": "45 min", "pace": "-", "hr": "118 ppm", "ai": "Detección de derrame sinovial reactivo en rodilla izquierda. Protocolo inmediato de Spanish Squats y descarga patelar."},
        "2026-11-06": {"dots": ["run"], "title": "Activación Pre-10K (25') + 4 Rectas", "type": "Running", "km": 5.0, "time": "24:30", "pace": "4:54/km", "hr": "142 ppm", "ai": "Puesta a punto neural. Tensión muscular óptima con 0 dolor en rodilla."},
        "2026-11-08": {"dots": ["run"], "title": "10K Media Maratón Ávila Monumental", "type": "Competición", "km": 10.0, "time": "38:26", "pace": "3:50/km", "hr": "174 ppm", "ai": "MARCA PERSONAL a 1.070m de altitud con viento y cuestas. Rendimiento fisiológico superlativo, gestión de umbral impecable."},
        "2026-11-10": {"dots": ["mountain"], "title": "Descanso Activo / Paseo Movilidad", "type": "Descanso", "km": 3.0, "time": "35 min", "pace": "Paseo", "hr": "92 ppm", "ai": "Eliminación de metabolitos post-competición y regeneración osteoarticular."},
        "2026-11-11": {"dots": ["run"], "title": "Rodaje de Transición Z2", "type": "Running", "km": 7.5, "time": "36:15", "pace": "4:50/km", "hr": "147 ppm", "ai": "Retorno a la carga aeróbica. Rodillas y gemelos respondiendo sin inflamación."},
        "2026-11-12": {"dots": ["gym"], "title": "Rutina 2 · Torso Tracción & Densidad", "type": "Gimnasio", "km": 0, "time": "50 min", "pace": "-", "hr": "115 ppm", "ai": "Fuerza de tracción: Jalón V a 59 kg y Remo Dorian a 30 kg. Espalda compacta para soporte postural de carrera."},
        "2026-11-13": {"dots": ["gym"], "title": "Rutina 3 · Pierna 2 (Cadena Posterior)", "type": "Gimnasio", "km": 0, "time": "50 min", "pace": "-", "hr": "122 ppm", "ai": "Hito de fuerza: Hip Thrust a 140 kg (4 reps @ RIR 1) y RDL unilateral a 24 kg. Blindaje total del isquiotibial proximal."},
        "2026-11-14": {"dots": ["run", "mountain"], "title": "6×800m Parque del Soto + Paintball 2h", "type": "Series Cross", "km": 10.5, "time": "52:00", "pace": "3:45/km real", "hr": "164 ppm", "ai": "Series en hierba/tierra con clavos de 6mm. Media de 3:00.0 con recuperación clavada a 90s. Gran tolerancia al lactato."},
        "2026-11-15": {"dots": ["gym"], "title": "Rutina 4 · Torso Empuje (Pectoral/Hombro)", "type": "Gimnasio", "km": 0, "time": "45 min", "pace": "-", "hr": "114 ppm", "ai": "Banca a 65 kg y Press inclinado a 22 kg/mano. Carga completada tras noche de celebración."},
        "2026-11-16": {"dots": ["run", "gym"], "title": "35' Drenaje Z1 (<145 ppm) + Rutina 2", "type": "Hoy", "km": 7.0, "time": "35:00", "pace": "5:00/km", "hr": "Z1", "ai": "Sesión activa de hoy: Recuperar tono y soltar piernas en asfalto plano."},
        "2026-11-17": {"dots": ["run"], "title": "Rodaje 50' Z2 con 6 Progresiones", "type": "Planificado", "km": 10.0, "time": "50:00", "pace": "4:45/km", "hr": "Z2", "ai": "Volumen base de la semana con reactividad neuromuscular en los últimos 2 km."},
        "2026-11-18": {"dots": ["run"], "title": "8×500m @ 1:40 (3:20/km) rec 75\"", "type": "Planificado", "km": 9.5, "time": "46:00", "pace": "3:20/km", "hr": "VO2max", "ai": "Sesión clave de VO2max en asfalto llano. Ajuste metabólico para el ritmo del Cross del Soto."},
        "2026-11-19": {"dots": ["gym"], "title": "Rutina 3 · Hip Thrust 135kg & RDL", "type": "Planificado", "km": 0, "time": "45 min", "pace": "-", "hr": "Fuerza", "ai": "Último estímulo pesado de cadena posterior antes de la semana de afinamiento."},
        "2026-11-20": {"dots": ["run"], "title": "Rodaje Suave 30' Pre-Viaje + 4 Rectas", "type": "Planificado", "km": 6.0, "time": "30:00", "pace": "5:05/km", "hr": "Z1", "ai": "Oxigenación antes de salir de viaje. Zapatillas rodadoras blandas."},
        "2026-11-21": {"dots": ["gym"], "title": "Rutina 4 · Torso Empuje Ligero", "type": "Planificado", "km": 0, "time": "40 min", "pace": "-", "hr": "Fuerza", "ai": "Mantenimiento neural de pectoral y hombro sin estrés en piernas."},
        "2026-11-22": {"dots": ["run"], "title": "Rodaje Continuo 40' Z2 (4:45/km)", "type": "Planificado", "km": 8.5, "time": "40:00", "pace": "4:45/km", "hr": "Z2", "ai": "Cierre de la Semana 1 Pre-Milán con 30-31 km completados."},
        "2026-11-24": {"dots": ["run"], "title": "12×200m @ 37\" (3:05/km) rec 45\"", "type": "Semana Cross", "km": 7.0, "time": "36:00", "pace": "3:05/km", "hr": "Neural", "ai": "Afinamiento neuromuscular: frecuencia de zancada sin acumulación de lactato residual."},
        "2026-11-26": {"dots": ["run"], "title": "20' Trote + 4 Rectas Clavos 6mm en El Soto", "type": "Semana Cross", "km": 4.5, "time": "22:00", "pace": "5:00/km", "hr": "Z1", "ai": "Reconocimiento de curvas y terreno deformable con clavos de 6mm."},
        "2026-11-28": {"dots": ["run"], "title": "CROSS POPULAR PARQUE DEL SOTO (5 KM)", "type": "COMPETICIÓN", "km": 5.0, "time": "17:30 obj", "pace": "3:30/km", "hr": "Máxima", "ai": "OBJETIVO PRIMARIO: 5 km en tierra/hierba @ 3:30/km (~17:30). Clavos 6mm obligatorios."}
    }
}

# SVG oficial del nuevo logotipo de Aegis Coach (Concepto 2 refinado: Fluid Kinetic 'A' Wing)
svg_logo = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">
  <defs>
    <linearGradient id="c2_left" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#6366F1"/>
      <stop offset="50%" stop-color="#7B88FF"/>
      <stop offset="100%" stop-color="#38BDF8"/>
    </linearGradient>
    <linearGradient id="c2_right" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF758C"/>
      <stop offset="40%" stop-color="#FF5E80"/>
      <stop offset="100%" stop-color="#E040FB"/>
    </linearGradient>
    <linearGradient id="c2_cross" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#7B88FF"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FF5E80"/>
    </linearGradient>
    <filter id="c2_softglow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#FF5E80" flood-opacity="0.35"/>
    </filter>
  </defs>
  <path d="M 24 85 C 20 81, 22 72, 28 56 C 35 38, 44 23, 49 13 C 51 9, 53 9, 54 13 C 52 23, 44 42, 38 58 C 33 71, 29 82, 26 86 C 25 87, 24 87, 24 85 Z" fill="url(#c2_left)"/>
  <path d="M 50 11 C 56 18, 69 40, 77 58 C 84 73, 83 83, 76 87 C 70 90, 61 88, 56 81 C 51 74, 49 64, 51 54 C 52 50, 56 50, 58 53 C 59 58, 60 67, 63 74 C 66 80, 71 81, 74 78 C 78 74, 76 64, 71 52 C 65 38, 54 20, 50 11 Z" fill="url(#c2_right)" filter="url(#c2_softglow)"/>
  <path d="M 14 58 C 28 55, 48 54, 68 54 C 80 54, 91 56, 94 58 C 93 61, 80 62, 68 62 C 48 62, 28 61, 14 58 Z" fill="url(#c2_cross)"/>
</svg>'''

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
const CALENDAR_DATA: any = ''' + json.dumps(calendar_nov_2026, indent=2, ensure_ascii=False) + ''';

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

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
  <link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23FF5E80' stroke-width='2.5'%3E%3Cpath d='M12 2L3 7v6c0 5.5 3.8 10.7 9 12 5.2-1.3 9-6.5 9-12V7l-9-5z'/%3E%3Cpath d='M9 12l2 2 4-4'/%3E%3C/svg%3E">
  
  <!-- Tipografía: Plus Jakarta Sans & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    :root {
      --bg-dark: #141522;
      --card-dark: #1D1E2C;
      --card-border: #2D2F45;
      --accent-pink: #FF5E80;
      --accent-blue: #7B88FF;
      --accent-green: #20D994;
      --text-muted: #8E8FA3;
    }
    body {
      font-family: 'Plus Jakarta Sans', -apple-system, sans-serif;
      background-color: var(--bg-dark);
      color: #FFFFFF;
      -webkit-font-smoothing: antialiased;
    }
    .font-mono {
      font-family: 'JetBrains Mono', monospace;
    }
    .luxury-card {
      background-color: var(--card-dark);
      border: 1px solid var(--card-border);
      border-radius: 1.5rem;
    }
    .glow-pink {
      box-shadow: 0 8px 30px -4px rgba(255, 94, 128, 0.25);
    }
    .bg-gradient-hero {
      background: linear-gradient(135deg, #FF5E80 0%, #B845ED 50%, #7B88FF 100%);
    }
    .active-nav-link {
      color: #FF5E80 !important;
      background-color: rgba(255, 94, 128, 0.12);
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
<body class="h-full flex flex-col bg-[#141522] text-white">

  <!-- =================================================== -->
  <!-- LAYOUT PRINCIPAL -->
  <!-- =================================================== -->
  <div class="flex-1 flex flex-col lg:flex-row min-h-screen">

    <!-- SIDEBAR ESCRITORIO -->
    <aside class="hidden lg:flex w-24 flex-col items-center py-6 border-r border-[#2D2F45] bg-[#141522] fixed top-0 bottom-0 left-0 z-30">
      <!-- Monograma Logo SVG -->
      <div onclick="switchTab('dashboard')" class="w-12 h-12 rounded-2xl flex items-center justify-center cursor-pointer transition hover:scale-105 mb-8">
        ''' + svg_logo + '''
      </div>

      <!-- Iconos de Navegación Vertical -->
      <div class="flex flex-col gap-6 items-center flex-1">
        <button onclick="switchTab('dashboard')" id="nav-desktop-dashboard" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#FF5E80] active-nav-link transition hover:text-white" title="Dashboard">
          <i data-lucide="layout-grid" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('workouts')" id="nav-desktop-workouts" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#8E8FA3] transition hover:text-white" title="Entrenos & Calendario">
          <i data-lucide="calendar" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('gym')" id="nav-desktop-gym" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#8E8FA3] transition hover:text-white" title="Gimnasio & Series">
          <i data-lucide="dumbbell" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('goals')" id="nav-desktop-goals" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#8E8FA3] transition hover:text-white" title="Objetivos">
          <i data-lucide="target" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('profile')" id="nav-desktop-profile" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#8E8FA3] transition hover:text-white" title="Perfil & IMC">
          <i data-lucide="user" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Botón Telegram en Sidebar -->
      <a href="https://t.me/aegis_coach_chatbot" target="_blank" class="w-11 h-11 rounded-2xl bg-[#1D1E2C] border border-[#2D2F45] text-[#7B88FF] flex items-center justify-center hover:border-[#7B88FF] transition" title="Bot de Telegram">
        <i data-lucide="send" class="w-4 h-4"></i>
      </a>
    </aside>

    <!-- CONTENEDOR CENTRAL -->
    <main class="flex-1 lg:pl-24 pb-28 lg:pb-12 flex flex-col min-w-0">
      
      <!-- TOPBAR / HEADER LIMPIO (Sin Buscador, Sin PRO, Sin Kilos Fijos) -->
      <header class="h-20 border-b border-[#2D2F45] px-4 sm:px-8 flex items-center justify-between bg-[#141522]/90 backdrop-blur sticky top-0 z-20">
        <div class="flex items-center gap-3 sm:gap-4">
          <!-- Monograma Logo -->
          <div onclick="switchTab('dashboard')" class="w-10 h-10 sm:w-11 sm:h-11 rounded-2xl flex items-center justify-center cursor-pointer transition hover:scale-105 flex-shrink-0">
            ''' + svg_logo + '''
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-base sm:text-lg font-black tracking-tight text-white">AEGIS COACH</span>
            </div>
            <p class="text-[11px] sm:text-xs text-[#8E8FA3] font-medium leading-none mt-0.5">
              Carlos Jiménez Andrino &bull; Fisiología & Rendimiento
            </p>
          </div>
        </div>

        <div class="flex items-center gap-2 sm:gap-3">
          <!-- Acceso Perfil Rápido -->
          <button onclick="switchTab('profile')" class="px-3 py-1.5 rounded-xl bg-[#1D1E2C] border border-[#2D2F45] text-white hover:border-[#7B88FF] text-xs font-bold transition flex items-center gap-1.5">
            <i data-lucide="user" class="w-3.5 h-3.5 text-[#7B88FF]"></i>
            <span class="hidden sm:inline">Perfil & IMC</span>
          </button>
          
          <!-- Botón Telegram -->
          <a href="https://t.me/aegis_coach_chatbot" target="_blank" class="px-3.5 py-1.5 rounded-xl bg-[#1D1E2C] border border-[#2D2F45] text-[#8E8FA3] hover:text-white hover:border-[#7B88FF] text-xs font-bold transition flex items-center gap-1.5">
            <i data-lucide="send" class="w-3.5 h-3.5 text-[#7B88FF]"></i>
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

          <!-- 1. BLOQUE DE LA SESIÓN DE HOY (ARRIBA DEL TODO) -->
          <div class="rounded-3xl p-6 sm:p-8 bg-gradient-hero text-white shadow-xl glow-pink flex flex-col justify-between relative overflow-hidden">
            <div class="flex items-center justify-between relative z-10 mb-4">
              <div class="flex items-center gap-2">
                <span class="text-xs uppercase font-extrabold tracking-wider bg-black/25 px-3.5 py-1.5 rounded-full backdrop-blur">
                  SESIÓN DE HOY &bull; ${todayPlan.day_name.toUpperCase()} ${todayPlan.date}
                </span>
                <span class="text-[11px] font-bold px-2.5 py-1 rounded-full bg-white/20 backdrop-blur">
                  ${todayPlan.running.is_rest ? 'Descanso' : todayPlan.running.session_type}
                </span>
              </div>
              <i data-lucide="zap" class="w-6 h-6 text-white"></i>
            </div>

            <div class="my-auto relative z-10 space-y-1">
              <div class="text-2xl sm:text-3xl font-black tracking-tight leading-tight">
                ${todayPlan.running.is_rest ? 'Día de Recuperación Activa' : todayPlan.running.title}
              </div>
              <div class="text-xs sm:text-sm text-white/95 font-mono font-semibold">
                ${todayPlan.running.is_rest ? 'Descanso de carrera para asimilar supercompensación' : `${todayPlan.running.duration_min} min &bull; ${todayPlan.running.target_distance_km} km &bull; Ritmo ${todayPlan.running.target_pace} &bull; ${todayPlan.running.hr_zone}`}
              </div>
            </div>

            <div class="flex flex-col sm:flex-row sm:items-center justify-between pt-4 mt-4 border-t border-white/25 relative z-10 gap-3">
              <div class="text-xs font-bold text-white/90 flex items-center gap-2">
                <i data-lucide="dumbbell" class="w-4 h-4"></i>
                <span>${todayPlan.gym.is_rest ? 'Descanso de gimnasio' : todayPlan.gym.routine_name}</span>
              </div>
              <div class="flex items-center gap-2">
                <button onclick="switchTab('workouts')" class="px-3.5 py-2 rounded-xl bg-white text-[#141522] text-xs font-black hover:bg-white/90 transition flex items-center gap-1.5">
                  <span>Ver Entrenos</span> &rarr;
                </button>
                <button onclick="goToGymRoutine(${todayPlan.gym.routine_id || 1})" class="px-3.5 py-2 rounded-xl bg-black/30 border border-white/30 text-white text-xs font-bold hover:bg-black/50 transition flex items-center gap-1.5">
                  <span>Registrar Gym</span>
                </button>
              </div>
            </div>
          </div>

          <!-- 2. TRES KPIS PRINCIPALES (VOLUMEN, FUERZA, ESTADO DE FORMA) -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-6">
            <!-- KPI 1: Volumen Semanal Run -->
            <div class="luxury-card p-6 flex flex-col justify-between">
              <div>
                <span class="text-xs font-bold text-[#8E8FA3] uppercase tracking-wider">Volumen Semanal (Run)</span>
                <div class="flex items-baseline gap-2 mt-2">
                  <span class="text-3xl sm:text-4xl font-extrabold text-white font-mono">27.0</span>
                  <span class="text-base text-[#8E8FA3]">km</span>
                </div>
                <div class="w-full bg-[#242638] h-2 rounded-full mt-3 overflow-hidden">
                  <div class="bg-[#FF5E80] h-full rounded-full" style="width: 90%;"></div>
                </div>
              </div>
              <p class="text-xs text-[#20D994] font-medium mt-3 flex items-center gap-1">
                <i data-lucide="trending-up" class="w-3.5 h-3.5"></i>
                <span>90% del objetivo semanal (30 km)</span>
              </p>
            </div>

            <!-- KPI 2: Sesiones de Fuerza -->
            <div class="luxury-card p-6 flex flex-col justify-between">
              <div>
                <span class="text-xs font-bold text-[#8E8FA3] uppercase tracking-wider">Sesiones de Fuerza</span>
                <div class="flex items-baseline gap-2 mt-2">
                  <span class="text-3xl sm:text-4xl font-extrabold text-white font-mono">4</span>
                  <span class="text-base text-[#8E8FA3]">sesiones</span>
                </div>
                <div class="w-full bg-[#242638] h-2 rounded-full mt-3 overflow-hidden">
                  <div class="bg-[#7B88FF] h-full rounded-full" style="width: 100%;"></div>
                </div>
              </div>
              <p class="text-xs text-[#20D994] font-medium mt-3 flex items-center gap-1">
                <i data-lucide="check-circle" class="w-3.5 h-3.5"></i>
                <span>100% cumplido (4 de 4 planificadas)</span>
              </p>
            </div>

            <!-- KPI 3: Estado de Forma TSB / CTL -->
            <div class="luxury-card p-6 flex flex-col justify-between">
              <div>
                <span class="text-xs font-bold text-[#8E8FA3] uppercase tracking-wider">Estado Forma (TSB / CTL)</span>
                <div class="flex items-baseline gap-2 mt-2">
                  <span class="text-3xl sm:text-4xl font-extrabold text-white font-mono">TSB -9.5</span>
                  <span class="text-base text-[#8E8FA3] font-mono">/ 16.1</span>
                </div>
                <div class="w-full bg-[#242638] h-2 rounded-full mt-3 overflow-hidden">
                  <div class="bg-[#20D994] h-full rounded-full" style="width: 75%;"></div>
                </div>
              </div>
              <p class="text-xs text-[#FF5E80] font-medium mt-3 flex items-center gap-1">
                <i data-lucide="activity" class="w-3.5 h-3.5"></i>
                <span>Fatiga asimilable (ATL 25.7)</span>
              </p>
            </div>
          </div>

          <!-- 3. GRÁFICO SPLINE DE EVOLUCIÓN DE VOLUMEN SEMANAL (KM REALES) -->
          <div class="luxury-card p-6 sm:p-8">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h3 class="text-lg font-black text-white">Evolución de Volumen Semanal (KM)</h3>
                <p class="text-xs text-[#8E8FA3] mt-1 font-medium">Kilómetros reales rodados semana a semana &bull; Tendencia de carga e historial</p>
              </div>
              <div class="flex items-center gap-3">
                <div class="flex items-center gap-2 text-xs font-bold text-[#FF5E80]">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#FF5E80]"></span>
                  <span>Run (km)</span>
                </div>
                <div class="flex items-center gap-2 text-xs font-bold text-[#7B88FF]">
                  <span class="w-2.5 h-2.5 rounded-full bg-[#7B88FF]"></span>
                  <span>Gym (sesiones)</span>
                </div>
              </div>
            </div>

            <!-- Canvas del Spline Chart -->
            <div class="h-64 sm:h-72 w-full relative">
              <canvas id="weeklySplineChart"></canvas>
            </div>

            <!-- Mini badges con las semanas clave -->
            <div class="grid grid-cols-4 sm:grid-cols-8 gap-2 mt-4 text-center">
              <div class="p-1.5 rounded-xl bg-[#242638] border border-[#2D2F45]">
                <div class="text-[10px] text-[#8E8FA3]">28 Sep</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">13.4k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#242638] border border-[#2D2F45]">
                <div class="text-[10px] text-[#8E8FA3]">05 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">19.2k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#242638] border border-[#2D2F45]">
                <div class="text-[10px] text-[#8E8FA3]">12 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">16.5k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#242638] border border-[#2D2F45]">
                <div class="text-[10px] text-[#8E8FA3]">19 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">25.4k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#242638] border border-[#2D2F45]">
                <div class="text-[10px] text-[#8E8FA3]">26 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">29.2k</div>
              </div>
              <div class="p-1.5 rounded-xl bg-[#242638]/60 border border-[#7B88FF]/30">
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

          <!-- 4. SESIONES CLAVE & PRÓXIMOS OBJETIVOS (DOS COLUMNAS) -->
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <!-- Columna Izquierda: 3 Sesiones Clave de Referencia -->
            <div class="luxury-card p-6">
              <div class="flex items-center justify-between mb-4">
                <h4 class="text-sm font-extrabold text-white flex items-center gap-2">
                  <i data-lucide="flame" class="w-4 h-4 text-[#FF5E80]"></i>
                  <span>3 Sesiones Clave de Referencia</span>
                </h4>
                <span class="text-[11px] text-[#8E8FA3]">Memoria Cuantitativa</span>
              </div>

              <div class="space-y-3">
                <div class="flex items-center justify-between p-3 rounded-2xl bg-[#242638] border border-[#2D2F45]">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-[#FF5E80]/20 text-[#FF5E80] flex items-center justify-center">
                      <i data-lucide="trophy" class="w-4 h-4"></i>
                    </div>
                    <div>
                      <div class="text-xs font-bold text-white">10K Ávila Monumental</div>
                      <div class="text-[11px] text-[#8E8FA3]">08 Nov &bull; 1.070m altitud, viento y cuestas</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-sm font-extrabold text-white font-mono">38:26</div>
                    <div class="text-[10px] text-[#20D994] font-bold">3:50/km</div>
                  </div>
                </div>

                <div class="flex items-center justify-between p-3 rounded-2xl bg-[#242638] border border-[#2D2F45]">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-[#7B88FF]/20 text-[#7B88FF] flex items-center justify-center">
                      <i data-lucide="timer" class="w-4 h-4"></i>
                    </div>
                    <div>
                      <div class="text-xs font-bold text-white">6&times;800m Parque del Soto</div>
                      <div class="text-[11px] text-[#8E8FA3]">14 Nov &bull; Clavos 6mm en hierba/tierra &bull; rec 90"</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-sm font-extrabold text-white font-mono">3:00.0 avg</div>
                    <div class="text-[10px] text-[#FF5E80] font-bold">3:45/km real</div>
                  </div>
                </div>

                <div class="flex items-center justify-between p-3 rounded-2xl bg-[#242638] border border-[#2D2F45]">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-[#20D994]/20 text-[#20D994] flex items-center justify-center">
                      <i data-lucide="dumbbell" class="w-4 h-4"></i>
                    </div>
                    <div>
                      <div class="text-xs font-bold text-white">Rutina 3 &bull; Pierna 2 (Fuerza)</div>
                      <div class="text-[11px] text-[#8E8FA3]">13 Nov &bull; Hip Thrust + RDL Unilateral</div>
                    </div>
                  </div>
                  <div class="text-right">
                    <div class="text-sm font-extrabold text-white font-mono">140 kg</div>
                    <div class="text-[10px] text-[#7B88FF] font-bold">RIR 1 &bull; 4 reps</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Columna Derecha: Próximos Objetivos & Cuenta Atrás -->
            <div class="luxury-card p-6">
              <div class="flex items-center justify-between mb-4">
                <h4 class="text-sm font-extrabold text-white flex items-center gap-2">
                  <i data-lucide="target" class="w-4 h-4 text-[#7B88FF]"></i>
                  <span>Próximas Competiciones</span>
                </h4>
                <span class="text-[11px] text-[#8E8FA3]">Cuenta Atrás</span>
              </div>

              <div class="space-y-3">
                <!-- Objetivo 1: Cross del Soto -->
                <div class="p-3.5 rounded-2xl bg-[#242638] border border-[#FF5E80]/40 relative overflow-hidden">
                  <div class="flex items-center justify-between">
                    <div>
                      <span class="text-[10px] font-extrabold px-2 py-0.5 rounded bg-[#FF5E80]/20 text-[#FF5E80] uppercase">
                        28 Noviembre 2026
                      </span>
                      <h5 class="text-sm font-extrabold text-white mt-1">Cross Popular Parque del Soto</h5>
                      <p class="text-xs text-[#8E8FA3]">5 km en tierra/hierba @ 3:30/km (~17:30) &bull; Clavos 6mm</p>
                    </div>
                    <div class="text-right pl-3">
                      <div class="text-2xl font-black text-[#FF5E80] font-mono leading-none">${daysRemaining}</div>
                      <div class="text-[10px] text-[#8E8FA3] mt-1 font-semibold">días</div>
                    </div>
                  </div>
                </div>

                <!-- Objetivo 2: San Silvestre -->
                <div class="p-3.5 rounded-2xl bg-[#242638] border border-[#2D2F45]">
                  <div class="flex items-center justify-between">
                    <div>
                      <span class="text-[10px] font-extrabold px-2 py-0.5 rounded bg-[#7B88FF]/20 text-[#7B88FF] uppercase">
                        31 Diciembre 2026
                      </span>
                      <h5 class="text-sm font-extrabold text-white mt-1">San Silvestre</h5>
                      <p class="text-xs text-[#8E8FA3]">6.5 km @ sub 3:35/km &bull; Asfalto &bull; Zapatilla voladora</p>
                    </div>
                    <div class="text-right pl-3">
                      <div class="text-2xl font-black text-white font-mono leading-none">45</div>
                      <div class="text-[10px] text-[#8E8FA3] mt-1 font-semibold">días</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

        </section>

        <!-- ========================================== -->
        <!-- PESTAÑA 2: ENTRENOS & CALENDARIO MENSUAL -->
        <!-- ========================================== -->
        <section id="tab-workouts" class="space-y-6 hidden">

          <!-- CALENDARIO MENSUAL MINIMALISTA -->
          <div class="luxury-card p-6 sm:p-8">
            <div class="flex items-center justify-between mb-6">
              <div>
                <h3 class="text-lg font-black text-white flex items-center gap-2">
                  <i data-lucide="calendar" class="w-5 h-5 text-[#FF5E80]"></i>
                  <span>Calendario de Entrenamientos</span>
                </h3>
                <p class="text-xs text-[#8E8FA3] mt-1">Puntos de color: <span class="text-[#FF5E80] font-bold">● Running</span> &bull; <span class="text-[#7B88FF] font-bold">● Gimnasio</span> &bull; <span class="text-[#20D994] font-bold">● Descanso/Outdoor</span></p>
              </div>

              <!-- Selector de Mes -->
              <div class="flex items-center gap-2 bg-[#242638] px-3 py-1.5 rounded-2xl border border-[#2D2F45]">
                <button onclick="changeCalendarMonth(-1)" class="w-7 h-7 rounded-lg hover:bg-[#1D1E2C] text-[#8E8FA3] hover:text-white flex items-center justify-center transition">
                  &larr;
                </button>
                <span id="calendar-month-label" class="text-xs font-extrabold text-white px-2">Noviembre 2026</span>
                <button onclick="changeCalendarMonth(1)" class="w-7 h-7 rounded-lg hover:bg-[#1D1E2C] text-[#8E8FA3] hover:text-white flex items-center justify-center transition">
                  &rarr;
                </button>
              </div>
            </div>

            <!-- Cabecera Días Semana -->
            <div class="grid grid-cols-7 gap-1 sm:gap-2 text-center text-[10px] sm:text-xs font-extrabold text-[#8E8FA3] pb-2 border-b border-[#2D2F45]">
              <div>LUN</div>
              <div>MAR</div>
              <div>MIÉ</div>
              <div>JUE</div>
              <div>VIE</div>
              <div>SÁB</div>
              <div>DOM</div>
            </div>

            <!-- Grid de Días del Mes -->
            <div id="calendar-days-grid" class="grid grid-cols-7 gap-1 sm:gap-2 pt-3">
              <!-- Renderizado dinámico vía JS -->
            </div>

            <!-- TARJETA DE DETALLE DEL DÍA SELECCIONADO -->
            <div id="calendar-day-detail" class="mt-6 p-4 sm:p-5 rounded-2xl bg-[#141522] border border-[#2D2F45] transition-all">
              <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-[#2D2F45] pb-3 mb-3">
                <div>
                  <span id="detail-date-badge" class="text-[10px] uppercase font-bold text-[#FF5E80]">Sábado 14 Noviembre 2026</span>
                  <h4 id="detail-title" class="text-base font-extrabold text-white mt-0.5">6&times;800m Parque del Soto con Clavos 6mm</h4>
                </div>
                <div id="detail-pills" class="flex items-center gap-2">
                  <span class="text-xs font-mono font-bold px-3 py-1 rounded-xl bg-[#242638] text-white">5.2 km &bull; 3:45/km real</span>
                </div>
              </div>

              <!-- Métricas del día -->
              <div class="grid grid-cols-3 gap-2 text-center py-2">
                <div class="p-2 rounded-xl bg-[#1D1E2C] border border-[#2D2F45]">
                  <div class="text-[10px] text-[#8E8FA3]">Distancia / Duración</div>
                  <div id="detail-dist" class="text-xs font-bold text-white font-mono mt-0.5">10.5 km (52 min)</div>
                </div>
                <div class="p-2 rounded-xl bg-[#1D1E2C] border border-[#2D2F45]">
                  <div class="text-[10px] text-[#8E8FA3]">Ritmo Medio / Carga</div>
                  <div id="detail-pace" class="text-xs font-bold text-[#FF5E80] font-mono mt-0.5">3:45/km (Cross)</div>
                </div>
                <div class="p-2 rounded-xl bg-[#1D1E2C] border border-[#2D2F45]">
                  <div class="text-[10px] text-[#8E8FA3]">Frecuencia Cardíaca</div>
                  <div id="detail-hr" class="text-xs font-bold text-[#20D994] font-mono mt-0.5">164 ppm (Máx 180)</div>
                </div>
              </div>

              <!-- Análisis de IA & Fisiología -->
              <div class="mt-3 p-3 rounded-xl bg-[#1D1E2C] border border-[#2D2F45]">
                <div class="flex items-center gap-2 mb-1">
                  <i data-lucide="sparkles" class="w-3.5 h-3.5 text-[#7B88FF]"></i>
                  <span class="text-[11px] font-extrabold text-white uppercase tracking-wider">Análisis Fisiológico Aegis AI</span>
                </div>
                <p id="detail-ai" class="text-xs text-[#8E8FA3] leading-relaxed">
                  Series ejecutadas en hierba y tierra con clavos de 6mm. Media de 3:00.0 con recuperaciones clavadas en 90s. Reclutamiento de fibras rápidas Tipo IIa/IIx óptimo sin fatiga residual excesiva en rodilla.
                </p>
              </div>
            </div>
          </div>

          <!-- ACORDEÓN DE MICROCICLO DE 14 DÍAS -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="text-base font-extrabold text-white">Microciclo Bi-Semanal (14 Días)</h3>
                <p class="text-xs text-[#8E8FA3]">Toca cualquier día para desplegar o colapsar el detalle técnico y directrices</p>
              </div>
              <span class="text-xs px-3 py-1.5 rounded-xl bg-[#242638] border border-[#2D2F45] text-[#8E8FA3]">
                Hoy: <strong class="text-white">${todayISO}</strong>
              </span>
            </div>

            <!-- Contenedor del Acordeón Táctil -->
            <div id="workouts-accordion-container" class="space-y-3">
              <!-- Renderizado dinámico vía JS -->
            </div>
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
                <span class="text-[10px] uppercase font-extrabold text-[#FF5E80] tracking-wider">
                  RUTINAS OFICIALES MAESTRAS (PDF PÁGS 1-4)
                </span>
                <h3 class="text-lg font-black text-white mt-0.5">Selecciona la Rutina de Gimnasio</h3>
                <p class="text-xs text-[#8E8FA3]">Sobrecarga progresiva: registra tus kilos y repeticiones serie a serie</p>
              </div>
              <div class="flex items-center gap-2 text-xs font-bold text-[#20D994]">
                <i data-lucide="check-circle" class="w-4 h-4"></i>
                <span>Sobrecarga: +2.5 kg al completar reps</span>
              </div>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <button onclick="selectGymRoutine(1)" id="gym-chip-1" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#242638] border-[#2D2F45] text-[#8E8FA3] hover:border-[#FF5E80]">
                <span class="text-[10px] uppercase font-bold text-[#8E8FA3]">Lunes 18:00</span>
                <span class="text-xs font-extrabold text-white mt-1">Pierna 1</span>
                <span class="text-[10px] text-[#8E8FA3] mt-0.5">Cuádriceps & Búlgaras</span>
              </button>

              <button onclick="selectGymRoutine(2)" id="gym-chip-2" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#242638] border-[#2D2F45] text-[#8E8FA3] hover:border-[#FF5E80]">
                <span class="text-[10px] uppercase font-bold text-[#8E8FA3]">Miércoles 17:30</span>
                <span class="text-xs font-extrabold text-white mt-1">Torso Tracción</span>
                <span class="text-[10px] text-[#8E8FA3] mt-0.5">Dorsal, Remo & Bíceps</span>
              </button>

              <button onclick="selectGymRoutine(3)" id="gym-chip-3" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#FF5E80] text-white border-[#FF5E80] font-semibold glow-pink">
                <span class="text-[10px] uppercase font-extrabold text-white/80">Jueves/Viernes</span>
                <span class="text-xs font-extrabold text-white mt-1">Pierna 2 (Hoy)</span>
                <span class="text-[10px] text-white/80 mt-0.5">Hip Thrust & Isquios</span>
              </button>

              <button onclick="selectGymRoutine(4)" id="gym-chip-4" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#242638] border-[#2D2F45] text-[#8E8FA3] hover:border-[#FF5E80]">
                <span class="text-[10px] uppercase font-bold text-[#8E8FA3]">Sábado 11:00</span>
                <span class="text-xs font-extrabold text-white mt-1">Torso Empuje</span>
                <span class="text-[10px] text-[#8E8FA3] mt-0.5">Pectoral & Deltoides</span>
              </button>
            </div>
          </div>

          <!-- Blindaje Articular (Rodilla & Isquiotibial) -->
          <div class="luxury-card p-5 border-l-4 border-l-[#20D994] flex items-start gap-4">
            <div class="w-10 h-10 rounded-2xl bg-[#20D994]/20 text-[#20D994] flex items-center justify-center flex-shrink-0 mt-0.5">
              <i data-lucide="shield-check" class="w-5 h-5"></i>
            </div>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <h4 class="text-sm font-extrabold text-white">Blindaje Articular & Rodilla Izquierda (Asintomático)</h4>
                <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-[#20D994]/20 text-[#20D994]">0/10 Dolor</span>
              </div>
              <p class="text-xs text-[#8E8FA3] mt-1 leading-relaxed">
                Derrame sinovial superado con éxito. Sustitución de Spanish Squat por <strong>Sentadilla Búlgara con Mancuernas</strong> para desarrollo de estabilidad unipodal y fuerza funcional de zancada.
              </p>
            </div>
          </div>

          <!-- Contenedor de Ejercicios con Tarjetas Vectoriales y Registro Serie a Serie -->
          <div id="gym-exercises-container" class="space-y-6"></div>

          <!-- Resumen Markdown para Garmin / Intervals -->
          <div class="luxury-card p-6 space-y-4">
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <h4 class="text-base font-extrabold text-white flex items-center gap-2">
                  <i data-lucide="file-text" class="w-5 h-5 text-[#FF5E80]"></i>
                  <span>Resumen Markdown para Notas de Garmin & Coach</span>
                </h4>
                <p class="text-xs text-[#8E8FA3] mt-0.5">Generado en tiempo real con las repeticiones y kilos anotados hoy.</p>
              </div>

              <button onclick="copyGymSessionToClipboard()" id="copy-gym-btn" class="px-5 py-2.5 rounded-xl bg-[#FF5E80] text-white font-extrabold text-xs transition hover:brightness-110 glow-pink flex items-center gap-2">
                <i data-lucide="copy" class="w-4 h-4"></i>
                <span id="copy-btn-text">Copiar para Notas de Garmin</span>
              </button>
            </div>

            <!-- Previsualización Markdown -->
            <div class="relative">
              <textarea id="markdown-summary-preview" readonly class="w-full h-40 bg-[#141522] border border-[#2D2F45] rounded-2xl p-4 font-mono text-xs text-[#9D9EA7] resize-none focus:outline-none"></textarea>
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
            <div class="luxury-card p-6 border-t-4 border-t-[#FF5E80] flex flex-col justify-between space-y-4">
              <div>
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black px-3 py-1 rounded-full bg-[#FF5E80]/20 text-[#FF5E80]">
                    OBJETIVO INMEDIATO &bull; 28 NOV 2026
                  </span>
                  <span class="text-xs font-mono font-bold text-[#8E8FA3]">${daysRemaining} días restantes</span>
                </div>
                <h3 class="text-xl font-black text-white mt-3">Cross Popular Parque del Soto (Ávila)</h3>
                <p class="text-xs text-[#8E8FA3] mt-1 leading-relaxed">5 km en terreno deformable (hierba y tierra). Exige máxima rigidez miotendinosa y clavos de 6mm para compensar las curvas sin peralte.</p>
              </div>

              <div class="grid grid-cols-3 gap-2 text-center pt-2 border-t border-[#2D2F45]">
                <div class="p-2 rounded-xl bg-[#242638]">
                  <div class="text-[10px] text-[#8E8FA3]">Distancia</div>
                  <div class="text-sm font-extrabold text-white font-mono">5.0 km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#242638]">
                  <div class="text-[10px] text-[#8E8FA3]">Ritmo Meta</div>
                  <div class="text-sm font-extrabold text-[#FF5E80] font-mono">3:30/km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#242638]">
                  <div class="text-[10px] text-[#8E8FA3]">Tiempo Obj</div>
                  <div class="text-sm font-extrabold text-[#20D994] font-mono">~17:30</div>
                </div>
              </div>
            </div>

            <!-- Objetivo 2: San Silvestre -->
            <div class="luxury-card p-6 border-t-4 border-t-[#7B88FF] flex flex-col justify-between space-y-4">
              <div>
                <div class="flex items-center justify-between">
                  <span class="text-xs font-black px-3 py-1 rounded-full bg-[#7B88FF]/20 text-[#7B88FF]">
                    OBJETIVO FIN DE AÑO &bull; 31 DIC 2026
                  </span>
                  <span class="text-xs font-mono font-bold text-[#8E8FA3]">45 días restantes</span>
                </div>
                <h3 class="text-xl font-black text-white mt-3">San Silvestre</h3>
                <p class="text-xs text-[#8E8FA3] mt-1 leading-relaxed">6.5 km sobre asfalto urbano frío. Reactividad pura y zapatilla voladora con placa de carbono para exprimir el umbral submáximo.</p>
              </div>

              <div class="grid grid-cols-3 gap-2 text-center pt-2 border-t border-[#2D2F45]">
                <div class="p-2 rounded-xl bg-[#242638]">
                  <div class="text-[10px] text-[#8E8FA3]">Distancia</div>
                  <div class="text-sm font-extrabold text-white font-mono">6.5 km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#242638]">
                  <div class="text-[10px] text-[#8E8FA3]">Ritmo Meta</div>
                  <div class="text-sm font-extrabold text-[#7B88FF] font-mono">sub 3:35/km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#242638]">
                  <div class="text-[10px] text-[#8E8FA3]">Tiempo Obj</div>
                  <div class="text-sm font-extrabold text-[#20D994] font-mono">~23:15</div>
                </div>
              </div>
            </div>
          </div>

          <!-- TABLA VISUAL DE RITMOS DE COMPETICIÓN VS ZONAS DE ENTRENAMIENTO -->
          <div class="luxury-card p-6 sm:p-8">
            <h4 class="text-base font-extrabold text-white flex items-center gap-2 mb-4">
              <i data-lucide="gauge" class="w-5 h-5 text-[#FF5E80]"></i>
              <span>Matriz Fisiológica de Ritmos de Carrera</span>
            </h4>

            <div class="overflow-x-auto">
              <table class="w-full text-left text-xs font-mono">
                <thead>
                  <tr class="border-b border-[#2D2F45] text-[10px] text-[#8E8FA3] uppercase tracking-wider">
                    <th class="pb-3">Distancia / Zona</th>
                    <th class="pb-3">Ritmo Exigible</th>
                    <th class="pb-3">Sustrato Energético</th>
                    <th class="pb-3">Foco Fisiológico</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-[#2D2F45]/50">
                  <tr>
                    <td class="py-3 font-bold text-white">1.500m / Milla</td>
                    <td class="py-3 text-[#FF5E80] font-bold">3:05 - 3:15/km</td>
                    <td class="py-3 text-[#8E8FA3]">Glucólisis Rápida / Lactato</td>
                    <td class="py-3 text-white">Potencia Anaeróbica & Frecuencia</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">5K Cross (El Soto)</td>
                    <td class="py-3 text-[#FF5E80] font-bold">3:30/km</td>
                    <td class="py-3 text-[#8E8FA3]">VO2max Puro (100%)</td>
                    <td class="py-3 text-white">Tolerancia a la fatiga en terreno blando</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">10K Ruta (Hito Ávila)</td>
                    <td class="py-3 text-[#7B88FF] font-bold">3:45 - 3:50/km</td>
                    <td class="py-3 text-[#8E8FA3]">Umbral Anaeróbico (LT2)</td>
                    <td class="py-3 text-white">Capacidad de aclaramiento de lactato</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">Media Maratón</td>
                    <td class="py-3 text-[#7B88FF] font-bold">3:55 - 4:00/km</td>
                    <td class="py-3 text-[#8E8FA3]">Glucógeno Mixto / Umbral LT1-LT2</td>
                    <td class="py-3 text-white">Ritmo crucero submáximo sostenido</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">Rodaje Z2 Base</td>
                    <td class="py-3 text-[#20D994] font-bold">4:35 - 4:55/km</td>
                    <td class="py-3 text-[#8E8FA3]">Oxidación Lipídica</td>
                    <td class="py-3 text-white">Capilarización & Biogénesis Mitocondrial</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">Rodaje Regenerativo Z1</td>
                    <td class="py-3 text-[#20D994] font-bold">5:00 - 5:20/km</td>
                    <td class="py-3 text-[#8E8FA3]">Grasas Puras / Flujo Sanguíneo</td>
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
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-6 border-b border-[#2D2F45]">
              <div class="flex items-center gap-4">
                <div class="w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0">
                  ''' + svg_logo + '''
                </div>
                <div>
                  <h3 class="text-xl font-black text-white">Carlos Jiménez Andrino</h3>
                  <p class="text-xs text-[#8E8FA3] mt-0.5">Atleta Medio Fondo & Fondo &bull; Categoría Senior</p>
                </div>
              </div>

              <button onclick="saveUserProfile()" id="save-profile-btn" class="px-5 py-2.5 rounded-xl bg-[#7B88FF] text-white font-extrabold text-xs transition hover:brightness-110 flex items-center gap-2">
                <i data-lucide="save" class="w-4 h-4"></i>
                <span id="save-profile-text">Guardar Cambios</span>
              </button>
            </div>

            <!-- Inputs de Parámetros Antropométricos -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 pt-6">
              <div>
                <label class="text-[10px] uppercase font-bold text-[#8E8FA3]">Peso Actual (kg)</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-weight" step="0.1" value="63.0" oninput="calculateBMI()" class="w-full bg-[#141522] border border-[#2D2F45] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#FF5E80]">
                </div>
                <span class="text-[10px] text-[#8E8FA3] mt-1 block">Varía según hidratación</span>
              </div>

              <div>
                <label class="text-[10px] uppercase font-bold text-[#8E8FA3]">Altura (cm)</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-height" value="173" oninput="calculateBMI()" class="w-full bg-[#141522] border border-[#2D2F45] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#FF5E80]">
                </div>
                <span class="text-[10px] text-[#8E8FA3] mt-1 block">1.73 metros</span>
              </div>

              <div>
                <label class="text-[10px] uppercase font-bold text-[#8E8FA3]">Edad</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-age" value="23" class="w-full bg-[#141522] border border-[#2D2F45] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#FF5E80]">
                </div>
                <span class="text-[10px] text-[#8E8FA3] mt-1 block">Años cumplidos</span>
              </div>

              <div>
                <label class="text-[10px] uppercase font-bold text-[#8E8FA3]">FC Reposo (FCR)</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-fcr" value="42" class="w-full bg-[#141522] border border-[#2D2F45] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#FF5E80]">
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
                <p class="text-xs text-[#8E8FA3]">Calculado automáticamente a partir de tu peso y altura en tiempo real</p>
              </div>

              <div class="flex items-baseline gap-2">
                <span id="bmi-display-value" class="text-3xl sm:text-4xl font-black text-white font-mono">21.05</span>
                <span class="text-xs text-[#8E8FA3] font-mono font-bold">kg/m&sup2;</span>
              </div>
            </div>

            <!-- Barra Segmentada Visual de IMC -->
            <div class="space-y-2">
              <div class="relative h-4 rounded-full overflow-hidden bg-[#242638] flex">
                <!-- Bajo peso (<18.5) -->
                <div style="width: 23%;" class="bg-[#38BDF8] h-full" title="Bajo peso (<18.5)"></div>
                <!-- Normal / Rango Óptimo Corredor (18.5 - 24.9) -->
                <div style="width: 43%;" class="bg-gradient-to-r from-[#20D994] to-[#7B88FF] h-full" title="Normopeso / Óptimo Atleta"></div>
                <!-- Sobrepeso (>25.0) -->
                <div style="width: 34%;" class="bg-[#FF5E80] h-full" title="Sobrepeso (>25.0)"></div>
              </div>

              <!-- Marcador Visual de Posición del IMC -->
              <div class="relative h-6">
                <div id="bmi-marker-pin" class="absolute -top-1 transform -translate-x-1/2 flex flex-col items-center transition-all duration-300" style="left: 40.3%;">
                  <div class="w-3 h-3 rounded-full bg-white ring-4 ring-[#20D994] shadow-lg"></div>
                  <span id="bmi-marker-text" class="text-[10px] font-extrabold text-[#20D994] mt-0.5 font-mono">21.05</span>
                </div>
              </div>

              <!-- Leyenda de rangos -->
              <div class="flex items-center justify-between text-[10px] font-mono text-[#8E8FA3] pt-1">
                <span>&lt; 18.5 (Bajo Peso)</span>
                <span class="text-[#20D994] font-bold">18.5 - 24.9 (Rango Óptimo Atleta: 20.5 - 21.5)</span>
                <span>&gt; 25.0 (Sobrepeso)</span>
              </div>
            </div>

            <!-- Veredicto Fisiológico del IMC -->
            <div class="p-4 rounded-2xl bg-[#141522] border border-[#2D2F45] space-y-2">
              <div class="flex items-center gap-2">
                <i data-lucide="check-circle-2" class="w-4 h-4 text-[#20D994]"></i>
                <span id="bmi-status-title" class="text-xs font-black text-[#20D994] uppercase tracking-wider">
                  Clasificación: Rango Óptimo de Rendimiento en Fondo
                </span>
              </div>
              <p id="bmi-status-desc" class="text-xs text-[#8E8FA3] leading-relaxed">
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
  <nav class="lg:hidden fixed bottom-3 left-3 right-3 h-16 bg-[#1D1E2C]/95 backdrop-blur-md border border-[#2D2F45] rounded-2xl flex items-center justify-around z-40 px-1 shadow-2xl">
    <button onclick="switchTab('dashboard')" id="dock-btn-dashboard" class="flex flex-col items-center justify-center text-[#FF5E80] flex-1 py-1">
      <i data-lucide="layout-grid" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Dashboard</span>
    </button>
    <button onclick="switchTab('workouts')" id="dock-btn-workouts" class="flex flex-col items-center justify-center text-[#8E8FA3] flex-1 py-1">
      <i data-lucide="calendar" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Entrenos</span>
    </button>
    <button onclick="switchTab('gym')" id="dock-btn-gym" class="flex flex-col items-center justify-center text-[#8E8FA3] flex-1 py-1">
      <i data-lucide="dumbbell" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Gimnasio</span>
    </button>
    <button onclick="switchTab('goals')" id="dock-btn-goals" class="flex flex-col items-center justify-center text-[#8E8FA3] flex-1 py-1">
      <i data-lucide="target" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Objetivos</span>
    </button>
    <button onclick="switchTab('profile')" id="dock-btn-profile" class="flex flex-col items-center justify-center text-[#8E8FA3] flex-1 py-1">
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
    const calendarData = ${JSON.stringify(CALENDAR_DATA)};
    const todayISO = "${todayISO}";

    const gymRoutinesData = {
      1: {
        title: "Rutina 1 · Pierna 1 (Dominancia Rodilla & Cuádriceps)",
        day: "Lunes 18:00 • 45-50 min • RIR 1-2",
        exercises: [
          { num: 1, name: "Sentadilla con Barra / Box Squat", vector: "/img/vector_ex_1_1.png", muscle: "Cuádriceps", target_sets: 4, target_reps: "4-6", target_weight: "65-70 kg", rir: "RIR 1-2", cue: "Rompe el paralelo al cajón. Empuja con todo el pie sin valgo de rodilla." },
          { num: 2, name: "Prensa de Piernas 45°", vector: "/img/vector_ex_1_2.png", muscle: "Cuádriceps & Aductores", target_sets: 3, target_reps: "6-8", target_weight: "+40 kg/lado", rir: "RIR 1", cue: "Pies anchura caderas. Cero despegue lumbar del respaldo." },
          { num: 3, name: "Extensión de Cuádriceps", vector: "/img/vector_ex_1_3.png", muscle: "Recto Femoral", target_sets: 3, target_reps: "8-10", target_weight: "66 kg", rir: "RIR 1", cue: "Aislamiento puro del recto femoral sin fatiga en columna." },
          { num: 4, name: "Gemelos de Pie con Barra", vector: "/img/vector_ex_1_4.png", muscle: "Gastrocnemio", target_sets: 4, target_reps: "6-8", target_weight: "85 kg", rir: "RIR 1", cue: "Pausa de 2s abajo para anular rebote tendinoso." },
          { num: 5, name: "Sentadilla Búlgara con Mancuernas", vector: "/img/vector_ex_1_5.png", muscle: "Estabilidad & Glúteo Medio", target_sets: 3, target_reps: "8-10", target_weight: "14-16 kg/mano", rir: "RIR 1", cue: "Fuerza unilateral de zancada. Apoyo firme del empeine trasero." },
          { num: 6, name: "Rueda Abdominal (Core)", vector: "/img/vector_ex_1_6.png", muscle: "Core & Abdomen", target_sets: 3, target_reps: "8-10", target_weight: "Autocarga", rir: "RIR 1", cue: "Retroversión pélvica activa en todo el recorrido." }
        ]
      },
      2: {
        title: "Rutina 2 · Torso Tracción (Dorsal, Espalda Alta & Bíceps)",
        day: "Miércoles 17:30 • 50 min • RIR 1",
        exercises: [
          { num: 1, name: "Jalón Agarre Cerrado V", vector: "/img/vector_ex_2_1.png", muscle: "Dorsal Ancho", target_sets: 4, target_reps: "4-6", target_weight: "54-59 kg", rir: "RIR 1", cue: "Codos hacia abajo y adentro apretando el dorsal." },
          { num: 2, name: "Remo Dorian Unilateral", vector: "/img/vector_ex_2_2.png", muscle: "Dorsal & Espalda Media", target_sets: 3, target_reps: "6-8", target_weight: "28-30 kg", rir: "RIR 1", cue: "Tracción hacia el bolsillo trasero, codo pegado al costado." },
          { num: 3, name: "Remo Gironda con Agarre Amplio", vector: "/img/vector_ex_2_3.png", muscle: "Espalda Alta", target_sets: 3, target_reps: "8-10", target_weight: "36 kg", rir: "RIR 1", cue: "Retracción escapular máxima en el punto de contracción." },
          { num: 4, name: "Face Pull en Polea Alta", vector: "/img/vector_ex_2_4.png", muscle: "Deltoides Posterior", target_sets: 3, target_reps: "10-12", target_weight: "23-27 kg", rir: "RIR 2", cue: "Cuerda a la frente con rotación externa de hombro." },
          { num: 5, name: "Curl Bíceps Mancuernas Inclinado", vector: "/img/vector_ex_2_5.png", muscle: "Bíceps", target_sets: 3, target_reps: "8-10", target_weight: "12 kg/mano", rir: "RIR 1", cue: "Estiramiento máximo con los codos perpendiculares al suelo." },
          { num: 6, name: "Curl en Banco Scott / Predicador", vector: "/img/vector_ex_2_6.png", muscle: "Braquial & Bíceps", target_sets: 3, target_reps: "8-10", target_weight: "25 kg", rir: "RIR 1", cue: "Aislamiento estricto sin balanceo del torso." }
        ]
      },
      3: {
        title: "Rutina 3 · Pierna 2 (Cadena Posterior & Blindaje Isquios)",
        day: "Jueves/Viernes 17:30 • 50 min • RIR 1",
        exercises: [
          { num: 1, name: "Hip Thrust con Barra", vector: "/img/vector_ex_3_1.png", muscle: "Glúteo Mayor", target_sets: 4, target_reps: "4-6", target_weight: "130-140 kg", rir: "RIR 1", cue: "Parada de 1s arriba con retroversión pélvica y mentón pegado." },
          { num: 2, name: "Peso Muerto Rumano Unilateral", vector: "/img/vector_ex_3_2.png", muscle: "Isquiotibiales", target_sets: 3, target_reps: "6-8", target_weight: "20-24 kg/mano", rir: "RIR 1-2", cue: "Bisagra de cadera unipodal pura con espalda neutra y pierna retrasada." },
          { num: 3, name: "Prensa Pies Altos y Anchos", vector: "/img/vector_ex_3_3.png", muscle: "Glúteos & Aductores", target_sets: 3, target_reps: "6-8", target_weight: "+40-45 kg/lado", rir: "RIR 1", cue: "Empuje de talones reduciendo el estrés en el tendón rotuliano." },
          { num: 4, name: "Sóleo Sentado en Máquina", vector: "/img/vector_ex_3_4.png", muscle: "Sóleo", target_sets: 4, target_reps: "8-10", target_weight: "40 kg", rir: "RIR 1", cue: "El sóleo absorbe hasta 8x el peso corporal en cada zancada." },
          { num: 5, name: "Curl Femoral Tumbado", vector: "/img/vector_ex_3_5.png", muscle: "Isquiotibiales", target_sets: 3, target_reps: "6-8", target_weight: "42 kg", rir: "RIR 1", cue: "Frena la fase excéntrica en 3s para blindar la unión miotendinosa." },
          { num: 6, name: "Elevaciones de Piernas Colgado", vector: "/img/vector_ex_3_6.png", muscle: "Core & Abdomen", target_sets: 3, target_reps: "10-12", target_weight: "Autocarga", rir: "RIR 1", cue: "Sube las piernas en L a 90° flexionando la pelvis sin balanceo." }
        ]
      },
      4: {
        title: "Rutina 4 · Torso Empuje (Pectoral, Deltoides & Tríceps)",
        day: "Sábado 11:00 • 45 min • RIR 1-2",
        exercises: [
          { num: 1, name: "Press de Banca Plano", vector: "/img/vector_ex_4_1.png", muscle: "Pectoral Mayor", target_sets: 4, target_reps: "4-6", target_weight: "60-65 kg", rir: "RIR 1-2", cue: "Escápulas retraídas, barra al esternón y empuje firme." },
          { num: 2, name: "Press Inclinado con Mancuernas 30°", vector: "/img/vector_ex_4_2.png", muscle: "Pectoral Superior", target_sets: 3, target_reps: "6-8", target_weight: "22 kg/mano", rir: "RIR 1", cue: "Banca a 30° para activación máxima de la porción clavicular." },
          { num: 3, name: "Pec Deck / Contractor", vector: "/img/vector_ex_4_3.png", muscle: "Pectoral (Aislamiento)", target_sets: 3, target_reps: "8-10", target_weight: "50 kg", rir: "RIR 1", cue: "Cierre al esternón con compresión isométrica de 1s." },
          { num: 4, name: "Elevaciones Laterales con Mancuernas", vector: "/img/vector_ex_4_4.png", muscle: "Deltoides Lateral", target_sets: 4, target_reps: "10-12", target_weight: "10 kg/mano", rir: "RIR 1", cue: "Eleva en el plano escapular liderando con los codos." },
          { num: 5, name: "Tríceps en Polea Unilateral", vector: "/img/vector_ex_4_5.png", muscle: "Tríceps", target_sets: 3, target_reps: "8-10", target_weight: "12-15 kg", rir: "RIR 1", cue: "Extensión unilateral estricta bloqueando abajo sin balancear el hombro." },
          { num: 6, name: "Plancha Frontal Core Estricta", vector: "/img/vector_ex_4_6.png", muscle: "Core & Abdomen", target_sets: 3, target_reps: "40-45s", target_weight: "Autocarga", rir: "RIR 0", cue: "Tensión de glúteos y abdomen como una tabla de piedra." }
        ]
      }
    };

    function handleImgError(img) {
      img.onerror = null;
      img.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200"><rect width="400" height="200" fill="%231D1E2C"/><text x="50%" y="50%" fill="%238E8FA3" font-family="sans-serif" font-size="14" text-anchor="middle" dominant-baseline="middle">Ilustración Vectorial</text></svg>';
    }

    function switchTab(tabId) {
      const tabs = ['dashboard', 'workouts', 'gym', 'goals', 'profile'];
      tabs.forEach(t => {
        const el = document.getElementById('tab-' + t);
        if (el) el.classList.toggle('hidden', t !== tabId);

        const deskBtn = document.getElementById('nav-desktop-' + t);
        if (deskBtn) {
          deskBtn.classList.toggle('active-nav-link', t === tabId);
          deskBtn.classList.toggle('text-[#FF5E80]', t === tabId);
          deskBtn.classList.toggle('text-[#8E8FA3]', t !== tabId);
        }

        const dockBtn = document.getElementById('dock-btn-' + t);
        if (dockBtn) {
          dockBtn.classList.toggle('text-[#FF5E80]', t === tabId);
          dockBtn.classList.toggle('text-[#8E8FA3]', t !== tabId);
        }
      });

      if (tabId === 'gym') {
        selectGymRoutine(3);
      }
      if (tabId === 'profile') {
        calculateBMI();
      }
      window.scrollTo({ top: 0, behavior: 'smooth' });
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

      const savedKey = 'aegis_workout_v3_' + todayISO + '_r' + routineId;
      const raw = localStorage.getItem(savedKey);
      if (raw) {
        try { currentGymState = JSON.parse(raw); } catch(e) { currentGymState = {}; }
      } else {
        currentGymState = {};
      }

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
            '<div class="w-full md:w-80 h-36 rounded-2xl overflow-hidden bg-[#141522] border border-[#2D2F45] flex items-center justify-center p-2 relative flex-shrink-0">' +
              '<img src="' + ex.vector + '" alt="' + ex.name + '" class="max-h-full max-w-full object-contain" onerror="handleImgError(this)">' +
              '<span class="absolute top-2 left-2 text-[10px] font-extrabold px-2 py-0.5 rounded-lg bg-[#242638] text-[#7B88FF] border border-[#2D2F45] uppercase tracking-wider">' +
                ex.muscle +
              '</span>' +
            '</div>' +

            '<!-- Detalle del Ejercicio -->' +
            '<div class="flex-1 w-full space-y-3">' +
              '<div>' +
                '<h4 class="text-base font-extrabold text-white">' + ex.name + '</h4>' +
                '<p class="text-xs text-[#8E8FA3] mt-0.5 font-medium">Objetivo: <strong class="text-white">' + ex.target_sets + ' series &times; ' + ex.target_reps + ' reps</strong> @ <strong class="text-[#FF5E80] font-mono">' + ex.target_weight + '</strong> (' + ex.rir + ')</p>' +
              '</div>' +

              '<!-- Tabla de Series (ORDEN: Serie - Reps - Carga - Acción) -->' +
              '<div class="overflow-x-auto">' +
                '<div class="min-w-[320px] space-y-2" id="sets-container-' + ex.num + '">' +
                  renderExerciseSetsHtml(routineId, ex.num) +
                '</div>' +
              '</div>' +

              '<!-- Botón Añadir Serie -->' +
              '<div class="flex items-center justify-between pt-1">' +
                '<button onclick="addSetRow(' + routineId + ', ' + ex.num + ')" id="add-set-btn-' + ex.num + '" class="px-3 py-1.5 rounded-xl bg-[#242638] border border-[#2D2F45] text-[#8E8FA3] hover:text-white text-xs font-bold transition flex items-center gap-1.5">' +
                  '<i data-lucide="plus" class="w-3.5 h-3.5 text-[#FF5E80]"></i> + Añadir Serie' +
                '</button>' +
                '<div class="text-[11px] text-[#8E8FA3] italic">' + ex.cue + '</div>' +
              '</div>' +

              '<!-- Notas del Ejercicio -->' +
              '<div class="pt-1">' +
                '<input type="text" value="' + (currentGymState[ex.num].notes || '') + '" oninput="updateExerciseNotes(' + routineId + ', ' + ex.num + ', this.value)" placeholder="Sensaciones, RIR o apuntes del ejercicio..." class="w-full bg-[#141522] border border-[#2D2F45] rounded-xl px-3 py-1.5 text-xs text-[#8E8FA3] focus:text-white focus:outline-none focus:border-[#7B88FF] transition">' +
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
      let out = '<div class="grid grid-cols-12 gap-2 text-[10px] text-[#8E8FA3] font-bold uppercase tracking-wider px-2 pb-1 border-b border-[#2D2F45]/60">' +
        '<div class="col-span-2">Serie</div>' +
        '<div class="col-span-4">Reps</div>' +
        '<div class="col-span-4">Carga (kg)</div>' +
        '<div class="col-span-2 text-center">Acción</div>' +
      '</div>';

      exState.sets.forEach((s, idx) => {
        out += '<div class="grid grid-cols-12 gap-2 items-center p-2 rounded-xl bg-[#141522] border border-[#2D2F45] text-xs font-mono">' +
          '<div class="col-span-2 font-bold text-[#8E8FA3] flex items-center gap-1">' +
            '<span class="w-5 h-5 rounded-lg bg-[#242638] text-white flex items-center justify-center text-[10px]">' + s.set_num + '</span>' +
          '</div>' +
          '<div class="col-span-4">' +
            '<input type="text" value="' + (s.reps || '') + '" oninput="updateSetReps(' + routineId + ', ' + exNum + ', ' + idx + ', this.value)" placeholder="reps" class="w-full bg-[#1D1E2C] border border-[#2D2F45] rounded-lg px-2.5 py-1 text-white font-bold text-xs focus:outline-none focus:border-[#FF5E80] transition">' +
          '</div>' +
          '<div class="col-span-4">' +
            '<input type="text" value="' + (s.weight || '') + '" oninput="updateSetWeight(' + routineId + ', ' + exNum + ', ' + idx + ', this.value)" placeholder="kg" class="w-full bg-[#1D1E2C] border border-[#2D2F45] rounded-lg px-2.5 py-1 text-white font-bold text-xs focus:outline-none focus:border-[#FF5E80] transition">' +
          '</div>' +
          '<div class="col-span-2 flex items-center justify-center gap-1">' +
            (exState.sets.length > 1 ? '<button onclick="removeSetRow(' + routineId + ', ' + exNum + ', ' + idx + ')" class="w-6 h-6 rounded-lg bg-[#242638] hover:bg-rose-500/20 text-[#8E8FA3] hover:text-[#FF5E80] flex items-center justify-center transition" title="Eliminar serie">&times;</button>' : '<span class="text-[#20D994] font-bold text-xs">✓</span>') +
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
        if (btn && btn.classList.contains('bg-[#FF5E80]')) {
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
          btn.classList.remove('bg-[#FF5E80]');
          setTimeout(() => {
            btnText.innerText = original;
            btn.classList.remove('bg-[#20D994]');
            btn.classList.add('bg-[#FF5E80]');
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
    let currentMonthOffset = 0; // 0 = Nov 2026

    function changeCalendarMonth(delta) {
      currentMonthOffset += delta;
      renderCalendarMonth();
    }

    function renderCalendarMonth() {
      const grid = document.getElementById('calendar-days-grid');
      const label = document.getElementById('calendar-month-label');
      if (!grid) return;

      // Noviembre 2026 como base
      label.innerText = currentMonthOffset === 0 ? "Noviembre 2026" : (currentMonthOffset === -1 ? "Octubre 2026" : "Diciembre 2026");

      let html = '';
      const totalDays = 30;
      const startOffset = 6; // Domingo 1 Nov (índice 6)

      // Celdas vacías antes del día 1
      for (let i = 0; i < startOffset; i++) {
        html += '<div class="h-14 sm:h-16 rounded-xl bg-[#141522]/30 border border-transparent"></div>';
      }

      // Días 1 a 30
      for (let day = 1; day <= totalDays; day++) {
        const dayStr = day < 10 ? '0' + day : '' + day;
        const dateKey = '2026-11-' + dayStr;
        const act = calendarData.activities[dateKey];
        const isToday = dateKey === todayISO;

        let dotHtml = '';
        if (act && act.dots) {
          act.dots.forEach(d => {
            let color = '#FF5E80';
            if (d === 'gym') color = '#7B88FF';
            if (d === 'mountain') color = '#20D994';
            dotHtml += '<span class="w-1.5 h-1.5 rounded-full" style="background-color: ' + color + ';"></span>';
          });
        }

        const borderCls = isToday ? 'border-[#FF5E80] glow-pink bg-[#1D1E2C]' : (act ? 'border-[#2D2F45] bg-[#1D1E2C]' : 'border-[#2D2F45]/40 bg-[#141522]');
        const textCls = isToday ? 'text-[#FF5E80] font-black' : (act ? 'text-white font-bold' : 'text-[#8E8FA3]/60');

        html += '<div data-date="' + dateKey + '" onclick="onCalendarDayClick(this)" class="h-14 sm:h-16 p-1.5 rounded-xl border ' + borderCls + ' flex flex-col justify-between cursor-pointer hover:border-[#7B88FF] transition select-none">' +
          '<div class="flex items-center justify-between">' +
            '<span class="text-xs sm:text-sm font-mono ' + textCls + '">' + day + '</span>' +
            (isToday ? '<span class="text-[8px] font-black uppercase px-1 rounded bg-[#FF5E80] text-white">HOY</span>' : '') +
          '</div>' +
          '<div class="flex items-center gap-1 justify-center pb-1">' +
            dotHtml +
          '</div>' +
        '</div>';
      }

      grid.innerHTML = html;
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

      document.getElementById('detail-date-badge').innerText = formattedDate;

      if (act) {
        document.getElementById('detail-title').innerText = act.title;
        document.getElementById('detail-dist').innerText = (act.km > 0 ? act.km + ' km' : act.time);
        document.getElementById('detail-pace').innerText = act.pace;
        document.getElementById('detail-hr').innerText = act.hr;
        document.getElementById('detail-ai').innerText = act.ai;
      } else {
        document.getElementById('detail-title').innerText = "Día de Descanso & Recuperación Celular";
        document.getElementById('detail-dist').innerText = "-";
        document.getElementById('detail-pace').innerText = "-";
        document.getElementById('detail-hr').innerText = "FCR 42 ppm";
        document.getElementById('detail-ai').innerText = "Asimilación fisiológica de la carga previa. Reparación del tejido conjuntivo y supercompensación de glucógeno muscular.";
      }
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
          badgeHtml = '<span class="text-[10px] font-black uppercase px-2.5 py-1 rounded-full bg-[#FF5E80] text-white glow-pink">HOY</span>';
        } else if (isPast) {
          badgeHtml = '<span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-[#20D994]/20 text-[#20D994] flex items-center gap-1"><i data-lucide="check" class="w-3 h-3"></i> Completado</span>';
        } else if (isKey) {
          badgeHtml = '<span class="text-[10px] font-bold uppercase px-2 py-0.5 rounded bg-[#7B88FF]/20 text-[#7B88FF]">Sesión Clave</span>';
        }

        const borderClass = isToday ? 'border-[#FF5E80] glow-pink' : 'border-[#2D2F45]';
        const startOpen = isToday || (!daysData.some(d => d.date === todayISO) && idx === 0);

        html += '<div class="luxury-card ' + borderClass + ' overflow-hidden transition-all">' +
          '<div onclick="toggleDayAccordion(' + idx + ')" class="p-4 sm:p-5 flex items-center justify-between cursor-pointer hover:bg-[#242638]/40 transition select-none">' +
            '<div class="flex items-center gap-3">' +
              badgeHtml +
              '<div>' +
                '<span class="text-sm sm:text-base font-extrabold text-white">' + day.day_name + ' ' + day.date.substring(8) + ' ' + (day.date.substring(5, 7) === '11' ? 'Nov' : 'Dic') + '</span>' +
                '<div class="text-xs text-[#8E8FA3] font-medium mt-0.5">' +
                  (day.running.is_rest ? 'Descanso carrera' : day.running.title) + ' &bull; ' +
                  (day.gym.is_rest ? 'Descanso fuerza' : day.gym.routine_name.split('·')[0]) +
                '</div>' +
              '</div>' +
            '</div>' +
            '<i id="day-icon-' + idx + '" data-lucide="chevron-down" class="w-5 h-5 text-[#8E8FA3] transition-transform duration-200" style="transform: ' + (startOpen ? 'rotate(180deg)' : 'rotate(0deg)') + ';"></i>' +
          '</div>' +

          '<div id="day-body-' + idx + '" class="px-4 pb-4 sm:px-6 sm:pb-6 pt-1 space-y-4 border-t border-[#2D2F45]/50 ' + (startOpen ? '' : 'hidden') + '">' +
            '<!-- Running -->' +
            (day.running.is_rest 
              ? '<div class="p-3.5 rounded-xl bg-[#141522] border border-[#2D2F45]/60 text-xs text-[#8E8FA3] flex items-center gap-2"><i data-lucide="moon" class="w-4 h-4 text-[#7B88FF]"></i> Descanso de running: Recuperación activa y regeneración celular.</div>'
              : '<div class="p-4 rounded-xl bg-[#141522] border border-[#2D2F45] space-y-2">' +
                '<div class="flex items-center justify-between text-xs font-bold text-[#FF5E80]">' +
                  '<span class="flex items-center gap-1.5">' +
                    '<i data-lucide="footprints" class="w-4 h-4"></i> ' + day.running.title +
                  '</span>' +
                  '<span class="text-xs font-mono font-black text-white">' + day.running.duration_min + ' min &bull; ' + day.running.target_distance_km + ' km</span>' +
                '</div>' +
                '<p class="text-xs text-white/90 leading-relaxed">' + day.running.main_work + '</p>' +
                '<div class="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-1 text-[11px] font-mono">' +
                  '<div class="p-2 rounded-lg bg-[#1D1E2C] border border-[#2D2F45] text-[#8E8FA3]">' +
                    'RITMO: <strong class="text-white">' + day.running.target_pace + '</strong>' +
                  '</div>' +
                  '<div class="p-2 rounded-lg bg-[#1D1E2C] border border-[#2D2F45] text-[#8E8FA3]">' +
                    'ZONA FC: <strong class="text-[#FF5E80]">' + day.running.hr_zone + '</strong>' +
                  '</div>' +
                  '<div class="p-2 rounded-lg bg-[#1D1E2C] border border-[#2D2F45] text-[#8E8FA3] col-span-2 sm:col-span-1">' +
                    'ZAPATILLA: <strong class="text-white">' + (day.running.shoe || 'Asics Novablast') + '</strong>' +
                  '</div>' +
                '</div>' +
              '</div>'
            ) +

            '<!-- Fuerza Gym -->' +
            (day.gym.is_rest
              ? '<div class="p-3.5 rounded-xl bg-[#141522] border border-[#2D2F45]/60 text-xs text-[#8E8FA3] flex items-center gap-2"><i data-lucide="coffee" class="w-4 h-4 text-[#20D994]"></i> Descanso de gimnasio: 0 fatiga neuromuscular.</div>'
              : '<div class="p-4 rounded-xl bg-[#141522] border border-[#2D2F45] space-y-3">' +
                '<div class="flex items-center justify-between text-xs font-bold text-[#7B88FF]">' +
                  '<span class="flex items-center gap-1.5">' +
                    '<i data-lucide="dumbbell" class="w-4 h-4"></i> ' + day.gym.routine_name +
                  '</span>' +
                  '<button onclick="goToGymRoutine(' + (day.gym.routine_id || 1) + ')" class="px-2.5 py-1 rounded-lg bg-[#7B88FF] text-white text-[11px] font-bold hover:brightness-110 transition">' +
                    'Ir a la Rutina &rarr;' +
                  '</button>' +
                '</div>' +
                '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">' +
                  (day.gym.highlight_exercises || day.gym.exercises || []).map(function(ex) {
                    return '<div class="p-2 rounded-lg bg-[#1D1E2C] border border-[#2D2F45] flex items-center justify-between text-[11px]">' +
                      '<span class="text-white font-medium">' + ex.name + '</span>' +
                      '<span class="font-mono text-[#7B88FF] font-bold">' + ex.load + ' (' + ex.rir + ')</span>' +
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
          statusTitle.className = "text-xs font-black text-[#FF5E80] uppercase tracking-wider";
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
      selectCalendarDay('2026-11-14');
      selectGymRoutine(3);
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

      // Gráfico Spline de Volumen Semanal
      const ctxSpline = document.getElementById('weeklySplineChart')?.getContext('2d');
      if (ctxSpline) {
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
                label: 'Volumen Running (KM)',
                data: kmValues,
                borderColor: '#FF5E80',
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                backgroundColor: gradientPink,
                pointBackgroundColor: '#FF5E80',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 2,
                pointRadius: 4,
                pointHoverRadius: 6,
                yAxisID: 'y'
              },
              {
                label: 'Sesiones Gimnasio',
                data: gymValues,
                borderColor: '#7B88FF',
                borderWidth: 2.5,
                borderDash: [4, 4],
                tension: 0.3,
                fill: false,
                backgroundColor: gradientBlue,
                pointBackgroundColor: '#7B88FF',
                pointBorderColor: '#FFFFFF',
                pointBorderWidth: 1.5,
                pointRadius: 3,
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
                backgroundColor: '#1D1E2C',
                borderColor: '#2D2F45',
                borderWidth: 1,
                titleColor: '#FFFFFF',
                bodyColor: '#8E8FA3',
                padding: 12,
                cornerRadius: 12,
                callbacks: {
                  label: function(ctx) {
                    return ctx.datasetIndex === 0 
                      ? ' ' + ctx.parsed.y + ' km rodados' 
                      : ' ' + ctx.parsed.y + ' sesiones gym';
                  }
                }
              }
            },
            scales: {
              x: {
                grid: { display: false },
                ticks: { color: '#8E8FA3', font: { family: 'Plus Jakarta Sans', size: 11 } }
              },
              y: {
                position: 'left',
                grid: { color: 'rgba(45, 47, 69, 0.4)', drawBorder: false },
                ticks: {
                  color: '#FF5E80',
                  font: { family: 'JetBrains Mono', size: 11 },
                  callback: function(v) { return v + ' km'; }
                }
              },
              y1: {
                position: 'right',
                grid: { display: false },
                min: 0,
                max: 6,
                ticks: {
                  color: '#7B88FF',
                  font: { family: 'JetBrains Mono', size: 10 },
                  callback: function(v) { return v + ' gym'; }
                }
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
    f.write(worker_ts)

print(f"Index.ts v3 actualizado exitosamente ({len(worker_ts)} bytes)")
