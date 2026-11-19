# PLAN MAESTRO DE INGENIERÍA: AEGIS COACH (CTO Blueprint)

Como CTO, mi primera directiva es no dar nada por sentado. Que tengamos un servidor en Oracle y un bot de Telegram funcionando no significa que sea la arquitectura correcta para escalar un producto B2C de Inteligencia Artificial que resuelva el problema real del usuario.

## 1. El Problema Real del Usuario
El atleta amateur o semi-profesional (ya sea de trail, asfalto o gimnasio) se enfrenta a tres problemas fundamentales:
1. **Desconexión de datos:** Los planes estáticos de PDF o apps genéricas no se adaptan a la fatiga real, a un mal sueño, o a un dolor repentino (ej. isquiotibiales).
2. **Falta de razonamiento clínico:** Los entrenadores personales humanos son caros ($100-$300/mes) y no están disponibles 24/7 para pivotar una sesión 15 minutos antes de empezar.
3. **Fricción de uso:** Las apps de fitness actuales requieren rellenar demasiados formularios, lo cual mata la retención. 

**La Solución:** Un "Cerebro Atlético" proactivo, con contexto médico, que viva en el bolsillo del usuario y consuma la mínima fricción posible, basando sus decisiones en literatura científica real (RAG).

---

## 2. Orquestación del Equipo de Investigación (Subagentes)
Para no sesgarnos hacia "lo que ya sabemos", voy a desplegar un escuadrón de 4 subagentes (IA) especializados. Su misión será peinar el estado del arte tecnológico y de mercado.

### 🕵️‍♂️ Subagente 1: Analista de Producto y UX (Product/UX Lead)
* **Misión:** Decidir la mejor interfaz para resolver el problema de fricción. 
* **Investigación:** ¿Deberíamos hacer una App Nativa (React Native/Flutter)? ¿Una WebApp PWA (Next.js)? ¿O Telegram/WhatsApp bots son el futuro del B2C por la retención? ¿Cómo manejamos el "Onboarding"?

### 🏗️ Subagente 2: Arquitecto de Software Cloud (Lead Backend)
* **Misión:** Definir la infraestructura más robusta y escalable (presupuesto abierto).
* **Investigación:** Comparar Serverless (Vercel, AWS Lambda) vs Servidores Dedicados (Oracle VPS, DigitalOcean). Comparar Backend-as-a-Service (Supabase, Firebase) vs bases de datos autogestionadas. Evaluar sistemas asíncronos y colas de mensajes (RabbitMQ, Redis) para los crons masivos.

### 🧠 Subagente 3: Ingeniero de Machine Learning & IA (Head of AI)
* **Misión:** Diseñar el "Cerebro" y evitar alucinaciones.
* **Investigación:** Analizar frameworks de agentes (LangGraph, CrewAI, AutoGen, n8n avanzado). Comparar bases de datos vectoriales (Pinecone, Weaviate, Milvus, Qdrant). Estudiar arquitecturas RAG avanzadas (GraphRAG, Reranking, Hybrid Search) aplicadas a papers médicos.

### 🌐 Subagente 4: Investigador OSINT (Tech Scavenger)
* **Misión:** Robar como un artista. Buscar en GitHub, YouTube, Reddit y Twitter proyectos open-source de IA deportiva, asistentes médicos de IA, y frameworks de los que podamos clonar arquitecturas o inspiración.

---

## 3. Hoja de Ruta del Proyecto (End-to-End)

Una vez que el equipo de subagentes termine su investigación, seguiremos esta estricta metodología de ingeniería:

### Fase 1: Investigación y Síntesis Arquitectónica (Actual)
Despliegue del equipo. Debate de resultados. Elaboración del documento de arquitectura definitivo donde elegiremos el Stack Tecnológico (UI, Cloud, DB, AI Framework).

### Fase 2: Diseño de Producto y Flujos (Wireframing)
Antes de escribir una línea de código, mapearemos los flujos lógicos (Máquinas de Estado, UI/UX, diagramas de secuencia de las llamadas a LLMs) basándonos en los hallazgos de UX.

### Fase 3: Construcción del MVP (Minimum Viable Product)
Desarrollo de la arquitectura base elegida. Conexión de las APIs, base de datos vectorial, y sistema de agentes. Se limitará a 1 solo deporte (ej. Running) para acotar la complejidad.

### Fase 4: Testing y QA (Aseguramiento de Calidad)
Creación de "evaluadores de IA" (LLMs que juzgan las respuestas de otros LLMs) para asegurar que el bot nunca recomiende algo lesivo. Pruebas de estrés de la base de datos de usuarios.

### Fase 5: Validación de Producto (Beta Privada)
Despliegue a un grupo reducido de atletas. Medición de retención, engagement, y análisis de logs para ver dónde se confunde la IA.

### Fase 6: Escalado e Iteración
Integración de pasarelas de pago (Stripe). Ampliación de la base RAG a nuevos deportes (ciclismo, fuerza). Optimización de costes de inferencia (cambiar a modelos más baratos u open-source para tareas sencillas).

---

> **Directiva del CTO:** Este archivo servirá como nuestro "Manifiesto". Una vez apruebes este plan de acción de investigación, ejecutaré el comando para lanzar a los 4 subagentes a que destripen internet y nos traigan los datos crudos y contrastados.
