## 2026-11-16T14:21:15Z

Implementa el plan por fases trabajando con los subagentes necesarios y las skills requeridas para el sistema Aegis Coach de Carlos Jiménez Andrino. No des por finalizada la tarea hasta conseguir el objetivo y revisar la auditoría punto por punto verificando que todos los aspectos de ciberseguridad, ergonomía UI/UX en móvil y persistencia PWA offline están implementados, corregidos y validados con tests automatizados (Playwright y pytest), finalizando con el despliegue en producción en Cloudflare.

Working directory: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach
Integrity mode: development

## Requirements

### R1. Ciberseguridad y Correcciones Críticas (Fase 1)
- [SEC-01] Rotación y migración de secretos: Extraer `INTERVALS_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` fuera de `wrangler.toml` [vars] y código estático hacia Cloudflare Secrets (`wrangler secret put`), `.dev.vars` y `.env` local.
- [SEC-02] Autenticación en endpoints `/api/save_gym_session` y `/api/save_profile`: Requerir cabecera `X-Aegis-Key` o Bearer token para impedir sobreescritura maliciosa o consumo indebido de cuotas en Cloudflare KV.
- [SEC-03] Blindaje de Telegram Webhook (`/webhook`): Validar cabecera `X-Telegram-Bot-Api-Secret-Token` y verificar estrictamente que `message.chat.id` coincida con `TELEGRAM_CHAT_ID`.
- [SEC-04] Sanitización XSS: Escapar notas y campos dinámicos con `escapeHtml()` y sanitizar la interpolación de JSON con `safeJsonStringify()` dentro de bloques `<script>`.
- [SEC-05] Cabeceras de seguridad HTTP: Inyectar CSP, HSTS, X-Frame-Options, X-Content-Type-Options y Referrer-Policy en todas las respuestas HTML del Worker.
- [BUG-PYTHON] En `scripts/sync_coaching_engine.py`, corregir `newest_date='2026-11-15'` por la fecha actual dinámica (`datetime.now().strftime('%Y-%m-%d')`) y añadir timeouts con backoff en las peticiones a Intervals.icu.

### R2. Ergonomía de Gimnasio, UI/UX y Rendimiento Frontend (Fase 2)
- Trasladar los steppers táctiles de gimnasio (botones ergonómicos ≥44px para `+2.5 kg`, `-2.5 kg`, `+1 rep`, `-1 rep`) del prototipo (`prototype/index.html`) a producción en `cloudflare/src/index.ts`.
- Integrar temporizador de descanso (Rest Timer) con opciones de `90s` y `2m` y alerta visual/táctil entre series.
- Debounce de 600 ms y SafeStorage: Implementar guardado diferido en inputs con indicador visual de estado (`🟢 Sincronizado en KV` / `🟡 Guardando...`).
- Header móvil compacto: Reducir altura de 80px a 52px en móvil, eliminando botones redundantes ya accesibles en el dock inferior.
- Widget Táctico T-12 Cross del Soto: Añadir tarjeta destacada con cuenta atrás, recordatorio de clavos 6-9 mm y objetivo de ritmo a 3:30/km.
- Simplificación de historial: Concentrar las 8 semanas en las 4 más recientes optimizando contraste tipográfico (`#C4B9C8`).
- Safe-area insets: Aplicar `env(safe-area-inset-bottom)` en el dock móvil para dispositivos móviles modernos.

### R3. Persistencia en la Nube y PWA Offline Total (Fase 3)
- Endpoints de lectura en KV: Implementar `GET /api/get_gym_session` y `GET /api/get_profile` para sincronización bidireccional entre móvil y PC.
- Service Worker cache-first: Registrar `/sw.js` para funcionamiento 100% offline en pista o gimnasio sin cobertura de datos.
- Handler `scheduled`: Exportar función `scheduled(controller, env, ctx)` en el Worker para ejecutar el ciclo Cron cada 4 horas y notificar nuevos entrenamientos vía Telegram.

### R4. Verificación, Auditoría Integral y Despliegue en Producción
- Ejecutar y revalidar punto por punto cada elemento de la auditoría usando tests automatizados con Playwright y pytest (`scripts/test_prototype_v10.py`, `tests/test_audit_suite.py` y suites complementarias).
- Desplegar la versión final en Cloudflare Workers mediante `wrangler deploy` una vez aprobados todos los tests.


## 2026-11-16T15:32:19Z

Resume work at c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach. State folder: c:\Users\carlo\OneDrive\Documentos\Proyectos\aegis-coach\.agents\teamwork\orchestrator_1_gen2. Your parent is 67abb764-fe7b-479a-8ef1-81517ed8e0d4.
Generation 2 Project Orchestrator missions:
1. Complete gate sign-off for Milestone 3 (run/evaluate verification agents or auditor check, update GATE_STATUS.md, and mark M3 DONE in PROJECT.md).
2. Execute Milestone 4 (M4: Verificación Integral, Playwright UI Tests & Despliegue en Producción Cloudflare Workers via `npx wrangler deploy`).
3. Smoke test the live Cloudflare deployment at `https://aegis-intervals-sync.uranuslabs.workers.dev` to ensure HTTP 200, security headers, PWA offline manifest & /sw.js, and API security.
4. Run the final Forensic Integrity Audit for the completed system.
5. Report final results and completion directly to parent/user.
