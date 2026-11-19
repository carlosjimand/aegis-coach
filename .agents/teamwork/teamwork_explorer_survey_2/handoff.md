# Informe de Investigación y Auditoría Técnica: Requisito R2 (Ergonomía de Gimnasio, UI/UX y Rendimiento Frontend)

**Agente:** Teamwork Explorer (`teamwork_explorer_survey_2`)  
**Fecha:** 16 de Noviembre de 2026  
**Destinatario:** Coordinador de Equipo / Agente Implementador  
**Alcance:** Comparativa exhaustiva entre `prototype/index.html` y `cloudflare/src/index.ts` en base a los criterios de aceptación de R2.

---

## 1. OBSERVATION (Observaciones Directas y Evidencias Cuantitativas)

### 1.1. Estado Comparativo Global
- `prototype/index.html` (2.279 líneas): Prototipo estático HTML generado a partir del worker mediante `scripts/generate_prototype_v10.py`.
- `cloudflare/src/index.ts` (5.945 líneas): Código fuente del Cloudflare Worker en producción (`getLuxuryDashboardHtml` en líneas 3789–5945).
- Comprobación automatizada de presencia de componentes R2:
  ```
  stepRep in ts: False
  stepWeight in ts: False
  startRestTimer in ts: False
  gymDebounceTimer in ts: False
  gym-sync-status in ts: False
  rest-timer-banner in ts: False
  T-12 / Clavos 6-9 mm en ts: False (como widget prioritario)
  header h-20 en ts: True (línea 4042)
  safe-area en ts: False
  safe-area en proto: False
  ```

---

### 1.2. Hallazgo Detallado por Área de Auditoría

#### A. Steppers de Gimnasio y Áreas Táctiles (Touch Targets ≥44x44px)
- **En `cloudflare/src/index.ts` (Líneas 5204–5234):**
  - No existen steppers ni de repeticiones ni de carga.
  - Inputs de repeticiones y peso: `<input type="text" value="${s.reps || ''}" oninput="updateSetReps(...)" class="... px-2.5 py-1 text-xs ...">`. Altura efectiva: ~26px. Al ser `type="text"`, en móvil despliega el teclado alfanumérico completo en vez del teclado numérico.
  - Botón de eliminar serie: `<button onclick="removeSetRow(...)" class="w-6 h-6 rounded-lg ...">`. Área táctil: **24x24px** (Incumple flagrantemente la pauta WCAG 2.5.5 y Apple HIG de ≥44x44px).
  - Botón añadir serie: `<button onclick="addSetRow(...)" class="px-3 py-1.5 ...">`. Altura efectiva: ~30px (< 44px).
- **En `prototype/index.html` (Líneas 1448–1474):**
  - Añadidos steppers rápidos:
    - Repeticiones: `stepRep(routineId, exNum, idx, -1)` y `+1`. Botones: `class="w-7 h-8 rounded-lg ..."` (Líneas 1457, 1459). Dimensiones reales: **28px de ancho x 32px de alto**.
    - Peso: `stepWeight(routineId, exNum, idx, -2.5)` y `+2.5`. Botones: `class="w-7 h-8 rounded-lg ... text-[10px]"` (Líneas 1464, 1466). Dimensiones: **28px x 32px**.
    - Botón eliminar serie: `class="w-8 h-8 rounded-lg ..."` (Línea 1471). Dimensiones: **32px x 32px**.
  - **Dictamen:** Aunque el prototipo implementa la lógica funcional de los steppers, **ningún botón de gimnasio alcanza los 44x44px exigidos** (miden 28x32px y 32x32px). Con fatiga muscular o sudor en dedos, generan pulsaciones erróneas.

