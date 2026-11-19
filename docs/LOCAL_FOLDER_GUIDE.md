# 📂 Guía de Carpetas y Estructura Local — Aegis Coach

Este documento cataloga y explica en detalle cada directorio, script y módulo existente en este repositorio local para que cualquier agente de IA o desarrollador entienda inmediatamente qué está activo, qué es legado y cómo interactúan las piezas.

---

## 1. Visión General de la Estructura

```
aegis-coach/
├── cloudflare/                  # 🟢 EN PRODUCCIÓN: PWA Edge, Worker, KV y Estilos
│   ├── src/
│   │   └── index.ts             # Código fuente del Worker (Router, PWA HTML, API, SW v8, Cron)
│   ├── public_exercises/        # Suite de imágenes procesadas y SVGs
│   ├── wrangler.toml            # Configuración de despliegue en Cloudflare Workers
│   └── .dev.vars.example        # Plantilla de secretos locales para desarrollo
│
├── data/                        # 🟢 EN PRODUCCIÓN: Base de datos híbrida local
│   ├── historial_entrenamientos_carlos.xlsx  # Libro Excel maestro (5 hojas: Actividades, Laps, Gimnasio, Salud, Objetivos)
│   ├── historial_entrenamientos_carlos.md    # Cuaderno técnico de análisis fisiológico
│   └── gym_images/              # Fotos reales de los ejercicios de las rutinas de Carlos
│
├── scripts/                     # 🟢 EN PRODUCCIÓN: Scripts de automatización y sincronización
│   ├── sync_coaching_engine.py  # Motor de sincronización automática con Intervals.icu API
│   ├── publish_plan_to_kv.py    # Publicador de planes de entrenamiento a Cloudflare KV
│   ├── build_perfect_pwa_icons.py # Generador de iconos 1:1 con safe-zone para Android/iOS
│   ├── upload_pwa_icons_to_kv.py # Subida de iconos y favicon a Cloudflare KV
│   ├── upload_css_to_kv.py      # Subida de la hoja de estilos Tailwind precompilada a KV
│   └── verify_live_pwa_and_mobile.py # Verificador E2E Playwright de la app en producción
│
├── tests/                       # 🟢 EN PRODUCCIÓN: Batería de 264 tests automatizados
│   ├── test_audit_suite.py      # Tests de seguridad, Service Worker, headers y ergonomía
│   ├── test_m3_core.py          # Tests del core y persistencia KV
│   ├── test_playwright_m2_ergonomics.py # Tests de UI en Playwright
│   └── ...                      # Tests de modelos fisiológicos, ACWR y escenarios límite
│
├── docs/                        # 📚 DOCUMENTACIÓN TÉCNICA MAESTRA
│   ├── ARCHITECTURE.md          # Arquitectura técnica, KV schema y ciclo de vida Edge
│   ├── GARMIN_INTEGRATION_GUIDE.md # Guía comparativa Garmin Personal API vs Intervals.icu
│   ├── LOCAL_FOLDER_GUIDE.md    # Este documento (mapa del repositorio)
│   └── ROADMAP.md               # Hoja de ruta de funcionalidades e interactividad
│
├── reports/                     # Informes de auditorías previas
│   └── auditoria_ui_ux_aegis_coach.md
│
├── prototype/                   # Prototipos estáticos HTML generados en sesiones de diseño
│   └── index.html
│
├── poc/                         # ⚪ LEGADO (Agosto 2026): Prototipo multi-agente abstracto
│   ├── agents/                  # Agentes genéricos previos (medical, nutrition, planner)
│   ├── models/                  # Modelos de datos del POC
│   ├── rag/                     # Módulo RAG conceptual
│   ├── router/                  # Enrutador abstracto
│   └── run_poc.py               # Ejecutable del POC anterior
│
├── AGENTS.md                    # 🧠 REGLAS SUPREMAS DE LOS AGENTES (Perfil de Carlos, Mandato Crítico)
├── PROJECT.md                   # 📋 Inventario de funcionalidades y estado de hitos
├── README.md                    # 📖 Manual principal de uso e instalación
├── Rutinas_Gimnasio_Carlos_Visual.pdf # Documento visual oficial de entrenamiento de fuerza
└── .gitignore                   # Exclusión estricta de secretos, node_modules y ficheros temporales
```

---

## 2. Detalle de Carpetas en Producción (Activas)

