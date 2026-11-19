# Project: Aegis Coach — Producción, Ciberseguridad, Ergonomía Móvil y PWA Offline

## Architecture
Aegis Coach es la plataforma de inteligencia y coaching fisiológico de alto rendimiento para Carlos Jiménez Andrino (23 años, 63 kg, 1.73 m).
La arquitectura actual integra:
1. **Frontend / PWA Shell (`cloudflare/src/index.ts` & `/sw.js`)**:
   - Single-Page PWA servida directamente por el Cloudflare Worker en el edge.
   - Dashboard fisiológico con modo táctico, tabs dinámicos (Dashboard, Running, Gimnasio, Perfil), selector de rutinas de gimnasio interactivas con steppers táctiles, temporizador de descanso con Web Audio API y sincronización diferida con debounce de 600 ms.
   - Modo Offline 100% mediante Service Worker (`/sw.js`) con estrategia Cache-First / Stale-While-Revalidate para app shell y assets.
2. **Backend en el Edge (Cloudflare Worker & KV Namespace `AEGIS_KV`)**:
   - Endpoints REST protegidos con `X-Aegis-Key` / Bearer token:
     - `POST /api/save_gym_session` & `GET /api/get_gym_session`
     - `POST /api/save_profile` & `GET /api/get_profile`
   - Webhook blindado de Telegram (`/webhook`) con validación de `X-Telegram-Bot-Api-Secret-Token` y restricción a `TELEGRAM_CHAT_ID`.
   - Handler programado `scheduled(controller, env, ctx)` ejecutando el cron `0 */4 * * *` para monitorizar nuevas actividades de Intervals.icu y notificar por Telegram evitando duplicados en KV.
   - Cabeceras de seguridad HTTP completas (CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy).
3. **Motor de Datos Local & Sincronización Python (`scripts/sync_coaching_engine.py`)**:
   - Cliente robusto de la API de Intervals.icu con fechas dinámicas (`datetime.now()`), timeouts por petición y reintentos con backoff exponencial.

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F01 | [SEC-01] Rotación y Migración de Secretos | Mover `INTERVALS_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` fuera de `wrangler.toml` [vars] hacia `.dev.vars`, Cloudflare Secrets y `.env`. Crear `.gitignore`. | M1 | Survey E1 |
| F02 | [SEC-02] Autenticación en Endpoints KV | Proteger `/api/save_gym_session` y `/api/save_profile` requiriendo cabecera `X-Aegis-Key` o Bearer token para impedir sobreescritura anónima. | M1 | Survey E1 |
| F03 | [SEC-03] Blindaje de Telegram Webhook | Validar `X-Telegram-Bot-Api-Secret-Token` y verificar estrictamente que `message.chat.id` coincida con `TELEGRAM_CHAT_ID`. | M1 | Survey E1 |
| F04 | [SEC-04] Sanitización XSS y Safe JSON | Escapar notas y entradas dinámicas con `escapeHtml()` y sanitizar interpolación de JSON en `<script>` mediante `safeJsonStringify()`. | M1 | Survey E1 |
| F05 | [SEC-05] Cabeceras de Seguridad HTTP | Inyectar CSP, HSTS, X-Frame-Options, X-Content-Type-Options, Referrer-Policy y Permissions-Policy en todas las respuestas HTML y API del Worker. | M1 | Survey E1 |
| F06 | [BUG-PYTHON] Sincronizador Python Robusto | Corregir fecha estática por `datetime.now()` dinámico, añadir timeouts `(5.0, 25.0)` y reintentos con backoff HTTPAdapter en `scripts/sync_coaching_engine.py`. | M1 | Survey E1 |
| F07 | Steppers Ergonómicos de Gimnasio | Trasladar y escalar steppers de repeticiones (+1/-1) y peso (+2.5/-2.5 kg) a touch targets ≥44x44px con teclado numérico `inputmode="decimal"`. | M2 | Survey E2 |
| F08 | Temporizador de Descanso (Rest Timer) | Añadir Rest Timer en pestaña Gimnasio con botones 90s y 2m, cuenta atrás, señal sonora con Web Audio API y alerta visual/vibración. | M2 | Survey E2 |
| F09 | Debounce 600ms y SafeStorage | Guardado diferido de 600 ms en inputs de gimnasio con verificación de `res.ok` e indicador de estado visual (`🟢 Sincronizado en KV`, `🟡 Guardando...`, `⚪ Modo local`). | M2 | Survey E2 |
| F10 | Header Móvil Compacto (52px) | Reducir altura del header en móvil a 52px (`h-[52px] sm:h-16`) ocultando botones duplicados en móvil que ya están en el dock inferior. | M2 | Survey E2 |
| F11 | Widget Táctico Cross del Soto | Tarjeta destacada dinámica previa al gráfico con cuenta atrás `${daysRemaining}`, calzado clave (Clavos 6-9 mm) y objetivo 5.0 km @ 3:30/km. | M2 | Survey E2 |
| F12 | Historial 4 Semanas & Contraste Tipográfico | Concentrar historial en las 4 semanas más recientes y actualizar texto secundario `#A297A6` a `#C4B9C8` (WCAG AA compliant). | M2 | Survey E2 |
| F13 | Safe-Area Insets en Móvil | Aplicar `bottom: calc(0.75rem + env(safe-area-inset-bottom, 0px))` al dock inferior y padding seguro al contenedor `main`. | M2 | Survey E2 |
| F14 | Endpoints de Lectura en KV | Implementar `GET /api/get_gym_session` y `GET /api/get_profile` en el Worker e hidratar el cliente al cargar la aplicación para sincronización bidireccional PC-móvil. | M3 | Survey E3 |
| F15 | Service Worker Offline (`/sw.js`) | Servir y registrar `/sw.js` con estrategia Cache-First para precachear el app shell y assets, garantizando funcionamiento 100% offline. | M3 | Survey E3 |
| F16 | Handler Scheduled (Cron 4 Horas) | Exportar `scheduled(controller, env, ctx)` en el Worker con lógica `checkNewActivities` para consultar Intervals.icu, deduplicar en KV y enviar alertas Telegram. | M3 | Survey E3 |
| F17 | Verificación E2E Pytest & Playwright | Actualizar `tests/test_audit_suite.py` y suites para verificar producción en `cloudflare/src/index.ts`, validar UI con Playwright y asegurar 100% de tests pasando. | M4 | Survey E3 |
| F18 | Despliegue en Producción Cloudflare | Desplegar la versión final mediante `wrangler deploy` en la cuenta de Cloudflare `uranuslabs.hq@gmail.com` verificando el estado del Worker en vivo. | M4 | Survey E3 |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Ciberseguridad & Backend Hardening | F01, F02, F03, F04, F05, F06 | none | **DONE** |
| M2 | Ergonomía Gimnasio & Frontend UI/UX | F07, F08, F09, F10, F11, F12, F13 | M1 | **DONE** |
| M3 | Persistencia Cloudflare KV & PWA Offline | F14, F15, F16 | M1, M2 | **DONE** |
| M4 | Verificación Integral, Tests & Despliegue Cloudflare | F17, F18 | M1, M2, M3 | **DONE** |