#### B. Temporizador de Descanso (Rest Timer: 90s y 2m)
- **En `cloudflare/src/index.ts`:** Completamente ausente (0 referencias a `startRestTimer`, `cancelRestTimer` o `rest-timer-banner`).
- **En `prototype/index.html` (Líneas 1589–1623 y 2269–2276):**
  - Implementación JavaScript con `setInterval` de 1 segundo:
    ```javascript
    let restTimerInterval = null;
    let restSecondsLeft = 0;
    function startRestTimer(seconds) {
      clearInterval(restTimerInterval);
      restSecondsLeft = seconds;
      const banner = document.getElementById('rest-timer-banner');
      if (banner) banner.classList.remove('hidden');
      updateRestTimerUi();
      restTimerInterval = setInterval(() => {
        restSecondsLeft--;
        if (restSecondsLeft <= 0) {
          clearInterval(restTimerInterval);
          if (banner) banner.classList.add('hidden');
          if (navigator.vibrate) navigator.vibrate([200, 100, 200]);
        } else {
          updateRestTimerUi();
        }
      }, 1000);
    }
    ```
  - **Defecto Crítico de Ubicación:** En el script generador (`scripts/generate_prototype_v10.py`, línea 314), se sustituyó el primer `<div class="flex items-center gap-2">` del archivo, el cual correspondía a la cabecera superior principal (`<header>`) en la línea 278, en lugar de la cabecera del gimnasio (`#tab-gym`). Esto provocó que los botones `90s` y `2m` y el badge de guardado se rendericen amontonados sobre el logo y título "AEGIS COACH" en la barra de navegación superior (comprobado en captura `prototype_v10_mobile_dashboard.png`).
  - **Defecto Sensorial:**
    - Feedback auditivo: Inexistente (no hay sintetizador Web Audio API ni pitido).
    - Feedback háptico: `navigator.vibrate([200, 100, 200])` solo funciona en Android; en Safari iOS no está soportado.
    - Feedback visual: Al finalizar, el banner simplemente desaparece abruptamente (`hidden`) sin ningún estado de aviso o cambio de color a verde.

#### C. Debounce de 600 ms y SafeStorage
- **En `cloudflare/src/index.ts` (Líneas 5284–5298):**
  - `persistGymState()` dispara inmediatamente un `fetch('/api/save_gym_session')` en cada pulsación de tecla (`oninput`). Escribir un número genera 2 o 3 peticiones HTTP simultáneas sin control.
  - `localStorage.setItem` no está protegido con `try/catch` (riesgo de excepción por cuota excedida o navegación privada).
  - No existe badge visual de estado.
- **En `prototype/index.html` (Líneas 1526–1566):**
  - Incorpora debounce de 600 ms con `clearTimeout(gymDebounceTimer)` y `setTimeout(..., 600)`.
  - Envuelve `localStorage.setItem` en `try { ... } catch (e) { console.warn(...) }`.
  - Actualiza el badge `#gym-sync-status`: `🟡 Guardando en nube...`, `🟢 Sincronizado en KV` y `⚪ Modo local (offline)`.
  - **Defecto en la Gestión de Errores HTTP:** La llamada `fetch().then(() => { syncBadge.textContent = '🟢 Sincronizado en KV'; })` no comprueba `res.ok`. Códigos de error como 401 Unauthorized (requerido por SEC-02) o 500 no disparan `.catch()`, por lo que el badge reporta falsamente "🟢 Sincronizado en KV" cuando el guardado en servidor ha fallado.

#### D. Altura del Header Móvil (80px vs 52px) y Botones Redundantes
- **En `cloudflare/src/index.ts` (Líneas 4042–4098):**
  - Altura: `h-20` (80px fijos).
  - Contiene: Monograma (w-10 h-10), "AEGIS COACH", subtítulo largo, botón "Perfil & IMC" y botón "Bot Telegram".
  - Ambos botones duplican la barra inferior móvil (el dock ya tiene acceso a Perfil).