### `cloudflare/` (El Corazón de la Aplicación en Vivo)
- **URL Desplegada:** `https://aegis-intervals-sync.uranuslabs.workers.dev`
- **`src/index.ts`:**
  - Sirve el HTML completo de la PWA móvil con la paleta de colores de lujo **Octet Interactive Dashboards** (`#171821`, `#292631`, `#a887ce`, `#9c526d`).
  - Implementa el **Service Worker `v8`** con estrategia *Network-First* para el documento de navegación y *Bypass Cross-Origin* para evitar bloqueos en navegadores como Brave.
  - Endpoints de API REST:
    - `POST /api/save_gym_session` / `GET /api/get_gym_session`: Guardado de series, repeticiones y cargas en tiempo real.
    - `POST /api/save_profile` / `GET /api/get_profile`: Lectura y actualización de peso, altura e IMC.
    - `GET /css/app.css`: Sirve la hoja de estilos Tailwind precompilada (`36 KB`) almacenada en KV para carga instantánea offline.
    - `GET /manifest.json`, `/favicon.ico`, `/favicon.png`, `/apple-touch-icon.png`: Suite PWA 1:1.
    - `POST /webhook`: Webhook autenticado para interacción con Telegram.
  - Cron Trigger `scheduled()`: Despierta cada 4 horas (`0 */4 * * *`) para revisar Intervals.icu y alertar a Carlos.

### `data/` (Almacenamiento Local Híbrido)
- **`historial_entrenamientos_carlos.xlsx`:** Base de datos relacional en Excel con 5 hojas maestras formateadas:
  1. `Actividades_Detalle`: Listado exhaustivo de sesiones con fecha, tipo, distancia, ritmo medio, FC media, desnivel y carga (TSS).
  2. `Series_y_Parciales`: Desglose vuelta a vuelta (laps) de entrenamientos de pista y competiciones.
  3. `Fuerza_Gym`: Registro histórico de cargas, ejercicios y RIR.
  4. `Fitness_y_Salud`: Evolución diaria de CTL, ATL, TSB y FCR.
  5. `Proximos_Objetivos`: Fechas de competición y ritmos meta.
- **`historial_entrenamientos_carlos.md`:** Cuaderno de bitácora técnico con explicaciones fisiológicas y tácticas.

### `scripts/` (Motores de Automatización)
- **`sync_coaching_engine.py`:** Se conecta a Intervals.icu API (`ATHLETE_ID: i690671`), descarga las últimas actividades, extrae los parciales por vuelta, calcula métricas de fatiga y regenera el Excel maestro y el Markdown.
- **`publish_plan_to_kv.py`:** Toma la estructura de microciclo semanal y la publica en Cloudflare KV (`key: current_plan`), actualizando al instante la PWA móvil y el bot de Telegram.
- **`build_perfect_pwa_icons.py`:** Genera mediante Playwright y Pillow los iconos PWA (`512x512`, `192x192`, `apple-touch-icon` y `favicon.ico`) con el 62% de zona segura para Android.
- **`upload_css_to_kv.py`:** Sube el CSS precompilado a la clave `css_app` en Cloudflare KV.
- **`verify_live_pwa_and_mobile.py`:** Test E2E Playwright que valida endpoints, tamaño de elementos y render móvil sin desbordamiento.

### `tests/` (Calidad y Blindaje)
- 264 tests automatizados ejecutables con `pytest tests/`.
- Verifican desde la ausencia de vulnerabilidades XSS y cabeceras de seguridad HTTP, hasta la calibración del ratio agudo:crónico (ACWR) y la ergonomía táctil en pantalla de móvil.

---

## 3. La Carpeta Legada (`poc/`) — Qué era y por qué se superó

La carpeta `poc/` data de agosto de 2026:
- **Propósito original:** Fue un boceto teórico de software multi-tenant para crear una plataforma SaaS de coaching con agentes de IA abstractos (`medical_agent.py`, `nutrition_agent.py`, `planner_agent.py`, `rag/`, `router/`).
- **Por qué no se usó:**
  1. Era un código teórico basado en plantillas genéricas sin conexión con la fisiología real de Carlos ni con su hardware (reloj Garmin, banda pectoral).
  2. No disponía de una interfaz web o móvil funcional para usarla en el día a día.
  3. Dependía de modelos pesados en vez de ejecutarse en el edge serverless ultrarrápido de Cloudflare.
- **Estado actual:** Se conserva intacta como archivo histórico, pero **no forma parte de la aplicación activa de Aegis Coach**. Todo el sistema en producción reside en `cloudflare/`, `data/`, `scripts/` y `tests/`.
