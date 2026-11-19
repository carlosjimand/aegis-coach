# 🗺️ Hoja de Ruta & Mejoras de Interactividad — Aegis Coach

Este documento recopila las próximas funcionalidades planificadas para evolucionar Aegis Coach, pasando de una PWA de consulta y registro de gimnasio a un ecosistema totalmente interactivo y bidireccional.

---

## 1. Fase 1: Interactividad en Carrera y Marcado de Sesiones (Próxima)

### A. Botón de Completado / Check-Off en Vivo
- **Objetivo:** Permitir a Carlos pulsar un botón de *"Marcar como Completado"* en la tarjeta de la sesión de hoy o en cualquier día del calendario.
- **Mecánica:**
  - Envío automático de un `POST /api/toggle_day_completion` a Cloudflare KV con debounce y feedback visual (cambio de chip a verde *"Completado"*).
  - Si la sesión ya se registró en Garmin / Intervals.icu, se vincula automáticamente mostrando el ritmo y pulso real alcanzado frente al ritmo objetivo prescrito.

### B. Ajuste Rápido de Ritmos y Notas Diarias
- **Objetivo:** Permitir a Carlos o a los agentes modificar sobre la marcha las notas de una sesión (ej: "Mover las series del miércoles al jueves por viaje a Madrid") directamente desde la interfaz móvil sin necesidad de editar ficheros JSON manualmente.

---

## 2. Fase 2: Integración Directa con la API de Garmin (Métricas de Recuperación)

### A. Telemetría de Recuperación Matutina
- **Objetivo:** Inyectar en el Dashboard los 3 biomarcadores clave de recuperación de Garmin:
  1. **Puntuación de Sueño (0-100)** y horas de descanso profundo.
  2. **HRV Nocturno (ms)** y estado (*Balanced / Unbalanced*).
  3. **Body Battery al Despertar (0-100)**.
- **Implementación:**
  - Módulo `scripts/sync_garmin_health.py` que consume la nueva **Garmin Connect Personal API** (`personal.connectapi.garmin.com`) o la librería `python-garminconnect`.
  - Tarjeta *"Biomarcadores de Recuperación"* en el Dashboard con semáforo inteligente para alertar al Agente Fisiólogo si Carlos amanece con fatiga antes de series clave.

---

## 3. Fase 3: Analítica Avanzada de Fuerza y Gimnasio

### A. Proyección de 1RM y Sobrecarga Progresiva
- **Objetivo:** Graficar la evolución de peso movido en los ejercicios principales de blindaje (Box Squat, Hip Thrust, Jalón Agarre Cerrado V, Remo Dorian).
- **Mecánica:**
  - Cálculo automático de 1RM estimado mediante la fórmula de Brzycki / Epley a partir de las series registradas en `gym_session_YYYY-MM-DD`.
  - Comparativa con las semanas previas para asegurar que no haya pérdida de rigidez miotendinosa (*tendon stiffness*) durante el tapering de competiciones.

---

## 4. Fase 4: Modo Coach Colaborativo Multi-Agente en Cloudflare

### A. Panel de Notas del Entrenador
- **Objetivo:** Un bloque colapsable donde los dos agentes de cabecera (Agente A: Fisiólogo y Agente B: S&C) dejen sus observaciones técnicas de la semana para que Carlos las lea desde el móvil antes de entrenar.
- **Persistencia:** Almacenado en la clave `coach_notes` de Cloudflare KV, actualizable tanto desde Antigravity como desde Telegram.