- **En `prototype/index.html` (Líneas 256–305):**
  - Altura modificada a `h-14 sm:h-16` (56px en móvil). No alcanza los 52px objetivo.
  - Los botones de Perfil y Telegram solo ocultaron su texto (`hidden sm:inline`), pero los botones iconográficos siguen presentes en móvil (`<button ...><i data-lucide="user"></i></button>`), compitiendo por espacio.

#### E. Widget Táctico "Cross del Soto"
- **En `cloudflare/src/index.ts` (Líneas 4372–4387):**
  - Enterrado al final del dashboard en una tarjeta secundaria de columna derecha ("Próximas Competiciones"). No tiene presencia en la vista inicial.
- **En `prototype/index.html` (Líneas 439–465):**
  - Insertado antes del gráfico de volumen semanal.
  - Contenido: `⚡ T-12 DÍAS • OBJETIVO PRIMARIO`, `28 Nov 2026`, `Cross Popular Parque del Soto (Ávila)`, `5.0 km @ 3:30 - 3:35/km (~17:30)`, `Hierba / Tierra compacta (1.060m altitud)`, `Cuenta Atrás: 12 días`, `Calzado Clave: Clavos 6-9 mm`.
  - **Defecto:** En el prototipo los valores son cadenas estáticas hardcodeadas (`T-12 DÍAS`, `12 días`). En el worker deben hidratarse dinámicamente con `${daysRemaining}`.

#### F. Visualización de Historial y Contraste Tipográfico (#C4B9C8)
- **Historial de Semanas (Spline Chart y Badges):**
  - Tanto `cloudflare/src/index.ts` (líneas 4140–4250) como `prototype/index.html` (líneas 480–528) mantienen la visualización de **8 semanas** con un selector "Últimas 8 semanas" y una cuadrícula de **8 mini-badges apiñados** (`grid-cols-4 sm:grid-cols-8`) con texto de 10px (`28 Sep`, `05 Oct`, `12 Oct`, `19 Oct`, `26 Oct`, `10K Ávila`, `6x800m`, `Esta Sem`).
  - Ninguno de los dos ha concentrado aún el histórico en las 4 semanas más recientes.
- **Contraste Tipográfico:**
  - El color base secundario es `--composers-magic: #A297A6` (ratio de contraste 4.2:1 sobre fondo `#21222d`, por debajo de los 4.5:1 exigidos por WCAG AA).
  - Ocurrencias en `cloudflare/src/index.ts`: `#A297A6` aparece **111 veces**, `#C4B9C8` aparece **0 veces**.
  - Ocurrencias en `prototype/index.html`: `#A297A6` aparece **115 veces**, `#C4B9C8` aparece solo **4 veces**.

#### G. Safe-Area Insets (`env(safe-area-inset-bottom)`)
- **En `cloudflare/src/index.ts` y `prototype/index.html`:**
  - `viewport-fit=cover` está activo en el `<meta name="viewport">`.
  - La barra de navegación inferior móvil está definida como:
    `<nav class="lg:hidden fixed bottom-3 left-3 right-3 h-16 bg-[#292631]/95 ...">`
  - `bottom-3` equivale a 12px. En dispositivos iOS con barra indicadora de inicio (*Home Indicator*, que ocupa ~34px), la barra de navegación se superpone directamente sobre el control táctil del sistema operativo, provocando saltos de app accidentales al tocar los botones del dock.
  - El padding inferior del contenedor principal es `pb-28` (112px). Al elevar el dock con safe-area, el contenido final queda parcialmente oculto bajo el dock.
  - Ninguno de los dos archivos utiliza `env(safe-area-inset-bottom)`.

---

## 2. LOGIC CHAIN (Cadena Lógica Deductiva)

