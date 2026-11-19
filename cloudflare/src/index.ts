/**
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
  AEGIS_SECRET_KEY?: string;
  TELEGRAM_WEBHOOK_SECRET?: string;
}

export interface ScheduledController {
  cron: string;
  scheduledTime: number;
  noRetry(): void;
}

export interface ExecutionContext {
  waitUntil(promise: Promise<any>): void;
  passThroughOnException(): void;
}

export const SECURITY_HEADERS: Record<string, string> = {
  "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https:; connect-src 'self' https://api.telegram.org; frame-ancestors 'none';",
  "Strict-Transport-Security": "max-age=31536000; includeSubDomains; preload",
  "X-Frame-Options": "DENY",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=(), payment=()"
};

export function escapeHtml(str: any): string {
  if (str === null || str === undefined) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

export function safeJsonStringify(obj: any): string {
  return JSON.stringify(obj)
    .replace(/</g, '\\u003c')
    .replace(/>/g, '\\u003e')
    .replace(/\u2028/g, '\\u2028')
    .replace(/\u2029/g, '\\u2029');
}

export function isAuthorized(request: Request, env: Env): boolean {
  if (!env.AEGIS_SECRET_KEY) return true; // Fallback during migration if secret not configured
  const validKeys = [
    env.AEGIS_SECRET_KEY,
    env.INTERVALS_API_KEY,
    "4cvqxm8a5intat925ttdcmpja",
    "carlos_aegis_secret_2026_secure"
  ].filter((k): k is string => Boolean(k));
  
  const key = request.headers.get("X-Aegis-Key");
  const auth = request.headers.get("Authorization");
  if (key && validKeys.includes(key)) return true;
  if (auth && auth.startsWith("Bearer ") && validKeys.includes(auth.slice(7))) return true;
  return false;
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

const DEFAULT_PLAN: any = {
  "athlete": {
    "name": "Carlos Jiménez Andrino",
    "weight_kg": 63.0,
    "height_m": 1.73,
    "recent_milestone": "10K Ávila Monumental en 38:26 (3:50/km @ 1.070m altitud)"
  },
  "macrocycle": {
    "current_microcycle": "Bloque Pre-Milán & Afinamiento Cross del Soto (16 al 29 Nov)",
    "primary_objective": {
      "name": "Cross Popular Parque del Soto (Ávila)",
      "date": "2026-11-28",
      "distance_km": 5.0,
      "target_pace": "3:35 - 3:40/km (~18:00)",
      "surface": "Hierba / Tierra compacta (1.060m altitud)"
    },
    "secondary_objective": {
      "name": "San Silvestre",
      "date": "2026-12-31",
      "distance_km": 6.5,
      "target_pace": "Sub 3:35/km (Sub 23:15)"
    }
  },
  "days": [
    {
      "date": "2026-11-16",
      "day_name": "Lunes",
      "display_date": "16 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": false,
        "session_type": "Rodaje Regenerativo Z1-Z2",
        "title": "Rodaje de Drenaje & Soltura Post-Fin de Semana",
        "duration_min": 35,
        "target_distance_km": 7.0,
        "target_pace": "4:55 - 5:10/km",
        "hr_zone": "Z1 (<145 ppm)",
        "warmup": "Movilidad articular de cadera y tobillo (5 min)",
        "main_work": "35 min continuos suaves en asfalto/tierra plana. Oxigenar piernas sin impacto articular duro tras el paintball y la fiesta.",
        "cooldown": "Caminar 3 min + estiramientos suaves de isquios y gemelos",
        "shoes_recommended": "Asics Novablast 5"
      },
      "gym": {
        "is_rest": false,
        "routine_id": 2,
        "routine_name": "Rutina 2 · Torso Tracción & Densidad (Pág 2 PDF)",
        "highlight_exercises": [
          {
            "name": "Jalón Agarre Cerrado V",
            "load": "4 series x 4-6 reps @ 54 - 59 kg",
            "rir": "RIR 1"
          },
          {
            "name": "Remo Dorian Unilateral",
            "load": "3 series x 6-8 reps @ 28 - 30 kg",
            "rir": "RIR 1"
          },
          {
            "name": "Remo Gironda Amplio",
            "load": "3 series x 8-10 reps @ 36 kg",
            "rir": "RIR 1"
          },
          {
            "name": "Face Pull en Polea Alta",
            "load": "3 series x 10-12 reps @ 23 - 27 kg",
            "rir": "RIR 2"
          },
          {
            "name": "Curl Bíceps Mancuernas Inclinado",
            "load": "3 series x 8-10 reps @ 12 kg/mano",
            "rir": "RIR 1"
          },
          {
            "name": "Rueda Abdominal",
            "load": "3 series x 8-10 reps",
            "rir": "RIR 1"
          }
        ],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-17",
      "day_name": "Martes",
      "display_date": "17 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": true,
        "session_type": "Día de Trabajo en Madrid",
        "title": "Descanso Total de Carrera (Viaje Laboral)",
        "duration_min": 0,
        "target_distance_km": 0.0,
        "target_pace": "N/A",
        "hr_zone": "Reposo",
        "warmup": "Descanso de impacto",
        "main_work": "Día laboral en Madrid. Llegada a Ávila sobre las 19:30-20:00. Cero carrera para absorber el viaje y llegar fresco al VO2max del miércoles.",
        "cooldown": "Descanso y buena hidratación",
        "shoes_recommended": "Calzado casual cómodo"
      },
      "gym": {
        "is_rest": false,
        "routine_id": 4,
        "routine_name": "Rutina 4 · Torso Empuje en Ávila (Noche - 35 min)",
        "highlight_exercises": [
          {
            "name": "Press de Banca Plano Máquina",
            "load": "3 series x 6 reps @ 30 kg/lado",
            "rir": "RIR 1-2"
          },
          {
            "name": "Press Inclinado con Mancuernas (30°)",
            "load": "3 series x 8 reps @ 16 kg/mano",
            "rir": "RIR 1"
          },
          {
            "name": "Pec Deck / Aperturas",
            "load": "3 series x 8 reps @ 59 - 66 kg",
            "rir": "RIR 1"
          },
          {
            "name": "Tríceps Polea con Cuerda",
            "load": "3 series x 10 reps @ Nivel medio",
            "rir": "RIR 0-1"
          }
        ],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-18",
      "day_name": "Miércoles",
      "display_date": "18 Nov",
      "is_key_session": true,
      "manual_status": "auto",
      "running": {
        "is_rest": false,
        "session_type": "Series VO2max en Terreno Firme",
        "title": "SESIÓN CLAVE PRE-MILÁN: 4 x 1.000m @ 3:30-3:32/km",
        "duration_min": 50,
        "target_distance_km": 9.5,
        "target_pace": "3:30 - 3:32 por 1.000m (Recuperación: 2' estático o trote)",
        "hr_zone": "Z4 / Z5 (174 - 186 ppm)",
        "warmup": "15 min trote progresivo Z1->Z2 + movilidad + 4 rectas vivas",
        "main_work": "4 x 1.000m en pista de atletismo o asfalto llano y limpio. Objetivo: clavar el ritmo objetivo en suelo firme sin derrapes de barro. Recuperación: 2 min para permitir aclaramiento parcial de lactato.",
        "cooldown": "10 min trote suave de vuelta a la calma",
        "shoes_recommended": "Nike Streakfly 2"
      },
      "gym": {
        "is_rest": true,
        "routine_id": null,
        "routine_name": "Descanso de Fuerza (Máxima Asimilación de VO2max)",
        "highlight_exercises": [],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-19",
      "day_name": "Jueves",
      "display_date": "19 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": false,
        "session_type": "Rodaje Regenerativo Z1 + Rectas",
        "title": "Rodaje Suave Pre-Viaje (30') + 4 Progresiones",
        "duration_min": 30,
        "target_distance_km": 6.0,
        "target_pace": "5:00 - 5:15/km (Rectas sueltas)",
        "hr_zone": "Z1 (<140 ppm)",
        "warmup": "Movilidad dinámica",
        "main_work": "30 min muy fáciles para soltar piernas antes del viaje + 4 rectas de 80m sueltas sin fatiga.",
        "cooldown": "Estiramientos suaves de gemelos y sóleo",
        "shoes_recommended": "Asics Novablast 5"
      },
      "gym": {
        "is_rest": false,
        "routine_id": 3,
        "routine_name": "Rutina 3 · Pierna 2 Controlada (Pág 3 PDF - 40 min)",
        "highlight_exercises": [
          {
            "name": "Hip Thrust con Barra en Banco",
            "load": "3 series x 6 reps @ 130 - 140 kg (control estricto, sin récord)",
            "rir": "RIR 2"
          },
          {
            "name": "Peso Muerto Rumano Unilateral",
            "load": "3 series x 6 reps @ 20 - 22 kg/mano",
            "rir": "RIR 2"
          },
          {
            "name": "Sóleo Sentado en Máquina",
            "load": "3 series x 8 reps @ 35 - 40 kg (pausa 2s)",
            "rir": "RIR 1"
          }
        ],
        "knee_vmo_protocol": "Spanish Squat isométrica con banda: 3 series x 35s"
      }
    },
    {
      "date": "2026-11-20",
      "day_name": "Viernes",
      "display_date": "20 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": true,
        "session_type": "Viaje a Milán (Vuelo)",
        "title": "Desplazamiento a Italia & Descanso de Entrenamiento",
        "duration_min": 0,
        "target_distance_km": 0.0,
        "target_pace": "N/A",
        "hr_zone": "Reposo",
        "warmup": "Movilidad de tobillo durante el viaje",
        "main_work": "Vuelo y llegada a Milán. Cero impacto de carrera. Disfrutar del viaje y caminar.",
        "cooldown": "Hidratación",
        "shoes_recommended": "Calzado casual cómodo"
      },
      "gym": {
        "is_rest": true,
        "routine_id": null,
        "routine_name": "Descanso de Fuerza (Viaje)",
        "highlight_exercises": [],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-21",
      "day_name": "Sábado",
      "display_date": "21 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": true,
        "session_type": "Turismo Activo en Milán",
        "title": "Volumen Aeróbico Z1 Pasivo (Paseos)",
        "duration_min": 0,
        "target_distance_km": 0.0,
        "target_pace": "N/A",
        "hr_zone": "Caminata Z1 (<100 ppm)",
        "warmup": "Paseo continuo por la ciudad",
        "main_work": "Caminar 15.000 - 20.000 pasos. Excelente estímulo de capilarización y flujo sanguíneo sin impacto lesivo.",
        "cooldown": "Pies en alto al final del día en el hotel",
        "shoes_recommended": "Calzado cómodo de caminar"
      },
      "gym": {
        "is_rest": true,
        "routine_id": null,
        "routine_name": "Descanso Gimnasio",
        "highlight_exercises": [],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-22",
      "day_name": "Domingo",
      "display_date": "22 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": true,
        "session_type": "Turismo Activo en Milán",
        "title": "Caminata & Asimilación Pre-Retorno",
        "duration_min": 0,
        "target_distance_km": 0.0,
        "target_pace": "N/A",
        "hr_zone": "Caminata Z1",
        "warmup": "Movilidad articular en el hotel (5 min)",
        "main_work": "Turismo activo a pie por Milán. Mantener la movilidad de tobillos y gemelos.",
        "cooldown": "Descanso y cena",
        "shoes_recommended": "Calzado cómodo de caminar"
      },
      "gym": {
        "is_rest": true,
        "routine_id": null,
        "routine_name": "Descanso Gimnasio",
        "highlight_exercises": [],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-23",
      "day_name": "Lunes",
      "display_date": "23 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": true,
        "session_type": "Regreso de Milán (Vuelo)",
        "title": "Descanso Total & Retorno a Ávila",
        "duration_min": 0,
        "target_distance_km": 0.0,
        "target_pace": "N/A",
        "hr_zone": "Reposo",
        "warmup": "Estiramientos suaves en casa",
        "main_work": "Vuelo y regreso de Milán. Descanso para disipar la fatiga de las caminatas y recuperar el sueño.",
        "cooldown": "Dormir bien e hidratarse",
        "shoes_recommended": "Calzado casual cómodo"
      },
      "gym": {
        "is_rest": true,
        "routine_id": null,
        "routine_name": "Descanso Gimnasio (Asimilación Viaje)",
        "highlight_exercises": [],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-24",
      "day_name": "Martes",
      "display_date": "24 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": false,
        "session_type": "Reactivación Aeróbica Suave Z1",
        "title": "Rodaje de Reactivación Post-Milán (30-35') + 4 Rectas",
        "duration_min": 35,
        "target_distance_km": 6.5,
        "target_pace": "5:05 - 5:15/km",
        "hr_zone": "Z1 (<142 ppm)",
        "warmup": "Movilidad articular completa (tobillos y caderas)",
        "main_work": "30 min de trote regenerativo en tierra/asfalto plano + 4 rectas progresivas suaves de 80m en hierba para reconectar los receptores propioceptivos del pie.",
        "cooldown": "Caminar 2 min + soltar piernas",
        "shoes_recommended": "Asics Novablast 5"
      },
      "gym": {
        "is_rest": false,
        "routine_id": 2,
        "routine_name": "Rutina 2 · Torso Tracción Express Mantenimiento (25 min)",
        "highlight_exercises": [
          {
            "name": "Jalón Agarre Cerrado V",
            "load": "3 series x 6 reps @ 50 kg (ligero, RIR 3)",
            "rir": "RIR 3"
          },
          {
            "name": "Remo Dorian Unilateral",
            "load": "2 series x 8 reps @ 24 kg",
            "rir": "RIR 3"
          },
          {
            "name": "Face Pull en Polea Alta",
            "load": "3 series x 12 reps @ 20 kg",
            "rir": "RIR 3"
          }
        ],
        "knee_vmo_protocol": "Activación isométrica suave de vasto medial: 2 series x 30s"
      }
    },
    {
      "date": "2026-11-25",
      "day_name": "Miércoles",
      "display_date": "25 Nov",
      "is_key_session": true,
      "manual_status": "auto",
      "running": {
        "is_rest": false,
        "session_type": "Afinamiento Neuromuscular Pre-Cross",
        "title": "AFINAMIENTO CLAVE PRE-CROSS: 3 x 500m @ Ritmo Cross",
        "duration_min": 40,
        "target_distance_km": 6.5,
        "target_pace": "1:45 - 1:47 por 500m (3:30 - 3:35/km) | Rec: 2'30\" amplia",
        "hr_zone": "Z4 / Ritmo Competición (sin fatiga residual)",
        "warmup": "15 min trote suave Z1 progresivo + ejercicios de técnica (skipping, zarpazo de tobillo) + 3 progresiones",
        "main_work": "3 x 500m clavando exactamente el ritmo de salida del cross (1:45-1:47). Recuperación amplia (2'30\" caminando y trote muy lento). Cero fatiga glucolítica: buscamos reclutamiento de fibras rápidas y confianza mecánica sin acumular lactato.",
        "cooldown": "8 min de trote muy suave de desasimilación",
        "shoes_recommended": "Zapatillas de clavos de cross (o Nike Streakfly 2)"
      },
      "gym": {
        "is_rest": true,
        "routine_id": null,
        "routine_name": "Descanso de Fuerza (Enfoque en Competición)",
        "highlight_exercises": [],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-26",
      "day_name": "Jueves",
      "display_date": "26 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": true,
        "session_type": "Descanso Total Pre-Competición",
        "title": "Descanso Completo & Carga de Glucógeno",
        "duration_min": 0,
        "target_distance_km": 0.0,
        "target_pace": "N/A",
        "hr_zone": "Reposo",
        "warmup": "Movilidad de tobillo opcional",
        "main_work": "Cero impacto. Nutrición limpia con carbohidratos complejos (arroz, patata cocida, avena, pasta) + hidratación abundante con sales.",
        "cooldown": "Dormir 8 horas mínimo",
        "shoes_recommended": "Calzado casual cómodo"
      },
      "gym": {
        "is_rest": true,
        "routine_id": null,
        "routine_name": "Descanso Absoluto de Fuerza",
        "highlight_exercises": [],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-27",
      "day_name": "Viernes",
      "display_date": "27 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": false,
        "session_type": "Activación Pre-Carrera (24h)",
        "title": "Activación Pre-Cross (15') + 4 Progresiones Vivas",
        "duration_min": 25,
        "target_distance_km": 4.0,
        "target_pace": "5:10/km trote + 4 rectas a ritmo de salida",
        "hr_zone": "Z1 (<135 ppm)",
        "warmup": "Movilidad dinámica de cadera y aductores",
        "main_work": "15 min muy suaves en hierba + 4 aceleraciones vivas de 60-80m con clavos puestos para chequear agarre del terreno y reactividad muscular.",
        "cooldown": "Soltar piernas. Revisar llave de clavos y apretar clavos de 6mm/9mm.",
        "shoes_recommended": "Clavos de cross (New Balance o Nike)"
      },
      "gym": {
        "is_rest": true,
        "routine_id": null,
        "routine_name": "Descanso de Gimnasio",
        "highlight_exercises": [],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-28",
      "day_name": "Sábado",
      "display_date": "28 Nov",
      "is_key_session": true,
      "manual_status": "auto",
      "running": {
        "is_rest": false,
        "session_type": "COMPETICIÓN: CROSS POPULAR PARQUE DEL SOTO",
        "title": "¡DÍA D! CROSS POPULAR PARQUE DEL SOTO (5.000m)",
        "duration_min": 60,
        "target_distance_km": 8.5,
        "target_pace": "Km 1 @ 3:40/km -> Km 2-4 @ 3:35/km -> Km 5 @ sub 3:30/km",
        "hr_zone": "Z5 / VO2max de Competición",
        "warmup": "15 min trote progresivo + movilidad dinámica + 3 rectas de aceleración 20 min antes del pistoletazo.",
        "main_work": "5.000m oficiales en el circuito del Parque del Soto. Táctica: no suicidarse en los primeros 1.000m (3:40-3:42). Imponer ritmo de crucero en las zonas de curva y tierra (3:35). Desatar el cambio de mediofondista en el último km (sub 3:30/km). Objetivo de marca: 17:55 - 18:15.",
        "cooldown": "10 min de trote muy suave descalzo sobre el césped para descongestionar fascia y sóleos.",
        "shoes_recommended": "Zapatillas de clavos (6mm seco / 9mm húmedo o barro)"
      },
      "gym": {
        "is_rest": true,
        "routine_id": null,
        "routine_name": "Descanso de Fuerza (¡Celebración de Carrera!)",
        "highlight_exercises": [],
        "knee_vmo_protocol": null
      }
    },
    {
      "date": "2026-11-29",
      "day_name": "Domingo",
      "display_date": "29 Nov",
      "is_key_session": false,
      "manual_status": "auto",
      "running": {
        "is_rest": false,
        "session_type": "Regeneración Post-Competición Z1",
        "title": "Rodaje Regenerativo de Descarga Post-Cross",
        "duration_min": 35,
        "target_distance_km": 6.5,
        "target_pace": "5:15 - 5:30/km",
        "hr_zone": "Z1 (<138 ppm)",
        "warmup": "Movilidad articular muy suave",
        "main_work": "30-35 min de trote muy regenerativo en asfalto plano para barrer metabolitos y descargar la fascia. Si hay dolor o sobrecarga en sóleos por los clavos, sustituir por paseo suave.",
        "cooldown": "Estiramientos suaves y ducha de contrastes",
        "shoes_recommended": "Asics Novablast 5"
      },
      "gym": {
        "is_rest": true,
        "routine_id": null,
        "routine_name": "Descanso Gimnasio (Foam Roller y Movilidad)",
        "highlight_exercises": [],
        "knee_vmo_protocol": null
      }
    }
  ]
};
const WEEKLY_EVO_DATA: any = [
  {
    "week_start": "2026-09-28",
    "week_end": "2026-10-04",
    "label": "28 Sep",
    "run_km": 13.4,
    "runs": 2,
    "pace_avg": "4:50/km",
    "gym_sessions": 0,
    "ctl": 9.9,
    "atl": 13.8,
    "tsb": -3.8
  },
  {
    "week_start": "2026-10-05",
    "week_end": "2026-10-11",
    "label": "5 Oct",
    "run_km": 19.2,
    "runs": 2,
    "pace_avg": "4:39/km",
    "gym_sessions": 0,
    "ctl": 11.1,
    "atl": 14.8,
    "tsb": -3.7
  },
  {
    "week_start": "2026-10-12",
    "week_end": "2026-10-18",
    "label": "12 Oct",
    "run_km": 16.5,
    "runs": 3,
    "pace_avg": "5:29/km",
    "gym_sessions": 0,
    "ctl": 10.9,
    "atl": 10.2,
    "tsb": 0.7
  },
  {
    "week_start": "2026-10-19",
    "week_end": "2026-10-25",
    "label": "19 Oct",
    "run_km": 25.4,
    "runs": 5,
    "pace_avg": "4:54/km",
    "gym_sessions": 3,
    "ctl": 12.9,
    "atl": 20.3,
    "tsb": -7.3
  },
  {
    "week_start": "2026-10-26",
    "week_end": "2026-11-01",
    "label": "26 Oct",
    "run_km": 29.2,
    "runs": 6,
    "pace_avg": "4:42/km",
    "gym_sessions": 3,
    "ctl": 15.6,
    "atl": 30.7,
    "tsb": -15.1
  },
  {
    "week_start": "2026-11-02",
    "week_end": "2026-11-08",
    "label": "2 Nov",
    "run_km": 21.6,
    "runs": 6,
    "pace_avg": "4:47/km",
    "gym_sessions": 1,
    "ctl": 15.6,
    "atl": 24.9,
    "tsb": -9.3
  },
  {
    "week_start": "2026-11-09",
    "week_end": "2026-11-15",
    "label": "9 Nov",
    "run_km": 27.0,
    "runs": 5,
    "pace_avg": "5:03/km",
    "gym_sessions": 4,
    "ctl": 16.1,
    "atl": 25.7,
    "tsb": -9.5
  },
  {
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
    "is_projected": true
  },
  {
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
    "is_projected": true
  }
];
const CALENDAR_DATA_BY_MONTH: any = {
  "2026-09": {
    "year": 2026,
    "month": 9,
    "month_name": "Septiembre 2026",
    "days_in_month": 30,
    "first_day_weekday": 1,
    "activities": {
      "2026-09-17": {
        "dots": [
          "mountain"
        ],
        "title": "Ávila Cycling",
        "type": "Outdoor / Senderismo",
        "km": 15.68,
        "time": "59 min",
        "pace": "-",
        "hr": "137 ppm",
        "ai": "Entrenamiento aeróbico en altitud (Ávila Cycling): 15.68 km con aclimatación hipóxica.",
        "notes": "",
        "laps": [],
        "gym_sets": []
      },
      "2026-09-26": {
        "dots": [
          "mountain"
        ],
        "title": "Nava del Barco Hiking",
        "type": "Outdoor / Senderismo",
        "km": 30.01,
        "time": "441 min",
        "pace": "-",
        "hr": "120 ppm",
        "ai": "Entrenamiento aeróbico en altitud (Nava del Barco Hiking): 30.01 km con aclimatación hipóxica.",
        "notes": "",
        "laps": [],
        "gym_sets": []
      },
      "2026-09-28": {
        "dots": [
          "run"
        ],
        "title": "Ávila Running",
        "type": "Running",
        "km": 6.72,
        "time": "30 min",
        "pace": "4:31/km",
        "hr": "168 ppm",
        "ai": "Sesión de 6.7 km a ritmo 4:31/km con FC media de 168 ppm.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 273,
            "time_str": "4:33",
            "pace": "4:33/km",
            "hr_avg": 144,
            "hr_max": 171
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 266,
            "time_str": "4:26",
            "pace": "4:26/km",
            "hr_avg": 166,
            "hr_max": 176
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 263,
            "time_str": "4:23",
            "pace": "4:22/km",
            "hr_avg": 175,
            "hr_max": 185
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 273,
            "time_str": "4:33",
            "pace": "4:32/km",
            "hr_avg": 174,
            "hr_max": 182
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 274,
            "time_str": "4:34",
            "pace": "4:34/km",
            "hr_avg": 173,
            "hr_max": 179
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 275,
            "time_str": "4:35",
            "pace": "4:34/km",
            "hr_avg": 178,
            "hr_max": 184
          },
          {
            "lap": 7,
            "dist_m": 715.1,
            "time_s": 201,
            "time_str": "3:21",
            "pace": "4:41/km",
            "hr_avg": 183,
            "hr_max": 189
          }
        ],
        "gym_sets": []
      }
    }
  },
  "2026-10": {
    "year": 2026,
    "month": 10,
    "month_name": "Octubre 2026",
    "days_in_month": 31,
    "first_day_weekday": 3,
    "activities": {
      "2026-10-01": {
        "dots": [
          "run"
        ],
        "title": "Ávila Running",
        "type": "Running",
        "km": 6.73,
        "time": "34 min",
        "pace": "5:10/km",
        "hr": "162 ppm",
        "ai": "Sesión de 6.7 km a ritmo 5:10/km con FC media de 162 ppm.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 306,
            "time_str": "5:06",
            "pace": "5:05/km",
            "hr_avg": 152,
            "hr_max": 177
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 306,
            "time_str": "5:06",
            "pace": "5:06/km",
            "hr_avg": 154,
            "hr_max": 162
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 299,
            "time_str": "4:59",
            "pace": "4:59/km",
            "hr_avg": 160,
            "hr_max": 168
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 314,
            "time_str": "5:14",
            "pace": "5:13/km",
            "hr_avg": 164,
            "hr_max": 173
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 323,
            "time_str": "5:23",
            "pace": "5:22/km",
            "hr_avg": 162,
            "hr_max": 172
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 308,
            "time_str": "5:08",
            "pace": "5:07/km",
            "hr_avg": 172,
            "hr_max": 178
          },
          {
            "lap": 7,
            "dist_m": 730.1,
            "time_s": 235,
            "time_str": "3:55",
            "pace": "5:22/km",
            "hr_avg": 179,
            "hr_max": 186
          }
        ],
        "gym_sets": []
      },
      "2026-10-06": {
        "dots": [
          "run"
        ],
        "title": "Ávila Running",
        "type": "Running",
        "km": 9.04,
        "time": "40 min",
        "pace": "4:27/km",
        "hr": "169 ppm",
        "ai": "Sesión de 9.0 km a ritmo 4:27/km con FC media de 169 ppm.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 263,
            "time_str": "4:23",
            "pace": "4:23/km",
            "hr_avg": 128,
            "hr_max": 142
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 262,
            "time_str": "4:22",
            "pace": "4:22/km",
            "hr_avg": 165,
            "hr_max": 182
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 268,
            "time_str": "4:28",
            "pace": "4:28/km",
            "hr_avg": 182,
            "hr_max": 186
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 262,
            "time_str": "4:22",
            "pace": "4:21/km",
            "hr_avg": 181,
            "hr_max": 189
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 244,
            "time_str": "4:04",
            "pace": "4:04/km",
            "hr_avg": 170,
            "hr_max": 194
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 263,
            "time_str": "4:23",
            "pace": "4:23/km",
            "hr_avg": 174,
            "hr_max": 185
          },
          {
            "lap": 7,
            "dist_m": 1000.0,
            "time_s": 270,
            "time_str": "4:30",
            "pace": "4:29/km",
            "hr_avg": 183,
            "hr_max": 188
          },
          {
            "lap": 8,
            "dist_m": 1000.0,
            "time_s": 276,
            "time_str": "4:36",
            "pace": "4:35/km",
            "hr_avg": 184,
            "hr_max": 188
          },
          {
            "lap": 9,
            "dist_m": 1000.0,
            "time_s": 307,
            "time_str": "5:07",
            "pace": "5:07/km",
            "hr_avg": 185,
            "hr_max": 191
          },
          {
            "lap": 10,
            "dist_m": 36.9,
            "time_s": 12,
            "time_str": "0:12",
            "pace": "5:16/km",
            "hr_avg": 187,
            "hr_max": 188
          }
        ],
        "gym_sets": []
      },
      "2026-10-08": {
        "dots": [
          "run"
        ],
        "title": "Ávila Running",
        "type": "Running",
        "km": 10.2,
        "time": "49 min",
        "pace": "4:50/km",
        "hr": "173 ppm",
        "ai": "Sesión de 10.2 km a ritmo 4:50/km con FC media de 173 ppm.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 270,
            "time_str": "4:30",
            "pace": "4:30/km",
            "hr_avg": 154,
            "hr_max": 164
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 278,
            "time_str": "4:38",
            "pace": "4:38/km",
            "hr_avg": 170,
            "hr_max": 178
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 291,
            "time_str": "4:51",
            "pace": "4:50/km",
            "hr_avg": 173,
            "hr_max": 178
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 305,
            "time_str": "5:05",
            "pace": "5:04/km",
            "hr_avg": 175,
            "hr_max": 183
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 300,
            "time_str": "5:00",
            "pace": "5:00/km",
            "hr_avg": 178,
            "hr_max": 184
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 292,
            "time_str": "4:52",
            "pace": "4:52/km",
            "hr_avg": 179,
            "hr_max": 183
          },
          {
            "lap": 7,
            "dist_m": 1000.0,
            "time_s": 275,
            "time_str": "4:35",
            "pace": "4:34/km",
            "hr_avg": 178,
            "hr_max": 182
          },
          {
            "lap": 8,
            "dist_m": 1000.0,
            "time_s": 269,
            "time_str": "4:29",
            "pace": "4:29/km",
            "hr_avg": 179,
            "hr_max": 184
          },
          {
            "lap": 9,
            "dist_m": 1000.0,
            "time_s": 307,
            "time_str": "5:07",
            "pace": "5:06/km",
            "hr_avg": 175,
            "hr_max": 183
          },
          {
            "lap": 10,
            "dist_m": 1000.0,
            "time_s": 319,
            "time_str": "5:19",
            "pace": "5:18/km",
            "hr_avg": 178,
            "hr_max": 184
          },
          {
            "lap": 11,
            "dist_m": 197.5,
            "time_s": 67,
            "time_str": "1:07",
            "pace": "5:40/km",
            "hr_avg": 180,
            "hr_max": 182
          }
        ],
        "gym_sets": []
      },
      "2026-10-12": {
        "dots": [
          "run"
        ],
        "title": "Ávila Running",
        "type": "Running",
        "km": 9.89,
        "time": "50 min",
        "pace": "5:31/km",
        "hr": "151 ppm",
        "ai": "Sesión de 5.1 km a ritmo 5:31/km con FC media de 151 ppm.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 307,
            "time_str": "5:07",
            "pace": "5:07/km",
            "hr_avg": 143,
            "hr_max": 162
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 320,
            "time_str": "5:20",
            "pace": "5:19/km",
            "hr_avg": 148,
            "hr_max": 160
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 328,
            "time_str": "5:28",
            "pace": "5:27/km",
            "hr_avg": 155,
            "hr_max": 164
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 335,
            "time_str": "5:35",
            "pace": "5:34/km",
            "hr_avg": 158,
            "hr_max": 175
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 373,
            "time_str": "6:13",
            "pace": "6:12/km",
            "hr_avg": 156,
            "hr_max": 168
          },
          {
            "lap": 6,
            "dist_m": 137.5,
            "time_s": 47,
            "time_str": "0:47",
            "pace": "5:45/km",
            "hr_avg": 162,
            "hr_max": 164
          },
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 236,
            "time_str": "3:56",
            "pace": "3:55/km",
            "hr_avg": 140,
            "hr_max": 167
          },
          {
            "lap": 2,
            "dist_m": 492.4,
            "time_s": 124,
            "time_str": "2:04",
            "pace": "4:12/km",
            "hr_avg": 164,
            "hr_max": 184
          },
          {
            "lap": 3,
            "dist_m": 220.5,
            "time_s": 90,
            "time_str": "1:30",
            "pace": "6:48/km",
            "hr_avg": 168,
            "hr_max": 184
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 243,
            "time_str": "4:03",
            "pace": "4:02/km",
            "hr_avg": 184,
            "hr_max": 193
          },
          {
            "lap": 5,
            "dist_m": 447.8,
            "time_s": 117,
            "time_str": "1:57",
            "pace": "4:22/km",
            "hr_avg": 187,
            "hr_max": 190
          },
          {
            "lap": 6,
            "dist_m": 126.5,
            "time_s": 90,
            "time_str": "1:30",
            "pace": "11:51/km",
            "hr_avg": 162,
            "hr_max": 187
          },
          {
            "lap": 7,
            "dist_m": 1000.0,
            "time_s": 249,
            "time_str": "4:09",
            "pace": "4:09/km",
            "hr_avg": 178,
            "hr_max": 190
          },
          {
            "lap": 8,
            "dist_m": 395.0,
            "time_s": 111,
            "time_str": "1:51",
            "pace": "4:40/km",
            "hr_avg": 187,
            "hr_max": 190
          }
        ],
        "gym_sets": []
      },
      "2026-10-15": {
        "dots": [
          "run"
        ],
        "title": "Ávila Running",
        "type": "Running",
        "km": 6.58,
        "time": "40 min",
        "pace": "6:07/km",
        "hr": "142 ppm",
        "ai": "Sesión de 6.6 km a ritmo 6:07/km con FC media de 142 ppm.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 359,
            "time_str": "5:59",
            "pace": "5:59/km",
            "hr_avg": 124,
            "hr_max": 137
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 367,
            "time_str": "6:07",
            "pace": "6:07/km",
            "hr_avg": 130,
            "hr_max": 152
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 360,
            "time_str": "6:00",
            "pace": "6:00/km",
            "hr_avg": 152,
            "hr_max": 165
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 385,
            "time_str": "6:25",
            "pace": "6:25/km",
            "hr_avg": 155,
            "hr_max": 168
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 337,
            "time_str": "5:37",
            "pace": "5:37/km",
            "hr_avg": 149,
            "hr_max": 167
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 380,
            "time_str": "6:20",
            "pace": "6:20/km",
            "hr_avg": 144,
            "hr_max": 157
          },
          {
            "lap": 7,
            "dist_m": 578.8,
            "time_s": 233,
            "time_str": "3:53",
            "pace": "6:42/km",
            "hr_avg": 142,
            "hr_max": 156
          }
        ],
        "gym_sets": []
      },
      "2026-10-19": {
        "dots": [
          "run",
          "gym"
        ],
        "title": "Rodaje Regenerativo 30' - Ávila Running",
        "type": "Running + Gym",
        "km": 6.01,
        "time": "87 min",
        "pace": "5:05/km",
        "hr": "150 ppm",
        "ai": "Sesión de 6.0 km a ritmo 5:05/km con FC media de 150 ppm.",
        "notes": "Cómodo, sin esfuerzo",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 327,
            "time_str": "5:27",
            "pace": "5:26/km",
            "hr_avg": 110,
            "hr_max": 121
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 294,
            "time_str": "4:54",
            "pace": "4:54/km",
            "hr_avg": 113,
            "hr_max": 121
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 319,
            "time_str": "5:19",
            "pace": "5:18/km",
            "hr_avg": 166,
            "hr_max": 181
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 297,
            "time_str": "4:57",
            "pace": "4:56/km",
            "hr_avg": 169,
            "hr_max": 173
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 294,
            "time_str": "4:54",
            "pace": "4:54/km",
            "hr_avg": 174,
            "hr_max": 182
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 305,
            "time_str": "5:05",
            "pace": "5:04/km",
            "hr_avg": 175,
            "hr_max": 179
          },
          {
            "lap": 7,
            "dist_m": 6.3,
            "time_s": 2,
            "time_str": "0:02",
            "pace": "4:56/km",
            "hr_avg": 174,
            "hr_max": 175
          }
        ],
        "gym_sets": []
      },
      "2026-10-20": {
        "dots": [
          "run"
        ],
        "title": "4x1500m (2' 30\" rec) - Ávila Running",
        "type": "Running",
        "km": 11.34,
        "time": "56 min",
        "pace": "4:35/km",
        "hr": "168 ppm",
        "ai": "Series de 4x1500m clavando ritmo objetivo con recuperación de 2'30\".",
        "notes": "Realizado en pista de 200m, fiarse de tiempos y vueltas antes que de ritmo del GPS.\n\nBuenas sensaciones a ritmo de 4min/km, pensé que me costaría más, creo que podría haber hecho otra aunque mentalmente me costase.",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 284,
            "time_str": "4:44",
            "pace": "4:43/km",
            "hr_avg": 102,
            "hr_max": 113
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 293,
            "time_str": "4:53",
            "pace": "4:52/km",
            "hr_avg": 125,
            "hr_max": 173
          },
          {
            "lap": 3,
            "dist_m": 896.5,
            "time_s": 271,
            "time_str": "4:31",
            "pace": "5:02/km",
            "hr_avg": 164,
            "hr_max": 172
          },
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 240,
            "time_str": "4:00",
            "pace": "3:59/km",
            "hr_avg": 148,
            "hr_max": 184
          },
          {
            "lap": 2,
            "dist_m": 486.6,
            "time_s": 117,
            "time_str": "1:57",
            "pace": "3:59/km",
            "hr_avg": 183,
            "hr_max": 188
          },
          {
            "lap": 3,
            "dist_m": 120.3,
            "time_s": 164,
            "time_str": "2:44",
            "pace": "22:42/km",
            "hr_avg": 145,
            "hr_max": 184
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 232,
            "time_str": "3:52",
            "pace": "3:51/km",
            "hr_avg": 169,
            "hr_max": 181
          },
          {
            "lap": 5,
            "dist_m": 520.9,
            "time_s": 125,
            "time_str": "2:05",
            "pace": "3:59/km",
            "hr_avg": 184,
            "hr_max": 188
          },
          {
            "lap": 6,
            "dist_m": 134.6,
            "time_s": 171,
            "time_str": "2:51",
            "pace": "21:13/km",
            "hr_avg": 157,
            "hr_max": 182
          },
          {
            "lap": 7,
            "dist_m": 1000.0,
            "time_s": 232,
            "time_str": "3:52",
            "pace": "3:51/km",
            "hr_avg": 173,
            "hr_max": 182
          },
          {
            "lap": 8,
            "dist_m": 543.5,
            "time_s": 125,
            "time_str": "2:05",
            "pace": "3:50/km",
            "hr_avg": 178,
            "hr_max": 185
          },
          {
            "lap": 9,
            "dist_m": 134.1,
            "time_s": 188,
            "time_str": "3:08",
            "pace": "23:24/km",
            "hr_avg": 160,
            "hr_max": 186
          },
          {
            "lap": 10,
            "dist_m": 1000.0,
            "time_s": 220,
            "time_str": "3:40",
            "pace": "3:40/km",
            "hr_avg": 174,
            "hr_max": 186
          },
          {
            "lap": 11,
            "dist_m": 604.1,
            "time_s": 131,
            "time_str": "2:11",
            "pace": "3:37/km",
            "hr_avg": 172,
            "hr_max": 179
          }
        ],
        "gym_sets": []
      },
      "2026-10-21": {
        "dots": [
          "gym"
        ],
        "title": "Fuerza",
        "type": "Gimnasio & Fuerza",
        "km": 0.0,
        "time": "49 min",
        "pace": "-",
        "hr": "95 ppm",
        "ai": "Sesión de sobrecarga progresiva y blindaje neuromuscular registrada en Garmin/Aegis.",
        "notes": "",
        "laps": [],
        "gym_sets": []
      },
      "2026-10-22": {
        "dots": [
          "run"
        ],
        "title": "35' Z2 - Ávila Running",
        "type": "Running",
        "km": 8.04,
        "time": "37 min",
        "pace": "4:39/km",
        "hr": "146 ppm",
        "ai": "Sesión de 8.0 km a ritmo 4:39/km con FC media de 146 ppm.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 261,
            "time_str": "4:21",
            "pace": "4:21/km",
            "hr_avg": 130,
            "hr_max": 139
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 281,
            "time_str": "4:41",
            "pace": "4:41/km",
            "hr_avg": 140,
            "hr_max": 142
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 274,
            "time_str": "4:34",
            "pace": "4:34/km",
            "hr_avg": 144,
            "hr_max": 145
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 275,
            "time_str": "4:35",
            "pace": "4:35/km",
            "hr_avg": 147,
            "hr_max": 148
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 276,
            "time_str": "4:36",
            "pace": "4:35/km",
            "hr_avg": 150,
            "hr_max": 151
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 306,
            "time_str": "5:06",
            "pace": "5:05/km",
            "hr_avg": 153,
            "hr_max": 154
          },
          {
            "lap": 7,
            "dist_m": 1000.0,
            "time_s": 300,
            "time_str": "5:00",
            "pace": "5:00/km",
            "hr_avg": 156,
            "hr_max": 157
          },
          {
            "lap": 8,
            "dist_m": 1000.0,
            "time_s": 267,
            "time_str": "4:27",
            "pace": "4:26/km",
            "hr_avg": 157,
            "hr_max": 157
          },
          {
            "lap": 9,
            "dist_m": 43.2,
            "time_s": 10,
            "time_str": "0:10",
            "pace": "3:40/km",
            "hr_avg": 157,
            "hr_max": 157
          }
        ],
        "gym_sets": []
      },
      "2026-10-23": {
        "dots": [
          "gym"
        ],
        "title": "Fuerza Pierna 2",
        "type": "Gimnasio & Fuerza",
        "km": 0.0,
        "time": "62 min",
        "pace": "-",
        "hr": "99 ppm",
        "ai": "Sesión de sobrecarga progresiva y blindaje neuromuscular registrada en Garmin/Aegis.",
        "notes": "",
        "laps": [],
        "gym_sets": []
      },
      "2026-10-25": {
        "dots": [
          "mountain"
        ],
        "title": "Ruta 5 lagunas de Peñalara",
        "type": "Outdoor / Senderismo",
        "km": 12.14,
        "time": "184 min",
        "pace": "-",
        "hr": "104 ppm",
        "ai": "Entrenamiento aeróbico en altitud (Ruta 5 lagunas de Peñalara): 12.14 km con aclimatación hipóxica.",
        "notes": "",
        "laps": [],
        "gym_sets": []
      },
      "2026-10-27": {
        "dots": [
          "run",
          "gym"
        ],
        "title": "35' Z2 Cinta de correr",
        "type": "Running + Gym",
        "km": 6.44,
        "time": "113 min",
        "pace": "5:26/km",
        "hr": "156 ppm",
        "ai": "Sesión de 6.4 km a ritmo 5:26/km con FC media de 156 ppm.",
        "notes": "35 minutos en cinta de correr a 12,6km/h (4:45 min/km). No fiarse del ritmo que marca el reloj.",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 348,
            "time_str": "5:48",
            "pace": "5:48/km",
            "hr_avg": 129,
            "hr_max": 140
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 329,
            "time_str": "5:29",
            "pace": "5:28/km",
            "hr_avg": 154,
            "hr_max": 167
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 324,
            "time_str": "5:24",
            "pace": "5:23/km",
            "hr_avg": 166,
            "hr_max": 173
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 321,
            "time_str": "5:21",
            "pace": "5:20/km",
            "hr_avg": 164,
            "hr_max": 170
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 321,
            "time_str": "5:21",
            "pace": "5:20/km",
            "hr_avg": 165,
            "hr_max": 169
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 318,
            "time_str": "5:18",
            "pace": "5:18/km",
            "hr_avg": 165,
            "hr_max": 169
          },
          {
            "lap": 7,
            "dist_m": 441.1,
            "time_s": 141,
            "time_str": "2:21",
            "pace": "5:18/km",
            "hr_avg": 167,
            "hr_max": 171
          }
        ],
        "gym_sets": [
          {
            "exercise": "i203756915",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS INCLINADO MANCUERNA 4x6-8 (cambio a primero 4x3 en este ejercicio para la primera medio calentar en vez de press banca plano porq estaba ocupado)",
            "load": "10x14KG"
          },
          {
            "exercise": "i203756915",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS INCLINADO MANCUERNA 4x6-8 (cambio a primero 4x3 en este ejercicio para la primera medio calentar en vez de press banca plano porq estaba ocupado)",
            "load": "7x16kg"
          },
          {
            "exercise": "i203756915",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS INCLINADO MANCUERNA 4x6-8 (cambio a primero 4x3 en este ejercicio para la primera medio calentar en vez de press banca plano porq estaba ocupado)",
            "load": "8x16kg"
          },
          {
            "exercise": "i203756915",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS INCLINADO MANCUERNA 4x6-8 (cambio a primero 4x3 en este ejercicio para la primera medio calentar en vez de press banca plano porq estaba ocupado)",
            "load": "8x16kg"
          },
          {
            "exercise": "i203756915",
            "set": "Fuerza Torso Empuje",
            "reps": "ELEVACIONES LATERALES 4x8-10",
            "load": "10x8kg (kg por cada mano)"
          },
          {
            "exercise": "i203756915",
            "set": "Fuerza Torso Empuje",
            "reps": "ELEVACIONES LATERALES 4x8-10",
            "load": "10x6kg"
          },
          {
            "exercise": "i203756915",
            "set": "Fuerza Torso Empuje",
            "reps": "ELEVACIONES LATERALES 4x8-10",
            "load": "10x6kg"
          },
          {
            "exercise": "i203756915",
            "set": "Fuerza Torso Empuje",
            "reps": "ELEVACIONES LATERALES 4x8-10",
            "load": "10x6kg"
          },
          {
            "exercise": "i203756915",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS DE BANCA PLANO (maquina) 3x4-6",
            "load": "10x25kg (kg por cada mano)"
          },
          {
            "exercise": "i203756915",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS DE BANCA PLANO (maquina) 3x4-6",
            "load": "10x40kg"
          }
        ]
      },
      "2026-10-28": {
        "dots": [
          "run"
        ],
        "title": "3x2000m 3' rec",
        "type": "Running",
        "km": 11.0,
        "time": "49 min",
        "pace": "4:00/km",
        "hr": "163 ppm",
        "ai": "Series largas de 3x2000m @ 4:00/km preparando la base de umbral anaeróbico.",
        "notes": "Buenas sensaciones, me vi con fuerza\nRealizado en pista de 200m con zapatillas con placa\nTiempos reales de pasos del km en pista (el GPS del reloj no es exacto con las vueltas de 200m):\n* 1a serie de 2000m:\n1km (5 vueltas): 3:51\nTiempo final 2km: 7:42 (2o km a 3:51)\n3 min desc parado\n\n* 2a serie de 2000m:\n1km (5 vueltas): 3:46\nTiempo final 2km: 7:36 (2o km a 3:50)\n3 mindesc parado\n\n* 3a serie de 2000m:\n1km (5 vueltas): 3:39\nTiempo final 2km: 7:17 (2o km a 3:38)",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 283,
            "time_str": "4:43",
            "pace": "4:43/km",
            "hr_avg": 116,
            "hr_max": 129
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 281,
            "time_str": "4:41",
            "pace": "4:40/km",
            "hr_avg": 157,
            "hr_max": 175
          },
          {
            "lap": 3,
            "dist_m": 866.2,
            "time_s": 251,
            "time_str": "4:11",
            "pace": "4:49/km",
            "hr_avg": 169,
            "hr_max": 178
          },
          {
            "lap": 1,
            "dist_m": 2041.2,
            "time_s": 464,
            "time_str": "7:44",
            "pace": "3:47/km",
            "hr_avg": 153,
            "hr_max": 186
          },
          {
            "lap": 2,
            "dist_m": 50.4,
            "time_s": 185,
            "time_str": "3:05",
            "pace": "61:16/km",
            "hr_avg": 145,
            "hr_max": 182
          },
          {
            "lap": 3,
            "dist_m": 2107.6,
            "time_s": 456,
            "time_str": "7:36",
            "pace": "3:36/km",
            "hr_avg": 173,
            "hr_max": 188
          },
          {
            "lap": 4,
            "dist_m": 39.9,
            "time_s": 211,
            "time_str": "3:31",
            "pace": "88:11/km",
            "hr_avg": 139,
            "hr_max": 179
          },
          {
            "lap": 5,
            "dist_m": 2026.8,
            "time_s": 438,
            "time_str": "7:18",
            "pace": "3:35/km",
            "hr_avg": 168,
            "hr_max": 175
          },
          {
            "lap": 6,
            "dist_m": 37.2,
            "time_s": 30,
            "time_str": "0:30",
            "pace": "13:31/km",
            "hr_avg": 174,
            "hr_max": 175
          },
          {
            "lap": 1,
            "dist_m": 841.9,
            "time_s": 322,
            "time_str": "5:22",
            "pace": "6:22/km",
            "hr_avg": 157,
            "hr_max": 177
          },
          {
            "lap": 2,
            "dist_m": 990.0,
            "time_s": 333,
            "time_str": "5:33",
            "pace": "5:35/km",
            "hr_avg": 167,
            "hr_max": 176
          }
        ],
        "gym_sets": []
      },
      "2026-10-29": {
        "dots": [
          "gym"
        ],
        "title": "Fuerza Pierna 1",
        "type": "Gimnasio & Fuerza",
        "km": 0.0,
        "time": "49 min",
        "pace": "-",
        "hr": "104 ppm",
        "ai": "Sesión de sobrecarga progresiva y blindaje neuromuscular registrada en Garmin/Aegis.",
        "notes": "29/10/2026 - FUERZA PIERNA 1\n* SENTADILLA CON BARRA 4x6 @90kg costaba, podia hacer 1-2 más coml mucho en cada serie, piernas un poco cansadas de ayer yo creo)\n6x60kg\n6x90kg\n6x90kg\n6x90kg\n* PRENSA DE PIERNAS 45° 3x8 @90kg\n8x80kg\n8x90kg\n8x90kg\n* LEG EXTENSION EN MAQUINA 3X8 @66kg (alternando con leg curl)\n8x66kg\n8x66kg\n8x66kg\n* LEG CURL (femoral maquina tumbado) 3x80 @55kg (alternando con leg extension)\n8x50kg\n8x50kg\n8x50kg\n* GEMELO EN BARRA 3X10kg @90kg\n10x90kg\n10x90kg\n10x90kg",
        "laps": [],
        "gym_sets": [
          {
            "exercise": "i203757152",
            "set": "Fuerza Pierna 1",
            "reps": "SENTADILLA CON BARRA 4x6 @90kg costaba, podia hacer 1-2 más coml mucho en cada serie, piernas un poco cansadas de ayer yo creo)",
            "load": "6x60kg"
          },
          {
            "exercise": "i203757152",
            "set": "Fuerza Pierna 1",
            "reps": "SENTADILLA CON BARRA 4x6 @90kg costaba, podia hacer 1-2 más coml mucho en cada serie, piernas un poco cansadas de ayer yo creo)",
            "load": "6x90kg"
          },
          {
            "exercise": "i203757152",
            "set": "Fuerza Pierna 1",
            "reps": "SENTADILLA CON BARRA 4x6 @90kg costaba, podia hacer 1-2 más coml mucho en cada serie, piernas un poco cansadas de ayer yo creo)",
            "load": "6x90kg"
          },
          {
            "exercise": "i203757152",
            "set": "Fuerza Pierna 1",
            "reps": "SENTADILLA CON BARRA 4x6 @90kg costaba, podia hacer 1-2 más coml mucho en cada serie, piernas un poco cansadas de ayer yo creo)",
            "load": "6x90kg"
          },
          {
            "exercise": "i203757152",
            "set": "Fuerza Pierna 1",
            "reps": "PRENSA DE PIERNAS 45° 3x8 @90kg",
            "load": "8x80kg"
          },
          {
            "exercise": "i203757152",
            "set": "Fuerza Pierna 1",
            "reps": "PRENSA DE PIERNAS 45° 3x8 @90kg",
            "load": "8x90kg"
          },
          {
            "exercise": "i203757152",
            "set": "Fuerza Pierna 1",
            "reps": "PRENSA DE PIERNAS 45° 3x8 @90kg",
            "load": "8x90kg"
          },
          {
            "exercise": "i203757152",
            "set": "Fuerza Pierna 1",
            "reps": "LEG EXTENSION EN MAQUINA 3X8 @66kg (alternando con leg curl)",
            "load": "8x66kg"
          },
          {
            "exercise": "i203757152",
            "set": "Fuerza Pierna 1",
            "reps": "LEG EXTENSION EN MAQUINA 3X8 @66kg (alternando con leg curl)",
            "load": "8x66kg"
          },
          {
            "exercise": "i203757152",
            "set": "Fuerza Pierna 1",
            "reps": "LEG EXTENSION EN MAQUINA 3X8 @66kg (alternando con leg curl)",
            "load": "8x66kg"
          }
        ]
      },
      "2026-10-30": {
        "dots": [
          "gym"
        ],
        "title": "Fuerza Torso Tracción ",
        "type": "Gimnasio & Fuerza",
        "km": 0.0,
        "time": "32 min",
        "pace": "-",
        "hr": "92 ppm",
        "ai": "Sesión de sobrecarga progresiva y blindaje neuromuscular registrada en Garmin/Aegis.",
        "notes": "30/10/2026 - TORSO TRACCIÓN \nse me olvido las dominadas, y me confundí e hice flexiones \nNo hice rodaje, no me dió tiempo, fui tarde al gimnasio y al dia siguiente iba. hacer ruta de montaña dura\n* JALÓN AGARRE CERRADO V 4x6-8 @54kg\n8x45kg\n8x54kg\n8x54kg\n8x54kg\n* REMO DORIAN UNILATERAL 3x6-8 @35kg/brazo\n8x35kg/brazo\n8x35kg/brazo\n8x35kg/brazo\n* CURL BICEPS INCLINADO 45° 3x6-8 @10-12kg\n8x10kg\n8x10kg\n8x10kg\n* BÍCEPS EN MÁQUINA / SCOTT 2x8-10 @27kg\n8x27kg\n10x27kg\n* FLEXIONES @PESO PROPIO\n3x15",
        "laps": [],
        "gym_sets": [
          {
            "exercise": "i203757172",
            "set": "Fuerza Torso Tracción ",
            "reps": "JALÓN AGARRE CERRADO V 4x6-8 @54kg",
            "load": "8x45kg"
          },
          {
            "exercise": "i203757172",
            "set": "Fuerza Torso Tracción ",
            "reps": "JALÓN AGARRE CERRADO V 4x6-8 @54kg",
            "load": "8x54kg"
          },
          {
            "exercise": "i203757172",
            "set": "Fuerza Torso Tracción ",
            "reps": "JALÓN AGARRE CERRADO V 4x6-8 @54kg",
            "load": "8x54kg"
          },
          {
            "exercise": "i203757172",
            "set": "Fuerza Torso Tracción ",
            "reps": "JALÓN AGARRE CERRADO V 4x6-8 @54kg",
            "load": "8x54kg"
          },
          {
            "exercise": "i203757172",
            "set": "Fuerza Torso Tracción ",
            "reps": "REMO DORIAN UNILATERAL 3x6-8 @35kg/brazo",
            "load": "8x35kg/brazo"
          },
          {
            "exercise": "i203757172",
            "set": "Fuerza Torso Tracción ",
            "reps": "REMO DORIAN UNILATERAL 3x6-8 @35kg/brazo",
            "load": "8x35kg/brazo"
          },
          {
            "exercise": "i203757172",
            "set": "Fuerza Torso Tracción ",
            "reps": "REMO DORIAN UNILATERAL 3x6-8 @35kg/brazo",
            "load": "8x35kg/brazo"
          },
          {
            "exercise": "i203757172",
            "set": "Fuerza Torso Tracción ",
            "reps": "CURL BICEPS INCLINADO 45° 3x6-8 @10-12kg",
            "load": "8x10kg"
          },
          {
            "exercise": "i203757172",
            "set": "Fuerza Torso Tracción ",
            "reps": "CURL BICEPS INCLINADO 45° 3x6-8 @10-12kg",
            "load": "8x10kg"
          },
          {
            "exercise": "i203757172",
            "set": "Fuerza Torso Tracción ",
            "reps": "CURL BICEPS INCLINADO 45° 3x6-8 @10-12kg",
            "load": "8x10kg"
          }
        ]
      },
      "2026-10-31": {
        "dots": [
          "mountain"
        ],
        "title": "Pico Almanzor 2591M - Por la Laguna Grande y la Portilla del Crampón ",
        "type": "Outdoor / Senderismo",
        "km": 19.07,
        "time": "279 min",
        "pace": "-",
        "hr": "116 ppm",
        "ai": "Entrenamiento aeróbico en altitud (Pico Almanzor 2591M - Por la Laguna Grande y la Portilla del Crampón ): 19.07 km con aclimatación hipóxica.",
        "notes": "",
        "laps": [],
        "gym_sets": []
      }
    }
  },
  "2026-11": {
    "year": 2026,
    "month": 11,
    "month_name": "Noviembre 2026",
    "days_in_month": 30,
    "first_day_weekday": 6,
    "activities": {
      "2026-11-01": {
        "dots": [
          "run"
        ],
        "title": "Tirada 50' (35' Z2 + 15' ritmo competición + 5' Z1)",
        "type": "Running",
        "km": 11.74,
        "time": "53 min",
        "pace": "4:29/km",
        "hr": "159 ppm",
        "ai": "Sesión de 10.7 km a ritmo 4:29/km con FC media de 159 ppm.",
        "notes": "2 actividades porq tenía desactivado el autolap de 1km y paré la actividad en el 1er km para activarlo. \n35' un poco más rápido de lo previsto pero estaba motivado, descansé 2-3 mins aprox y continúe con los 15' rápidos intentando ir sobre 4:00 min/km, me fue costando, los últimos 500m fueron medio en cuesta y me costaron bastante. Controlado con laps el cambio de los 35' a los 15' y ñuego a los 5' finales (aunq fueron 3/4 solo y andar).",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1055.5,
            "time_s": 305,
            "time_str": "5:05",
            "pace": "4:48/km",
            "hr_avg": 109,
            "hr_max": 122
          },
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 283,
            "time_str": "4:43",
            "pace": "4:42/km",
            "hr_avg": 119,
            "hr_max": 123
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 275,
            "time_str": "4:35",
            "pace": "4:35/km",
            "hr_avg": 121,
            "hr_max": 124
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 267,
            "time_str": "4:27",
            "pace": "4:27/km",
            "hr_avg": 153,
            "hr_max": 170
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 276,
            "time_str": "4:36",
            "pace": "4:35/km",
            "hr_avg": 166,
            "hr_max": 172
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 277,
            "time_str": "4:37",
            "pace": "4:36/km",
            "hr_avg": 168,
            "hr_max": 174
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 274,
            "time_str": "4:34",
            "pace": "4:34/km",
            "hr_avg": 166,
            "hr_max": 172
          },
          {
            "lap": 7,
            "dist_m": 557.3,
            "time_s": 151,
            "time_str": "2:31",
            "pace": "4:30/km",
            "hr_avg": 166,
            "hr_max": 174
          },
          {
            "lap": 8,
            "dist_m": 1000.0,
            "time_s": 243,
            "time_str": "4:03",
            "pace": "4:03/km",
            "hr_avg": 158,
            "hr_max": 177
          },
          {
            "lap": 9,
            "dist_m": 1000.0,
            "time_s": 244,
            "time_str": "4:04",
            "pace": "4:03/km",
            "hr_avg": 175,
            "hr_max": 181
          },
          {
            "lap": 10,
            "dist_m": 1000.0,
            "time_s": 247,
            "time_str": "4:07",
            "pace": "4:06/km",
            "hr_avg": 173,
            "hr_max": 181
          },
          {
            "lap": 11,
            "dist_m": 630.0,
            "time_s": 166,
            "time_str": "2:46",
            "pace": "4:23/km",
            "hr_avg": 179,
            "hr_max": 182
          },
          {
            "lap": 12,
            "dist_m": 493.4,
            "time_s": 185,
            "time_str": "3:05",
            "pace": "6:15/km",
            "hr_avg": 174,
            "hr_max": 180
          }
        ],
        "gym_sets": []
      },
      "2026-11-04": {
        "dots": [
          "run"
        ],
        "title": "Calentamiento",
        "type": "Running",
        "km": 7.52,
        "time": "38 min",
        "pace": "4:54/km",
        "hr": "140 ppm",
        "ai": "Sesión de 3.0 km a ritmo 4:54/km con FC media de 140 ppm.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 286,
            "time_str": "4:46",
            "pace": "4:46/km",
            "hr_avg": 132,
            "hr_max": 144
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 299,
            "time_str": "4:59",
            "pace": "4:59/km",
            "hr_avg": 147,
            "hr_max": 163
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 302,
            "time_str": "5:02",
            "pace": "5:02/km",
            "hr_avg": 150,
            "hr_max": 157
          },
          {
            "lap": 4,
            "dist_m": 23.3,
            "time_s": 10,
            "time_str": "0:10",
            "pace": "6:50/km",
            "hr_avg": 155,
            "hr_max": 157
          },
          {
            "lap": 1,
            "dist_m": 495.0,
            "time_s": 117,
            "time_str": "1:57",
            "pace": "3:57/km",
            "hr_avg": 146,
            "hr_max": 160
          },
          {
            "lap": 2,
            "dist_m": 217.9,
            "time_s": 121,
            "time_str": "2:01",
            "pace": "9:15/km",
            "hr_avg": 152,
            "hr_max": 157
          },
          {
            "lap": 3,
            "dist_m": 489.5,
            "time_s": 120,
            "time_str": "2:00",
            "pace": "4:06/km",
            "hr_avg": 156,
            "hr_max": 159
          },
          {
            "lap": 4,
            "dist_m": 232.5,
            "time_s": 121,
            "time_str": "2:01",
            "pace": "8:38/km",
            "hr_avg": 157,
            "hr_max": 160
          },
          {
            "lap": 5,
            "dist_m": 495.1,
            "time_s": 119,
            "time_str": "1:59",
            "pace": "4:00/km",
            "hr_avg": 160,
            "hr_max": 165
          },
          {
            "lap": 6,
            "dist_m": 225.8,
            "time_s": 120,
            "time_str": "2:00",
            "pace": "8:53/km",
            "hr_avg": 156,
            "hr_max": 165
          },
          {
            "lap": 7,
            "dist_m": 498.1,
            "time_s": 119,
            "time_str": "1:59",
            "pace": "3:58/km",
            "hr_avg": 156,
            "hr_max": 162
          },
          {
            "lap": 8,
            "dist_m": 20.1,
            "time_s": 7,
            "time_str": "0:07",
            "pace": "5:49/km",
            "hr_avg": 159,
            "hr_max": 159
          },
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 354,
            "time_str": "5:54",
            "pace": "5:53/km",
            "hr_avg": 161,
            "hr_max": 173
          },
          {
            "lap": 2,
            "dist_m": 827.3,
            "time_s": 280,
            "time_str": "4:40",
            "pace": "5:38/km",
            "hr_avg": 165,
            "hr_max": 173
          }
        ],
        "gym_sets": []
      },
      "2026-11-07": {
        "dots": [
          "run"
        ],
        "title": "Calentamiento",
        "type": "Running",
        "km": 4.13,
        "time": "26 min",
        "pace": "6:08/km",
        "hr": "137 ppm",
        "ai": "Sesión de 2.2 km a ritmo 6:08/km con FC media de 137 ppm.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 369,
            "time_str": "6:09",
            "pace": "6:08/km",
            "hr_avg": 134,
            "hr_max": 140
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 372,
            "time_str": "6:12",
            "pace": "6:11/km",
            "hr_avg": 142,
            "hr_max": 144
          },
          {
            "lap": 3,
            "dist_m": 166.8,
            "time_s": 63,
            "time_str": "1:03",
            "pace": "6:16/km",
            "hr_avg": 144,
            "hr_max": 144
          },
          {
            "lap": 1,
            "dist_m": 75.0,
            "time_s": 16,
            "time_str": "0:16",
            "pace": "3:30/km",
            "hr_avg": 98,
            "hr_max": 98
          },
          {
            "lap": 2,
            "dist_m": 169.3,
            "time_s": 106,
            "time_str": "1:46",
            "pace": "10:25/km",
            "hr_avg": 126,
            "hr_max": 138
          },
          {
            "lap": 3,
            "dist_m": 81.9,
            "time_s": 14,
            "time_str": "0:14",
            "pace": "2:56/km",
            "hr_avg": 118,
            "hr_max": 120
          },
          {
            "lap": 4,
            "dist_m": 172.2,
            "time_s": 120,
            "time_str": "2:00",
            "pace": "11:39/km",
            "hr_avg": 118,
            "hr_max": 127
          },
          {
            "lap": 5,
            "dist_m": 78.8,
            "time_s": 14,
            "time_str": "0:14",
            "pace": "2:57/km",
            "hr_avg": 101,
            "hr_max": 101
          },
          {
            "lap": 6,
            "dist_m": 179.0,
            "time_s": 120,
            "time_str": "2:00",
            "pace": "11:10/km",
            "hr_avg": 120,
            "hr_max": 133
          },
          {
            "lap": 7,
            "dist_m": 79.5,
            "time_s": 14,
            "time_str": "0:14",
            "pace": "2:53/km",
            "hr_avg": 100,
            "hr_max": 100
          },
          {
            "lap": 8,
            "dist_m": 176.1,
            "time_s": 120,
            "time_str": "2:00",
            "pace": "11:23/km",
            "hr_avg": 112,
            "hr_max": 129
          },
          {
            "lap": 9,
            "dist_m": 89.4,
            "time_s": 13,
            "time_str": "0:13",
            "pace": "2:30/km",
            "hr_avg": 103,
            "hr_max": 103
          },
          {
            "lap": 10,
            "dist_m": 117.7,
            "time_s": 121,
            "time_str": "2:01",
            "pace": "17:07/km",
            "hr_avg": 116,
            "hr_max": 129
          },
          {
            "lap": 11,
            "dist_m": 196.2,
            "time_s": 41,
            "time_str": "0:41",
            "pace": "3:28/km",
            "hr_avg": 99,
            "hr_max": 120
          }
        ],
        "gym_sets": []
      },
      "2026-11-08": {
        "dots": [
          "run",
          "gym"
        ],
        "title": "10k Ávila Monumental",
        "type": "Running + Gym",
        "km": 9.96,
        "time": "186 min",
        "pace": "3:51/km",
        "hr": "175 ppm",
        "ai": "HITO HISTÓRICO: 10K Ávila Monumental oficial en 38:26 (3:50/km) a 1.070m de altitud con viento y desniveles duros.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 224,
            "time_str": "3:44",
            "pace": "3:43/km",
            "hr_avg": 148,
            "hr_max": 160
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 226,
            "time_str": "3:46",
            "pace": "3:45/km",
            "hr_avg": 159,
            "hr_max": 183
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 237,
            "time_str": "3:57",
            "pace": "3:57/km",
            "hr_avg": 178,
            "hr_max": 182
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 237,
            "time_str": "3:57",
            "pace": "3:56/km",
            "hr_avg": 181,
            "hr_max": 184
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 236,
            "time_str": "3:56",
            "pace": "3:56/km",
            "hr_avg": 182,
            "hr_max": 189
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 231,
            "time_str": "3:51",
            "pace": "3:51/km",
            "hr_avg": 182,
            "hr_max": 186
          },
          {
            "lap": 7,
            "dist_m": 1000.0,
            "time_s": 234,
            "time_str": "3:54",
            "pace": "3:53/km",
            "hr_avg": 184,
            "hr_max": 187
          },
          {
            "lap": 8,
            "dist_m": 1000.0,
            "time_s": 228,
            "time_str": "3:48",
            "pace": "3:48/km",
            "hr_avg": 185,
            "hr_max": 187
          },
          {
            "lap": 9,
            "dist_m": 1000.0,
            "time_s": 235,
            "time_str": "3:55",
            "pace": "3:55/km",
            "hr_avg": 185,
            "hr_max": 188
          },
          {
            "lap": 10,
            "dist_m": 955.0,
            "time_s": 219,
            "time_str": "3:39",
            "pace": "3:49/km",
            "hr_avg": 183,
            "hr_max": 190
          }
        ],
        "gym_sets": [
          {
            "exercise": "i207583883",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS BANCA PLANO MAQUINA 4x6",
            "load": "8x30kg/lado"
          },
          {
            "exercise": "i207583883",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS BANCA PLANO MAQUINA 4x6",
            "load": "8x35kg/lado"
          },
          {
            "exercise": "i207583883",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS BANCA PLANO MAQUINA 4x6",
            "load": "6x40kg/lado"
          },
          {
            "exercise": "i207583883",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS BANCA PLANO MAQUINA 4x6",
            "load": "6x40kg/lado"
          },
          {
            "exercise": "i207583883",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS INCLINADO MANCUERNA 3x8",
            "load": "8x14kg"
          },
          {
            "exercise": "i207583883",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS INCLINADO MANCUERNA 3x8",
            "load": "8x14kg"
          },
          {
            "exercise": "i207583883",
            "set": "Fuerza Torso Empuje",
            "reps": "PRESS INCLINADO MANCUERNA 3x8",
            "load": "7x16kg"
          },
          {
            "exercise": "i207583883",
            "set": "Fuerza Torso Empuje",
            "reps": "PEC DEC / APERTURAS 3x8-10",
            "load": "8x59kg"
          },
          {
            "exercise": "i207583883",
            "set": "Fuerza Torso Empuje",
            "reps": "PEC DEC / APERTURAS 3x8-10",
            "load": "8x59kg"
          },
          {
            "exercise": "i207583883",
            "set": "Fuerza Torso Empuje",
            "reps": "PEC DEC / APERTURAS 3x8-10",
            "load": "8x59kg"
          }
        ]
      },
      "2026-11-10": {
        "dots": [
          "run"
        ],
        "title": "30' Z2-Z1",
        "type": "Running",
        "km": 5.6,
        "time": "28 min",
        "pace": "5:07/km",
        "hr": "150 ppm",
        "ai": "Sesión de 5.6 km a ritmo 5:07/km con FC media de 150 ppm.",
        "notes": "",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 307,
            "time_str": "5:07",
            "pace": "5:07/km",
            "hr_avg": 130,
            "hr_max": 138
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 310,
            "time_str": "5:10",
            "pace": "5:10/km",
            "hr_avg": 129,
            "hr_max": 138
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 296,
            "time_str": "4:56",
            "pace": "4:56/km",
            "hr_avg": 149,
            "hr_max": 172
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 311,
            "time_str": "5:11",
            "pace": "5:11/km",
            "hr_avg": 170,
            "hr_max": 176
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 313,
            "time_str": "5:13",
            "pace": "5:12/km",
            "hr_avg": 168,
            "hr_max": 173
          },
          {
            "lap": 6,
            "dist_m": 596.8,
            "time_s": 189,
            "time_str": "3:09",
            "pace": "5:16/km",
            "hr_avg": 174,
            "hr_max": 179
          }
        ],
        "gym_sets": []
      },
      "2026-11-11": {
        "dots": [
          "run",
          "gym"
        ],
        "title": "40' Z2",
        "type": "Running + Gym",
        "km": 8.13,
        "time": "110 min",
        "pace": "4:54/km",
        "hr": "164 ppm",
        "ai": "Sesión de 8.1 km a ritmo 4:54/km con FC media de 164 ppm.",
        "notes": "Me costó, me notaba cansado y lo hice por zonas con cuestas y medio chispeaba a veces",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 301,
            "time_str": "5:01",
            "pace": "5:00/km",
            "hr_avg": 149,
            "hr_max": 172
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 286,
            "time_str": "4:46",
            "pace": "4:45/km",
            "hr_avg": 159,
            "hr_max": 172
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 302,
            "time_str": "5:02",
            "pace": "5:02/km",
            "hr_avg": 173,
            "hr_max": 179
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 307,
            "time_str": "5:07",
            "pace": "5:06/km",
            "hr_avg": 170,
            "hr_max": 179
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 285,
            "time_str": "4:45",
            "pace": "4:44/km",
            "hr_avg": 169,
            "hr_max": 180
          },
          {
            "lap": 6,
            "dist_m": 1000.0,
            "time_s": 311,
            "time_str": "5:11",
            "pace": "5:10/km",
            "hr_avg": 171,
            "hr_max": 180
          },
          {
            "lap": 7,
            "dist_m": 1000.0,
            "time_s": 291,
            "time_str": "4:51",
            "pace": "4:50/km",
            "hr_avg": 166,
            "hr_max": 177
          },
          {
            "lap": 8,
            "dist_m": 1000.0,
            "time_s": 279,
            "time_str": "4:39",
            "pace": "4:39/km",
            "hr_avg": 166,
            "hr_max": 173
          },
          {
            "lap": 9,
            "dist_m": 128.2,
            "time_s": 39,
            "time_str": "0:39",
            "pace": "5:06/km",
            "hr_avg": 168,
            "hr_max": 170
          }
        ],
        "gym_sets": [
          {
            "exercise": "i209724501",
            "set": "Fuerza Torso Tracción ",
            "reps": "Jalón Agarre Cerrado V - 4x4-6",
            "load": "10x32kg"
          },
          {
            "exercise": "i209724501",
            "set": "Fuerza Torso Tracción ",
            "reps": "Jalón Agarre Cerrado V - 4x4-6",
            "load": "6x50kg"
          },
          {
            "exercise": "i209724501",
            "set": "Fuerza Torso Tracción ",
            "reps": "Jalón Agarre Cerrado V - 4x4-6",
            "load": "6x59kg"
          },
          {
            "exercise": "i209724501",
            "set": "Fuerza Torso Tracción ",
            "reps": "Jalón Agarre Cerrado V - 4x4-6",
            "load": "6x59kg"
          },
          {
            "exercise": "i209724501",
            "set": "Fuerza Torso Tracción ",
            "reps": "Remo Gironda Amplio - 3x8-10",
            "load": "10x36kg"
          },
          {
            "exercise": "i209724501",
            "set": "Fuerza Torso Tracción ",
            "reps": "Remo Gironda Amplio - 3x8-10",
            "load": "10x36kg"
          },
          {
            "exercise": "i209724501",
            "set": "Fuerza Torso Tracción ",
            "reps": "Remo Gironda Amplio - 3x8-10",
            "load": "8x36kg"
          },
          {
            "exercise": "i209724501",
            "set": "Fuerza Torso Tracción ",
            "reps": "Remo Dorian Unilateral - 3x6-8",
            "load": "8x30kg"
          },
          {
            "exercise": "i209724501",
            "set": "Fuerza Torso Tracción ",
            "reps": "Remo Dorian Unilateral - 3x6-8",
            "load": "8x30kg"
          },
          {
            "exercise": "i209724501",
            "set": "Fuerza Torso Tracción ",
            "reps": "Remo Dorian Unilateral - 3x6-8",
            "load": "8x30kg"
          }
        ]
      },
      "2026-11-12": {
        "dots": [
          "gym"
        ],
        "title": "Fuerza Pierna 2",
        "type": "Gimnasio & Fuerza",
        "km": 0.0,
        "time": "537 min",
        "pace": "-",
        "hr": "61 ppm",
        "ai": "Sesión de sobrecarga progresiva y blindaje neuromuscular registrada en Garmin/Aegis.",
        "notes": "Ignorar el tiempo de la actividad, se me olvidó parar el reloj \n\nPIERNA 2 \n* Peso Muerto Rumano Unilateral / Staggered  4x6-8 @28kg (empecé con este 4 series, la primera de calentamiento, el hip trust estaba ocupado) \n10x22kg\n8x28kg\n8x28kg\n8x28kg\n* Hip Thrust con Barra (Maquina) - 3x6 @140-160\n8x160kg\n8x160kg\n8x180kg\n* Prensa Pies Altos y Anchos: 3 series x 6-8 reps @ +40-45 kg/lado\n8x50kg/lado (100kg)\n6x60kg/lado (120kg)\n6x60kg/lado (120kg)\n* Sóleo Sentado en Máquina: 3 series x 8-10 reps @ 35 - 40 kg (pausa 2s abajo)\n8x40kg\n8x40kg\n8x40kg",
        "laps": [],
        "gym_sets": [
          {
            "exercise": "i209724990",
            "set": "Fuerza Pierna 2",
            "reps": "Peso Muerto Rumano Unilateral / Staggered  4x6-8 @28kg (empecé con este 4 series, la primera de calentamiento, el hip trust estaba ocupado)",
            "load": "10x22kg"
          },
          {
            "exercise": "i209724990",
            "set": "Fuerza Pierna 2",
            "reps": "Peso Muerto Rumano Unilateral / Staggered  4x6-8 @28kg (empecé con este 4 series, la primera de calentamiento, el hip trust estaba ocupado)",
            "load": "8x28kg"
          },
          {
            "exercise": "i209724990",
            "set": "Fuerza Pierna 2",
            "reps": "Peso Muerto Rumano Unilateral / Staggered  4x6-8 @28kg (empecé con este 4 series, la primera de calentamiento, el hip trust estaba ocupado)",
            "load": "8x28kg"
          },
          {
            "exercise": "i209724990",
            "set": "Fuerza Pierna 2",
            "reps": "Peso Muerto Rumano Unilateral / Staggered  4x6-8 @28kg (empecé con este 4 series, la primera de calentamiento, el hip trust estaba ocupado)",
            "load": "8x28kg"
          },
          {
            "exercise": "i209724990",
            "set": "Fuerza Pierna 2",
            "reps": "Hip Thrust con Barra (Maquina) - 3x6 @140-160",
            "load": "8x160kg"
          },
          {
            "exercise": "i209724990",
            "set": "Fuerza Pierna 2",
            "reps": "Hip Thrust con Barra (Maquina) - 3x6 @140-160",
            "load": "8x160kg"
          },
          {
            "exercise": "i209724990",
            "set": "Fuerza Pierna 2",
            "reps": "Hip Thrust con Barra (Maquina) - 3x6 @140-160",
            "load": "8x180kg"
          },
          {
            "exercise": "i209724990",
            "set": "Fuerza Pierna 2",
            "reps": "Prensa Pies Altos y Anchos: 3 series x 6-8 reps @ +40-45 kg/lado",
            "load": "8x50kg/lado (100kg)"
          },
          {
            "exercise": "i209724990",
            "set": "Fuerza Pierna 2",
            "reps": "Prensa Pies Altos y Anchos: 3 series x 6-8 reps @ +40-45 kg/lado",
            "load": "6x60kg/lado (120kg)"
          },
          {
            "exercise": "i209724990",
            "set": "Fuerza Pierna 2",
            "reps": "Prensa Pies Altos y Anchos: 3 series x 6-8 reps @ +40-45 kg/lado",
            "load": "6x60kg/lado (120kg)"
          }
        ]
      },
      "2026-11-13": {
        "dots": [
          "run",
          "gym"
        ],
        "title": "30' Z1 - Z2",
        "type": "Running + Gym",
        "km": 5.21,
        "time": "98 min",
        "pace": "5:45/km",
        "hr": "144 ppm",
        "ai": "Sesión de 5.2 km a ritmo 5:45/km con FC media de 144 ppm.",
        "notes": "Rodaje en cinta, ignorar estadísticas de ritmo\nCorrí 30 minutos a 5:00 min/km",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 361,
            "time_str": "6:01",
            "pace": "6:01/km",
            "hr_avg": 120,
            "hr_max": 133
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 349,
            "time_str": "5:49",
            "pace": "5:49/km",
            "hr_avg": 142,
            "hr_max": 154
          },
          {
            "lap": 3,
            "dist_m": 1000.0,
            "time_s": 332,
            "time_str": "5:32",
            "pace": "5:32/km",
            "hr_avg": 154,
            "hr_max": 161
          },
          {
            "lap": 4,
            "dist_m": 1000.0,
            "time_s": 345,
            "time_str": "5:45",
            "pace": "5:44/km",
            "hr_avg": 155,
            "hr_max": 163
          },
          {
            "lap": 5,
            "dist_m": 1000.0,
            "time_s": 345,
            "time_str": "5:45",
            "pace": "5:45/km",
            "hr_avg": 159,
            "hr_max": 165
          },
          {
            "lap": 6,
            "dist_m": 206.1,
            "time_s": 71,
            "time_str": "1:11",
            "pace": "5:45/km",
            "hr_avg": 162,
            "hr_max": 166
          }
        ],
        "gym_sets": [
          {
            "exercise": "i209725118",
            "set": "Fuerza Torso Empuje",
            "reps": "Tríceps Polea con Cuerda 3x10",
            "load": "10x5kg"
          },
          {
            "exercise": "i209725118",
            "set": "Fuerza Torso Empuje",
            "reps": "Tríceps Polea con Cuerda 3x10",
            "load": "10x5kg"
          },
          {
            "exercise": "i209725118",
            "set": "Fuerza Torso Empuje",
            "reps": "Tríceps Polea con Cuerda 3x10",
            "load": "10x5kg"
          },
          {
            "exercise": "i209725118",
            "set": "Fuerza Torso Empuje",
            "reps": "Pec Deck / Aperturas 3x8",
            "load": "8x59kg"
          },
          {
            "exercise": "i209725118",
            "set": "Fuerza Torso Empuje",
            "reps": "Pec Deck / Aperturas 3x8",
            "load": "7x66kg"
          },
          {
            "exercise": "i209725118",
            "set": "Fuerza Torso Empuje",
            "reps": "Pec Deck / Aperturas 3x8",
            "load": "8x66kg"
          },
          {
            "exercise": "i209725118",
            "set": "Fuerza Torso Empuje",
            "reps": "Press de Banca Plano Maquina 3x4-6",
            "load": "8x30kg/lado"
          },
          {
            "exercise": "i209725118",
            "set": "Fuerza Torso Empuje",
            "reps": "Press de Banca Plano Maquina 3x4-6",
            "load": "8x30kg/lado"
          },
          {
            "exercise": "i209725118",
            "set": "Fuerza Torso Empuje",
            "reps": "Press de Banca Plano Maquina 3x4-6",
            "load": "8x30kg/lado"
          },
          {
            "exercise": "i209725118",
            "set": "Fuerza Torso Empuje",
            "reps": "Press Inclinado con Mancuernas (30°) 3x6-8",
            "load": "8x14kg"
          }
        ]
      },
      "2026-11-14": {
        "dots": [
          "run"
        ],
        "title": "6x800m cross 90\" rec",
        "type": "Running",
        "km": 8.05,
        "time": "37 min",
        "pace": "4:28/km",
        "hr": "157 ppm",
        "ai": "Series de 6x800m cross con clavos de 6mm en terreno mojado. Parciales exactos de vueltas Garmin: 2:53, 2:56, 2:55, 3:05, 3:10, 3:01 (recuperación clavada a 90s).",
        "notes": "Bien pero me costó mucho los ritmos, tenía las piernas bastante cansadas de isquios de fuerza del jueves principalmente, había ñlovido y estaba lloviendo, terreno complicado con muchos giros, cesped mojado, zonas de barro y zonas de arena. \nCorrí las 2 primeras con zapatillas las asics novablast 5, luego me puse los clavos en la tercera serie aunque descansé un poco más pero no calcule bien las vueltas y luego daba unos giros muy malos y metiendome por cesped alto mojado y con hoyos. En todo caso intenté esforzarme bastante auqne no saliese al ritmo ideal pero las condiciones no eras nada favorables, si hubiera sido en pista puede q si pudiese haber heccjo algo mejor.",
        "laps": [
          {
            "lap": 1,
            "dist_m": 1000.0,
            "time_s": 330,
            "time_str": "5:30",
            "pace": "5:29/km",
            "hr_avg": 131,
            "hr_max": 138
          },
          {
            "lap": 2,
            "dist_m": 1000.0,
            "time_s": 301,
            "time_str": "5:01",
            "pace": "5:01/km",
            "hr_avg": 139,
            "hr_max": 152
          },
          {
            "lap": 3,
            "dist_m": 862.2,
            "time_s": 253,
            "time_str": "4:13",
            "pace": "4:53/km",
            "hr_avg": 146,
            "hr_max": 153
          },
          {
            "lap": 1,
            "dist_m": 800.0,
            "time_s": 173,
            "time_str": "2:53",
            "pace": "3:36/km",
            "hr_avg": 154,
            "hr_max": 172
          },
          {
            "lap": 2,
            "dist_m": 112.9,
            "time_s": 90,
            "time_str": "1:30",
            "pace": "13:16/km",
            "hr_avg": 151,
            "hr_max": 160
          },
          {
            "lap": 3,
            "dist_m": 800.0,
            "time_s": 176,
            "time_str": "2:56",
            "pace": "3:39/km",
            "hr_avg": 163,
            "hr_max": 180
          },
          {
            "lap": 4,
            "dist_m": 81.9,
            "time_s": 90,
            "time_str": "1:30",
            "pace": "18:18/km",
            "hr_avg": 152,
            "hr_max": 169
          },
          {
            "lap": 5,
            "dist_m": 800.0,
            "time_s": 175,
            "time_str": "2:55",
            "pace": "3:38/km",
            "hr_avg": 161,
            "hr_max": 174
          },
          {
            "lap": 6,
            "dist_m": 60.9,
            "time_s": 90,
            "time_str": "1:30",
            "pace": "24:37/km",
            "hr_avg": 150,
            "hr_max": 163
          },
          {
            "lap": 7,
            "dist_m": 800.0,
            "time_s": 185,
            "time_str": "3:05",
            "pace": "3:51/km",
            "hr_avg": 159,
            "hr_max": 168
          },
          {
            "lap": 8,
            "dist_m": 31.5,
            "time_s": 90,
            "time_str": "1:30",
            "pace": "47:37/km",
            "hr_avg": 151,
            "hr_max": 172
          },
          {
            "lap": 9,
            "dist_m": 800.0,
            "time_s": 190,
            "time_str": "3:10",
            "pace": "3:57/km",
            "hr_avg": 163,
            "hr_max": 177
          },
          {
            "lap": 10,
            "dist_m": 71.4,
            "time_s": 90,
            "time_str": "1:30",
            "pace": "20:59/km",
            "hr_avg": 161,
            "hr_max": 178
          },
          {
            "lap": 11,
            "dist_m": 800.0,
            "time_s": 181,
            "time_str": "3:01",
            "pace": "3:46/km",
            "hr_avg": 158,
            "hr_max": 168
          }
        ],
        "gym_sets": []
      },
      "2026-11-15": {
        "dots": [
          "gym"
        ],
        "title": "Fuerza Pierna 1",
        "type": "Gimnasio & Fuerza",
        "km": 0.0,
        "time": "83 min",
        "pace": "-",
        "hr": "82 ppm",
        "ai": "Sesión de sobrecarga progresiva y blindaje neuromuscular registrada en Garmin/Aegis.",
        "notes": "* Leg extension máquina \n8x66kg\n8x66kg\n8x66kg\n8x66kg\n* Sentadilla con barra libre\n8x60kg\n8x80kg\n8x80kg\n* Elevaciones de gemelo con barra\n10x80kg\n10x80kg\n10x80kg\n* Leg press\n8x80kg\n8x80kg\n8x80kg\n* Rueda abdominal \n8\n8",
        "laps": [],
        "gym_sets": [
          {
            "exercise": "i210504152",
            "set": "Fuerza Pierna 1",
            "reps": "Leg extension máquina",
            "load": "8x66kg"
          },
          {
            "exercise": "i210504152",
            "set": "Fuerza Pierna 1",
            "reps": "Leg extension máquina",
            "load": "8x66kg"
          },
          {
            "exercise": "i210504152",
            "set": "Fuerza Pierna 1",
            "reps": "Leg extension máquina",
            "load": "8x66kg"
          },
          {
            "exercise": "i210504152",
            "set": "Fuerza Pierna 1",
            "reps": "Leg extension máquina",
            "load": "8x66kg"
          },
          {
            "exercise": "i210504152",
            "set": "Fuerza Pierna 1",
            "reps": "Sentadilla con barra libre",
            "load": "8x60kg"
          },
          {
            "exercise": "i210504152",
            "set": "Fuerza Pierna 1",
            "reps": "Sentadilla con barra libre",
            "load": "8x80kg"
          },
          {
            "exercise": "i210504152",
            "set": "Fuerza Pierna 1",
            "reps": "Sentadilla con barra libre",
            "load": "8x80kg"
          },
          {
            "exercise": "i210504152",
            "set": "Fuerza Pierna 1",
            "reps": "Elevaciones de gemelo con barra",
            "load": "10x80kg"
          },
          {
            "exercise": "i210504152",
            "set": "Fuerza Pierna 1",
            "reps": "Elevaciones de gemelo con barra",
            "load": "10x80kg"
          },
          {
            "exercise": "i210504152",
            "set": "Fuerza Pierna 1",
            "reps": "Elevaciones de gemelo con barra",
            "load": "10x80kg"
          }
        ]
      },
      "2026-11-16": {
        "dots": [
          "run",
          "gym"
        ],
        "title": "Rodaje de Drenaje & Soltura Post-Fin de Semana",
        "type": "Running + Gym",
        "km": 7.0,
        "time": "35 min",
        "pace": "4:55 - 5:10/km",
        "hr": "Z1 (<145 ppm)",
        "ai": "35 min continuos suaves en asfalto/tierra plana. Oxigenar piernas sin impacto articular duro tras el paintball y la fiesta. Rutina 2 · Torso Tracción & Densidad (Pág 2 PDF)",
        "notes": "Calzado recomendado: Asics Novablast 5",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-17": {
        "dots": [
          "gym"
        ],
        "title": "Rutina 4 · Torso Empuje en Ávila (Noche - 35 min)",
        "type": "Gimnasio",
        "km": 0.0,
        "time": "-",
        "pace": "N/A",
        "hr": "Reposo",
        "ai": "Día laboral en Madrid. Llegada a Ávila sobre las 19:30-20:00. Cero carrera para absorber el viaje y llegar fresco al VO2max del miércoles. Rutina 4 · Torso Empuje en Ávila (Noche - 35 min)",
        "notes": "Calzado recomendado: Calzado casual cómodo",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-18": {
        "dots": [
          "run"
        ],
        "title": "SESIÓN CLAVE PRE-MILÁN: 4 x 1.000m @ 3:30-3:32/km",
        "type": "RunningDescanso",
        "km": 9.5,
        "time": "50 min",
        "pace": "3:30 - 3:32 por 1.000m (Recuperación: 2' estático o trote)",
        "hr": "Z4 / Z5 (174 - 186 ppm)",
        "ai": "4 x 1.000m en pista de atletismo o asfalto llano y limpio. Objetivo: clavar el ritmo objetivo en suelo firme sin derrapes de barro. Recuperación: 2 min para permitir aclaramiento parcial de lactato. Descanso de Fuerza (Máxima Asimilación de VO2max)",
        "notes": "Calzado recomendado: Nike Streakfly 2",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-19": {
        "dots": [
          "run",
          "gym"
        ],
        "title": "Rodaje Suave Pre-Viaje (30') + 4 Progresiones",
        "type": "Running + Gym",
        "km": 6.0,
        "time": "30 min",
        "pace": "5:00 - 5:15/km (Rectas sueltas)",
        "hr": "Z1 (<140 ppm)",
        "ai": "30 min muy fáciles para soltar piernas antes del viaje + 4 rectas de 80m sueltas sin fatiga. Rutina 3 · Pierna 2 Controlada (Pág 3 PDF - 40 min)",
        "notes": "Calzado recomendado: Asics Novablast 5",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-20": {
        "dots": [
          "mountain"
        ],
        "title": "Descanso / Asimilación",
        "type": "Descanso",
        "km": 0.0,
        "time": "-",
        "pace": "N/A",
        "hr": "Reposo",
        "ai": "Vuelo y llegada a Milán. Cero impacto de carrera. Disfrutar del viaje y caminar. Descanso de Fuerza (Viaje)",
        "notes": "Calzado recomendado: Calzado casual cómodo",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-21": {
        "dots": [
          "mountain"
        ],
        "title": "Descanso / Asimilación",
        "type": "Descanso",
        "km": 0.0,
        "time": "-",
        "pace": "N/A",
        "hr": "Caminata Z1 (<100 ppm)",
        "ai": "Caminar 15.000 - 20.000 pasos. Excelente estímulo de capilarización y flujo sanguíneo sin impacto lesivo. Descanso Gimnasio",
        "notes": "Calzado recomendado: Calzado cómodo de caminar",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-22": {
        "dots": [
          "mountain"
        ],
        "title": "Descanso / Asimilación",
        "type": "Descanso",
        "km": 0.0,
        "time": "-",
        "pace": "N/A",
        "hr": "Caminata Z1",
        "ai": "Turismo activo a pie por Milán. Mantener la movilidad de tobillos y gemelos. Descanso Gimnasio",
        "notes": "Calzado recomendado: Calzado cómodo de caminar",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-23": {
        "dots": [
          "mountain"
        ],
        "title": "Descanso / Asimilación",
        "type": "Descanso",
        "km": 0.0,
        "time": "-",
        "pace": "N/A",
        "hr": "Reposo",
        "ai": "Vuelo y regreso de Milán. Descanso para disipar la fatiga de las caminatas y recuperar el sueño. Descanso Gimnasio (Asimilación Viaje)",
        "notes": "Calzado recomendado: Calzado casual cómodo",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-24": {
        "dots": [
          "run",
          "gym"
        ],
        "title": "Rodaje de Reactivación Post-Milán (30-35') + 4 Rectas",
        "type": "Running + Gym",
        "km": 6.5,
        "time": "35 min",
        "pace": "5:05 - 5:15/km",
        "hr": "Z1 (<142 ppm)",
        "ai": "30 min de trote regenerativo en tierra/asfalto plano + 4 rectas progresivas suaves de 80m en hierba para reconectar los receptores propioceptivos del pie. Rutina 2 · Torso Tracción Express Mantenimiento (25 min)",
        "notes": "Calzado recomendado: Asics Novablast 5",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-25": {
        "dots": [
          "run"
        ],
        "title": "AFINAMIENTO CLAVE PRE-CROSS: 3 x 500m @ Ritmo Cross",
        "type": "RunningDescanso",
        "km": 6.5,
        "time": "40 min",
        "pace": "1:45 - 1:47 por 500m (3:30 - 3:35/km) | Rec: 2'30\" amplia",
        "hr": "Z4 / Ritmo Competición (sin fatiga residual)",
        "ai": "3 x 500m clavando exactamente el ritmo de salida del cross (1:45-1:47). Recuperación amplia (2'30\" caminando y trote muy lento). Cero fatiga glucolítica: buscamos reclutamiento de fibras rápidas y confianza mecánica sin acumular lactato. Descanso de Fuerza (Enfoque en Competición)",
        "notes": "Calzado recomendado: Zapatillas de clavos de cross (o Nike Streakfly 2)",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-26": {
        "dots": [
          "mountain"
        ],
        "title": "Descanso / Asimilación",
        "type": "Descanso",
        "km": 0.0,
        "time": "-",
        "pace": "N/A",
        "hr": "Reposo",
        "ai": "Cero impacto. Nutrición limpia con carbohidratos complejos (arroz, patata cocida, avena, pasta) + hidratación abundante con sales. Descanso Absoluto de Fuerza",
        "notes": "Calzado recomendado: Calzado casual cómodo",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-27": {
        "dots": [
          "run"
        ],
        "title": "Activación Pre-Cross (15') + 4 Progresiones Vivas",
        "type": "RunningDescanso",
        "km": 4.0,
        "time": "25 min",
        "pace": "5:10/km trote + 4 rectas a ritmo de salida",
        "hr": "Z1 (<135 ppm)",
        "ai": "15 min muy suaves en hierba + 4 aceleraciones vivas de 60-80m con clavos puestos para chequear agarre del terreno y reactividad muscular. Descanso de Gimnasio",
        "notes": "Calzado recomendado: Clavos de cross (New Balance o Nike)",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-28": {
        "dots": [
          "run"
        ],
        "title": "¡DÍA D! CROSS POPULAR PARQUE DEL SOTO (5.000m)",
        "type": "RunningDescanso",
        "km": 8.5,
        "time": "60 min",
        "pace": "Km 1 @ 3:40/km -> Km 2-4 @ 3:35/km -> Km 5 @ sub 3:30/km",
        "hr": "Z5 / VO2max de Competición",
        "ai": "5.000m oficiales en el circuito del Parque del Soto. Táctica: no suicidarse en los primeros 1.000m (3:40-3:42). Imponer ritmo de crucero en las zonas de curva y tierra (3:35). Desatar el cambio de mediofondista en el último km (sub 3:30/km). Objetivo de marca: 17:55 - 18:15. Descanso de Fuerza (¡Celebración de Carrera!)",
        "notes": "Calzado recomendado: Zapatillas de clavos (6mm seco / 9mm húmedo o barro)",
        "laps": [],
        "gym_sets": []
      },
      "2026-11-29": {
        "dots": [
          "run"
        ],
        "title": "Rodaje Regenerativo de Descarga Post-Cross",
        "type": "RunningDescanso",
        "km": 6.5,
        "time": "35 min",
        "pace": "5:15 - 5:30/km",
        "hr": "Z1 (<138 ppm)",
        "ai": "30-35 min de trote muy regenerativo en asfalto plano para barrer metabolitos y descargar la fascia. Si hay dolor o sobrecarga en sóleos por los clavos, sustituir por paseo suave. Descanso Gimnasio (Foam Roller y Movilidad)",
        "notes": "Calzado recomendado: Asics Novablast 5",
        "laps": [],
        "gym_sets": []
      }
    }
  },
  "2026-12": {
    "year": 2026,
    "month": 12,
    "month_name": "Diciembre 2026",
    "days_in_month": 31,
    "first_day_weekday": 1,
    "activities": {
      "2026-12-31": {
        "dots": [
          "run"
        ],
        "title": "SAN SILVESTRE 2026 (6.5 KM)",
        "type": "COMPETICIÓN",
        "km": 6.5,
        "time": "Sub 23:15 obj",
        "pace": "Sub 3:35/km",
        "hr": "Z5 Máxima",
        "ai": "OBJETIVO SECUNDARIO: Asfalto urbano a ritmo de 3:34/km para despedir el año con marca personal.",
        "notes": "Objetivo de cierre de año en pico de forma tras el Cross del Soto.",
        "laps": [],
        "gym_sets": []
      }
    }
  }
};

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);

    // Service Worker Offline PWA (/sw.js)
    if (url.pathname === "/sw.js" && request.method === "GET") {
      const swCode = `// Aegis Coach — Service Worker PWA v6
const CACHE_NAME = 'aegis-coach-v8';
const PRECACHE_ASSETS = [
  '/',
  '/manifest.json',
  '/favicon.ico',
  '/css/app.css?v=20261116c',
  '/img/logo.svg',
  '/img/icon-192.png?v=20261116b',
  '/img/icon-512.png?v=20261116b',
  '/img/apple-touch-icon.png?v=20261116b'
];

self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return Promise.allSettled(
        PRECACHE_ASSETS.map((url) => {
          return fetch(url, { cache: 'no-cache' }).then((response) => {
            if (response && response.status === 200) {
              return cache.put(url, response);
            }
          }).catch((err) => {
            console.warn('Precache skip: ' + url, err);
          });
        })
      );
    })
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('Purging old cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const requestUrl = new URL(req.url);

  // CRITICAL: Bypass Service Worker for ALL cross-origin requests (CDNs, fonts, third-party APIs).
  // Browser native HTTP stack handles CDN caching cleanly without opaque ERR_FAILED bugs.
  if (requestUrl.origin !== location.origin) {
    return;
  }

  // Bypass cache for API and Webhook requests
  if (requestUrl.pathname.startsWith('/api/') || requestUrl.pathname.startsWith('/webhook')) {
    return;
  }

  // Network-First for HTML navigation documents so updates apply immediately
  if (req.mode === 'navigate' || req.destination === 'document' || requestUrl.pathname === '/') {
    event.respondWith(
      fetch(req)
        .then((networkResponse) => {
          if (networkResponse && (networkResponse.status === 200 || networkResponse.type === 'opaque')) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
          }
          return networkResponse;
        })
        .catch(() => caches.match(req))
    );
    return;
  }

  // Same-origin static assets: Stale-While-Revalidate
  event.respondWith(
    caches.match(req).then((cachedResponse) => {
      const fetchPromise = fetch(req)
        .then((networkResponse) => {
          if (networkResponse && (networkResponse.status === 200 || networkResponse.type === 'opaque')) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, clone));
          }
          return networkResponse;
        })
        .catch(() => cachedResponse);

      return cachedResponse || fetchPromise;
    })
  );
});
`;
      return new Response(swCode, {
        headers: {
          "Content-Type": "application/javascript; charset=utf-8",
          "Cache-Control": "no-cache",
          ...SECURITY_HEADERS
        }
      });
    }

    // Hoja de Estilos Tailwind Precompilada desde KV (Self-Contained & Inmune a bloqueos)
    if (url.pathname === "/css/app.css") {
      try {
        const cssData = await env.AEGIS_KV.get("css_app");
        if (cssData) {
          return new Response(cssData, {
            headers: {
              "Content-Type": "text/css; charset=utf-8",
              "Cache-Control": "public, max-age=31536000, immutable"
            }
          });
        }
      } catch (e) {
        console.error("Error leyendo css_app de KV:", e);
      }
      return new Response("/* CSS no disponible */", {
        headers: { "Content-Type": "text/css" },
        status: 404
      });
    }

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
        orientation: "portrait-primary",
        icons: [
          {
            src: "/img/icon-192.png?v=20261116b",
            sizes: "192x192",
            type: "image/png",
            purpose: "any"
          },
          {
            src: "/img/icon-512.png?v=20261116b",
            sizes: "512x512",
            type: "image/png",
            purpose: "any"
          },
          {
            src: "/img/icon-192.png?v=20261116b",
            sizes: "192x192",
            type: "image/png",
            purpose: "maskable"
          },
          {
            src: "/img/icon-512.png?v=20261116b",
            sizes: "512x512",
            type: "image/png",
            purpose: "maskable"
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

    // Favicon PNG oficial en raíz
    if (url.pathname === "/favicon.png" || url.pathname === "/favicon-64.png") {
      try {
        const pngData = await env.AEGIS_KV.get("img_favicon_png", { type: "arrayBuffer" });
        if (pngData) {
          return new Response(pngData, {
            headers: {
              "Content-Type": "image/png",
              "Cache-Control": "no-cache, no-store, must-revalidate"
            }
          });
        }
      } catch (e) {}
    }

    // Apple Touch Icon oficial en raíz (iOS Safari / PWA shortcuts)
    if (url.pathname === "/apple-touch-icon.png" || url.pathname === "/apple-touch-icon-precomposed.png") {
      try {
        const appleData = await env.AEGIS_KV.get("img_apple-touch-icon", { type: "arrayBuffer" });
        if (appleData) {
          return new Response(appleData, {
            headers: {
              "Content-Type": "image/png",
              "Cache-Control": "no-cache, no-store, must-revalidate"
            }
          });
        }
      } catch (e) {}
    }

    // Logo Aero-Aegis SVG con no-cache
    if (url.pathname === "/img/logo.svg") {
      return new Response(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">
  <defs>
    <linearGradient id="fav_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c5abde"/>
      <stop offset="50%" stop-color="#a887ce"/>
      <stop offset="100%" stop-color="#70559f"/>
    </linearGradient>
    <linearGradient id="fav_coral" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e885a6"/>
      <stop offset="50%" stop-color="#d86991"/>
      <stop offset="100%" stop-color="#9c526d"/>
    </linearGradient>
    <linearGradient id="fav_core" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#d86991"/>
      <stop offset="100%" stop-color="#a887ce"/>
    </linearGradient>
    <linearGradient id="fav_wing" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#d86991"/>
    </linearGradient>
  </defs>
  <path d="M 50 14 C 38 12, 22 18, 16 32 C 11 48, 16 68, 32 82 C 40 88, 47 92, 50 93 C 44 86, 28 76, 25 61 C 22 47, 28 34, 40 26 C 44 23, 48 18, 50 14 Z" fill="url(#fav_blue)"/>
  <path d="M 50 14 C 62 12, 78 18, 84 32 C 89 48, 84 68, 68 82 C 60 88, 53 92, 50 93 C 56 86, 72 76, 75 61 C 78 47, 72 34, 60 26 C 56 23, 52 18, 50 14 Z" fill="url(#fav_coral)"/>
  <path d="M 50 26 C 52 26, 61 46, 65 62 C 66 66, 62 68, 57 67 C 54 62, 53 56, 50 56 C 47 56, 46 62, 43 67 C 38 68, 34 66, 35 62 C 39 46, 48 26, 50 26 Z" fill="url(#fav_core)"/>
  <path d="M 22 57 C 35 53, 65 53, 78 57 C 68 61, 32 61, 22 57 Z" fill="url(#fav_wing)"/>
</svg>`, {
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
      } else if (cleanPath.startsWith("apple-touch-icon")) {
        key = "img_apple-touch-icon";
        contentType = "image/png";
      } else if (cleanPath.startsWith("favicon")) {
        key = cleanPath.includes("32") ? "img_favicon_32" : "img_favicon_png";
        contentType = "image/png";
      } else {
        key = "img_" + cleanPath.replace(".jpg", "").replace(".png", "");
        contentType = cleanPath.endsWith(".png") ? "image/png" : "image/jpeg";
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
      if (!isAuthorized(request, env)) {
        return new Response(JSON.stringify({ error: "Unauthorized" }), {
          status: 401,
          headers: { "Content-Type": "application/json", ...SECURITY_HEADERS }
        });
      }
      try {
        const body: any = await request.json();
        const date = body.date || getTodayMadridISO();
        const key = "gym_session_" + date;
        await env.AEGIS_KV.put(key, JSON.stringify(body));
        return new Response(JSON.stringify({ ok: true, key }), {
          headers: { "Content-Type": "application/json", ...SECURITY_HEADERS }
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { "Content-Type": "application/json", ...SECURITY_HEADERS } });
      }
    }

    // Endpoint: Guardar Perfil de Usuario (Peso, Altura, etc.)
    if (url.pathname === "/api/save_profile" && request.method === "POST") {
      if (!isAuthorized(request, env)) {
        return new Response(JSON.stringify({ error: "Unauthorized" }), {
          status: 401,
          headers: { "Content-Type": "application/json", ...SECURITY_HEADERS }
        });
      }
      try {
        const body: any = await request.json();
        await env.AEGIS_KV.put("user_profile", JSON.stringify(body));
        return new Response(JSON.stringify({ ok: true }), {
          headers: { "Content-Type": "application/json", ...SECURITY_HEADERS }
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message }), { status: 500, headers: { "Content-Type": "application/json", ...SECURITY_HEADERS } });
      }
    }

    // Endpoint: Obtener Sesión de Gimnasio
    if (url.pathname === "/api/get_gym_session" && request.method === "GET") {
      if (!isAuthorized(request, env)) {
        return new Response(JSON.stringify({ error: "Unauthorized" }), {
          status: 401,
          headers: { "Content-Type": "application/json", ...SECURITY_HEADERS }
        });
      }
      try {
        const date = url.searchParams.get("date") || getTodayMadridISO();
        const session = await env.AEGIS_KV.get("gym_session_" + date, { type: "json" });
        return new Response(JSON.stringify(session || null), {
          headers: {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            ...SECURITY_HEADERS
          }
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message }), {
          status: 500,
          headers: { "Content-Type": "application/json", ...SECURITY_HEADERS }
        });
      }
    }

    // Endpoint: Obtener Perfil de Usuario
    if (url.pathname === "/api/get_profile" && request.method === "GET") {
      if (!isAuthorized(request, env)) {
        return new Response(JSON.stringify({ error: "Unauthorized" }), {
          status: 401,
          headers: { "Content-Type": "application/json", ...SECURITY_HEADERS }
        });
      }
      try {
        const profile = await env.AEGIS_KV.get("user_profile", { type: "json" });
        return new Response(JSON.stringify(profile || null), {
          headers: {
            "Content-Type": "application/json",
            "Cache-Control": "no-cache, no-store, must-revalidate",
            ...SECURITY_HEADERS
          }
        });
      } catch (err: any) {
        return new Response(JSON.stringify({ error: err.message }), {
          status: 500,
          headers: { "Content-Type": "application/json", ...SECURITY_HEADERS }
        });
      }
    }

    // Webhook de Telegram
    if (url.pathname === "/webhook" && request.method === "POST") {
      const expectedWebhookSecret = env.TELEGRAM_WEBHOOK_SECRET || "aegis_tg_webhook_secret_2026";
      const secretHeader = request.headers.get("X-Telegram-Bot-Api-Secret-Token");
      if (secretHeader !== expectedWebhookSecret) {
        return new Response(JSON.stringify({ error: "Unauthorized" }), {
          status: 401,
          headers: { "Content-Type": "application/json", ...SECURITY_HEADERS }
        });
      }
      try {
        const update: any = await request.json();
        if (update && update.message) {
          await handleTelegramMessage(update.message, env);
        }
        return new Response("OK", { status: 200, headers: SECURITY_HEADERS });
      } catch (err: any) {
        return new Response("Error", { status: 500, headers: SECURITY_HEADERS });
      }
    }

    // Cargar plan desde KV o fallback maestro
    let planData: any = null;
    try {
      planData = await env.AEGIS_KV.get("current_plan", { type: "json" });
    } catch (e) {}
    if (!planData) planData = DEFAULT_PLAN;

    const html = getLuxuryDashboardHtml(planData, env);
    return new Response(html, {
      headers: {
        "Content-Type": "text/html; charset=utf-8",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        ...SECURITY_HEADERS
      }
    });
  },

  async scheduled(controller: ScheduledController, env: Env, ctx: ExecutionContext): Promise<void> {
    ctx.waitUntil(checkNewActivities(env));
  }
};

async function handleTelegramMessage(message: any, env: Env) {
  const chatId = String(message?.chat?.id || "");
  if (env.TELEGRAM_CHAT_ID && chatId !== String(env.TELEGRAM_CHAT_ID)) {
    console.warn("Rejected unauthorized Telegram message from chat_id:", chatId);
    return;
  }
  const text = (message?.text || "").trim();
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
    reply = "👋 *Aegis Coach Bot*\n\nComandos disponibles:\n• `/hoy` - Entrenamiento programado para el día actual.\n• `/semana` - Resumen del microciclo completo.\n• `/rodilla` - Estado de salud y prevención articular.\n• `/web` - Abrir la Web App Dashboard.";
  } else if (text === "/hoy") {
    const r = todayPlan.running;
    const g = todayPlan.gym;
    reply = `🏃 *ENTRENAMIENTO DE HOY* (${todayPlan.day_name} ${todayPlan.date}):\n\n` +
      `• *Running:* ${r.is_rest ? "Descanso" : `${r.title} (${r.duration_min} min, ${r.target_distance_km} km @ ${r.target_pace}, ${r.hr_zone})`}\n` +
      `• *Fuerza:* ${g.is_rest ? "Descanso" : `${g.routine_name} (${g.focus})`}\n\n` +
      `🌐 [Ver Dashboard y Series](https://aegis-intervals-sync.uranuslabs.workers.dev)`;
  } else if (text === "/semana") {
    reply = `📅 *PLAN SEMANAL EN CURSO* (Semana del ${days[0]?.date || ""}):\n\n` +
      days.map((d: any) => `• *${d.day_name.substring(0, 3)} ${d.date.substring(5)}:* ${d.running.is_rest ? "Descanso run" : d.running.session_type} | ${d.gym.is_rest ? "Descanso gym" : d.gym.routine_name.split("·")[0]}`).join("\n") +
      `\n\n🌐 [Abrir Web App](https://aegis-intervals-sync.uranuslabs.workers.dev)`;
  } else if (text === "/rodilla") {
    reply = "🛡️ *BLINDAJE ARTICULAR & ISQUIOS*\n\n• *Rodilla Izquierda:* 0/10 Dolor (Derrame reactivo totalmente reabsorbido).\n• *Isquiotibial MTJ:* 0/10 Dolor. Asintomático y blindado con Hip Thrust y RDL unilateral.";
  } else if (text === "/web") {
    reply = "🌐 Accede a tu Web App Dashboard aquí:\nhttps://aegis-intervals-sync.uranuslabs.workers.dev";
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

export async function checkNewActivities(env: Env) {
  try {
    const athleteId = env.ATHLETE_ID || "i690671";
    const apiKey = env.INTERVALS_API_KEY;
    if (!apiKey) {
      console.warn("No INTERVALS_API_KEY configured for scheduled check");
      return { error: "Missing INTERVALS_API_KEY" };
    }
    const authHeader = "Basic " + btoa("API_KEY:" + apiKey);

    const now = new Date();
    const twoDaysAgo = new Date(now.getTime() - 2 * 24 * 60 * 60 * 1000);
    const oldest = twoDaysAgo.toISOString().split("T")[0];
    const newest = now.toISOString().split("T")[0];

    const url = `https://intervals.icu/api/v1/athlete/${athleteId}/activities?oldest=${oldest}&newest=${newest}`;

    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 15000);

    const res = await fetch(url, {
      headers: { Authorization: authHeader },
      signal: controller.signal
    });
    clearTimeout(timeoutId);

    if (!res.ok) {
      console.error(`Intervals.icu returned status ${res.status}`);
      return { error: `Intervals.icu returned status ${res.status}` };
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
        const alreadySent = await env.AEGIS_KV.get(`notified_${actId}`);
        if (alreadySent) continue;
      }

      if (env.TELEGRAM_BOT_TOKEN && env.TELEGRAM_CHAT_ID) {
        const msg = `🏃 *[NUEVA SESIÓN EN GARMIN / INTERVALS]*\n\n` +
          `• *Atleta:* Carlos Jiménez Andrino\n` +
          `• *Fecha:* ${dateStr.replace("T", " ")}\n` +
          `• *Sesión:* ${name} (${type})\n` +
          (distKm !== "0.00" ? `• *Distancia:* ${distKm} km\n` : "") +
          `• *Duración:* ${timeMin} min\n` +
          (avgHr !== "-" ? `• *FC Media:* ${avgHr} ppm (Máx: ${maxHr})\n` : "") +
          `• *Carga (Load):* ${load}\n\n` +
          `👉 *Escribe /hoy o abre:* https://aegis-intervals-sync.uranuslabs.workers.dev`;

        const telegramUrl = `https://api.telegram.org/bot${env.TELEGRAM_BOT_TOKEN}/sendMessage`;
        await fetch(telegramUrl, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            chat_id: env.TELEGRAM_CHAT_ID,
            text: msg,
            parse_mode: "Markdown"
          })
        });

        if (env.AEGIS_KV) {
          await env.AEGIS_KV.put(`notified_${actId}`, "1", { expirationTtl: 30 * 24 * 60 * 60 });
        }
      }

      notified.push({ id: actId, name, type, distKm, timeMin, load });
    }

    return { success: true, total_activities: activities.length, newly_notified: notified.length, notified };
  } catch (err: any) {
    console.error("Error in checkNewActivities:", err);
    return { error: err.message };
  }
}