---

## Interface Contracts & Data Schemas

### 1. KV Session Data Schema
- Key: `gym_session_YYYY-MM-DD`
- Value JSON:
  ```json
  {
    "date": "2026-11-16",
    "routine_id": 1,
    "routine_name": "Rutina 1 — Fuerza Máxima & RFD",
    "state": {
      "1": {
        "sets": [{"set_num": 1, "reps": "5", "weight": "80"}],
        "notes": ""
      }
    }
  }
  ```

### 2. KV User Profile Schema
- Key: `user_profile`
- Value JSON:
  ```json
  {
    "weight": 63.0,
    "height": 1.73,
    "age": 23,
    "fcr": 44,
    "updatedAt": "2026-11-16T15:00:00Z"
  }
  ```

### 3. API Headers Contract
- All `/api/save_*` and `/api/get_*` endpoints accept header:
  `X-Aegis-Key: <AEGIS_SECRET_KEY>` OR `Authorization: Bearer <AEGIS_SECRET_KEY>`.
- Telegram `/webhook` checks:
  `X-Telegram-Bot-Api-Secret-Token: <TELEGRAM_WEBHOOK_SECRET>`.

---

## Code Layout
```
aegis-coach/
├── .gitignore                             # Secretos, dev.vars, node_modules ignorados
├── cloudflare/
│   ├── .dev.vars.example                  # Plantilla de secretos locales
│   ├── .dev.vars                          # Secretos locales para wrangler dev
│   ├── wrangler.toml                      # Configuración limpia sin secretos expuestos
│   └── src/
│       └── index.ts                       # Cloudflare Worker: HTTP API, PWA HTML, Service Worker & Scheduled Cron
├── prototype/
│   └── index.html                         # Prototipo HTML de referencia
├── scripts/
│   ├── sync_coaching_engine.py            # Motor de sincronización Intervals.icu con backoff y fecha dinámica
│   ├── test_prototype_v10.py              # Suite Playwright con capturas móviles y escritorio
│   └── publish_plan_to_kv.py              # Script para actualizar plan en KV
├── tests/
│   ├── conftest.py                        # Fixtures y entorno de pruebas
│   ├── test_audit_suite.py                # Suite de auditoría de ciberseguridad y ergonomía UI
│   └── ...                                # Tests unitarios y de integración existentes (210 tests)
├── ORIGINAL_REQUEST.md                    # Requerimiento original inmutable
└── PROJECT.md                             # Blueprint maestro y registro de hitos
```