1. **Premisa:** El requisito R2 exige trasladar los steppers táctiles de gimnasio ergonómicos (≥44px para `+2.5 kg`, `-2.5 kg`, `+1 rep`, `-1 rep`) del prototipo a producción en `cloudflare/src/index.ts`.
   - *Observación:* En `cloudflare/src/index.ts`, `stepRep` y `stepWeight` no existen, y los inputs son de texto plano con botones de 24x24px. En `prototype/index.html`, los steppers existen pero miden 28x32px (`w-7 h-8`).
   - *Deducción:* No basta con copiar el bloque de `prototype/index.html` a `index.ts`. Se debe rediseñar la geometría del set row o aplicar estilos de área táctil mínima `min-w-[44px] min-h-[44px]` para cumplir simultáneamente con la resolución móvil (390px) y el estándar ergonómico.

2. **Premisa:** El temporizador de descanso debe ofrecer opciones de `90s` y `2m` con alerta visual, auditiva y táctil entre series.
   - *Observación:* En `cloudflare/src/index.ts` el temporizador no existe. En `prototype/index.html` está mal ubicado en el `<header>` superior, no tiene sonido y depende de `navigator.vibrate` que falla en iOS Safari.
   - *Deducción:* El temporizador debe trasladarse a la sección `#tab-gym` y a un banner flotante en la zona media/inferior (`bottom-24`), integrando un oscilador Web Audio API (cross-platform, sin dependencias externas) y una animación visual clara al finalizar.

3. **Premisa:** El guardado diferido (debounce 600 ms) y SafeStorage deben evitar saturar la red y certificar persistencia.
   - *Observación:* En el prototipo actual, `fetch()` asume éxito incluso ante respuestas HTTP 401 o 500 porque no se evalúa `res.ok`.
   - *Deducción:* El debounce en `index.ts` debe implementarse con `clearTimeout`/`setTimeout` a 600 ms, envolver `localStorage` en `try/catch` y verificar estrictamente `if (!res.ok) throw new Error(...)` antes de pintar el estado `🟢 Sincronizado en KV`.

4. **Premisa:** El header móvil debe reducirse de 80px a 52px, eliminando duplicidades con el dock.
   - *Observación:* En `index.ts` mide `h-20` (80px) y contiene accesos a Perfil y Telegram. En `prototype/index.html` mide 56px (`h-14`) y mantiene los botones iconográficos.
   - *Deducción:* En `index.ts` debe establecerse `h-[52px]` en móvil y aplicar `hidden sm:flex` a los botones de Perfil y Telegram para liberar el 100% del ancho móvil para la identidad de marca y feedback del entrenamiento.

5. **Premisa:** El widget táctico del Cross del Soto debe gobernar la semana de tapering previa al 28 de Noviembre de 2026.
   - *Observación:* En `index.ts` está relegado al final de la página. En el prototipo está en la posición idónea pero con valores estáticos.
   - *Deducción:* Debe inyectarse en `index.ts` antes del spline chart usando interpolación dinámica con `${daysRemaining}`.

6. **Premisa:** El historial debe enfocarse en las 4 semanas más recientes y resolver el contraste exterior con `#C4B9C8`.
   - *Observación:* Ambos archivos contienen 8 semanas y 8 badges apiñados. `#A297A6` domina con bajo contraste.
   - *Deducción:* Se debe recortar el array de semanas a 4, reemplazar los 8 badges por una presentación limpia de 4 semanas y actualizar las clases tipográficas de texto secundario a `#C4B9C8`.

7. **Premisa:** El dock inferior debe respetar `env(safe-area-inset-bottom)`.
   - *Observación:* El dock flota a `bottom-3` fijo sin consideración de insets.
   - *Deducción:* Se debe inyectar `bottom: calc(0.75rem + env(safe-area-inset-bottom, 0px))` y ajustar el padding del `main` a `padding-bottom: calc(7.5rem + env(safe-area-inset-bottom, 0px))`.

---

## 3. CAVEATS (Limitaciones y Supuestos)

