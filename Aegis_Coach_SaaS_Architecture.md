# AEGIS COACH: Plataforma SaaS de Entrenamiento IA (Arquitectura de Portfolio)

## 1. La Visión y el Objetivo Final (The "Endgame")
El objetivo ha evolucionado de un simple bot personal a un **Producto SaaS Multi-Tenant (B2C) de élite**. 
No es solo un script para un dolor de isquios; es un **Entrenador Físico y Médico de Inteligencia Artificial disponible 24/7**, capaz de gestionar a múltiples atletas (clientes).

**Características del Producto Final:**
* **Accesibilidad Total:** Funciona 100% en Telegram. Si un usuario es avanzado, sincroniza su Garmin/Intervals.icu vía API. Si es principiante, simplemente chatea: *"Hoy corrí 5km por la montaña en 30 minutos y luego hice pesas"*, y la IA procesa, estructura y guarda el progreso automáticamente.
* **Inteligencia Basada en Ciencia (RAG):** El cerebro no inventa; consulta una base de datos vectorial con papers reales de biomecánica, trail running, hipertrofia y rehabilitación.
* **Onboarding Visual (Telegram WebApp):** Un proceso de alta conversión y fricción cero, con una interfaz web (UI) incrustada en Telegram.
* **Portfolio-Ready:** Es un proyecto que demuestra dominio en *Multi-Agent Swarm architectures*, *Retrieval-Augmented Generation (RAG)*, y *State Machines* asíncronas.

---

## 2. El Stack Tecnológico (Infraestructura Local & Oracle Cloud)

* **Orquestador Principal:** `n8n` (Self-hosted en Oracle).
* **Motor Base de Datos (Memoria e Identidad):** `PostgreSQL`. 
  * Tabla `users`: Control de identidad, tokens, estado del onboarding, y perfil atlético (objetivos, lesiones).
  * Tabla `workouts`: Registro del historial de entrenamientos de cada atleta (para quienes no usen Intervals.icu).
* **Base de Datos Vectorial (El "Cerebro RAG"):** `Qdrant` (ideal para Docker ARM).
  * Almacena *Chunks* (fragmentos) de artículos científicos etiquetados por metadatos (ej: `disciplina: trail`, `lesion: rodilla`).
* **UI de Onboarding:** `Next.js` o `React` estático, servido como Telegram Web App.
* **Modelos LLM:** 
  * `GPT-4o-mini` (para tareas de enrutamiento rápido, parsing de entrenamientos manuales, y small-talk).
  * `GPT-4o` o `Claude 3.5 Sonnet` (para el diagnóstico médico, planificación del mesociclo, y búsqueda RAG profunda).

---

## 3. Arquitectura "Multi-Agent Swarm" (Inspirado en Hermes)
En lugar de un bot monolítico que se confunde, usaremos el patrón **"Swarm" (Enjambre)**. n8n actuará como el router principal que despierta al agente adecuado.

1. **Agente Enrutador (El Recepcionista):** Recibe tu mensaje de Telegram y clasifica tu intención (Duda Médica, Registro de Entreno, Charla General).
2. **Agente Médico / Fisioterapeuta:** Se activa si detecta palabras de dolor o lesión. Tiene acceso exclusivo a la herramienta `RAG_Qdrant_Search` filtrada por la colección de lesiones.
3. **Agente Planificador (Fisiólogo):** Se activa para generar la rutina semanal. Tiene acceso a la herramienta `Intervals_Sync` y al `Postgres_Profile_Reader`.
4. **Agente Data-Entry (Parseador):** Se activa cuando el usuario manda un entreno manual en texto o audio. Su única función es extraer métricas (distancia, RPE, tiempo) e insertarlas en Postgres o Intervals, sin dar consejos.

---

## 4. El "Viaje del Usuario" (User Journey)

### A. Fase 1: Adquisición & Onboarding (Telegram WebApp)
1. El atleta busca el bot en Telegram y pulsa `/start`.
2. El bot responde con un mensaje premium y un gran botón incrustado: **"🏃‍♂️ Configurar mi Entrenador"**.
3. Se abre un mini-formulario visual (WebApp):
   * *Paso 1:* Nivel actual, deportes (Trail, Gym, Asfalto).
   * *Paso 2:* Lesiones históricas.
   * *Paso 3:* Modalidad de trackeo: [ ] Soy Pro (Conectar Intervals.icu) / [ ] Soy Casual (Le contaré mis entrenos al bot por chat).
4. La WebApp envía los datos a un Webhook de n8n, el cual guarda todo en Postgres y pone el estado del usuario en `ACTIVE`.

### B. Fase 2: Proactividad Diaria (Cron Jobs)
1. **Cron 08:00 AM:** n8n busca todos los usuarios en `ACTIVE`. Envía el prompt de buenos días personalizado según si les toca entrenar o descansar.
2. **Manejo del Estado:** Si el usuario no responde, la base de datos registra un `MISSED_CHECKIN` para no agobiarlo.

### C. Fase 3: Feedback y RAG en Acción
1. **Input del Usuario:** *"Hoy me dolía el tendón de aquiles al hacer cuestas."*
2. **Proceso del Swarm:**
   * El Enrutador detecta "dolor de aquiles".
   * Llama al **Agente Médico**.
   * El Agente lee el perfil en Postgres y ve que el usuario hace Trail.
   * Hace una query a **Qdrant**: `"manejo conservador tendinopatía aquiles en corredores de montaña"`.
   * El Agente estructura la respuesta basándose 100% en la ciencia extraída de Qdrant.
   * El Agente cambia temporalmente el plan semanal y manda un mensaje reconfortante y científico al usuario.

---

## 5. Hoja de Ruta de Implementación (Fases del Portfolio)

* **Fase 1 (MVP RAG & Infraestructura):** Levantar Qdrant y Postgres en el Docker de Oracle. Crear el flujo RAG en n8n para ingestar tus primeros PDFs (Trail y Rehabilitación).
* **Fase 2 (Swarm Básico):** Modificar el workflow actual para implementar el "Router" (Enrutador) y separar al Agente Médico del Planificador.
* **Fase 3 (Democratización Casual):** Implementar el parsing de texto plano para que el bot extraiga y guarde entrenos narrados por chat sin necesitar APIs técnicas.
* **Fase 4 (WebApp Onboarding):** Programar el mini-frontend incrustado en Telegram para la captación visual de nuevos atletas.

> NOTA: Esta arquitectura garantiza que Aegis Coach sirva para ti mismo hoy, pero esté construido sobre cimientos empresariales (Multi-tenant, Swarm AI, RAG) ideales para mostrar en tu CV/Portfolio como producto SaaS de Inteligencia Artificial.
