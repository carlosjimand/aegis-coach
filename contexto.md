# DOCUMENTO MAESTRO DE CONTEXTO: "AEGIS COACH"
**Proyecto:** Agente de IA / Entrenador Personal Autónomo para Alto Rendimiento y Rehabilitación. **Fecha de Actualización:** Agosto 2026.
## 1. Perfil del Atleta y Fisiopatología
* **Datos Demográficos:** 23 años, 173 cm, 58 kg.
* **Historial Deportivo:** Corredor de 800m (Marca Personal: 1:54.51). Perfil explosivo, alta predominancia de fibras rápidas (Tipo IIa/IIx). Transición a Trail Running y rutas exigentes de montaña, con interés en carreras populares de asfalto/pista.
* **Historial Lesivo:** 
    * Septiembre 2025: Intento de vuelta, molestias generales.
    * Febrero 2026: Retorno fuerte al Trail Running.
    * Mayo 2026: Rotura de unión miotendinosa del isquiotibial proximal tras un sprint.
    * Junio/Julio 2026: Recaída/tirón agudo jugando al fútbol (impacto en fase elástica sin preparación previa excéntrica).
    * Agosto 2026: Vuelta actual a la carrera continua con buenas sensaciones.
* **Objetivo Médico/Deportivo:** Fortalecer la cadena posterior (HSR, excéntricos, isometría) para erradicar las recaídas y automatizar la planificación del entrenamiento mediante inteligencia artificial.
## 2. Tecnologías Evaluadas (Adoptadas y Descartadas)
### Plataformas de Ingesta de Datos Deportivos
* **Garmin Connect API (Oficial):** ❌ Descartada. Requiere licencias comerciales enterprise B2B; imposible para desarrolladores indie/SaaS iniciales.
* **Strava API:** ⚠️ Descartada para el core. Solo lectura post-entreno. No da datos de VFC (HRV) matutina, sueño ni permite subir entrenamientos estructurados al reloj.
* **Intervals.icu API:** ✅ Adoptada. Gratuita, API REST abierta, lee HRV, sueño, calcula CTL/ATL (carga aguda/crónica) y permite escritura bidireccional (subir rutinas al reloj Garmin).
* **python-garminconnect (GitHub):** ✅ Opción en reserva. Emula la app móvil para login directo sin API comercial.
### Modelos de Inteligencia Artificial (LLMs)
* **Llama-3.2-3B / Modelos locales pequeños:** ❌ Descartados. El análisis del proyecto "Carson" demostró que fallan al estructurar JSON complejos y sus prescripciones son genéricas. Peligroso para readaptación de lesiones.
* **GPT-4o-mini / Claude 3.5 Sonnet / DeepSeek V3:** ✅ Adoptados. Bajísimo coste vía API (o local en modelos de 14B+ si hay hardware), razonamiento lógico superior, adherencia estricta a RAG médico.
### Infraestructura y Conectividad
* **Port Forwarding / IPs Públicas:** ❌ Descartadas. Riesgo de seguridad en redes domésticas.
* **Cloudflare Tunnels:** ✅ Adoptado. Permite recibir Webhooks de Telegram y de Intervals.icu en un servidor local (n8n o FastAPI) de forma segura y gratuita con HTTPS.
## 3. Arquitecturas Estudiadas
### Opción 1: El Sistema MVP Ágil (Enfoque "Carson 2.0")
* **Stack:** n8n (orquestador visual) + Telegram Bot + Intervals.icu API + GPT-4o-mini + Cloudflare Tunnels.
* **Flujo:** A las 08:00, n8n lee el HRV de Intervals. Telegram pregunta el dolor de isquio (0-10). GPT-4 genera entreno de Trail/Fuerza en base a las notas Obsidian Markdown. n8n lo envía al Garmin.
* **Pros:** Listo en 48 horas. UI familiar (chat).
* **Contras:** Poco escalable si se quiere vender a miles de usuarios.
* **Coste:** ~2-5€/mes (Costes de LLM API y VPS básico, o 0€ si es en PC local).
### Opción 2: SaaS Escalable (Web App Multi-Usuario)Stack: Next.js + FastAPI + Supabase (PostgreSQL + pgvector).
* **Flujo:** Plataforma web donde los usuarios hacen login, vinculan su Strava/Garmin y ven gráficos interactivos y chatean con el agente.
* **Pros:** Altamente monetizable (ej. 15€/mes). Base de datos robusta.
* **Contras:** Semanas de desarrollo. Mantenimiento de infraestructura y pasarelas de pago.
* **Coste:** 0-15€/mes inicial (Free Tiers).
### Opción 3: Agentes Autónomos y Frameworks de Orquestación
* **Stack:** Antigravity / OpenHands / OpenClaw / Hermes Agent + Graphify (Knowledge Graphs).
* **Flujo:** Agentes que operan en local, analizan GitHub buscando scripts de automatización, leen tu bóveda de Obsidian y autoejecutan código Python para programar tus entrenos.
* **Pros:** Automatización extrema, privacidad total (self-hosted).
* **Contras:** Requiere hardware local potente o VPS dedicado; mayor latencia de respuesta.