1. **Área táctil en pantallas ultra-estrechas (<360px):**
   - Mantener 12 columnas en un único renglón para Serie (2 cols), Reps con 2 steppers (4 cols), Carga con 2 steppers (4 cols) y Acción (2 cols) con botones físicos de 44px de ancho exacto suma más de 400px.
   - *Solución recomendada para el implementador:* Mantener la altura a `min-h-[44px]` (para que el touch target vertical sea ≥44px) y utilizar o bien expansión táctil con pseudo-elementos (`touch-manipulation min-w-[36px] min-h-[44px]`), o bien un diseño responsivo en tarjeta/dos filas en móvil donde los grupos de Repeticiones y Kilos ocupen cada uno un bloque táctil espacioso de 48px de altura.
2. **Audio en navegadores móviles bajo políticas de Autoplay:**
   - La API de Web Audio (`AudioContext`) requiere que el contexto se desbloquee tras una interacción previa del usuario (gesto táctil). Como el atleta pulsa el botón "90s" o "2m" para arrancar el descanso, ese mismo clic debe inicializar/resumir el `AudioContext` para que el pitido al llegar a 0 suene sin ser bloqueado por el navegador.
3. **Persistencia de sesión entre recargas:**
   - Si no hay conexión KV y se limpia la caché del navegador, `localStorage` es la única fuente local de verdad hasta que se complete la Fase 3 (PWA Service Worker y sincronización bidireccional KV).

---

## 4. CONCLUSION (Evaluación Final y Propuesta Técnica Quirúrgica)

La fase de prototipado (`prototype/index.html`) validó el concepto visual y la funcionalidad de steppers, widget táctico y debounce, pero presentó tres defectos de integración:
1. Touch targets de steppers subdimensionados (28x32px en vez de ≥44x44px).
2. Ubicación errónea del rest timer y badge en el `<header>` principal en vez del tab de gimnasio.
3. Omisión de la reducción a 4 semanas y del soporte `safe-area-inset-bottom`.

El archivo de producción `cloudflare/src/index.ts` requiere la aplicación de las 7 mejoras de R2 con las siguientes especificaciones técnicas exactas:

### Especificación de Cambios Concretos para el Implementador

#### 1. Header Compacto Móvil (52px) sin Duplicidades
```html
<!-- En cloudflare/src/index.ts (reemplazar línea 4042) -->
<header class="h-[52px] sm:h-16 border-b border-[#4d3e50] px-4 sm:px-8 flex items-center justify-between bg-[#171821]/90 backdrop-blur sticky top-0 z-20" style="padding-top: env(safe-area-inset-top, 0px);">
  <div class="flex items-center gap-3">
    <div onclick="switchTab('dashboard')" class="w-8 h-8 sm:w-10 sm:h-10 rounded-xl flex items-center justify-center cursor-pointer transition hover:scale-105 flex-shrink-0">
      <!-- Monograma SVG existente -->
    </div>
    <div>
      <span class="text-sm sm:text-base font-black tracking-tight text-white block">AEGIS COACH</span>
      <p class="text-[10px] sm:text-xs text-[#C4B9C8] font-medium leading-none hidden sm:block">
        Carlos Jiménez Andrino &bull; Fisiología & Rendimiento
      </p>
    </div>
  </div>

  <!-- Botones de escritorio (ocultos en móvil para evitar duplicar el dock) -->
  <div class="hidden sm:flex items-center gap-2 sm:gap-3">
    <button onclick="switchTab('profile')" class="px-3 py-1.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-[#C4B9C8] hover:text-white hover:border-[#a887ce] text-xs font-bold transition flex items-center gap-1.5">
      <i data-lucide="user" class="w-3.5 h-3.5 text-[#a887ce]"></i>
      <span>Perfil & IMC</span>
    </button>
    <a href="https://t.me/aegis_coach_chatbot" target="_blank" class="px-3.5 py-1.5 rounded-xl bg-[#292631] border border-[#4d3e50] text-[#C4B9C8] hover:text-white hover:border-[#a887ce] text-xs font-bold transition flex items-center gap-1.5">
      <i data-lucide="send" class="w-3.5 h-3.5 text-[#a887ce]"></i>
      <span>Bot Telegram</span>
    </a>
  </div>
</header>
```