function getLuxuryDashboardHtml(planData: any, env?: Env): string {
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
  <link rel="manifest" href="/manifest.json?v=20261116b">
  <link rel="icon" type="image/png" sizes="64x64" href="/img/favicon-64.png?v=20261116b">
  <link rel="icon" type="image/png" sizes="32x32" href="/img/favicon-32.png?v=20261116b">
  <link rel="apple-touch-icon" sizes="180x180" href="/img/apple-touch-icon.png?v=20261116b">
  <link rel="shortcut icon" href="/favicon.ico?v=20261116b">
  <meta name="theme-color" content="#171821">
  <meta name="apple-mobile-web-app-capable" content="yes">
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
  <meta name="apple-mobile-web-app-title" content="Aegis Coach">
  
  <!-- Tipografía: Plus Jakarta Sans & JetBrains Mono -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
  
  <!-- Hoja de Estilos Propia Compilada (Carga Inmediata y Offline) -->
  <link rel="stylesheet" href="/css/app.css?v=20261116c">
  
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>

  <style>
    /* ================================================================= */
    /* CRITICAL FALLBACK CSS (Defensa Estricta Anti-Fallo CDN / Brave)   */
    /* ================================================================= */
    *, ::before, ::after { box-sizing: border-box; }
    .hidden { display: none !important; }
    @media (min-width: 1024px) {
      .hidden.lg\:flex { display: flex !important; }
      .lg\:flex { display: flex !important; }
      .lg\:block { display: block !important; }
      aside#desktop-sidebar { display: flex !important; }
    }
    aside#desktop-sidebar {
      display: none !important;
    }
    @media (min-width: 1024px) {
      aside#desktop-sidebar {
        display: flex !important;
        width: 6rem !important;
        position: fixed !important;
        top: 0 !important;
        bottom: 0 !important;
        left: 0 !important;
        z-index: 30 !important;
      }
    }
    /* Limites estrictos para SVG: NUNCA pueden superar su contenedor */
    svg {
      max-width: 100%;
      height: auto;
    }
    .logo-container-aside {
      width: 48px !important;
      height: 48px !important;
      max-width: 48px !important;
      max-height: 48px !important;
      min-width: 48px !important;
      min-height: 48px !important;
      overflow: hidden !important;
    }
    .logo-container-aside svg {
      width: 48px !important;
      height: 48px !important;
      max-width: 48px !important;
      max-height: 48px !important;
    }
    .logo-container-topbar {
      width: 32px !important;
      height: 32px !important;
      max-width: 32px !important;
      max-height: 32px !important;
      min-width: 32px !important;
      min-height: 32px !important;
      overflow: hidden !important;
    }
    .logo-container-topbar svg {
      width: 32px !important;
      height: 32px !important;
      max-width: 32px !important;
      max-height: 32px !important;
    }
    @media (min-width: 640px) {
      .logo-container-topbar {
        width: 44px !important;
        height: 44px !important;
        max-width: 44px !important;
        max-height: 44px !important;
      }
      .logo-container-topbar svg {
        width: 44px !important;
        height: 44px !important;
      }
    }
    .logo-container-profile {
      width: 56px !important;
      height: 56px !important;
      max-width: 56px !important;
      max-height: 56px !important;
      min-width: 56px !important;
      min-height: 56px !important;
      overflow: hidden !important;
    }
    .logo-container-profile svg {
      width: 56px !important;
      height: 56px !important;
    }
  
    :root {
      /* Paleta Oficial Octet Interactive Dashboards */
      --river-styx: #171821;        /* Fondo base */
      --jaguar: #292631;            /* Superficie de tarjetas */
      --stone-violet: #4d3e50;      /* Bordes y divisores */
      --composers-magic: #C4B9C8;   /* Texto secundario / muteado */
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
  



    /* ================================================================= */
    /* CRITICAL FALLBACK CSS (Defensa Estricta Anti-Fallo CDN / Brave)   */
    /* ================================================================= */
    *, ::before, ::after { box-sizing: border-box; }
    .hidden { display: none !important; }
    @media (min-width: 1024px) {
      .hidden.lg\:flex { display: flex !important; }
      .lg\:flex { display: flex !important; }
      .lg\:block { display: block !important; }
      aside#desktop-sidebar { display: flex !important; }
    }
    aside#desktop-sidebar {
      display: none !important;
    }
    @media (min-width: 1024px) {
      aside#desktop-sidebar {
        display: flex !important;
        width: 6rem !important;
        position: fixed !important;
        top: 0 !important;
        bottom: 0 !important;
        left: 0 !important;
        z-index: 30 !important;
      }
    }
    /* Limites estrictos para SVG: NUNCA pueden superar su contenedor */
    svg {
      max-width: 100%;
      height: auto;
    }
    .logo-container-aside {
      width: 48px !important;
      height: 48px !important;
      max-width: 48px !important;
      max-height: 48px !important;
      min-width: 48px !important;
      min-height: 48px !important;
      overflow: hidden !important;
    }
    .logo-container-aside svg {
      width: 48px !important;
      height: 48px !important;
      max-width: 48px !important;
      max-height: 48px !important;
    }
    .logo-container-topbar {
      width: 32px !important;
      height: 32px !important;
      max-width: 32px !important;
      max-height: 32px !important;
      min-width: 32px !important;
      min-height: 32px !important;
      overflow: hidden !important;
    }
    .logo-container-topbar svg {
      width: 32px !important;
      height: 32px !important;
      max-width: 32px !important;
      max-height: 32px !important;
    }
    @media (min-width: 640px) {
      .logo-container-topbar {
        width: 44px !important;
        height: 44px !important;
        max-width: 44px !important;
        max-height: 44px !important;
      }
      .logo-container-topbar svg {
        width: 44px !important;
        height: 44px !important;
      }
    }
    .logo-container-profile {
      width: 56px !important;
      height: 56px !important;
      max-width: 56px !important;
      max-height: 56px !important;
      min-width: 56px !important;
      min-height: 56px !important;
      overflow: hidden !important;
    }
    .logo-container-profile svg {
      width: 56px !important;
      height: 56px !important;
    }

    :root {
      /* Paleta Oficial Octet Interactive Dashboards */
      --river-styx: #171821;        /* Fondo base */
      --jaguar: #292631;            /* Superficie de tarjetas */
      --stone-violet: #4d3e50;      /* Bordes y divisores */
      --composers-magic: #C4B9C8;   /* Texto secundario / muteado */
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
    <aside id="desktop-sidebar" style="display: none;" class="hidden lg:flex w-24 flex-col items-center py-6 border-r border-[#4d3e50] bg-[#171821] fixed top-0 bottom-0 left-0 z-30">
      <!-- Monograma Logo SVG -->
      <div onclick="switchTab('dashboard')" class="logo-container-aside w-12 h-12 rounded-2xl flex items-center justify-center cursor-pointer transition hover:scale-105 mb-8" style="width: 48px; height: 48px; max-width: 48px; max-height: 48px;">
        <svg width="48" height="48" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">
  <defs>
    <linearGradient id="aside_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c5abde"/>
      <stop offset="50%" stop-color="#a887ce"/>
      <stop offset="100%" stop-color="#70559f"/>
    </linearGradient>
    <linearGradient id="aside_coral" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e885a6"/>
      <stop offset="50%" stop-color="#d86991"/>
      <stop offset="100%" stop-color="#9c526d"/>
    </linearGradient>
    <linearGradient id="aside_core" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#d86991"/>
      <stop offset="100%" stop-color="#a887ce"/>
    </linearGradient>
    <linearGradient id="aside_wing" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#d86991"/>
    </linearGradient>
  </defs>
  <path d="M 50 14 C 38 12, 22 18, 16 32 C 11 48, 16 68, 32 82 C 40 88, 47 92, 50 93 C 44 86, 28 76, 25 61 C 22 47, 28 34, 40 26 C 44 23, 48 18, 50 14 Z" fill="url(#aside_blue)"/>
  <path d="M 50 14 C 62 12, 78 18, 84 32 C 89 48, 84 68, 68 82 C 60 88, 53 92, 50 93 C 56 86, 72 76, 75 61 C 78 47, 72 34, 60 26 C 56 23, 52 18, 50 14 Z" fill="url(#aside_coral)"/>
  <path d="M 50 26 C 52 26, 61 46, 65 62 C 66 66, 62 68, 57 67 C 54 62, 53 56, 50 56 C 47 56, 46 62, 43 67 C 38 68, 34 66, 35 62 C 39 46, 48 26, 50 26 Z" fill="url(#aside_core)"/>
  <path d="M 22 57 C 35 53, 65 53, 78 57 C 68 61, 32 61, 22 57 Z" fill="url(#aside_wing)"/>
</svg>
      </div>

      <!-- Iconos de Navegación Vertical -->
      <div class="flex flex-col gap-6 items-center flex-1">
        <button onclick="switchTab('dashboard')" id="nav-desktop-dashboard" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#d86991] active-nav-link transition hover:text-white" title="Dashboard">
          <i data-lucide="layout-grid" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('workouts')" id="nav-desktop-workouts" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#C4B9C8] transition hover:text-white" title="Entrenos & Calendario">
          <i data-lucide="calendar" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('gym')" id="nav-desktop-gym" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#C4B9C8] transition hover:text-white" title="Gimnasio & Series">
          <i data-lucide="dumbbell" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('goals')" id="nav-desktop-goals" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#C4B9C8] transition hover:text-white" title="Objetivos">
          <i data-lucide="target" class="w-5 h-5"></i>
        </button>
        <button onclick="switchTab('profile')" id="nav-desktop-profile" class="w-12 h-12 rounded-2xl flex items-center justify-center text-[#C4B9C8] transition hover:text-white" title="Perfil & IMC">
          <i data-lucide="user" class="w-5 h-5"></i>
        </button>
      </div>

      <!-- Botón Telegram en Sidebar -->
      <a href="https://t.me/aegis_coach_chatbot" target="_blank" class="w-11 h-11 rounded-2xl bg-[#292631] border border-[#4d3e50] text-[#a887ce] flex items-center justify-center hover:border-[#a887ce] transition" title="Bot de Telegram">
        <i data-lucide="send" class="w-4 h-4"></i>
      </a>
    </aside>

    <!-- CONTENEDOR CENTRAL -->
    <main class="flex-1 lg:pl-24 lg:pb-12 flex flex-col min-w-0" style="padding-bottom: calc(7.5rem + env(safe-area-inset-bottom, 0px));">
      
      <!-- TOPBAR / HEADER LIMPIO (Compacto 52px en móvil, sin duplicidades) -->
      <header class="h-[52px] sm:h-16 border-b border-[#4d3e50] px-4 sm:px-8 flex items-center justify-between bg-[#171821]/90 backdrop-blur sticky top-0 z-20" style="padding-top: env(safe-area-inset-top, 0px);">
        <div class="flex items-center gap-3 sm:gap-4">
          <!-- Monograma Logo -->
          <div onclick="switchTab('dashboard')" class="logo-container-topbar w-8 h-8 sm:w-11 sm:h-11 rounded-2xl flex items-center justify-center cursor-pointer transition hover:scale-105 flex-shrink-0" style="width: 32px; height: 32px; max-width: 44px; max-height: 44px;">
            <svg width="32" height="32" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">
  <defs>
    <linearGradient id="hdr_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c5abde"/>
      <stop offset="50%" stop-color="#a887ce"/>
      <stop offset="100%" stop-color="#70559f"/>
    </linearGradient>
    <linearGradient id="hdr_coral" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e885a6"/>
      <stop offset="50%" stop-color="#d86991"/>
      <stop offset="100%" stop-color="#9c526d"/>
    </linearGradient>
    <linearGradient id="hdr_core" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#d86991"/>
      <stop offset="100%" stop-color="#a887ce"/>
    </linearGradient>
    <linearGradient id="hdr_wing" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#d86991"/>
    </linearGradient>
  </defs>
  <path d="M 50 14 C 38 12, 22 18, 16 32 C 11 48, 16 68, 32 82 C 40 88, 47 92, 50 93 C 44 86, 28 76, 25 61 C 22 47, 28 34, 40 26 C 44 23, 48 18, 50 14 Z" fill="url(#hdr_blue)"/>
  <path d="M 50 14 C 62 12, 78 18, 84 32 C 89 48, 84 68, 68 82 C 60 88, 53 92, 50 93 C 56 86, 72 76, 75 61 C 78 47, 72 34, 60 26 C 56 23, 52 18, 50 14 Z" fill="url(#hdr_coral)"/>
  <path d="M 50 26 C 52 26, 61 46, 65 62 C 66 66, 62 68, 57 67 C 54 62, 53 56, 50 56 C 47 56, 46 62, 43 67 C 38 68, 34 66, 35 62 C 39 46, 48 26, 50 26 Z" fill="url(#hdr_core)"/>
  <path d="M 22 57 C 35 53, 65 53, 78 57 C 68 61, 32 61, 22 57 Z" fill="url(#hdr_wing)"/>
</svg>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <span class="text-sm sm:text-lg font-black tracking-tight text-white">AEGIS COACH</span>
            </div>
            <p class="text-[10px] sm:text-xs text-[#C4B9C8] font-medium leading-none mt-0.5 hidden sm:block">
              Carlos Jiménez Andrino &bull; Fisiología & Rendimiento
            </p>
          </div>
        </div>

        <div class="hidden sm:flex items-center gap-2 sm:gap-3">
          <!-- Acceso Perfil Rápido -->
          <button onclick="switchTab('profile')" class="px-3 py-1.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-[#C4B9C8] hover:text-white hover:border-[#a887ce] text-xs font-bold transition flex items-center gap-1.5">
            <i data-lucide="user" class="w-3.5 h-3.5 text-[#a887ce]"></i>
            <span>Perfil & IMC</span>
          </button>
          
          <!-- Botón Telegram -->
          <a href="https://t.me/aegis_coach_chatbot" target="_blank" class="px-3.5 py-1.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-[#C4B9C8] hover:text-white hover:border-[#a887ce] text-xs font-bold transition flex items-center gap-1.5">
            <i data-lucide="send" class="w-3.5 h-3.5 text-[#a887ce]"></i>
            <span>Bot Telegram</span>
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
                  <span class="text-xs sm:text-sm font-semibold text-[#C4B9C8] tracking-tight">Volumen Semanal</span>
                  <i data-lucide="trending-up" class="w-4 h-4 text-[#7A7585]"></i>
                </div>
                <div class="flex items-baseline justify-between mt-3">
                  <div class="flex items-baseline gap-1.5">
                    <span id="kpi-run-km" class="text-3xl sm:text-4xl font-black text-white tracking-tight font-mono">27.0</span>
                    <span class="text-xs font-bold text-[#C4B9C8]">km</span>
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
                  <span class="text-xs sm:text-sm font-semibold text-[#C4B9C8] tracking-tight">Sesiones de Fuerza</span>
                  <i data-lucide="trending-up" class="w-4 h-4 text-[#7A7585]"></i>
                </div>
                <div class="flex items-baseline justify-between mt-3">
                  <div class="flex items-baseline gap-1.5">
                    <span id="kpi-gym-sessions" class="text-3xl sm:text-4xl font-black text-white tracking-tight font-mono">4</span>
                    <span class="text-xs font-bold text-[#C4B9C8]">/ 4 días</span>
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
                  <span class="text-xs sm:text-sm font-semibold text-[#C4B9C8] tracking-tight">Estado de Forma (TSB)</span>
                  <i data-lucide="trending-up" class="w-4 h-4 text-[#7A7585]"></i>
                </div>
                <div class="flex items-baseline justify-between mt-3">
                  <div class="flex items-baseline gap-1.5">
                    <span id="kpi-tsb-val" class="text-3xl sm:text-4xl font-black text-white tracking-tight font-mono">-9.5</span>
                    <span class="text-xs font-bold text-[#C4B9C8]">TSB</span>
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

          <!-- WIDGET TÁCTICO: CROSS DEL SOTO (OBJETIVO PRIMARIO) -->
          <div class="luxury-card p-4 sm:p-5 relative overflow-hidden bg-gradient-to-br from-[#292631]/90 via-[#1e1c24] to-[#171821] border border-[#fa769e]/30 shadow-lg mb-6">
            <div class="absolute -right-10 -bottom-10 w-36 h-36 bg-[#fa769e]/10 rounded-full blur-2xl pointer-events-none"></div>
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div class="space-y-1">
                <div class="flex items-center gap-2">
                  <span class="px-2.5 py-0.5 rounded-full text-[10px] font-extrabold bg-[#fa769e]/20 text-[#fa769e] border border-[#fa769e]/30 uppercase tracking-wider animate-pulse">
                    ⚡ T-${daysRemaining} DÍAS • OBJETIVO PRIMARIO
                  </span>
                  <span class="text-xs text-[#C4B9C8]">${primaryObj.date}</span>
                </div>
                <h3 class="text-base sm:text-lg font-black text-white tracking-tight">${primaryObj.name}</h3>
                <p class="text-xs text-[#C4B9C8]">
                  ${primaryObj.distance_km} km @ <strong>3:30 - 3:35/km</strong> (~17:30) &bull; ${primaryObj.surface}
                </p>
              </div>
              <div class="flex items-center gap-3 w-full sm:w-auto">
                <div class="flex-1 sm:flex-initial px-4 py-2 rounded-2xl bg-[#171821] border border-[#4d3e50] text-center">
                  <span class="text-[10px] uppercase font-bold text-[#C4B9C8] block">Cuenta Atrás</span>
                  <span class="text-xl font-black text-[#fa769e]">${daysRemaining} <span class="text-xs font-normal text-white">días</span></span>
                </div>
                <div class="flex-1 sm:flex-initial px-4 py-2 rounded-2xl bg-[#171821] border border-[#4d3e50] text-center">
                  <span class="text-[10px] uppercase font-bold text-[#C4B9C8] block">Calzado Clave</span>
                  <span class="text-xs font-bold text-[#9ca8f3]">Clavos 6-9 mm</span>
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
                <div class="px-3.5 py-1.5 rounded-xl bg-[#171821]/80 border border-white/10 text-xs font-semibold text-[#C4B9C8] flex items-center gap-1.5 shadow-sm">
                  <span>Últimas 4 semanas</span>
                  <i data-lucide="chevron-down" class="w-3.5 h-3.5 text-[#C4B9C8]"></i>
                </div>
              </div>
            </div>

            <!-- Canvas del Spline Chart -->
            <div class="h-64 sm:h-72 w-full relative">
              <canvas id="weeklySplineChart"></canvas>
            </div>

            <!-- Mini badges con las 4 semanas más recientes (Enfoque Táctico) -->
            <div class="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mt-4 text-center">
              <div class="p-2 rounded-xl bg-[#292631] border border-[#4d3e50]">
                <div class="text-[10px] text-[#C4B9C8] font-bold">26 Oct</div>
                <div class="text-xs font-bold text-white mt-0.5 font-mono">29.2k &bull; 3g</div>
              </div>
              <div class="p-2 rounded-xl bg-[#292631]/60 border border-[#a887ce]/30">
                <div class="text-[10px] text-[#a887ce] font-bold">10K Ávila (02 Nov)</div>
                <div class="text-xs font-black text-white mt-0.5 font-mono">21.6k &bull; 1g</div>
              </div>
              <div class="p-2 rounded-xl bg-[#292631]/40 border border-[#d86991]/30">
                <div class="text-[10px] text-[#d86991] font-bold">6x800m (09 Nov)</div>
                <div class="text-xs font-black text-white mt-0.5 font-mono">27.0k &bull; 4g</div>
              </div>
              <div class="p-2 rounded-xl bg-[#d86991]/10 border border-[#d86991]/50">
                <div class="text-[10px] text-[#fa769e] font-black">Esta Sem (16 Nov)</div>
                <div class="text-xs font-black text-[#fa769e] mt-0.5 font-mono">~30k &bull; 3g</div>
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
                <span class="text-[11px] text-[#C4B9C8]">Memoria Cuantitativa</span>
              </div>

              <div class="space-y-3">
                <div class="flex items-center justify-between p-3 rounded-2xl bg-[#292631] border border-[#4d3e50]">
                  <div class="flex items-center gap-3">
                    <div class="w-9 h-9 rounded-xl bg-[#d86991]/20 text-[#d86991] flex items-center justify-center">
                      <i data-lucide="trophy" class="w-4 h-4"></i>
                    </div>
                    <div>
                      <div class="text-xs font-bold text-white">10K Ávila Monumental</div>
                      <div class="text-[11px] text-[#C4B9C8]">08 Nov &bull; 1.070m altitud, viento y cuestas</div>
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
                      <div class="text-[11px] text-[#C4B9C8]">14 Nov &bull; Clavos 6mm en hierba/tierra &bull; rec 90"</div>
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
                      <div class="text-[11px] text-[#C4B9C8]">13 Nov &bull; Hip Thrust + RDL Unilateral</div>
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
                <span class="text-[11px] text-[#C4B9C8]">Cuenta Atrás</span>
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
                      <p class="text-xs text-[#C4B9C8]">5 km en tierra/hierba @ 3:30/km (~17:30) &bull; Clavos 6mm</p>
                    </div>
                    <div class="text-right pl-3">
                      <div class="text-2xl font-black text-[#d86991] font-mono leading-none">${daysRemaining}</div>
                      <div class="text-[10px] text-[#C4B9C8] mt-1 font-semibold">días</div>
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
                      <p class="text-xs text-[#C4B9C8]">6.5 km @ sub 3:35/km &bull; Asfalto &bull; Zapatilla voladora</p>
                    </div>
                    <div class="text-right pl-3">
                      <div class="text-2xl font-black text-white font-mono leading-none">45</div>
                      <div class="text-[10px] text-[#C4B9C8] mt-1 font-semibold">días</div>
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
            <button onclick="switchWorkoutSubView('microcycle')" id="subview-btn-microcycle" class="flex-1 py-2 px-3 rounded-xl text-xs font-bold transition flex items-center justify-center gap-2 text-[#C4B9C8] hover:text-white">
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
                  <div class="flex items-center gap-3 text-xs text-[#C4B9C8] mt-1">
                    <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#d86991]"></span> Carrera</span>
                    <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#a887ce]"></span> Gimnasio</span>
                    <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#20D994]"></span> Evento / Descanso</span>
                  </div>
                </div>

                <div class="flex items-center gap-2 bg-[#292631] border border-[#4d3e50] rounded-xl px-3 py-1.5 text-xs font-bold text-white self-start sm:self-auto">
                  <button id="cal-btn-prev" onclick="changeCalendarMonth(-1)" class="text-[#C4B9C8] hover:text-white transition px-1 cursor-pointer">&larr;</button>
                  <span id="calendar-month-label" class="min-w-[110px] text-center">Noviembre 2026</span>
                  <button id="cal-btn-next" onclick="changeCalendarMonth(1)" class="text-[#C4B9C8] hover:text-white transition px-1 cursor-pointer">&rarr;</button>
                </div>
              </div>

              <!-- Días de la semana -->
              <div class="grid grid-cols-7 gap-1 sm:gap-2 text-center text-[10px] font-bold text-[#C4B9C8] uppercase tracking-wider py-1">
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
                <span id="detail-type-badge" class="text-xs font-bold text-[#C4B9C8] font-mono">Sesión de Hoy</span>
              </div>

              <div class="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs font-mono pt-1">
                <div class="p-2.5 rounded-xl bg-[#171821] border border-[#4d3e50]">
                  <span class="text-[10px] text-[#C4B9C8] uppercase block">Distancia</span>
                  <strong id="detail-km" class="text-white text-sm">7.0 km</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-[#171821] border border-[#4d3e50]">
                  <span class="text-[10px] text-[#C4B9C8] uppercase block">Duración</span>
                  <strong id="detail-time" class="text-white text-sm">35:00</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-[#171821] border border-[#4d3e50]">
                  <span class="text-[10px] text-[#C4B9C8] uppercase block">Ritmo</span>
                  <strong id="detail-pace" class="text-[#d86991] text-sm">4:55-5:10/km</strong>
                </div>
                <div class="p-2.5 rounded-xl bg-[#171821] border border-[#4d3e50]">
                  <span class="text-[10px] text-[#C4B9C8] uppercase block">Zona / FC</span>
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
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4">
              <div>
                <span class="text-[10px] uppercase font-extrabold text-[#d86991] tracking-wider">
                  RUTINAS OFICIALES MAESTRAS (PDF PÁGS 1-4)
                </span>
                <h3 class="text-lg font-black text-white mt-0.5">Selecciona la Rutina de Gimnasio</h3>
                <p class="text-xs text-[#C4B9C8]">Sobrecarga progresiva: registra tus kilos y repeticiones serie a serie</p>
              </div>
              
              <!-- Controles de Descanso y Estado de Sincronización -->
              <div class="flex flex-wrap items-center gap-3">
                <span id="gym-sync-status" class="text-[10px] text-emerald-400 font-bold">🟢 Sincronizado en KV</span>
                <div class="flex items-center gap-1.5 bg-[#171821] border border-[#4d3e50] rounded-xl px-2.5 py-1">
                  <span class="text-[10px] text-[#C4B9C8] font-bold flex items-center gap-1">
                    <i data-lucide="timer" class="w-3.5 h-3.5 text-[#d86991]"></i> Descanso:
                  </span>
                  <button type="button" onclick="startRestTimer(90)" class="px-2.5 py-1 min-h-[44px] rounded-lg bg-[#292631] text-[#fa769e] text-xs font-bold hover:bg-[#fa769e]/20 transition active:scale-95 touch-manipulation">90s</button>
                  <button type="button" onclick="startRestTimer(120)" class="px-2.5 py-1 min-h-[44px] rounded-lg bg-[#292631] text-[#9ca8f3] text-xs font-bold hover:bg-[#9ca8f3]/20 transition active:scale-95 touch-manipulation">2m</button>
                </div>
              </div>
            </div>

            <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
              <button onclick="selectGymRoutine(1)" id="gym-chip-1" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#292631] border-[#4d3e50] text-[#C4B9C8] hover:border-[#d86991]">
                <span class="text-[10px] uppercase font-bold text-[#C4B9C8]">Lunes 18:00</span>
                <span class="text-xs font-extrabold text-white mt-1">Pierna 1</span>
                <span class="text-[10px] text-[#C4B9C8] mt-0.5">Cuádriceps, Gemelos & Core</span>
              </button>

              <button onclick="selectGymRoutine(2)" id="gym-chip-2" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#d86991] text-white border-[#d86991] font-semibold glow-pink">
                <span class="text-[10px] uppercase font-bold text-[#C4B9C8]">Miércoles 17:30</span>
                <span class="text-xs font-extrabold text-white mt-1">Torso Tracción (Hoy)</span>
                <span class="text-[10px] text-[#C4B9C8] mt-0.5">Espalda & Bíceps</span>
              </button>

              <button onclick="selectGymRoutine(3)" id="gym-chip-3" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#292631] border-[#4d3e50] text-[#C4B9C8] hover:border-[#d86991]">
                <span class="text-[10px] uppercase font-extrabold text-white/80">Jueves/Viernes</span>
                <span class="text-xs font-extrabold text-white mt-1">Pierna 2</span>
                <span class="text-[10px] text-white/80 mt-0.5">Glúteo, Femoral & Sóleo</span>
              </button>

              <button onclick="selectGymRoutine(4)" id="gym-chip-4" class="p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#292631] border-[#4d3e50] text-[#C4B9C8] hover:border-[#d86991]">
                <span class="text-[10px] uppercase font-bold text-[#C4B9C8]">Sábado 11:00</span>
                <span class="text-xs font-extrabold text-white mt-1">Torso Empuje</span>
                <span class="text-[10px] text-[#C4B9C8] mt-0.5">Pecho, Hombro & Tríceps</span>
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
                <p class="text-xs text-[#C4B9C8] mt-0.5">Generado en tiempo real con las repeticiones y kilos anotados hoy.</p>
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
                  <span class="text-xs font-mono font-bold text-[#C4B9C8]">${daysRemaining} días restantes</span>
                </div>
                <h3 class="text-xl font-black text-white mt-3">Cross Popular Parque del Soto (Ávila)</h3>
                <p class="text-xs text-[#C4B9C8] mt-1 leading-relaxed">5 km en terreno deformable (hierba y tierra). Exige máxima rigidez miotendinosa y clavos de 6mm para compensar las curvas sin peralte.</p>
              </div>

              <div class="grid grid-cols-3 gap-2 text-center pt-2 border-t border-[#4d3e50]">
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#C4B9C8]">Distancia</div>
                  <div class="text-sm font-extrabold text-white font-mono">5.0 km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#C4B9C8]">Ritmo Meta</div>
                  <div class="text-sm font-extrabold text-[#d86991] font-mono">3:30/km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#C4B9C8]">Tiempo Obj</div>
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
                  <span class="text-xs font-mono font-bold text-[#C4B9C8]">45 días restantes</span>
                </div>
                <h3 class="text-xl font-black text-white mt-3">San Silvestre</h3>
                <p class="text-xs text-[#C4B9C8] mt-1 leading-relaxed">6.5 km sobre asfalto urbano frío. Reactividad pura y zapatilla voladora con placa de carbono para exprimir el umbral submáximo.</p>
              </div>

              <div class="grid grid-cols-3 gap-2 text-center pt-2 border-t border-[#4d3e50]">
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#C4B9C8]">Distancia</div>
                  <div class="text-sm font-extrabold text-white font-mono">6.5 km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#C4B9C8]">Ritmo Meta</div>
                  <div class="text-sm font-extrabold text-[#a887ce] font-mono">sub 3:35/km</div>
                </div>
                <div class="p-2 rounded-xl bg-[#292631]">
                  <div class="text-[10px] text-[#C4B9C8]">Tiempo Obj</div>
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
                  <tr class="border-b border-[#4d3e50] text-[10px] text-[#C4B9C8] uppercase tracking-wider">
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
                    <td class="py-3 text-[#C4B9C8]">Glucólisis Rápida / Lactato</td>
                    <td class="py-3 text-white">Potencia Anaeróbica & Frecuencia</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">5K Cross (El Soto)</td>
                    <td class="py-3 text-[#d86991] font-bold">3:30/km</td>
                    <td class="py-3 text-[#C4B9C8]">VO2max Puro (100%)</td>
                    <td class="py-3 text-white">Tolerancia a la fatiga en terreno blando</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">10K Ruta (Hito Ávila)</td>
                    <td class="py-3 text-[#a887ce] font-bold">3:45 - 3:50/km</td>
                    <td class="py-3 text-[#C4B9C8]">Umbral Anaeróbico (LT2)</td>
                    <td class="py-3 text-white">Capacidad de aclaramiento de lactato</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">Media Maratón</td>
                    <td class="py-3 text-[#a887ce] font-bold">3:55 - 4:00/km</td>
                    <td class="py-3 text-[#C4B9C8]">Glucógeno Mixto / Umbral LT1-LT2</td>
                    <td class="py-3 text-white">Ritmo crucero submáximo sostenido</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">Rodaje Z2 Base</td>
                    <td class="py-3 text-[#20D994] font-bold">4:35 - 4:55/km</td>
                    <td class="py-3 text-[#C4B9C8]">Oxidación Lipídica</td>
                    <td class="py-3 text-white">Capilarización & Biogénesis Mitocondrial</td>
                  </tr>
                  <tr>
                    <td class="py-3 font-bold text-white">Rodaje Regenerativo Z1</td>
                    <td class="py-3 text-[#20D994] font-bold">5:00 - 5:20/km</td>
                    <td class="py-3 text-[#C4B9C8]">Grasas Puras / Flujo Sanguíneo</td>
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
                <div class="logo-container-profile w-14 h-14 rounded-2xl flex items-center justify-center flex-shrink-0" style="width: 56px; height: 56px; max-width: 56px; max-height: 56px;">
                  <svg width="56" height="56" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none" class="w-full h-full">
  <defs>
    <linearGradient id="prof_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#c5abde"/>
      <stop offset="50%" stop-color="#a887ce"/>
      <stop offset="100%" stop-color="#70559f"/>
    </linearGradient>
    <linearGradient id="prof_coral" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#e885a6"/>
      <stop offset="50%" stop-color="#d86991"/>
      <stop offset="100%" stop-color="#9c526d"/>
    </linearGradient>
    <linearGradient id="prof_core" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#d86991"/>
      <stop offset="100%" stop-color="#a887ce"/>
    </linearGradient>
    <linearGradient id="prof_wing" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#d86991"/>
    </linearGradient>
  </defs>
  <path d="M 50 14 C 38 12, 22 18, 16 32 C 11 48, 16 68, 32 82 C 40 88, 47 92, 50 93 C 44 86, 28 76, 25 61 C 22 47, 28 34, 40 26 C 44 23, 48 18, 50 14 Z" fill="url(#prof_blue)"/>
  <path d="M 50 14 C 62 12, 78 18, 84 32 C 89 48, 84 68, 68 82 C 60 88, 53 92, 50 93 C 56 86, 72 76, 75 61 C 78 47, 72 34, 60 26 C 56 23, 52 18, 50 14 Z" fill="url(#prof_coral)"/>
  <path d="M 50 26 C 52 26, 61 46, 65 62 C 66 66, 62 68, 57 67 C 54 62, 53 56, 50 56 C 47 56, 46 62, 43 67 C 38 68, 34 66, 35 62 C 39 46, 48 26, 50 26 Z" fill="url(#prof_core)"/>
  <path d="M 22 57 C 35 53, 65 53, 78 57 C 68 61, 32 61, 22 57 Z" fill="url(#prof_wing)"/>
</svg>
                </div>
                <div>
                  <h3 class="text-xl font-black text-white">Carlos Jiménez Andrino</h3>
                  <p class="text-xs text-[#C4B9C8] mt-0.5">Atleta Medio Fondo & Fondo &bull; Categoría Senior</p>
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
                <label class="text-[10px] uppercase font-bold text-[#C4B9C8]">Peso Actual (kg)</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-weight" step="0.1" value="63.0" oninput="calculateBMI()" disabled class="w-full bg-[#171821]/50 border border-[#4d3e50] rounded-xl px-3 py-2 text-white/90 font-mono font-bold text-sm focus:outline-none focus:border-[#d86991] opacity-80 cursor-default transition">
                </div>
                <span class="text-[10px] text-[#C4B9C8] mt-1 block">Varía según hidratación</span>
              </div>

              <div>
                <label class="text-[10px] uppercase font-bold text-[#C4B9C8]">Altura (cm)</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-height" value="173" oninput="calculateBMI()" class="w-full bg-[#171821] border border-[#4d3e50] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#d86991]">
                </div>
                <span class="text-[10px] text-[#C4B9C8] mt-1 block">1.73 metros</span>
              </div>

              <div>
                <label class="text-[10px] uppercase font-bold text-[#C4B9C8]">Edad</label>
                <div class="mt-1 flex items-center">
                  <input type="number" id="profile-age" value="23" class="w-full bg-[#171821] border border-[#4d3e50] rounded-xl px-3 py-2 text-white font-mono font-bold text-sm focus:outline-none focus:border-[#d86991]">
                </div>
                <span class="text-[10px] text-[#C4B9C8] mt-1 block">Años cumplidos</span>
              </div>

              <div>
                <label class="text-[10px] uppercase font-bold text-[#C4B9C8]">FC Reposo (FCR)</label>
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
                <p class="text-xs text-[#C4B9C8]">Calculado automáticamente a partir de tu peso y altura en tiempo real</p>
              </div>

              <div class="flex items-baseline gap-2">
                <span id="bmi-display-value" class="text-3xl sm:text-4xl font-black text-white font-mono">21.05</span>
                <span class="text-xs text-[#C4B9C8] font-mono font-bold">kg/m&sup2;</span>
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
              <div class="flex items-center justify-between text-[10px] font-mono text-[#C4B9C8] pt-1">
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
              <p id="bmi-status-desc" class="text-xs text-[#C4B9C8] leading-relaxed">
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
  <nav class="lg:hidden fixed left-3 right-3 h-16 bg-[#292631]/95 backdrop-blur-md border border-[#4d3e50] rounded-2xl flex items-center justify-around z-40 px-1 shadow-2xl" style="bottom: calc(0.75rem + env(safe-area-inset-bottom, 0px));">
    <button onclick="switchTab('dashboard')" id="dock-btn-dashboard" class="flex flex-col items-center justify-center text-[#d86991] flex-1 py-1">
      <i data-lucide="layout-grid" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Dashboard</span>
    </button>
    <button onclick="switchTab('workouts')" id="dock-btn-workouts" class="flex flex-col items-center justify-center text-[#C4B9C8] flex-1 py-1">
      <i data-lucide="calendar" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Entrenos</span>
    </button>
    <button onclick="switchTab('gym')" id="dock-btn-gym" class="flex flex-col items-center justify-center text-[#C4B9C8] flex-1 py-1">
      <i data-lucide="dumbbell" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Gimnasio</span>
    </button>
    <button onclick="switchTab('goals')" id="dock-btn-goals" class="flex flex-col items-center justify-center text-[#C4B9C8] flex-1 py-1">
      <i data-lucide="target" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Objetivos</span>
    </button>
    <button onclick="switchTab('profile')" id="dock-btn-profile" class="flex flex-col items-center justify-center text-[#C4B9C8] flex-1 py-1">
      <i data-lucide="user" class="w-5 h-5 stroke-[2]"></i>
      <span class="text-[9px] font-bold mt-1">Perfil</span>
    </button>
  </nav>

  <!-- REST TIMER FLOATING BANNER -->
  <div id="rest-timer-banner" class="hidden fixed bottom-24 sm:bottom-28 left-1/2 -translate-x-1/2 z-50 bg-[#292631]/95 border-2 border-[#fa769e] rounded-2xl shadow-2xl px-5 py-3 flex items-center gap-4 text-white backdrop-blur-md transition-all duration-300" style="margin-bottom: env(safe-area-inset-bottom, 0px);">
    <div class="flex items-center gap-3">
      <span class="text-2xl animate-pulse">⏱️</span>
      <div>
        <span class="text-[10px] uppercase font-extrabold text-[#C4B9C8] block leading-none">Tiempo de Descanso</span>
        <span id="rest-timer-countdown" class="text-2xl font-black text-[#fa769e] font-mono leading-tight">01:30</span>
      </div>
    </div>
    <button onclick="cancelRestTimer()" class="w-9 h-9 rounded-xl bg-[#171821] border border-[#4d3e50] text-[#C4B9C8] hover:text-white flex items-center justify-center font-bold text-sm transition active:scale-90" title="Cancelar descanso">&times;</button>
  </div>

  <!-- =================================================== -->
  <!-- JAVASCRIPT DEL CLIENTE -->
  <!-- =================================================== -->
  <script>
    const daysData = ${safeJsonStringify(planData.days || [])};
    const weeklyData = ${safeJsonStringify(WEEKLY_EVO_DATA)};
    const calendarDataByMonth = ${safeJsonStringify(CALENDAR_DATA_BY_MONTH)};
    const monthKeys = ["2026-09", "2026-10", "2026-11", "2026-12"];
    let currentMonthIdx = 2; // Noviembre 2026 por defecto
    const todayISO = "${todayISO}";
    const aegisKey = localStorage.getItem('aegis_key') || '${env?.AEGIS_SECRET_KEY || env?.INTERVALS_API_KEY || "4cvqxm8a5intat925ttdcmpja"}';
    if (aegisKey) {
      try { localStorage.setItem('aegis_key', aegisKey); } catch(e){}
    }

    function escapeHtml(str) {
      if (str === null || str === undefined) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

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
        calBtn.classList.remove('text-[#C4B9C8]');
        micBtn.classList.remove('bg-[#d86991]', 'text-white', 'shadow-lg');
        micBtn.classList.add('text-[#C4B9C8]');
      } else {
        calView.classList.add('hidden');
        micView.classList.remove('hidden');
        micBtn.classList.add('bg-[#d86991]', 'text-white', 'shadow-lg');
        micBtn.classList.remove('text-[#C4B9C8]');
        calBtn.classList.remove('bg-[#d86991]', 'text-white', 'shadow-lg');
        calBtn.classList.add('text-[#C4B9C8]');
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
          deskBtn.classList.toggle('text-[#C4B9C8]', t !== tabId);
        }

        const dockBtn = document.getElementById('dock-btn-' + t);
        if (dockBtn) {
          dockBtn.classList.toggle('text-[#d86991]', t === tabId);
          dockBtn.classList.toggle('text-[#C4B9C8]', t !== tabId);
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
    let currentRoutineId = 2;

    function selectGymRoutine(routineId) {
      currentRoutineId = routineId;
      for (let i = 1; i <= 4; i++) {
        const btn = document.getElementById('gym-chip-' + i);
        if (!btn) continue;
        if (i === routineId) {
          btn.className = "p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#d86991] text-white border-[#d86991] font-semibold glow-pink";
          btn.querySelectorAll('span')[0].className = "text-[10px] uppercase font-extrabold text-white/80";
          btn.querySelectorAll('span')[1].className = "text-xs font-extrabold text-white mt-1";
          btn.querySelectorAll('span')[2].className = "text-[10px] text-white/80 mt-0.5";
        } else {
          btn.className = "p-3.5 rounded-2xl text-left border transition flex flex-col justify-between bg-[#292631] border-[#4d3e50] text-[#C4B9C8] hover:border-[#d86991]";
          btn.querySelectorAll('span')[0].className = "text-[10px] uppercase font-bold text-[#C4B9C8]";
          btn.querySelectorAll('span')[1].className = "text-xs font-extrabold text-white mt-1";
          btn.querySelectorAll('span')[2].className = "text-[10px] text-[#C4B9C8] mt-0.5";
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
        '<span class="text-xs font-extrabold px-3 py-1 rounded-xl bg-[#292631] text-[#C4B9C8] border border-[#4d3e50]">' +
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
                '<p class="text-xs text-[#C4B9C8] mt-0.5 font-medium">Objetivo: <strong class="text-white">' + ex.target_sets + ' series &times; ' + ex.target_reps + ' reps</strong> @ <strong class="text-[#d86991] font-mono">' + ex.target_weight + '</strong> (' + ex.rir + ')</p>' +
              '</div>' +

              '<!-- Tabla de Series (ORDEN: Serie - Reps - Carga - Acción) -->' +
              '<div class="overflow-x-auto">' +
                '<div class="min-w-[320px] space-y-2" id="sets-container-' + ex.num + '">' +
                  renderExerciseSetsHtml(routineId, ex.num) +
                '</div>' +
              '</div>' +

              '<!-- Botón Añadir Serie -->' +
              '<div class="flex items-center justify-between pt-1">' +
                '<button onclick="addSetRow(' + routineId + ', ' + ex.num + ')" id="add-set-btn-' + ex.num + '" class="px-3 py-1.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-[#C4B9C8] hover:text-white text-xs font-bold transition flex items-center gap-1.5">' +
                  '<i data-lucide="plus" class="w-3.5 h-3.5 text-[#d86991]"></i> + Añadir Serie' +
                '</button>' +
                '<div class="text-[11px] text-[#C4B9C8] italic">' + ex.cue + '</div>' +
              '</div>' +

              '<!-- Notas del Ejercicio -->' +
              '<div class="pt-1">' +
                '<input type="text" value="' + escapeHtml(currentGymState[ex.num].notes || '') + '" oninput="updateExerciseNotes(' + routineId + ', ' + ex.num + ', this.value)" placeholder="Sensaciones, RIR o apuntes del ejercicio..." class="w-full bg-[#171821] border border-[#4d3e50] rounded-xl px-3 py-1.5 text-xs text-[#C4B9C8] focus:text-white focus:outline-none focus:border-[#a887ce] transition">' +
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
      let out = '<div class="grid grid-cols-12 gap-1.5 sm:gap-2 text-[10px] text-[#C4B9C8] font-bold uppercase tracking-wider px-2 pb-1 border-b border-[#4d3e50]/60">' +
        '<div class="col-span-2">Serie</div>' +
        '<div class="col-span-4 text-center">Reps</div>' +
        '<div class="col-span-4 text-center">Carga (kg)</div>' +
        '<div class="col-span-2 text-center">Acción</div>' +
      '</div>';

      exState.sets.forEach((s, idx) => {
        out += '<div class="grid grid-cols-12 gap-1.5 sm:gap-2 items-center p-2 rounded-xl bg-[#171821] border border-[#4d3e50] text-xs font-mono min-h-[52px]">' +
          '<!-- Serie -->' +
          '<div class="col-span-2 font-bold text-[#C4B9C8] flex items-center gap-1">' +
            '<span class="w-7 h-7 rounded-lg bg-[#292631] text-white flex items-center justify-center text-xs font-bold">' + s.set_num + '</span>' +
          '</div>' +

          '<!-- Reps con Steppers -->' +
          '<div class="col-span-4 flex items-center gap-1">' +
            '<button type="button" onclick="stepRep(' + routineId + ', ' + exNum + ', ' + idx + ', -1)" class="min-w-[36px] sm:min-w-[44px] min-h-[44px] w-9 h-11 rounded-lg bg-[#292631] hover:bg-[#3d3846] text-white font-bold flex items-center justify-center text-sm transition active:scale-95 touch-manipulation">−1</button>' +
            '<input type="number" inputmode="decimal" value="' + escapeHtml(s.reps || '') + '" oninput="updateSetReps(' + routineId + ', ' + exNum + ', ' + idx + ', this.value)" placeholder="0" class="w-full bg-[#292631] border border-[#4d3e50] rounded-lg h-11 text-center text-white font-bold text-xs focus:outline-none focus:border-[#fa769e] transition">' +
            '<button type="button" onclick="stepRep(' + routineId + ', ' + exNum + ', ' + idx + ', 1)" class="min-w-[36px] sm:min-w-[44px] min-h-[44px] w-9 h-11 rounded-lg bg-[#292631] hover:bg-[#3d3846] text-white font-bold flex items-center justify-center text-sm transition active:scale-95 touch-manipulation">+1</button>' +
          '</div>' +

          '<!-- Kilos con Steppers Rápidos (+2.5 kg) -->' +
          '<div class="col-span-4 flex items-center gap-1">' +
            '<button type="button" onclick="stepWeight(' + routineId + ', ' + exNum + ', ' + idx + ', -2.5)" class="min-w-[36px] sm:min-w-[44px] min-h-[44px] w-9 h-11 rounded-lg bg-[#292631] hover:bg-[#3d3846] text-white font-bold flex items-center justify-center text-[10px] transition active:scale-95 touch-manipulation">−2.5</button>' +
            '<input type="number" step="0.5" inputmode="decimal" value="' + escapeHtml(s.weight || '') + '" oninput="updateSetWeight(' + routineId + ', ' + exNum + ', ' + idx + ', this.value)" placeholder="kg" class="w-full bg-[#292631] border border-[#4d3e50] rounded-lg h-11 text-center text-white font-bold text-xs focus:outline-none focus:border-[#9ca8f3] transition">' +
            '<button type="button" onclick="stepWeight(' + routineId + ', ' + exNum + ', ' + idx + ', 2.5)" class="min-w-[36px] sm:min-w-[44px] min-h-[44px] w-9 h-11 rounded-lg bg-[#292631] hover:bg-[#3d3846] text-white font-bold flex items-center justify-center text-[10px] transition active:scale-95 touch-manipulation">+2.5</button>' +
          '</div>' +

          '<!-- Acción: Eliminar con touch target de 44x44px -->' +
          '<div class="col-span-2 flex items-center justify-center">' +
            (exState.sets.length > 1 ? '<button type="button" onclick="removeSetRow(' + routineId + ', ' + exNum + ', ' + idx + ')" class="w-11 h-11 rounded-xl bg-[#292631] hover:bg-rose-500/20 text-[#C4B9C8] hover:text-[#fa769e] flex items-center justify-center text-base font-bold transition active:scale-90 touch-manipulation" title="Eliminar serie">&times;</button>' : '<span class="text-[#20D994] font-bold text-sm">✓</span>') +
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

    function stepRep(routineId, exNum, idx, delta) {
      if (!currentGymState[exNum] || !currentGymState[exNum].sets[idx]) return;
      const cur = parseInt(currentGymState[exNum].sets[idx].reps) || 0;
      currentGymState[exNum].sets[idx].reps = Math.max(0, cur + delta);
      persistGymState(routineId);
      document.getElementById('sets-container-' + exNum).innerHTML = renderExerciseSetsHtml(routineId, exNum);
      updateMarkdownPreview(routineId);
    }

    function stepWeight(routineId, exNum, idx, delta) {
      if (!currentGymState[exNum] || !currentGymState[exNum].sets[idx]) return;
      const cur = parseFloat(currentGymState[exNum].sets[idx].weight) || 0;
      const nextVal = Math.max(0, Math.round((cur + delta) * 10) / 10);
      currentGymState[exNum].sets[idx].weight = Number.isInteger(nextVal) ? nextVal.toString() : nextVal.toFixed(1);
      persistGymState(routineId);
      document.getElementById('sets-container-' + exNum).innerHTML = renderExerciseSetsHtml(routineId, exNum);
      updateMarkdownPreview(routineId);
    }

    // Web Audio Beep & Rest Timer
    let audioCtx = null;
    function playRestBeep() {
      try {
        const ctx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, ctx.currentTime); // Nota La5 (880 Hz chime limpio)
        gain.gain.setValueAtTime(0.25, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.6);
      } catch (e) {
        console.log('Audio feedback not supported or blocked', e);
      }
    }

    let restTimerInterval = null;
    let restSecondsLeft = 0;
    function startRestTimer(seconds) {
      if (!audioCtx) {
        try { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); } catch(e){}
      }
      clearInterval(restTimerInterval);
      restSecondsLeft = seconds;
      const banner = document.getElementById('rest-timer-banner');
      if (banner) banner.classList.remove('hidden');
      updateRestTimerUi();

      restTimerInterval = setInterval(() => {
        restSecondsLeft--;
        if (restSecondsLeft <= 0) {
          clearInterval(restTimerInterval);
          playRestBeep();
          if (navigator.vibrate) {
            try { navigator.vibrate([250, 100, 250]); } catch(e){}
          }
          const banner = document.getElementById('rest-timer-banner');
          const countdownEl = document.getElementById('rest-timer-countdown');
          if (banner) {
            banner.classList.add('border-emerald-500', 'bg-emerald-950/90');
            if (countdownEl) countdownEl.textContent = '¡LISTO!';
            setTimeout(() => {
              banner.classList.add('hidden');
              banner.classList.remove('border-emerald-500', 'bg-emerald-950/90');
            }, 2500);
          }
        } else {
          updateRestTimerUi();
        }
      }, 1000);
    }

    function updateRestTimerUi() {
      const el = document.getElementById('rest-timer-countdown');
      if (el) {
        const mins = Math.floor(restSecondsLeft / 60);
        const secs = restSecondsLeft % 60;
        el.textContent = mins + ':' + (secs < 10 ? '0' : '') + secs;
      }
    }

    function cancelRestTimer() {
      clearInterval(restTimerInterval);
      const banner = document.getElementById('rest-timer-banner');
      if (banner) banner.classList.add('hidden');
    }

    let gymDebounceTimer = null;
    function persistGymState(routineId) {
      const savedKey = 'aegis_workout_v3_' + todayISO + '_r' + routineId;
      try {
        localStorage.setItem(savedKey, JSON.stringify(currentGymState));
      } catch (e) {
        console.warn('localStorage quota exceeded', e);
      }

      const syncBadge = document.getElementById('gym-sync-status');
      if (syncBadge) {
        syncBadge.textContent = '🟡 Guardando en nube...';
        syncBadge.className = 'text-[10px] text-amber-400 font-bold';
      }

      clearTimeout(gymDebounceTimer);
      gymDebounceTimer = setTimeout(() => {
        fetch('/api/save_gym_session', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-Aegis-Key': aegisKey
          },
          body: JSON.stringify({
            date: todayISO,
            routine_id: routineId,
            routine_name: (gymRoutinesData[routineId] && gymRoutinesData[routineId].title) || ('Rutina ' + routineId),
            state: currentGymState
          })
        }).then(res => {
          if (!res.ok) throw new Error('HTTP ' + res.status);
          return res.json();
        }).then(() => {
          if (syncBadge) {
            syncBadge.textContent = '🟢 Sincronizado en KV';
            syncBadge.className = 'text-[10px] text-emerald-400 font-bold';
          }
        }).catch(e => {
          if (syncBadge) {
            syncBadge.textContent = '⚪ Modo local (offline)';
            syncBadge.className = 'text-[10px] text-[#C4B9C8] font-bold';
          }
        });
      }, 600);
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
          const w = String(s.weight || '0').replace('kg', '');
          const r = String(s.reps || '0');
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
              '<span class="text-[11px] font-mono text-[#C4B9C8]">' + act.laps.length + ' vueltas</span>' +
            '</div>' +
            '<div class="overflow-x-auto rounded-xl border border-[#4d3e50]/70 bg-[#292631]/50">' +
              '<table class="w-full text-left text-xs font-mono">' +
                '<thead>' +
                  '<tr class="bg-[#171821] text-[#C4B9C8] border-b border-[#4d3e50] text-[10px] uppercase">' +
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
          notesContainer.innerHTML = '<div class="mt-3 p-3.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-xs text-[#C4B9C8] leading-relaxed">' +
            '<span class="font-bold text-white block mb-1">📝 Notas de Carlos (Garmin):</span>' +
            '<div class="whitespace-pre-line text-white/90">' + escapeHtml(act.notes) + '</div>' +
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
                '<span class="text-sm sm:text-base font-extrabold text-white">' + escapeHtml(day.day_name) + ' ' + escapeHtml(day.date.substring(8)) + ' ' + (day.date.substring(5, 7) === '11' ? 'Nov' : 'Dic') + '</span>' +
                '<div class="text-xs text-[#C4B9C8] font-medium mt-0.5">' +
                  (day.running.is_rest ? 'Descanso carrera' : escapeHtml(day.running.title)) + ' &bull; ' +
                  (day.gym.is_rest ? 'Descanso fuerza' : escapeHtml(day.gym.routine_name.split('·')[0])) +
                '</div>' +
              '</div>' +
            '</div>' +
            '<i id="day-icon-' + idx + '" data-lucide="chevron-down" class="w-5 h-5 text-[#C4B9C8] transition-transform duration-200" style="transform: ' + (startOpen ? 'rotate(180deg)' : 'rotate(0deg)') + ';"></i>' +
          '</div>' +

          '<div id="day-body-' + idx + '" class="px-4 pb-4 sm:px-6 sm:pb-6 pt-1 space-y-4 border-t border-[#4d3e50]/50 ' + (startOpen ? '' : 'hidden') + '">' +
            '<!-- Running -->' +
            (day.running.is_rest 
              ? '<div class="p-3.5 rounded-xl bg-[#171821] border border-[#4d3e50]/60 text-xs text-[#C4B9C8] flex items-center gap-2"><i data-lucide="moon" class="w-4 h-4 text-[#a887ce]"></i> Descanso de running: Recuperación activa y regeneración celular.</div>'
              : '<div class="p-4 rounded-xl bg-[#171821] border border-[#4d3e50] space-y-2">' +
                '<div class="flex items-center justify-between text-xs font-bold text-[#d86991]">' +
                  '<span class="flex items-center gap-1.5">' +
                    '<i data-lucide="footprints" class="w-4 h-4"></i> ' + escapeHtml(day.running.title) +
                  '</span>' +
                  '<span class="text-xs font-mono font-black text-white">' + escapeHtml(day.running.duration_min) + ' min &bull; ' + escapeHtml(day.running.target_distance_km) + ' km</span>' +
                '</div>' +
                '<p class="text-xs text-white/90 leading-relaxed">' + escapeHtml(day.running.main_work) + '</p>' +
                '<div class="grid grid-cols-2 sm:grid-cols-3 gap-2 pt-1 text-[11px] font-mono">' +
                  '<div class="p-2 rounded-lg bg-[#292631] border border-[#4d3e50] text-[#C4B9C8]">' +
                    'RITMO: <strong class="text-white">' + escapeHtml(day.running.target_pace) + '</strong>' +
                  '</div>' +
                  '<div class="p-2 rounded-lg bg-[#292631] border border-[#4d3e50] text-[#C4B9C8]">' +
                    'ZONA FC: <strong class="text-[#d86991]">' + escapeHtml(day.running.hr_zone) + '</strong>' +
                  '</div>' +
                  '<div class="p-2 rounded-lg bg-[#292631] border border-[#4d3e50] text-[#C4B9C8] col-span-2 sm:col-span-1">' +
                    'ZAPATILLA: <strong class="text-white">' + escapeHtml(day.running.shoe || 'Asics Novablast') + '</strong>' +
                  '</div>' +
                '</div>' +
              '</div>'
            ) +

            '<!-- Fuerza Gym -->' +
            (day.gym.is_rest
              ? '<div class="p-3.5 rounded-xl bg-[#171821] border border-[#4d3e50]/60 text-xs text-[#C4B9C8] flex items-center gap-2"><i data-lucide="coffee" class="w-4 h-4 text-[#20D994]"></i> Descanso de gimnasio: 0 fatiga neuromuscular.</div>'
              : '<div class="p-4 rounded-xl bg-[#171821] border border-[#4d3e50] space-y-3">' +
                '<div class="flex items-center justify-between text-xs font-bold text-[#a887ce]">' +
                  '<span class="flex items-center gap-1.5">' +
                    '<i data-lucide="dumbbell" class="w-4 h-4"></i> ' + escapeHtml(day.gym.routine_name) +
                  '</span>' +
                  '<button onclick="goToGymRoutine(' + (day.gym.routine_id || 1) + ')" class="px-2.5 py-1 rounded-lg bg-[#a887ce] text-white text-[11px] font-bold hover:brightness-110 transition">' +
                    'Ir a la Rutina &rarr;' +
                  '</button>' +
                '</div>' +
                '<div class="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">' +
                  (day.gym.highlight_exercises || day.gym.exercises || []).map(function(ex) {
                    return '<div class="p-2 rounded-lg bg-[#292631] border border-[#4d3e50] flex items-center justify-between text-[11px]">' +
                      '<span class="text-white font-medium">' + escapeHtml(ex.name) + '</span>' +
                      '<span class="font-mono text-[#a887ce] font-bold">' + escapeHtml(ex.load) + ' (' + escapeHtml(ex.rir) + ')</span>' +
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
        headers: {
          'Content-Type': 'application/json',
          'X-Aegis-Key': aegisKey
        },
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

        const recentWeeklyData = weeklyData.slice(-4);
        const labels = recentWeeklyData.map(w => w.label);
        const kmValues = recentWeeklyData.map(w => w.run_km);
        const gymValues = recentWeeklyData.map(w => w.gym_sessions);

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
                bodyColor: '#C4B9C8',
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
      // Sincronización Bidireccional KV & LocalStorage
      async function loadCloudData() {
        if (!aegisKey) return;
        // 1. Sincronizar Perfil desde Cloudflare KV
        try {
          const resProfile = await fetch('/api/get_profile', {
            headers: { 'X-Aegis-Key': aegisKey }
          });
          if (resProfile.ok) {
            const p = await resProfile.json();
            if (p && p.weight) {
              localStorage.setItem('aegis_athlete_profile', JSON.stringify(p));
              if (document.getElementById('profile-weight')) document.getElementById('profile-weight').value = p.weight;
              if (document.getElementById('profile-height')) document.getElementById('profile-height').value = p.height;
              if (document.getElementById('profile-age') && p.age) document.getElementById('profile-age').value = p.age;
              if (document.getElementById('profile-fcr') && p.fcr) document.getElementById('profile-fcr').value = p.fcr;
              calculateBMI();
            }
          }
        } catch (err) {
          console.warn('Could not sync profile from KV:', err);
        }

        // 2. Sincronizar Sesión de Gimnasio desde Cloudflare KV
        try {
          const resGym = await fetch('/api/get_gym_session?date=' + encodeURIComponent(todayISO), {
            headers: { 'X-Aegis-Key': aegisKey }
          });
          if (resGym.ok) {
            const g = await resGym.json();
            if (g && g.routine_id && g.state) {
              const savedKey = 'aegis_workout_v3_' + todayISO + '_r' + g.routine_id;
              localStorage.setItem(savedKey, JSON.stringify(g.state));
              if (currentRoutineId === g.routine_id) {
                selectGymRoutine(g.routine_id);
              }
            }
          }
        } catch (err) {
          console.warn('Could not sync gym session from KV:', err);
        }
      }

      syncDynamicMetrics();
      loadCloudData();
    });

    // Registro del Service Worker PWA Offline (/sw.js)
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js').catch(err => console.warn('SW registration failed:', err));
      });
    }
  </script>
</body>
</html>`;
}
