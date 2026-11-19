const fs = require('fs');
const vm = require('vm');
const path = require('path');

const planJson = fs.readFileSync(path.join(__dirname, '../cloudflare/plan.json'), 'utf8');
const planData = JSON.parse(planJson);

const indexTsContent = `export interface Env {
  ATHLETE_ID: string;
  INTERVALS_API_KEY: string;
  TELEGRAM_BOT_TOKEN?: string;
  TELEGRAM_CHAT_ID?: string;
  AEGIS_KV?: KVNamespace;
}

// ==========================================
// DATE & TIMEZONE HELPERS (EUROPE/MADRID)
// ==========================================
function getTodayMadridISO(): string {
  return new Intl.DateTimeFormat('en-CA', {
    timeZone: 'Europe/Madrid',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  }).format(new Date());
}

function calculateDaysRemaining(targetDateISO: string, todayISO: string): number {
  const target = new Date(targetDateISO + "T00:00:00Z").getTime();
  const today = new Date(todayISO + "T00:00:00Z").getTime();
  const diffDays = Math.ceil((target - today) / (1000 * 60 * 60 * 24));
  return Math.max(0, diffDays);
}

// ==========================================
// MASTER FALLBACK PLAN (14 DÍAS)
// ==========================================
const DEFAULT_PLAN: any = ${JSON.stringify(planData, null, 2)};

export default {
  // Cron Trigger: se ejecuta cada 4 horas
  async scheduled(event: ScheduledEvent, env: Env, ctx: ExecutionContext): Promise<void> {
    ctx.waitUntil(checkNewActivities(env));
  },

  // Manejo de peticiones HTTP
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // 1. Servir imágenes de ejercicios desde KV
    if (url.pathname.startsWith("/img/")) {
      const key = "img_" + url.pathname.replace("/img/", "").replace(".jpg", "");
      if (env.AEGIS_KV) {
        const imgData = await env.AEGIS_KV.get(key, { type: "arrayBuffer" });
        if (imgData) {
          return new Response(imgData, {
            headers: {
              "Content-Type": "image/jpeg",
              "Cache-Control": "public, max-age=31536000, immutable"
            }
          });
        }
      }
      return new Response("Not found", { status: 404 });
    }

    // 2. Webhook interactivo de Telegram (POST)
    if (request.method === "POST" && env.TELEGRAM_BOT_TOKEN) {
      try {
        const update = (await request.json()) as any;
        if (update.message && update.message.text) {
          await handleTelegramMessage(update.message, env);
        }
      } catch (e) {}
      return new Response("OK");
    }

    // 3. Endpoint API JSON si se pide con ?format=json
    if (url.searchParams.get("format") === "json") {
      const summary = await checkNewActivities(env);
      return new Response(JSON.stringify(summary, null, 2), {
        headers: { "Content-Type": "application/json; charset=utf-8" }
      });
    }

    // 4. Obtener el plan dinámico desde KV (o fallback maestro)
    let activePlan: any = null;
    if (env.AEGIS_KV) {
      try {
        const raw = await env.AEGIS_KV.get("current_plan");
        if (raw) activePlan = JSON.parse(raw);
      } catch (e) {}
    }
    if (!activePlan) {
      activePlan = DEFAULT_PLAN;
    }

    // 5. Servir el Dashboard Móvil Dinámico
    const html = getMobileDashboardHtml(activePlan);
    return new Response(html, {
      headers: { "Content-Type": "text/html; charset=utf-8" }
    });
  }
};

// ==========================================
// TELEGRAM INTERACTIVO (DINÁMICO POR FECHA MADRID)
// ==========================================
async function handleTelegramMessage(message: any, env: Env) {
  const chatId = message.chat.id;
  const text = (message.text || "").trim().toLowerCase();
  const token = env.TELEGRAM_BOT_TOKEN!;
  const todayISO = getTodayMadridISO();

  let plan: any = null;
  if (env.AEGIS_KV) {
    try {
      const raw = await env.AEGIS_KV.get("current_plan");
      if (raw) plan = JSON.parse(raw);
    } catch (e) {}
  }
  if (!plan) plan = DEFAULT_PLAN;

  const targetRaceDate = plan?.macrocycle?.primary_objective?.date || "2026-11-28";
  const targetRaceName = plan?.macrocycle?.primary_objective?.name || "Cross Popular Parque del Soto (Ávila)";
  const daysLeft = calculateDaysRemaining(targetRaceDate, todayISO);

  let reply = "";

  if (text.includes("hoy") || text === "/hoy") {
    const todayDay = plan?.days?.find((d: any) => d.date === todayISO) || plan?.days?.[0];

    if (todayDay) {
      const runTxt = todayDay.running?.is_rest
        ? "• Carrera: Descanso total de carrera (Asimilación)."
        : \`• Carrera: \${todayDay.running?.title}\\n\` +
          \`  - Ritmo: \${todayDay.running?.target_pace}\\n\` +
          \`  - Duración: \${todayDay.running?.duration_min} min (~\${todayDay.running?.target_distance_km} km)\\n\` +
          \`  - Calzado: \${todayDay.running?.shoes_recommended}\`;

      let gymTxt = "";
      if (todayDay.gym?.is_rest) {
        gymTxt = "• Gimnasio: Descanso de fuerza.";
      } else {
        gymTxt = \`• Gimnasio: \${todayDay.gym?.routine_name}\\n\` +
          (todayDay.gym?.highlight_exercises || []).map((e: any) => \`  - \${e.name}: \${e.load}\`).join('\\n') +
          (todayDay.gym?.knee_vmo_protocol ? \`\\n  - VMO Rodilla: \${todayDay.gym.knee_vmo_protocol}\` : "");
      }

      reply = \`[ENTRENAMIENTO DE HOY - \${todayDay.day_name} \${todayDay.display_date}]\\n\\n\` +
        \`\${runTxt}\\n\\n\` +
        \`\${gymTxt}\\n\\n\` +
        \`🎯 Quedan \${daysLeft} días para el Cross del Soto.\\n\` +
        \`👉 Dashboard interactivo: https://aegis-intervals-sync.uranuslabs.workers.dev\`;
    } else {
      reply = \`[HOY - \${todayISO}]\\n\\n\` +
        \`No hay sesión cargada para hoy en el plan.\\n\` +
        \`Próximo objetivo: \${targetRaceName} en \${daysLeft} días.\\n\` +
        \`Dashboard: https://aegis-intervals-sync.uranuslabs.workers.dev\`;
    }
  } else if (text.includes("semana") || text === "/semana") {
    if (plan && plan.days) {
      reply = \`[MICROCICLO 14 DÍAS - \${plan.macrocycle?.current_microcycle || 'Afinamiento Cross'}]\\n\` +
        \`Objetivo: \${targetRaceName} (\${daysLeft} días restantes)\\n\\n\`;

      for (const d of plan.days) {
        let tag = "[PEND]";
        if (d.date < todayISO || d.manual_status === "done") tag = "[OK]";
        else if (d.date === todayISO) tag = "[HOY]";
        else if (d.is_key_session) tag = "[CLAVE]";

        const runBrief = d.running?.is_rest ? "Descanso Run" : \`\${d.running?.session_type} (\${d.running?.target_pace})\`;
        const gymBrief = d.gym?.is_rest ? "Sin Gym" : (d.gym?.routine_name?.split('·')[1]?.trim() || "Gym");

        reply += \`\${tag} \${d.day_name} \${d.display_date}: \${runBrief} | \${gymBrief}\\n\`;
      }
      reply += \`\\n👉 Ver fotos y registrar cargas: https://aegis-intervals-sync.uranuslabs.workers.dev\`;
    } else {
      reply = \`[PLAN ACTIVO]\\nConsulta tu plan completo en: https://aegis-intervals-sync.uranuslabs.workers.dev\`;
    }
  } else if (text.includes("rodilla") || text === "/rodilla") {
    reply = \`[VIGILANCIA BIOMECÁNICA - RODILLA IZQUIERDA]\\n\\n\` +
      \`• Atleta: Carlos Jiménez Andrino\\n\` +
      \`• Estado actual: Asintomático (0/10 dolor tras derrame sinovial 05/11).\\n\` +
      \`• Pauta estricta: Cero sentadillas libres profundas ni prensa pesada a 90°.\\n\` +
      \`• Blindaje VMO: Spanish Squat isométrica con banda elástica (4x35-40s) para reclutamiento puro del vasto medial sin rozamiento patelofemoral.\`;
  } else {
    reply = \`Aegis Coach — Carlos Jiménez Andrino\\n\\n\` +
      \`Comandos tácticos:\\n\` +
      \`• /hoy — Qué te toca hoy (carrera + gym)\\n\` +
      \`• /semana — Microciclo semanal completo (14 días)\\n\` +
      \`• /rodilla — Protocolo de descarga y VMO\\n\\n\` +
      \`📊 Dashboard Web App: https://aegis-intervals-sync.uranuslabs.workers.dev\`;
  }

  const url = \`https://api.telegram.org/bot\${token}/sendMessage\`;
  await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      chat_id: chatId,
      text: reply
    })
  });
}

// ==========================================
// CRON BACKGROUND MONITORING
// ==========================================
async function checkNewActivities(env: Env) {
  const athleteId = env.ATHLETE_ID || "i690671";
  const apiKey = env.INTERVALS_API_KEY || "4cvqxm8a5intat925ttdcmpja";
  const authHeader = "Basic " + btoa("API_KEY:" + apiKey);

  const now = new Date();
  const twoDaysAgo = new Date(now.getTime() - 2 * 24 * 60 * 60 * 1000);
  const oldest = twoDaysAgo.toISOString().split("T")[0];
  const newest = now.toISOString().split("T")[0];

  const url = \`https://intervals.icu/api/v1/athlete/\${athleteId}/activities?oldest=\${oldest}&newest=\${newest}\`;
  const res = await fetch(url, { headers: { Authorization: authHeader } });

  if (!res.ok) {
    return { error: \`Intervals.icu returned status \${res.status}\` };
  }

  const activities = (await res.json()) as any[];
  const notified: any[] = [];

  for (const act of activities) {
    const actId = act.id;
    const name = act.name || "Entrenamiento";
    const type = act.type || "Workout";
    const distKm = ((act.distance || 0) / 1000).toFixed(2);
    const timeMin = Math.round((act.moving_time || 0) / 60);
    const avgHr = act.average_heartrate || "-";
    const maxHr = act.max_heartrate || "-";
    const load = act.icu_training_load || 0;
    const dateStr = act.start_date_local || "";

    if (env.AEGIS_KV) {
      const alreadySent = await env.AEGIS_KV.get(\`notified_\${actId}\`);
      if (alreadySent) continue;
    }

    if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
      const msg = \`[NUEVA SESIÓN EN GARMIN]\\n\\n\` +
        \`• Atleta: Carlos Jiménez Andrino\\n\` +
        \`• Fecha: \${dateStr.replace("T", " ")}\\n\` +
        \`• Sesión: \${name} (\${type})\\n\` +
        (distKm !== "0.00" ? \`• Distancia: \${distKm} km\\n\` : "") +
        \`• Duración: \${timeMin} min\\n\` +
        (avgHr !== "-" ? \`• FC Media: \${avgHr} ppm (Máx: \${maxHr})\\n\` : "") +
        \`• Carga (Load): \${load}\\n\\n\` +
        \`👉 Escribe /hoy o abre: https://aegis-intervals-sync.uranuslabs.workers.dev\`;

      const telegramUrl = \`https://api.telegram.org/bot\${env.TELEGRAM_BOT_TOKEN}/sendMessage\`;
      await fetch(telegramUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: env.TELEGRAM_CHAT_ID,
          text: msg
        })
      });

      if (env.AEGIS_KV) {
        await env.AEGIS_KV.put(\`notified_\${actId}\`, "true", { expirationTtl: 30 * 24 * 60 * 60 });
      }
    }

    notified.push({ id: actId, name, type, distKm, timeMin, load });
  }

  return { success: true, total_activities: activities.length, newly_notified: notified.length, notified };
}

// ==========================================
// DASHBOARD WEB APP (REFINED PETROLEUM UX)
// ==========================================
function getMobileDashboardHtml(planData: any): string {
  const plan = planData || DEFAULT_PLAN;
  const athleteName = plan?.athlete?.name || "Carlos Jiménez Andrino";
  const todayISO = getTodayMadridISO();
  const raceDate = plan?.macrocycle?.primary_objective?.date || "2026-11-28";
  const raceName = plan?.macrocycle?.primary_objective?.name || "Cross Popular Parque del Soto (Ávila)";
  const targetPace = plan?.macrocycle?.primary_objective?.target_pace || "3:35 - 3:40/km (~18:00)";
  const countdownDays = calculateDaysRemaining(raceDate, todayISO);
  const weeksRemaining = (countdownDays / 7).toFixed(1);

  // Lista de 14 días
  const daysList: any[] = plan?.days || DEFAULT_PLAN.days || [];
  const todayIndex = daysList.findIndex((d: any) => d.date === todayISO);
  const activeDayIndex = todayIndex >= 0 ? todayIndex : 0;
  const todayDay = daysList[activeDayIndex] || daysList[0];

  return \`<!DOCTYPE html>
<html lang="es" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Aegis Coach — \${athleteName}</title>
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="theme-color" content="#05161A">
  <!-- Tailwind CSS -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Fonts: Outfit (Titulares & Números de Rendimiento) + Manrope (Cuerpo & Legibilidad) -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Outfit:wght@500;600;700;800;900&display=swap" rel="stylesheet">
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  <!-- Chart.js -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            heading: ['"Outfit"', 'sans-serif'],
            sans: ['"Manrope"', 'system-ui', 'sans-serif'],
            mono: ['"Outfit"', 'monospace'],
          },
          colors: {
            brand: {
              base: '#05161A',        // Base / Fondo principal
              card: '#072E33',        // Contenedores / Tarjetas principales
              interactive: '#0C7075', // Elementos interactivos / Botones secundarios
              accent: '#0F969C',      // Acento primario / Acciones clave / Badges
              muted: '#6DA5C0',       // Texto secundario / Métricas / Iconos suaves
              border: '#294D61',      // Bordes sutiles / Separadores
              light: '#E6F4F6',       // Texto claro legible
              white: '#FFFFFF'
            }
          }
        }
      }
    }
  </script>
  <style>
    body {
      background-color: #05161A;
      color: #E6F4F6;
      font-family: 'Manrope', sans-serif;
      -webkit-font-smoothing: antialiased;
    }
    h1, h2, h3, h4, .font-heading {
      font-family: 'Outfit', sans-serif;
    }
    .mono-num {
      font-family: 'Outfit', monospace;
      font-variant-numeric: tabular-nums;
    }
    .custom-scroll::-webkit-scrollbar {
      display: none;
    }
    .custom-scroll {
      -ms-overflow-style: none;
      scrollbar-width: none;
    }
    .card-aegis {
      background: #072E33;
      border: 1px solid #294D61;
      box-shadow: 0 4px 20px rgba(5, 22, 26, 0.45);
    }
    .subcard-aegis {
      background: rgba(5, 22, 26, 0.55);
      border: 1px solid #294D61;
    }
    .tab-active {
      background: #0F969C;
      color: #05161A;
      font-weight: 800;
      box-shadow: 0 2px 12px rgba(15, 150, 156, 0.35);
    }
    .tab-inactive {
      background: #072E33;
      color: #6DA5C0;
      border: 1px solid #294D61;
    }
    .tab-inactive:hover {
      background: #0C7075;
      color: #FFFFFF;
    }
    .accordion-body {
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
    }
  </style>
</head>
<body class="min-h-screen pb-24 selection:bg-[#0F969C] selection:text-[#05161A]">

  <!-- TOP APP BAR -->
  <header class="sticky top-0 z-40 bg-[#05161A]/95 backdrop-blur-md border-b border-[#294D61] px-4 py-3">
    <div class="max-w-4xl mx-auto flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-[#0C7075] to-[#0F969C] flex items-center justify-center shadow-lg shadow-[#0F969C]/20 border border-[#294D61]">
          <i data-lucide="zap" class="w-5 h-5 text-[#05161A]"></i>
        </div>
        <div>
          <h1 class="text-sm font-extrabold text-white tracking-tight flex items-center gap-2 leading-none font-heading">
            \${athleteName}
            <span class="inline-block w-2 h-2 rounded-full bg-[#0F969C] animate-pulse"></span>
          </h1>
          <p class="text-[11px] text-[#6DA5C0] font-medium mt-1">Aegis Coach &bull; Fisiología & Fuerza</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <a href="https://t.me/aegis_coach_chatbot" target="_blank" class="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-[#072E33] border border-[#294D61] text-xs font-semibold text-[#6DA5C0] hover:text-white hover:border-[#0C7075] transition">
          <i data-lucide="send" class="w-3.5 h-3.5 text-[#0F969C]"></i>
          <span>Telegram</span>
        </a>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER -->
  <main class="max-w-4xl mx-auto px-4 pt-4 space-y-5">

    <!-- 1. COUNTDOWN HERO BANNER DINÁMICO -->
    <section class="card-aegis rounded-2xl p-4 sm:p-5 relative overflow-hidden">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div class="flex items-center gap-2 mb-1.5">
            <span class="px-2.5 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-[#0F969C]/15 text-[#0F969C] border border-[#0F969C]/30 font-heading">
              Próximo Hito Competitivo
            </span>
            <span class="text-xs text-[#6DA5C0]">28 de Noviembre de 2026</span>
          </div>
          <h2 class="text-xl sm:text-2xl font-extrabold text-white tracking-tight font-heading">
            \${raceName}
          </h2>
          <p class="text-xs text-[#6DA5C0] mt-1 font-sans">
            5.0 km hierba / tierra &bull; Ritmo objetivo: <span class="text-white font-mono font-bold">\${targetPace}</span>
          </p>
        </div>

        <div class="flex items-baseline gap-4 bg-[#05161A] px-4 py-2.5 rounded-xl border border-[#294D61]">
          <div>
            <div class="text-2xl sm:text-3xl font-extrabold text-[#0F969C] font-heading leading-none">\${countdownDays}</div>
            <div class="text-[10px] uppercase tracking-wider text-[#6DA5C0] font-bold mt-1">Días</div>
          </div>
          <div class="w-px h-8 bg-[#294D61]"></div>
          <div>
            <div class="text-2xl sm:text-3xl font-extrabold text-white font-heading leading-none">\${weeksRemaining}</div>
            <div class="text-[10px] uppercase tracking-wider text-[#6DA5C0] font-bold mt-1">Semanas</div>
          </div>
        </div>
      </div>

      <!-- Barra de progreso macrociclo -->
      <div class="mt-4 pt-3 border-t border-[#294D61]">
        <div class="flex items-center justify-between text-[11px] mb-1.5 font-medium">
          <span class="text-[#6DA5C0]">Fase de Afinamiento Competitivo</span>
          <span class="text-[#0F969C] font-mono font-bold">78% completado</span>
        </div>
        <div class="w-full h-2 rounded-full bg-[#05161A] overflow-hidden border border-[#294D61]/50">
          <div class="h-full bg-gradient-to-r from-[#0C7075] to-[#0F969C] rounded-full" style="width: 78%;"></div>
        </div>
      </div>
    </section>

    <!-- 2. HIGH DENSITY KPI CARDS ROW -->
    <section class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 sm:gap-3">
      <div class="card-aegis rounded-xl p-3 sm:p-3.5 flex flex-col justify-between">
        <div class="flex items-center justify-between text-[#6DA5C0] mb-2">
          <span class="text-[11px] font-semibold tracking-wide">Volumen 8 Sem.</span>
          <i data-lucide="clock" class="w-4 h-4 text-[#0F969C]"></i>
        </div>
        <div>
          <div class="text-xl sm:text-2xl font-extrabold font-heading text-white">28.5<span class="text-xs text-[#6DA5C0] font-normal ml-1">h</span></div>
          <div class="text-[10px] text-[#0F969C] font-semibold flex items-center gap-1 mt-0.5">
            <i data-lucide="trending-up" class="w-3 h-3"></i>
            <span>+3.2h vs ciclo previo</span>
          </div>
        </div>
      </div>

      <div class="card-aegis rounded-xl p-3 sm:p-3.5 flex flex-col justify-between">
        <div class="flex items-center justify-between text-[#6DA5C0] mb-2">
          <span class="text-[11px] font-semibold tracking-wide">Distancia Run</span>
          <i data-lucide="footprints" class="w-4 h-4 text-[#0F969C]"></i>
        </div>
        <div>
          <div class="text-xl sm:text-2xl font-extrabold font-heading text-white">142.8<span class="text-xs text-[#6DA5C0] font-normal ml-1">km</span></div>
          <div class="text-[10px] text-[#6DA5C0] font-medium mt-0.5">5.1 km/sesión avg</div>
        </div>
      </div>

      <div class="card-aegis rounded-xl p-3 sm:p-3.5 flex flex-col justify-between">
        <div class="flex items-center justify-between text-[#6DA5C0] mb-2">
          <span class="text-[11px] font-semibold tracking-wide">Fuerza & Gym</span>
          <i data-lucide="dumbbell" class="w-4 h-4 text-[#0C7075]"></i>
        </div>
        <div>
          <div class="text-xl sm:text-2xl font-extrabold font-heading text-white">16<span class="text-xs text-[#6DA5C0] font-normal ml-1">ses</span></div>
          <div class="text-[10px] text-[#0F969C] font-medium mt-0.5">Hip Thrust: 140 kg</div>
        </div>
      </div>

      <div class="card-aegis rounded-xl p-3 sm:p-3.5 flex flex-col justify-between">
        <div class="flex items-center justify-between text-[#6DA5C0] mb-2">
          <span class="text-[11px] font-semibold tracking-wide">Estado Articular</span>
          <i data-lucide="shield-check" class="w-4 h-4 text-[#0F969C]"></i>
        </div>
        <div>
          <div class="text-xl sm:text-2xl font-extrabold font-heading text-[#0F969C]">0 / 10</div>
          <div class="text-[10px] text-[#6DA5C0] font-medium mt-0.5">Rodilla asintomática</div>
        </div>
      </div>
    </section>

    <!-- 3. NAVIGATION TABS -->
    <div class="flex gap-1.5 p-1 bg-[#05161A] rounded-xl border border-[#294D61] overflow-x-auto custom-scroll">
      <button onclick="switchTab('overview')" id="tab-btn-overview" class="tab-trigger flex-1 min-w-[90px] py-2 px-3 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 tab-active font-heading">
        <i data-lucide="layout-dashboard" class="w-3.5 h-3.5"></i>
        <span>Dashboard</span>
      </button>
      <button onclick="switchTab('workouts')" id="tab-btn-workouts" class="tab-trigger flex-1 min-w-[90px] py-2 px-3 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 tab-inactive font-heading">
        <i data-lucide="calendar" class="w-3.5 h-3.5"></i>
        <span>Entrenos</span>
      </button>
      <button onclick="switchTab('gym')" id="tab-btn-gym" class="tab-trigger flex-1 min-w-[90px] py-2 px-3 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 tab-inactive font-heading">
        <i data-lucide="dumbbell" class="w-3.5 h-3.5"></i>
        <span>Gimnasio</span>
      </button>
      <button onclick="switchTab('coach')" id="tab-btn-coach" class="tab-trigger flex-1 min-w-[90px] py-2 px-3 rounded-lg text-xs font-bold transition flex items-center justify-center gap-1.5 tab-inactive font-heading">
        <i data-lucide="activity" class="w-3.5 h-3.5"></i>
        <span>Coach Crítico</span>
      </button>
    </div>

    <!-- TAB 1: OVERVIEW & TELEMETRY CHARTS -->
    <div id="tab-content-overview" class="tab-pane space-y-5">
      <!-- Volume Charts -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="card-aegis md:col-span-2 rounded-2xl p-4 sm:p-5">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h3 class="text-sm font-bold text-white flex items-center gap-2 font-heading">
                <i data-lucide="bar-chart-2" class="w-4 h-4 text-[#0F969C]"></i>
                <span>Volumen Semanal Apilado (minutos)</span>
              </h3>
              <p class="text-[11px] text-[#6DA5C0] mt-0.5">Distribución de carrera, fuerza y montaña en 8 semanas</p>
            </div>
            <div class="flex items-center gap-2.5 text-[10px]">
              <span class="flex items-center gap-1 text-[#E6F4F6]"><span class="w-2 h-2 rounded-full bg-[#0F969C]"></span> Run</span>
              <span class="flex items-center gap-1 text-[#E6F4F6]"><span class="w-2 h-2 rounded-full bg-[#0C7075]"></span> Gym</span>
              <span class="flex items-center gap-1 text-[#E6F4F6]"><span class="w-2 h-2 rounded-full bg-[#6DA5C0]"></span> Trail</span>
            </div>
          </div>
          <div class="h-56">
            <canvas id="stackedVolumeChart"></canvas>
          </div>
        </div>

        <div class="card-aegis rounded-2xl p-4 sm:p-5 flex flex-col justify-between">
          <div>
            <h3 class="text-sm font-bold text-white flex items-center gap-2 mb-1 font-heading">
              <i data-lucide="pie-chart" class="w-4 h-4 text-[#0F969C]"></i>
              <span>Distribución Disciplinar</span>
            </h3>
            <p class="text-[11px] text-[#6DA5C0] mb-3">Porcentaje de tiempo dedicado</p>
            <div class="h-44 relative flex items-center justify-center">
              <canvas id="distributionDonutChart"></canvas>
            </div>
          </div>
          <div class="grid grid-cols-3 gap-2 text-center pt-3 border-t border-[#294D61] text-[11px]">
            <div>
              <div class="font-extrabold text-[#0F969C] font-heading text-sm">54%</div>
              <div class="text-[10px] text-[#6DA5C0]">Carrera</div>
            </div>
            <div>
              <div class="font-extrabold text-[#0C7075] font-heading text-sm">31%</div>
              <div class="text-[10px] text-[#6DA5C0]">Fuerza</div>
            </div>
            <div>
              <div class="font-extrabold text-[#6DA5C0] font-heading text-sm">15%</div>
              <div class="text-[10px] text-[#6DA5C0]">Montaña</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Telemetry Card (FIT Dashboard) -->
      <div class="card-aegis rounded-2xl p-4 sm:p-5">
        <div class="flex items-center justify-between mb-4">
          <div>
            <span class="px-2.5 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-[#0F969C]/15 text-[#0F969C] border border-[#0F969C]/30 font-heading">
              Hito de Calibración Cuantitativa
            </span>
            <h3 class="text-base font-extrabold text-white mt-1 font-heading">10K Media Maratón Ávila Monumental</h3>
            <p class="text-xs text-[#6DA5C0]">08/11/2026 &bull; 1.070 m altitud &bull; Oficial: 38:26 (3:50/km)</p>
          </div>
          <div class="text-right">
            <span class="text-xs font-heading font-extrabold text-[#0F969C] px-2.5 py-1 rounded-lg bg-[#0F969C]/10 border border-[#0F969C]/30">
              VO2max: 58.4 ml/kg/min
            </span>
          </div>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-6 gap-2 text-center mb-4">
          <div class="subcard-aegis p-2.5 rounded-xl">
            <div class="text-[10px] text-[#6DA5C0] uppercase font-bold">Distancia</div>
            <div class="text-base font-extrabold font-heading text-white mt-0.5">10.02 km</div>
          </div>
          <div class="subcard-aegis p-2.5 rounded-xl">
            <div class="text-[10px] text-[#6DA5C0] uppercase font-bold">Tiempo Neto</div>
            <div class="text-base font-extrabold font-heading text-white mt-0.5">38:26</div>
          </div>
          <div class="subcard-aegis p-2.5 rounded-xl">
            <div class="text-[10px] text-[#6DA5C0] uppercase font-bold">Ritmo Medio</div>
            <div class="text-base font-extrabold font-heading text-[#0F969C] mt-0.5">3:50 /km</div>
          </div>
          <div class="subcard-aegis p-2.5 rounded-xl">
            <div class="text-[10px] text-[#6DA5C0] uppercase font-bold">FC Media</div>
            <div class="text-base font-extrabold font-heading text-[#6DA5C0] mt-0.5">173 ppm</div>
          </div>
          <div class="subcard-aegis p-2.5 rounded-xl">
            <div class="text-[10px] text-[#6DA5C0] uppercase font-bold">FC Máx</div>
            <div class="text-base font-extrabold font-heading text-white mt-0.5">188 ppm</div>
          </div>
          <div class="subcard-aegis p-2.5 rounded-xl">
            <div class="text-[10px] text-[#6DA5C0] uppercase font-bold">Desnivel</div>
            <div class="text-base font-extrabold font-heading text-[#0F969C] mt-0.5">+142 m</div>
          </div>
        </div>

        <!-- Parciales por Kilómetro -->
        <div class="overflow-x-auto custom-scroll">
          <table class="w-full text-left text-xs">
            <thead>
              <tr class="text-[#6DA5C0] border-b border-[#294D61]">
                <th class="pb-2 font-bold font-heading">KM</th>
                <th class="pb-2 font-bold font-heading">Ritmo</th>
                <th class="pb-2 font-bold font-heading">FC Med</th>
                <th class="pb-2 font-bold font-heading">Cadencia</th>
                <th class="pb-2 font-bold font-heading">Comportamiento Táctico</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-[#294D61]/60 text-[#E6F4F6] font-mono">
              <tr>
                <td class="py-2 text-white font-bold font-heading">KM 1</td>
                <td class="py-2 text-[#0F969C] font-bold">3:42</td>
                <td class="py-2 text-[#6DA5C0]">162 ppm</td>
                <td class="py-2">178 spm</td>
                <td class="py-2 text-[#6DA5C0] font-sans">Bajada inicial controlada</td>
              </tr>
              <tr>
                <td class="py-2 text-white font-bold font-heading">KM 2</td>
                <td class="py-2 text-[#0F969C] font-bold">3:49</td>
                <td class="py-2 text-[#6DA5C0]">168 ppm</td>
                <td class="py-2">180 spm</td>
                <td class="py-2 text-[#6DA5C0] font-sans">Ritmo crucero óptimo</td>
              </tr>
              <tr>
                <td class="py-2 text-white font-bold font-heading">KM 3</td>
                <td class="py-2 text-white">3:55</td>
                <td class="py-2 text-[#6DA5C0]">172 ppm</td>
                <td class="py-2">179 spm</td>
                <td class="py-2 text-[#6DA5C0] font-sans">Primer repecho muralla</td>
              </tr>
              <tr>
                <td class="py-2 text-white font-bold font-heading">KM 4</td>
                <td class="py-2 text-white">3:57</td>
                <td class="py-2 text-[#6DA5C0]">174 ppm</td>
                <td class="py-2">181 spm</td>
                <td class="py-2 text-[#6DA5C0] font-sans">Viento en contra continuo</td>
              </tr>
              <tr>
                <td class="py-2 text-white font-bold font-heading">KM 5</td>
                <td class="py-2 text-[#0F969C] font-bold">3:51</td>
                <td class="py-2 text-[#6DA5C0]">175 ppm</td>
                <td class="py-2">180 spm</td>
                <td class="py-2 text-[#6DA5C0] font-sans">Paso 5K en 19:14</td>
              </tr>
              <tr>
                <td class="py-2 text-white font-bold font-heading">KM 6-9</td>
                <td class="py-2 text-white">3:52 avg</td>
                <td class="py-2 text-[#6DA5C0]">176 ppm</td>
                <td class="py-2">182 spm</td>
                <td class="py-2 text-[#6DA5C0] font-sans">Solidez aeróbica sin claudicación</td>
              </tr>
              <tr>
                <td class="py-2 text-white font-bold font-heading">KM 10</td>
                <td class="py-2 text-[#0F969C] font-extrabold">3:46</td>
                <td class="py-2 text-white font-bold">186 ppm</td>
                <td class="py-2">186 spm</td>
                <td class="py-2 text-[#6DA5C0] font-sans">Sprint final neuromuscular</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- TAB 2: WORKOUTS SCHEDULE (CALENDARIO 14 DÍAS CON ACORDEÓN TÁCTIL) -->
    <div id="tab-content-workouts" class="tab-pane hidden space-y-4">
      <div class="flex items-center justify-between px-1">
        <div>
          <h3 class="text-base font-extrabold text-white flex items-center gap-2 font-heading">
            <i data-lucide="calendar-range" class="w-5 h-5 text-[#0F969C]"></i>
            <span>Microciclo Bi-Semanal (14 Días)</span>
          </h3>
          <p class="text-xs text-[#6DA5C0] mt-0.5 font-sans">Toca cualquier día para desplegar ritmos, series y cargas</p>
        </div>
        <span class="text-[11px] font-heading font-extrabold text-[#0F969C] px-2.5 py-1 rounded-lg bg-[#0F969C]/10 border border-[#0F969C]/30">
          Hoy: \${todayISO}
        </span>
      </div>

      <!-- LISTA DE DÍAS CON ACORDEÓN INTERACTIVO -->
      <div class="space-y-3" id="weekly-days-list">
        \${daysList.map((d: any, index: number) => {
          const isToday = d.date === todayISO || (todayIndex === -1 && index === 0);
          const isDone = d.manual_status === "done" || d.date < todayISO;
          const isKey = d.is_key_session;

          let badgeStyle = "bg-[#294D61]/40 text-[#6DA5C0] border border-[#294D61]";
          let badgeText = "PEND";
          let borderStyle = "border-[#294D61]";

          if (isToday) {
            badgeStyle = "bg-[#0F969C] text-[#05161A] font-extrabold shadow-md shadow-[#0F969C]/30";
            badgeText = "HOY";
            borderStyle = "border-l-4 border-l-[#0F969C] border-[#0C7075] bg-[#072E33]";
          } else if (isDone) {
            badgeStyle = "bg-[#0C7075]/30 text-[#6DA5C0] border border-[#294D61] font-bold";
            badgeText = "OK";
          } else if (isKey) {
            badgeStyle = "bg-[#0C7075] text-white border border-[#0F969C] font-extrabold shadow-md shadow-[#0C7075]/30";
            badgeText = "CLAVE";
            borderStyle = "border-l-4 border-l-[#0F969C] border-[#294D61] bg-[#072E33]";
          }

          const runShort = d.running?.is_rest ? "Descanso carrera" : \`\${d.running?.session_type} (\${d.running?.target_pace})\`;
          const gymShort = d.gym?.is_rest ? "Sin gym" : (d.gym?.routine_name?.split('·')[1]?.trim() || "Gym");

          // Inserción de cabeceras de semana (Semana 1 y Semana 2)
          let weekHeaderHtml = "";
          if (index === 0) {
            weekHeaderHtml = \`
              <div class="flex items-center gap-2 pt-1 pb-1">
                <span class="w-2 h-2 rounded-full bg-[#0F969C]"></span>
                <h4 class="text-xs font-heading font-extrabold uppercase tracking-wider text-[#0F969C]">Semana 1 · Pre-Milán (16 al 22 Nov)</h4>
                <div class="flex-1 h-px bg-[#294D61]"></div>
              </div>
            \`;
          } else if (index === 7) {
            weekHeaderHtml = \`
              <div class="flex items-center gap-2 pt-3 pb-1">
                <span class="w-2 h-2 rounded-full bg-[#0C7075]"></span>
                <h4 class="text-xs font-heading font-extrabold uppercase tracking-wider text-[#6DA5C0]">Semana 2 · Afinamiento & Cross del Soto (23 al 29 Nov)</h4>
                <div class="flex-1 h-px bg-[#294D61]"></div>
              </div>
            \`;
          }

          return \`
            \${weekHeaderHtml}
            <div id="card-day-\${d.date}" class="card-aegis rounded-2xl overflow-hidden transition \${borderStyle}">
              <!-- Cabecera del Día (Clicable) -->
              <button onclick="toggleDayAccordion('\${d.date}')" class="w-full p-4 flex items-center justify-between text-left hover:bg-white/[0.02] transition">
                <div class="flex items-center gap-3">
                  <span class="w-8 h-8 rounded-lg \${badgeStyle} flex items-center justify-center font-heading text-xs shrink-0 font-bold">
                    \${badgeText}
                  </span>
                  <div>
                    <div class="flex items-center gap-2">
                      <h4 class="text-sm font-extrabold text-white font-heading">\${d.day_name} \${d.display_date}</h4>
                      \${isToday ? '<span class="inline-block w-2 h-2 rounded-full bg-[#0F969C] animate-pulse"></span>' : ''}
                      \${isKey ? '<span class="px-2 py-0.5 rounded text-[9px] uppercase font-extrabold bg-[#0F969C]/20 text-[#0F969C] border border-[#0F969C]/30 font-heading">Sesión Clave</span>' : ''}
                    </div>
                    <p class="text-xs text-[#6DA5C0] mt-0.5 font-sans">\${runShort} &bull; <span class="text-[#E6F4F6] font-medium">\${gymShort}</span></p>
                  </div>
                </div>
                <div class="flex items-center gap-2">
                  <i data-lucide="chevron-down" id="chevron-\${d.date}" class="w-5 h-5 text-[#6DA5C0] transition-transform duration-200 \${isToday ? 'rotate-180 text-[#0F969C]' : ''}"></i>
                </div>
              </button>

              <!-- Contenido Desplegable (Expandido si es HOY) -->
              <div id="detail-\${d.date}" class="accordion-body px-4 pb-4 pt-1 space-y-3 \${isToday ? '' : 'hidden'} border-t border-[#294D61]">
                
                <!-- Bloque Running Detallado -->
                <div class="p-3.5 rounded-xl subcard-aegis">
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="text-xs font-bold text-[#0F969C] flex items-center gap-1.5 font-heading">
                      <i data-lucide="footprints" class="w-4 h-4"></i>
                      <span>\${d.running?.title}</span>
                    </span>
                    \${d.running?.duration_min ? \`<span class="text-[11px] font-heading font-extrabold text-white">\${d.running.duration_min} min</span>\` : ''}
                  </div>
                  
                  <p class="text-xs text-[#E6F4F6] leading-relaxed font-sans mb-2.5">
                    \${d.running?.main_work}
                  </p>

                  <div class="grid grid-cols-2 sm:grid-cols-3 gap-2 text-[11px] bg-[#05161A]/70 p-2 rounded-lg border border-[#294D61]">
                    <div>
                      <span class="text-[#6DA5C0] block text-[10px] font-bold uppercase font-heading">Ritmo Objetivo</span>
                      <span class="font-heading font-extrabold text-[#0F969C]">\${d.running?.target_pace}</span>
                    </div>
                    <div>
                      <span class="text-[#6DA5C0] block text-[10px] font-bold uppercase font-heading">Zona Cardíaca</span>
                      <span class="font-heading font-bold text-white">\${d.running?.hr_zone}</span>
                    </div>
                    <div class="col-span-2 sm:col-span-1">
                      <span class="text-[#6DA5C0] block text-[10px] font-bold uppercase font-heading">Zapatilla</span>
                      <span class="font-sans text-[#E6F4F6] truncate block font-medium">\${d.running?.shoes_recommended}</span>
                    </div>
                  </div>
                </div>

                <!-- Bloque Gimnasio Detallado con Botón Deep Link -->
                <div class="p-3.5 rounded-xl subcard-aegis">
                  <div class="flex items-center justify-between mb-1.5">
                    <span class="text-xs font-bold text-[#E6F4F6] flex items-center gap-1.5 font-heading">
                      <i data-lucide="dumbbell" class="w-4 h-4 text-[#0F969C]"></i>
                      <span>\${d.gym?.routine_name}</span>
                    </span>
                    \${d.gym?.routine_id ? \`<span class="text-[10px] font-heading font-extrabold px-2 py-0.5 rounded bg-[#0C7075]/40 text-[#0F969C] border border-[#294D61]">Rutina \${d.gym.routine_id}</span>\` : ''}
                  </div>

                  \${(d.gym?.highlight_exercises && d.gym.highlight_exercises.length > 0) ? \`
                    <div class="space-y-1.5 my-2">
                      \${d.gym.highlight_exercises.map((e: any) => \`
                        <div class="flex items-center justify-between text-xs py-1 px-2 rounded bg-[#05161A]/60 border border-[#294D61]">
                          <span class="text-[#E6F4F6] font-medium">\${e.name}</span>
                          <span class="font-heading font-extrabold text-[#0F969C] text-[11px]">\${e.load}</span>
                        </div>
                      \`).join('')}
                    </div>
                  \` : '<p class="text-xs text-[#6DA5C0] italic my-1 font-sans">Descanso programado de fuerza para asimilación adaptativa.</p>'}

                  \${d.gym?.knee_vmo_protocol ? \`
                    <div class="p-2 rounded-lg bg-[#0C7075]/20 border border-[#0C7075] text-[11px] text-[#E6F4F6] flex items-start gap-1.5 my-2 font-sans">
                      <i data-lucide="shield-check" class="w-3.5 h-3.5 text-[#0F969C] shrink-0 mt-0.5"></i>
                      <span><strong>VMO:</strong> \${d.gym.knee_vmo_protocol}</span>
                    </div>
                  \` : ''}

                  \${d.gym?.routine_id ? \`
                    <div class="mt-3">
                      <button onclick="navigateToGymRoutine(\${d.gym.routine_id})" class="w-full py-2 px-3 rounded-xl bg-[#0C7075] hover:bg-[#0F969C] hover:text-[#05161A] text-white text-xs font-extrabold font-heading flex items-center justify-center gap-2 transition shadow-md shadow-[#0C7075]/20 border border-[#294D61]">
                        <i data-lucide="eye" class="w-4 h-4"></i>
                        <span>Ver Rutina \${d.gym.routine_id} con Fotos y Registro</span>
                      </button>
                    </div>
                  \` : ''}
                </div>

              </div>
            </div>
          \`;
        }).join('')}
      </div>
    </div>

    <!-- TAB 3: GYM & STRENGTH INTERACTIVE REPOSITORY -->
    <div id="tab-content-gym" class="tab-pane hidden space-y-4">
      <!-- Selector de Rutinas del PDF Oficial -->
      <div class="card-aegis rounded-2xl p-4 sm:p-5">
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
          <div>
            <span class="px-2.5 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-[#0F969C]/15 text-[#0F969C] border border-[#0F969C]/30 font-heading">
              Rutinas Oficiales Visuales
            </span>
            <h3 class="text-base font-extrabold text-white mt-1 font-heading">Selecciona tu Sesión de Gimnasio</h3>
            <p class="text-xs text-[#6DA5C0]">Cargas exactas, imágenes de ejecución técnica y campos de auto-guardado</p>
          </div>
          <div class="flex items-center gap-1.5 text-xs text-[#6DA5C0] font-medium">
            <i data-lucide="info" class="w-3.5 h-3.5 text-[#0F969C]"></i>
            <span>Progresión: RIR 1-2 &bull; +2.5 kg al completar</span>
          </div>
        </div>

        <!-- Chips de selección rápida -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 mb-2">
          <button onclick="selectGymRoutine(1)" id="gym-chip-1" class="gym-routine-btn py-2.5 px-3 rounded-xl text-left border transition flex flex-col justify-between bg-[#05161A] border-[#294D61] text-[#6DA5C0]">
            <span class="text-[10px] uppercase font-bold text-[#6DA5C0] font-heading">Rutina 1 &bull; Lunes</span>
            <span class="text-xs font-bold text-white mt-1 font-heading">Pierna 1</span>
            <span class="text-[10px] text-[#6DA5C0]">Cuádriceps & Rodilla</span>
          </button>

          <button onclick="selectGymRoutine(2)" id="gym-chip-2" class="gym-routine-btn py-2.5 px-3 rounded-xl text-left border transition flex flex-col justify-between bg-[#05161A] border-[#294D61] text-[#6DA5C0]">
            <span class="text-[10px] uppercase font-bold text-[#6DA5C0] font-heading">Rutina 2 &bull; Miércoles</span>
            <span class="text-xs font-bold text-white mt-1 font-heading">Torso Tracción</span>
            <span class="text-[10px] text-[#6DA5C0]">Espalda & Bíceps</span>
          </button>

          <button onclick="selectGymRoutine(3)" id="gym-chip-3" class="gym-routine-btn py-2.5 px-3 rounded-xl text-left border transition flex flex-col justify-between bg-[#0F969C] text-[#05161A] border-[#0F969C] font-semibold shadow-lg shadow-[#0F969C]/20">
            <span class="text-[10px] uppercase font-extrabold text-[#05161A]/80 font-heading">Rutina 3 &bull; Jueves/Viernes</span>
            <span class="text-xs font-extrabold text-[#05161A] mt-1 font-heading">Pierna 2 (Hoy)</span>
            <span class="text-[10px] text-[#05161A]/80">Hip Thrust & Isquios</span>
          </button>

          <button onclick="selectGymRoutine(4)" id="gym-chip-4" class="gym-routine-btn py-2.5 px-3 rounded-xl text-left border transition flex flex-col justify-between bg-[#05161A] border-[#294D61] text-[#6DA5C0]">
            <span class="text-[10px] uppercase font-bold text-[#6DA5C0] font-heading">Rutina 4 &bull; Sábado</span>
            <span class="text-xs font-bold text-white mt-1 font-heading">Torso Empuje</span>
            <span class="text-[10px] text-[#6DA5C0]">Pectoral & Deltoides</span>
          </button>
        </div>
      </div>

      <!-- Protocolo Especial VMO / Rodilla -->
      <div class="card-aegis rounded-2xl p-4 border border-[#0F969C]/40 bg-[#072E33]">
        <div class="flex items-start gap-3">
          <div class="p-2 rounded-xl bg-[#0F969C]/20 text-[#0F969C] mt-0.5 border border-[#0F969C]/30">
            <i data-lucide="shield-alert" class="w-5 h-5"></i>
          </div>
          <div class="flex-1">
            <div class="flex items-center justify-between">
              <h4 class="text-xs font-extrabold uppercase tracking-wider text-[#0F969C] font-heading">Blindaje VMO & Rodilla Izquierda (Activo)</h4>
              <span class="text-[10px] font-heading font-bold text-[#0F969C] px-2 py-0.5 rounded bg-[#05161A] border border-[#294D61]">0/10 Dolor</span>
            </div>
            <p class="text-xs text-[#E6F4F6] mt-1 leading-relaxed font-sans">
              <strong>Spanish Squat Isométrica con Banda:</strong> 4 series &times; 35-40s de retención. Ancla una banda de resistencia pesada tras el hueco poplíteo de ambas rodillas y mantén la flexión a 70°-80°. Reclutamiento máximo del vasto medial sin compresión patelofemoral.
            </p>
          </div>
        </div>
      </div>

      <!-- Contenedor Dinámico de Ejercicios -->
      <div id="gym-exercises-container" class="space-y-4"></div>
    </div>

    <!-- TAB 4: CRITICAL COACH -->
    <div id="tab-content-coach" class="tab-pane hidden space-y-4">
      <div class="card-aegis rounded-2xl p-4 sm:p-5 border-l-4 border-l-[#0F969C]">
        <div class="flex items-center gap-2 mb-2">
          <i data-lucide="alert-triangle" class="w-5 h-5 text-[#0F969C]"></i>
          <h3 class="text-sm font-extrabold text-white font-heading">Auditoría Fisiológica Crítica: Objetivo Cross del Soto (28 Nov)</h3>
        </div>
        <div class="text-xs text-[#E6F4F6] space-y-2.5 leading-relaxed font-sans">
          <p>
            <strong>Evaluación de Ritmo (3:30/km en Cross):</strong> Tu 10K en Ávila (38:26 @ 3:50/km a 1.070m con cuestas y viento) equivale en asfalto llano a nivel del mar a un tiempo estimado de <strong>~18:00 en 5K (3:36/km)</strong>.
          </p>
          <p>
            <strong>Penalización por Superficie:</strong> La hierba y la tierra deformable absorben retorno elástico, sumando entre <strong>8 y 12 segundos extra por kilómetro</strong> frente a asfalto. Por tanto, 3:30/km en cross equivale a correr a <strong>3:18-3:22/km en asfalto llano</strong> (sub-16:50 en 5K).
          </p>
          <div class="p-3 rounded-xl subcard-aegis border border-[#294D61] text-[#E6F4F6]">
            <strong class="text-[#0F969C] block mb-0.5">Estrategia Táctica Ganadora:</strong> Salir los primeros 3 km a <strong>3:34 - 3:36/km</strong>. En los últimos 1.500m, desata tu pasado neuromuscular de 800m (1:54) para abrir zancada en progresión terminal.
          </div>
        </div>
      </div>

      <div class="card-aegis rounded-2xl p-4 sm:p-5">
        <h3 class="text-sm font-extrabold text-white flex items-center gap-2 mb-2 font-heading">
          <i data-lucide="cpu" class="w-4 h-4 text-[#0F969C]"></i>
          <span>Requerimientos de Hardware & Material</span>
        </h3>
        <ul class="text-xs text-[#E6F4F6] space-y-2 leading-relaxed font-sans">
          <li class="flex items-start gap-2">
            <i data-lucide="check" class="w-4 h-4 text-[#0F969C] mt-0.5 shrink-0"></i>
            <span><strong>Banda Pectoral (Polar H10 / Garmin HRM-Pro):</strong> Imprescindible para las series de micro-intervalos para eliminar el retardo óptico y el bloqueo por cadencia.</span>
          </li>
          <li class="flex items-start gap-2">
            <i data-lucide="check" class="w-4 h-4 text-[#0F969C] mt-0.5 shrink-0"></i>
            <span><strong>Clavos en el Soto:</strong> 6 mm si la hierba está seca; sustituir por clavos de 9 mm si llueve previamente.</span>
          </li>
        </ul>
      </div>
    </div>

  </main>

  <!-- JAVASCRIPT: DATA & INTERACTIVITY (CLEAN & TESTED) -->
  <script>
    // Fallback limpio y seguro para imágenes de ejercicios
    function handleImgError(img) {
      img.onerror = null;
      img.src = 'data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="400" height="200" viewBox="0 0 400 200"><rect width="400" height="200" fill="%23072E33"/><text x="50%" y="50%" fill="%236DA5C0" font-family="sans-serif" font-size="14" text-anchor="middle" dominant-baseline="middle">Ejercicio Visual</text></svg>';
    }

    const gymRoutinesData = {
      1: {
        title: "Rutina 1 · Pierna 1 (Dominancia Rodilla & Cuádriceps)",
        day: "Lunes 18:00 &bull; 45-50 min &bull; RIR 1-2",
        exercises: [
          {
            num: 1,
            name: "Sentadilla con Barra",
            sub: "Back Squat en Jaula (Sustituir por Box Squat en fase VMO)",
            img: "/img/ex_1_1.jpg",
            muscle: "Cuádriceps & Glúteos",
            series: "4 series &times; 4-6 reps",
            weight: "65 - 70 kg (Box Squat)",
            rest: "3.0 min",
            rir: "RIR 1-2",
            tempo: "3-1-X-0",
            cue: "Rompe el paralelo al cajón. Empuja con todo el pie sin meter las rodillas hacia dentro."
          },
          {
            num: 2,
            name: "Prensa de Piernas 45°",
            sub: "Incline Leg Press",
            img: "/img/ex_1_2.jpg",
            muscle: "Cuádriceps & Aductores",
            series: "3 series &times; 6-8 reps",
            weight: "+40 kg / lado",
            rest: "2.5 min",
            rir: "RIR 1",
            tempo: "3-0-1-0",
            cue: "Pies a la anchura de las caderas. Cero despegue lumbar del respaldo en todo el recorrido."
          },
          {
            num: 3,
            name: "Curl Femoral Tumbado",
            sub: "Lying Leg Curl",
            img: "/img/ex_1_3.jpg",
            muscle: "Isquiotibiales (Cabeza corta & larga)",
            series: "3 series &times; 6-8 reps",
            weight: "42 kg",
            rest: "2.0 min",
            rir: "RIR 1",
            tempo: "3-1-1-0",
            cue: "Frena la bajada de forma excéntrica para estimular sarcómeros en serie del isquiotibial."
          },
          {
            num: 4,
            name: "Extensión de Cuádriceps",
            sub: "Leg Extension en Máquina",
            img: "/img/ex_1_4.jpg",
            muscle: "Recto Femoral & Vasto Medial",
            series: "3 series &times; 8-10 reps",
            weight: "66 kg",
            rest: "90 seg",
            rir: "RIR 1",
            tempo: "2-0-1-1",
            cue: "Aislamiento puro del recto femoral sin fatiga en la columna lumbar."
          },
          {
            num: 5,
            name: "Gemelos de Pie con Barra",
            sub: "Standing Calf Raise",
            img: "/img/ex_1_5.jpg",
            muscle: "Gastrocnemio (Gemelos)",
            series: "4 series &times; 6-8 reps",
            weight: "85 kg",
            rest: "90 seg",
            rir: "RIR 1",
            tempo: "3-2-X-0",
            cue: "La pausa de 2s abajo anula el rebote del tendón y carga la masa muscular del gastrocnemio."
          },
          {
            num: 6,
            name: "Rueda Abdominal (Core)",
            sub: "Ab Wheel Rollout",
            img: "/img/ex_1_6.jpg",
            muscle: "Core & Anti-extensión Lumbar",
            series: "3 series &times; 8-10 reps",
            weight: "Autocarga estricta",
            rest: "60 seg",
            rir: "RIR 0",
            tempo: "2-1-2-0",
            cue: "Retroversión pélvica activa: bloquea la pelvis neutra y evita arquear la espalda baja."
          }
        ]
      },
      2: {
        title: "Rutina 2 · Torso Tracción (Dorsal, Espalda Alta & Bíceps)",
        day: "Miércoles 17:30 &bull; 50 min &bull; RIR 1",
        exercises: [
          {
            num: 1,
            name: "Jalón Agarre Cerrado V",
            sub: "Close-Grip Lat Pulldown",
            img: "/img/ex_2_1.jpg",
            muscle: "Dorsal Ancho & Redondo Mayor",
            series: "4 series &times; 4-6 reps",
            weight: "54 - 59 kg",
            rest: "2.5 min",
            rir: "RIR 1",
            tempo: "3-0-X-1",
            cue: "Codos pegados viajando directamente a las costillas. Máxima carga de tracción vertical."
          },
          {
            num: 2,
            name: "Remo Dorian Unilateral",
            sub: "One-Arm Row Máquina / Mancuerna",
            img: "/img/ex_2_2.jpg",
            muscle: "Dorsal Ancho & Trapecio Medio",
            series: "3 series &times; 6-8 reps",
            weight: "28 - 30 kg / mano",
            rest: "2.0 min",
            rir: "RIR 1",
            tempo: "2-0-1-1",
            cue: "Pecho firme. Conduce el codo directamente hacia el bolsillo trasero sin rotar el tronco."
          },
          {
            num: 3,
            name: "Remo Gironda Amplio",
            sub: "Seated Cable Row Wide Grip",
            img: "/img/ex_2_3.jpg",
            muscle: "Espalda Alta, Romboides & Trapecio",
            series: "3 series &times; 8-10 reps",
            weight: "36 kg",
            rest: "90 seg",
            rir: "RIR 1",
            tempo: "2-0-1-2",
            cue: "Codos a 45°-60°. Junta escápulas firmemente para consolidar el soporte postural de carrera."
          },
          {
            num: 4,
            name: "Face Pull en Polea Alta",
            sub: "Rope Face Pull a la Frente",
            img: "/img/ex_2_4.jpg",
            muscle: "Deltoides Posterior & Manguito Rotador",
            series: "3 series &times; 10-12 reps",
            weight: "23 - 27 kg",
            rest: "75 seg",
            rir: "RIR 2",
            tempo: "2-0-1-1",
            cue: "Manos a la altura de los ojos separando la cuerda al máximo. Salud del manguito."
          },
          {
            num: 5,
            name: "Curl Inclinado 45° Mancuernas",
            sub: "Incline Dumbbell Bicep Curl",
            img: "/img/ex_2_5.jpg",
            muscle: "Cabeza Larga del Bíceps",
            series: "3 series &times; 6-8 reps",
            weight: "12 kg / mano",
            rest: "90 seg",
            rir: "RIR 1",
            tempo: "3-0-1-0",
            cue: "Brazos cuelgan atrás del cuerpo para máxima tensión de estiramiento en la cabeza larga."
          },
          {
            num: 6,
            name: "Bíceps en Máquina / Banco Scott",
            sub: "Machine Preacher Curl",
            img: "/img/ex_2_6.jpg",
            muscle: "Braquial Anterior & Bíceps",
            series: "2 series &times; 8-10 reps",
            weight: "Medio-Alto",
            rest: "75 seg",
            rir: "RIR 0-1",
            tempo: "2-0-1-1",
            cue: "Codos fijos y apoyados. Contracción pico de 1 segundo arriba para densidad de flexores."
          }
        ]
      },
      3: {
        title: "Rutina 3 · Pierna 2 (Cadena Posterior & Blindaje Isquios)",
        day: "Jueves/Viernes 17:30 &bull; 50 min &bull; RIR 1",
        exercises: [
          {
            num: 1,
            name: "Hip Thrust con Barra",
            sub: "Barbell Hip Thrust en Banco",
            img: "/img/ex_3_1.jpg",
            muscle: "Glúteo Mayor (Blindaje de Carrera)",
            series: "4 series &times; 4-6 reps",
            weight: "130 - 140 kg",
            rest: "3.0 min",
            rir: "RIR 1",
            tempo: "2-1-X-1",
            cue: "Empuje directo con los talones. Extensión total de cadera apretando glúteos arriba 1s."
          },
          {
            num: 2,
            name: "Peso Muerto Rumano Unilateral / Staggered",
            sub: "Single-Leg / Staggered RDL con Mancuerna",
            img: "/img/ex_3_2.jpg",
            muscle: "Isquiotibial Proximal & Cadena Posterior",
            series: "3 series &times; 6-8 reps",
            weight: "20 - 24 kg / mano",
            rest: "2.0 min",
            rir: "RIR 1-2",
            tempo: "3-1-1-0",
            cue: "Bisagra de cadera pura con espalda neutra y máxima tensión excéntrica en isquiotibial."
          },
          {
            num: 3,
            name: "Prensa Pies Altos y Anchos",
            sub: "High Foot Stance Leg Press",
            img: "/img/ex_3_3.jpg",
            muscle: "Glúteos & Aductores",
            series: "3 series &times; 6-8 reps",
            weight: "+40 - 45 kg / lado",
            rest: "2.0 min",
            rir: "RIR 1",
            tempo: "3-0-1-0",
            cue: "Pies situados arriba en la plancha para enfatizar glúteo y descargar tensión en rótula."
          },
          {
            num: 4,
            name: "Curl Femoral Controlado (HSR)",
            sub: "Lying Leg Curl Tempo Estricto",
            img: "/img/ex_3_4.jpg",
            muscle: "Isquiotibiales (Resistencia a Lesión)",
            series: "3 series &times; 6-8 reps",
            weight: "42 kg",
            rest: "90 seg",
            rir: "RIR 1",
            tempo: "3-1-1-0",
            cue: "Cero inercia o balanceo de cadera. Carga excéntrica pura sin cizallamiento articular."
          },
          {
            num: 5,
            name: "Sóleo Sentado en Máquina",
            sub: "Seated Calf Raise",
            img: "/img/ex_3_5.jpg",
            muscle: "Sóleo (Absorción de Impacto en Running)",
            series: "3 series &times; 8-10 reps",
            weight: "35 - 40 kg",
            rest: "90 seg",
            rir: "RIR 1",
            tempo: "3-2-1-0",
            cue: "Rodilla a 90° aísla el sóleo, que absorbe entre 6 y 8 veces el peso corporal en cada zancada."
          },
          {
            num: 6,
            name: "Pallof Press + Paseo de Granjero",
            sub: "Anti-rotación Lumbar & Estabilidad Pélvica",
            img: "/img/ex_3_6.jpg",
            muscle: "Core Profundo & Oblicuos",
            series: "3 series &times; 10 reps + 30m",
            weight: "Medio-Pesado",
            rest: "60 seg",
            rir: "RIR 0",
            tempo: "Isométrico",
            cue: "Anti-rotación pura: elimina el balanceo lateral de la pelvis durante la zancada de carrera."
          }
        ]
      },
      4: {
        title: "Rutina 4 · Torso Empuje (Pectoral, Hombro & Tríceps)",
        day: "Sábado Mañana &bull; 50 min &bull; RIR 1-2",
        exercises: [
          {
            num: 1,
            name: "Press de Banca Plano con Barra",
            sub: "Barbell Bench Press",
            img: "/img/ex_4_1.jpg",
            muscle: "Pectoral Mayor & Tríceps",
            series: "4 series &times; 4-6 reps",
            weight: "Pesado progresivo",
            rest: "2.5 min",
            rir: "RIR 1-2",
            tempo: "3-1-X-0",
            cue: "Retracción escapular firme. La barra toca el esternón sin rebotar y subida explosiva."
          },
          {
            num: 2,
            name: "Press Inclinado con Mancuernas (30°)",
            sub: "Incline 30° Dumbbell Press",
            img: "/img/ex_4_2.jpg",
            muscle: "Pectoral Clavicular & Deltoides Anterior",
            series: "3 series &times; 6-8 reps",
            weight: "Pesado",
            rest: "2.0 min",
            rir: "RIR 1",
            tempo: "3-0-1-0",
            cue: "Banco a 30° para enfatizar la porción superior del pecho y deltoides anterior."
          },
          {
            num: 3,
            name: "Pec Deck / Aperturas en Máquina",
            sub: "Machine Butterfly",
            img: "/img/ex_4_3.jpg",
            muscle: "Pectoral Mayor (Aislamiento)",
            series: "3 series &times; 8-10 reps",
            weight: "Medio",
            rest: "90 seg",
            rir: "RIR 1",
            tempo: "2-0-1-1",
            cue: "Junta los codos al frente y aprieta el pectoral 1 segundo en máxima contracción concéntrica."
          },
          {
            num: 4,
            name: "Elevaciones Laterales",
            sub: "Side Lateral Raise con Mancuerna / Polea",
            img: "/img/ex_4_4.jpg",
            muscle: "Deltoides Lateral (Amplitud)",
            series: "4 series &times; 8-10 reps",
            weight: "Pesado estricto",
            rest: "75 seg",
            rir: "RIR 1",
            tempo: "2-0-1-1",
            cue: "Codos ligeramente flexionados. Clave para la amplitud y soporte de hombro."
          },
          {
            num: 5,
            name: "Press Francés con Barra Z",
            sub: "Lying Triceps Press en Banco",
            img: "/img/ex_4_5.jpg",
            muscle: "Cabeza Larga del Tríceps",
            series: "3 series &times; 6-8 reps",
            weight: "Medio-Pesado",
            rest: "90 seg",
            rir: "RIR 1",
            tempo: "3-0-1-0",
            cue: "Codos fijos apuntando al techo. Estímulo directo a la cabeza larga del tríceps."
          },
          {
            num: 6,
            name: "Tríceps Polea con Cuerda",
            sub: "Triceps Pushdown con Cuerda",
            img: "/img/ex_4_6.jpg",
            muscle: "Cabezas Lateral & Medial del Tríceps",
            series: "3 series &times; 8-10 reps",
            weight: "Medio-Alto",
            rest: "75 seg",
            rir: "RIR 0-1",
            tempo: "2-0-1-1",
            cue: "Abre la cuerda al final del recorrido para acortar las cabezas lateral y medial."
          }
        ]
      }
    };

    // Alternar acordeón de días
    function toggleDayAccordion(targetDate) {
      const targetDetail = document.getElementById('detail-' + targetDate);
      const targetChevron = document.getElementById('chevron-' + targetDate);
      if (!targetDetail) return;

      const isCurrentlyOpen = !targetDetail.classList.contains('hidden');

      // Colapsar todos los acordeones
      document.querySelectorAll('.accordion-body').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('[id^="chevron-"]').forEach(el => {
        el.classList.remove('rotate-180', 'text-[#0F969C]');
        el.classList.add('text-[#6DA5C0]');
      });

      // Si estaba cerrado, abrirlo
      if (!isCurrentlyOpen) {
        targetDetail.classList.remove('hidden');
        if (targetChevron) {
          targetChevron.classList.add('rotate-180', 'text-[#0F969C]');
          targetChevron.classList.remove('text-[#6DA5C0]');
        }
        document.getElementById('card-day-' + targetDate)?.scrollIntoView({
          behavior: 'smooth',
          block: 'nearest'
        });
      }
    }

    // Salto directo desde la semana a la rutina de gimnasio
    function navigateToGymRoutine(routineId) {
      switchTab('gym');
      selectGymRoutine(routineId);
      window.scrollTo({ top: 380, behavior: 'smooth' });
    }

    // Renderizar ejercicios de la rutina seleccionada
    function selectGymRoutine(routineId) {
      for (let i = 1; i <= 4; i++) {
        const btn = document.getElementById('gym-chip-' + i);
        if (!btn) continue;
        if (i === routineId) {
          btn.className = "gym-routine-btn py-2.5 px-3 rounded-xl text-left border transition flex flex-col justify-between bg-[#0F969C] text-[#05161A] border-[#0F969C] font-semibold shadow-lg shadow-[#0F969C]/20";
          btn.querySelectorAll('span')[0].className = "text-[10px] uppercase font-extrabold text-[#05161A]/80 font-heading";
          btn.querySelectorAll('span')[1].className = "text-xs font-extrabold text-[#05161A] mt-1 font-heading";
          btn.querySelectorAll('span')[2].className = "text-[10px] text-[#05161A]/80";
        } else {
          btn.className = "gym-routine-btn py-2.5 px-3 rounded-xl text-left border transition flex flex-col justify-between bg-[#05161A] border-[#294D61] text-[#6DA5C0]";
          btn.querySelectorAll('span')[0].className = "text-[10px] uppercase font-bold text-[#6DA5C0] font-heading";
          btn.querySelectorAll('span')[1].className = "text-xs font-bold text-white mt-1 font-heading";
          btn.querySelectorAll('span')[2].className = "text-[10px] text-[#6DA5C0]";
        }
      }

      const routine = gymRoutinesData[routineId];
      if (!routine) return;

      const container = document.getElementById('gym-exercises-container');
      let html = '<div class="card-aegis rounded-2xl p-4 sm:p-5 mb-2 flex items-center justify-between border-b border-[#294D61]">' +
        '<div>' +
          '<h3 class="text-base font-extrabold text-white font-heading">' + routine.title + '</h3>' +
          '<p class="text-xs text-[#0F969C] font-medium mt-0.5">' + routine.day + '</p>' +
        '</div>' +
        '<span class="text-xs font-heading font-extrabold px-2.5 py-1 rounded-lg bg-[#05161A] text-[#6DA5C0] border border-[#294D61]">' +
          routine.exercises.length + ' Ejercicios' +
        '</span>' +
      '</div>';

      routine.exercises.forEach(function(ex) {
        html += '<div class="card-aegis rounded-2xl overflow-hidden">' +
          '<div class="relative bg-[#05161A] border-b border-[#294D61]">' +
            '<img src="' + ex.img + '" alt="' + ex.name + '" class="w-full h-48 sm:h-56 object-contain bg-[#05161A] p-2" loading="lazy" onerror="handleImgError(this)">' +
            '<div class="absolute top-2.5 left-2.5 flex items-center gap-1.5">' +
              '<span class="w-6 h-6 rounded-lg bg-[#0F969C] text-[#05161A] font-extrabold font-heading text-xs flex items-center justify-center shadow-md">' + ex.num + '</span>' +
              '<span class="px-2 py-0.5 rounded text-[10px] font-extrabold uppercase tracking-wider bg-[#05161A]/85 backdrop-blur-md text-[#0F969C] border border-[#294D61] font-heading">' + ex.muscle + '</span>' +
            '</div>' +
          '</div>' +
          '<div class="p-4">' +
            '<div class="flex items-start justify-between gap-2">' +
              '<div>' +
                '<h4 class="text-base font-extrabold text-white leading-snug font-heading">' + ex.name + '</h4>' +
                '<p class="text-xs text-[#6DA5C0] font-sans">' + ex.sub + '</p>' +
              '</div>' +
            '</div>' +
            '<div class="grid grid-cols-2 sm:grid-cols-4 gap-2 my-3 text-center">' +
              '<div class="subcard-aegis p-2 rounded-xl">' +
                '<div class="text-[10px] text-[#6DA5C0] uppercase font-bold font-heading">Series & Reps</div>' +
                '<div class="text-xs font-extrabold text-white mt-0.5 font-heading">' + ex.series + '</div>' +
              '</div>' +
              '<div class="subcard-aegis p-2 rounded-xl">' +
                '<div class="text-[10px] text-[#6DA5C0] uppercase font-bold font-heading">Carga Objetivo</div>' +
                '<div class="text-xs font-extrabold text-[#0F969C] mt-0.5 font-heading">' + ex.weight + '</div>' +
              '</div>' +
              '<div class="subcard-aegis p-2 rounded-xl">' +
                '<div class="text-[10px] text-[#6DA5C0] uppercase font-bold font-heading">Descanso</div>' +
                '<div class="text-xs font-extrabold text-[#6DA5C0] mt-0.5 font-heading">' + ex.rest + '</div>' +
              '</div>' +
              '<div class="subcard-aegis p-2 rounded-xl">' +
                '<div class="text-[10px] text-[#6DA5C0] uppercase font-bold font-heading">Esfuerzo</div>' +
                '<div class="text-xs font-extrabold text-[#0C7075] mt-0.5 font-heading">' + ex.rir + '</div>' +
              '</div>' +
            '</div>' +
            '<div class="text-xs text-[#E6F4F6] subcard-aegis p-2.5 rounded-xl flex items-start gap-2 font-sans">' +
              '<span class="text-[#0F969C] font-extrabold shrink-0 font-heading">Clave técnica:</span>' +
              '<span class="leading-relaxed">' + ex.cue + '</span>' +
            '</div>' +
            '<div class="mt-3 p-3 rounded-xl bg-[#05161A]/80 border border-[#294D61] space-y-2">' +
              '<div class="flex items-center justify-between text-[11px] font-bold text-[#E6F4F6] font-heading">' +
                '<span class="flex items-center gap-1.5"><i data-lucide="edit-3" class="w-3.5 h-3.5 text-[#0F969C]"></i> Tu Registro Real de Hoy</span>' +
                '<span class="text-[10px] text-[#6DA5C0] font-sans font-normal">Auto-guardado local</span>' +
              '</div>' +
              '<div class="grid grid-cols-2 gap-2">' +
                '<div>' +
                  '<label class="text-[10px] uppercase tracking-wider text-[#6DA5C0] font-bold block mb-1 font-heading">Carga Usada</label>' +
                  '<input type="text" id="log-weight-' + routineId + '-' + ex.num + '" placeholder="' + ex.weight + '" class="w-full bg-[#072E33] border border-[#294D61] rounded-lg px-2.5 py-1.5 text-xs text-[#0F969C] font-heading font-bold focus:border-[#0F969C] focus:outline-none" oninput="saveGymLog(' + routineId + ')">' +
                '</div>' +
                '<div>' +
                  '<label class="text-[10px] uppercase tracking-wider text-[#6DA5C0] font-bold block mb-1 font-heading">Series x Reps</label>' +
                  '<input type="text" id="log-reps-' + routineId + '-' + ex.num + '" placeholder="' + ex.series + '" class="w-full bg-[#072E33] border border-[#294D61] rounded-lg px-2.5 py-1.5 text-xs text-white font-heading font-bold focus:border-[#0F969C] focus:outline-none" oninput="saveGymLog(' + routineId + ')">' +
                '</div>' +
              '</div>' +
              '<div>' +
                '<label class="text-[10px] uppercase tracking-wider text-[#6DA5C0] font-bold block mb-1 font-heading">Notas / RIR / Sensaciones</label>' +
                '<input type="text" id="log-notes-' + routineId + '-' + ex.num + '" placeholder="Ej: RIR 1, rodilla perfecta, subí peso..." class="w-full bg-[#072E33] border border-[#294D61] rounded-lg px-2.5 py-1.5 text-xs text-[#E6F4F6] font-sans focus:border-[#0F969C] focus:outline-none" oninput="saveGymLog(' + routineId + ')">' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>';
      });

      html += '<div class="card-aegis rounded-2xl p-4 mt-4 space-y-3 border border-[#0F969C]/40 bg-[#072E33]">' +
        '<div class="flex items-center justify-between">' +
          '<div class="flex items-center gap-2">' +
            '<i data-lucide="clipboard-check" class="w-5 h-5 text-[#0F969C]"></i>' +
            '<h4 class="text-sm font-extrabold text-white font-heading">Resumen de la Sesión</h4>' +
          '</div>' +
          '<span id="save-status-indicator" class="text-[10px] text-[#0F969C] font-bold font-heading">✓ Guardado en tu móvil</span>' +
        '</div>' +
        '<p class="text-xs text-[#E6F4F6] leading-relaxed font-sans">Toca para copiar todos los pesos y notas anotadas hoy en formato limpio listo para pegar en Telegram o enviar al entrenador:</p>' +
        '<button onclick="copyGymSessionToClipboard(' + routineId + ')" class="w-full py-2.5 px-4 rounded-xl bg-gradient-to-r from-[#0C7075] to-[#0F969C] hover:from-[#0F969C] hover:to-[#0C7075] text-[#05161A] font-extrabold text-xs shadow-lg shadow-[#0F969C]/25 flex items-center justify-center gap-2 transition active:scale-95 font-heading">' +
          '<i data-lucide="copy" class="w-4 h-4"></i>' +
          '<span id="copy-btn-text">📋 Copiar Registro de Hoy al Portapapeles</span>' +
        '</button>' +
      '</div>';

      container.innerHTML = html;
      loadGymLog(routineId);
      lucide.createIcons();
    }

    // Funciones de Registro Interactivo de Gimnasio
    function saveGymLog(routineId) {
      const routine = gymRoutinesData[routineId];
      if (!routine) return;
      const logData = {
        updatedAt: new Date().toISOString(),
        exercises: {}
      };
      routine.exercises.forEach(function(ex) {
        const wEl = document.getElementById('log-weight-' + routineId + '-' + ex.num);
        const rEl = document.getElementById('log-reps-' + routineId + '-' + ex.num);
        const nEl = document.getElementById('log-notes-' + routineId + '-' + ex.num);
        logData.exercises[ex.num] = {
          name: ex.name,
          weight: wEl ? wEl.value : '',
          reps: rEl ? rEl.value : '',
          notes: nEl ? nEl.value : ''
        };
      });
      try {
        localStorage.setItem('aegis_gym_log_' + routineId, JSON.stringify(logData));
        const ind = document.getElementById('save-status-indicator');
        if (ind) {
          ind.textContent = '✓ Guardado ' + new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }
      } catch(e) {}
    }

    function loadGymLog(routineId) {
      const routine = gymRoutinesData[routineId];
      if (!routine) return;
      try {
        const raw = localStorage.getItem('aegis_gym_log_' + routineId);
        if (!raw) return;
        const logData = JSON.parse(raw);
        if (!logData || !logData.exercises) return;
        routine.exercises.forEach(function(ex) {
          const data = logData.exercises[ex.num];
          if (!data) return;
          const wEl = document.getElementById('log-weight-' + routineId + '-' + ex.num);
          const rEl = document.getElementById('log-reps-' + routineId + '-' + ex.num);
          const nEl = document.getElementById('log-notes-' + routineId + '-' + ex.num);
          if (wEl && data.weight) wEl.value = data.weight;
          if (rEl && data.reps) rEl.value = data.reps;
          if (nEl && data.notes) nEl.value = data.notes;
        });
        const ind = document.getElementById('save-status-indicator');
        if (ind && logData.updatedAt) {
          ind.textContent = '✓ Último registro cargado';
        }
      } catch(e) {}
    }

    function copyGymSessionToClipboard(routineId) {
      const routine = gymRoutinesData[routineId];
      if (!routine) return;
      saveGymLog(routineId);
      const now = new Date();
      const dateStr = now.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
      const lines = [
        '🏋️ REGISTRO DE GIMNASIO — ' + routine.title + ' (' + dateStr + ')',
        'Atleta: Carlos Jiménez Andrino',
        ''
      ];
      
      routine.exercises.forEach(function(ex) {
        const wEl = document.getElementById('log-weight-' + routineId + '-' + ex.num);
        const rEl = document.getElementById('log-reps-' + routineId + '-' + ex.num);
        const nEl = document.getElementById('log-notes-' + routineId + '-' + ex.num);
        const w = wEl ? wEl.value.trim() : '';
        const r = rEl ? rEl.value.trim() : '';
        const n = nEl ? nEl.value.trim() : '';
        
        if (w || r || n) {
          lines.push('• ' + ex.name + ': ' + (r || ex.series) + ' @ ' + (w || ex.weight) + (n ? ' [' + n + ']' : ''));
        } else {
          lines.push('• ' + ex.name + ': ' + ex.series + ' @ ' + ex.weight);
        }
      });

      lines.push('');
      lines.push('📱 Registrado vía Aegis Coach PWA');
      const txt = lines.join(String.fromCharCode(10));

      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(txt).then(function() {
          const btnText = document.getElementById('copy-btn-text');
          if (btnText) {
            const orig = btnText.textContent;
            btnText.textContent = '✅ ¡Copiado con Éxito al Portapapeles!';
            setTimeout(function() { btnText.textContent = orig; }, 3000);
          }
        }).catch(function() {
          prompt('Copia tu registro:', txt);
        });
      } else {
        prompt('Copia tu registro:', txt);
      }
    }

    // Switch de Pestañas
    function switchTab(tabId) {
      document.querySelectorAll('.tab-pane').forEach(el => el.classList.add('hidden'));
      document.querySelectorAll('.tab-trigger').forEach(el => {
        el.classList.remove('tab-active');
        el.classList.add('tab-inactive');
      });

      const targetContent = document.getElementById('tab-content-' + tabId);
      const targetBtn = document.getElementById('tab-btn-' + tabId);
      if (targetContent) targetContent.classList.remove('hidden');
      if (targetBtn) {
        targetBtn.classList.remove('tab-inactive');
        targetBtn.classList.add('tab-active');
      }

      if (tabId === 'gym') {
        selectGymRoutine(3);
      }
    }

    // Inicializar Gráficos (Chart.js)
    document.addEventListener("DOMContentLoaded", function() {
      lucide.createIcons();
      selectGymRoutine(3);

      const ctxStacked = document.getElementById('stackedVolumeChart')?.getContext('2d');
      if (ctxStacked) {
        new Chart(ctxStacked, {
          type: 'bar',
          data: {
            labels: ['S1 (20S)', 'S2 (27S)', 'S3 (4O)', 'S4 (11O)', 'S5 (18O)', 'S6 (25O)', 'S7 (1N)', 'S8 (8N)'],
            datasets: [
              {
                label: 'Carrera',
                data: [180, 210, 240, 260, 210, 270, 190, 245],
                backgroundColor: '#0F969C',
                borderRadius: 4
              },
              {
                label: 'Fuerza',
                data: [120, 140, 150, 150, 130, 160, 110, 140],
                backgroundColor: '#0C7075',
                borderRadius: 4
              },
              {
                label: 'Montaña',
                data: [0, 0, 120, 0, 0, 0, 180, 0],
                backgroundColor: '#6DA5C0',
                borderRadius: 4
              }
            ]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
              x: {
                stacked: true,
                grid: { display: false },
                ticks: { color: '#6DA5C0', font: { family: 'Outfit', size: 10 } }
              },
              y: {
                stacked: true,
                grid: { color: 'rgba(41, 77, 97, 0.35)' },
                ticks: { color: '#6DA5C0', font: { family: 'Outfit', size: 10 } }
              }
            },
            plugins: {
              legend: { display: false }
            }
          }
        });
      }

      const ctxDonut = document.getElementById('distributionDonutChart')?.getContext('2d');
      if (ctxDonut) {
        new Chart(ctxDonut, {
          type: 'doughnut',
          data: {
            labels: ['Carrera', 'Fuerza', 'Montaña'],
            datasets: [{
              data: [54, 31, 15],
              backgroundColor: ['#0F969C', '#0C7075', '#6DA5C0'],
              borderWidth: 0,
              hoverOffset: 4
            }]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '72%',
            plugins: {
              legend: { display: false }
            }
          }
        });
      }
    });
  </script>
</body>
</html>\`;
}
`;

fs.writeFileSync(path.join(__dirname, '../cloudflare/src/index.ts'), indexTsContent, 'utf8');
console.log('Successfully written cloudflare/src/index.ts. Size:', indexTsContent.length);