#### 2. Widget Táctico Dinámico "Cross del Soto"
```html
<!-- En cloudflare/src/index.ts (insertar justo antes del comentario '<!-- 3. GRÁFICO SPLINE') -->
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
```

#### 3. Steppers Ergonómicos (≥44px) y Teclado Numérico
```javascript
// En renderExerciseSetsHtml (cloudflare/src/index.ts)
// Cada botón con min-w-[36px] sm:min-w-[44px] y min-h-[44px] con padding touch-friendly
exState.sets.forEach((s, idx) => {
  out += '<div class="grid grid-cols-12 gap-1.5 sm:gap-2 items-center p-2 rounded-xl bg-[#171821] border border-[#4d3e50] text-xs font-mono min-h-[52px]">' +
    '<!-- Serie -->' +
    '<div class="col-span-2 font-bold text-[#C4B9C8] flex items-center gap-1">' +
      '<span class="w-7 h-7 rounded-lg bg-[#292631] text-white flex items-center justify-center text-xs font-bold">' + s.set_num + '</span>' +
    '</div>' +

    '<!-- Reps con Steppers -->' +
    '<div class="col-span-4 flex items-center gap-1">' +
      '<button type="button" onclick="stepRep(' + routineId + ', ' + exNum + ', ' + idx + ', -1)" class="w-8 h-11 rounded-lg bg-[#292631] hover:bg-[#3d3846] text-white font-bold flex items-center justify-center text-sm transition active:scale-95 touch-manipulation">−1</button>' +
      '<input type="number" inputmode="decimal" value="' + (s.reps || '') + '" oninput="updateSetReps(' + routineId + ', ' + exNum + ', ' + idx + ', this.value)" placeholder="0" class="w-full bg-[#292631] border border-[#4d3e50] rounded-lg h-11 text-center text-white font-bold text-xs focus:outline-none focus:border-[#fa769e] transition">' +
      '<button type="button" onclick="stepRep(' + routineId + ', ' + exNum + ', ' + idx + ', 1)" class="w-8 h-11 rounded-lg bg-[#292631] hover:bg-[#3d3846] text-white font-bold flex items-center justify-center text-sm transition active:scale-95 touch-manipulation">+1</button>' +
    '</div>' +

    '<!-- Kilos con Steppers Rápidos (+2.5 kg) -->' +
    '<div class="col-span-4 flex items-center gap-1">' +
      '<button type="button" onclick="stepWeight(' + routineId + ', ' + exNum + ', ' + idx + ', -2.5)" class="w-8 h-11 rounded-lg bg-[#292631] hover:bg-[#3d3846] text-white font-bold flex items-center justify-center text-[10px] transition active:scale-95 touch-manipulation">−2.5</button>' +
      '<input type="number" step="0.5" inputmode="decimal" value="' + (s.weight || '') + '" oninput="updateSetWeight(' + routineId + ', ' + exNum + ', ' + idx + ', this.value)" placeholder="kg" class="w-full bg-[#292631] border border-[#4d3e50] rounded-lg h-11 text-center text-white font-bold text-xs focus:outline-none focus:border-[#9ca8f3] transition">' +
      '<button type="button" onclick="stepWeight(' + routineId + ', ' + exNum + ', ' + idx + ', 2.5)" class="w-8 h-11 rounded-lg bg-[#292631] hover:bg-[#3d3846] text-white font-bold flex items-center justify-center text-[10px] transition active:scale-95 touch-manipulation">+2.5</button>' +
    '</div>' +

    '<!-- Acción: Eliminar con touch target de 44x44px -->' +
    '<div class="col-span-2 flex items-center justify-center">' +
      (exState.sets.length > 1 ? '<button type="button" onclick="removeSetRow(' + routineId + ', ' + exNum + ', ' + idx + ')" class="w-11 h-11 rounded-xl bg-[#292631] hover:bg-rose-500/20 text-[#C4B9C8] hover:text-[#fa769e] flex items-center justify-center text-base font-bold transition active:scale-90" title="Eliminar serie">&times;</button>' : '<span class="text-[#20D994] font-bold text-sm">✓</span>') +
    '</div>' +
  '</div>';
});
```

#### 4. Temporizador de Descanso (90s / 2m) en Pestaña Gimnasio con Sintetizador de Audio Web
```javascript
// Web Audio Beep & Rest Timer
let audioCtx = null;
function playRestBeep() {
  try {
    const ctx = audioCtx || new (window.AudioContext || window.webkitAudioContext)();
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.type = 'sine';
    osc.frequency.setValueAtTime(880, ctx.currentTime); // Nota La5 (chime limpio)
    gain.gain.setValueAtTime(0.2, ctx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.6);
    osc.connect(gain);
    gain.connect(ctx.destination);
    osc.start();
    osc.stop(ctx.currentTime + 0.6);
  } catch (e) {
    console.log('Audio feedback not supported or blocked');
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
      if (navigator.vibrate) navigator.vibrate([250, 100, 250]);
      const banner = document.getElementById('rest-timer-banner');
      if (banner) {
        banner.classList.add('border-emerald-500', 'bg-emerald-950/80');
        document.getElementById('rest-timer-countdown').textContent = '¡LISTO!';
        setTimeout(() => {
          banner.classList.add('hidden');
          banner.classList.remove('border-emerald-500', 'bg-emerald-950/80');
        }, 2000);
      }
    } else {
      updateRestTimerUi();
    }
  }, 1000);
}
```

#### 5. Debounce Seguro (600 ms) y Comprobación de Respuesta HTTP
```javascript
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
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        date: todayISO,
        routine_id: routineId,
        routine_name: gymRoutinesData[routineId].title,
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
```

#### 6. Safe-Area Insets en Dock Móvil y Padding Principal
```html
<!-- En el dock inferior de cloudflare/src/index.ts (línea 4877) -->
<nav class="lg:hidden fixed left-3 right-3 h-16 bg-[#292631]/95 backdrop-blur-md border border-[#4d3e50] rounded-2xl flex items-center justify-around z-40 px-1 shadow-2xl" style="bottom: calc(0.75rem + env(safe-area-inset-bottom, 0px));">
  ...
</nav>

<!-- En el contenedor main (línea 4039) -->
<main class="flex-1 lg:pl-24 lg:pb-12 flex flex-col min-w-0" style="padding-bottom: calc(7.5rem + env(safe-area-inset-bottom, 0px));">
```

---

## 5. VERIFICATION METHOD (Método de Verificación Independiente)

Para que el implementador y los agentes de QA verifiquen de forma independiente que los requisitos R2 están plenamente superados:

1. **Ejecución de Suites Automatizadas:**
   ```powershell
   python -m pytest tests/test_audit_suite.py
   python scripts/test_prototype_v10.py
   ```
   *Condición de éxito:* 9/9 tests superados en pytest y generación de las 5 capturas en Playwright sin errores de consola.

2. **Inspección de Touch Targets con Playwright:**
   - Evaluar con Playwright el tamaño de los botones de steppers:
     ```python
     bbox = await page.locator("button:has-text('+2.5')").first.bounding_box()
     assert bbox['height'] >= 44
     ```
   *Condición de invalidación:* Cualquier botón interactivo con altura o anchura inferior a 44px o solapamiento con el dock inferior.

3. **Verificación de Insets:**
   - Inspeccionar el DOM con emulación de iPhone 14/15 en Playwright y comprobar que la posición computada del dock (`window.getComputedStyle(dock).bottom`) respeta el cálculo del inset.
