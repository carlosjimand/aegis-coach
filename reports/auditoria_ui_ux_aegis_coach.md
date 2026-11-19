# 📱 INFORME DE AUDITORÍA SENIOR UI/UX Y DISEÑO WEB — AEGIS COACH (v9 -> v10)
**Auditor:** Senior UI/UX Designer & Mobile Usability Specialist  
**Destinatario:** Sistema de Inteligencia y Coaching Aegis Coach  
**Atleta:** Carlos Jiménez Andrino (23 años, 63 kg, 1.73 m | 10K en 38:26 @ Ávila | Objetivo Inmediato: Cross del Soto 28-Nov, T-12 días)  
**Fecha:** 16 de Noviembre de 2026  

---

## 1. RESUMEN EJECUTIVO Y DIAGNÓSTICO GLOBAL

La interfaz actual (`v9`) implementa fielmente los fundamentos estéticos del sistema **Octet Luxury**: paleta oscura atmosférica (*River Styx* `#171821`, *Jaguar* `#21222d`, acentos *Candy Rose* `#fa769e` y *Periwinkle Blue* `#9ca8f3`), curvas suaves con `border-radius: 1.75rem`, y gradientes sutiles. La integración de datos reales de Garmin FIT y la biblioteca de ejercicios vectoriales representa un activo diferencial de inmenso valor.

Sin embargo, desde la perspectiva de **usabilidad atlética y ergonomía móvil bajo fatiga**, la app sufre de:
1. **Sobrecarga de información en primer scroll:** Demasiados bloques compitiendo por atención (Hero Card + 3 KPIs + Gráfico Spline de 8 semanas + 8 mini-badges + Sesiones Clave + Objetivos).
2. **Duplicidad de navegación y header sobredimensionado:** En pantallas móviles, el header ocupa 80px (`h-20`) con enlaces repetidos a Perfil y Telegram, restando valioso espacio vertical sobre el dock inferior de 64px.
3. **Puntos ciegos ergonómicos en el Gimnasio (Fuerza):** El logger de series utiliza inputs de texto estándar y botones de eliminación diminutos (24x24px), lo cual genera frustración con dedos sudorosos o tras una serie pesada a RIR 1.
4. **Falta de jerarquía orientada a la competición inminente:** Faltan solo **12 días para el Cross del Soto (28 Nov)**, pero la cuenta atrás se encuentra en una tarjeta secundaria abajo a la derecha, en lugar de gobernar el estado de "Tapering" de la semana.

---

## 2. VALOR REAL APORTADO VS. RUIDO COGNITIVO

### A. Lo que Carlos necesita de un vistazo en 3 segundos (Golden Path Diario):
1. **¿Qué entreno toca HOY?**
   - Running: Tipo (Rodaje Z1, Intervalos VO2max, etc.), Ritmo exigible (`4:55-5:10/km`), Distancia/Tiempo (`35 min`), Zonas de FC (`<145 ppm`) y Calzado (`Asics Novablast 5`).
   - Gimnasio: Rutina del día (ej. `Torso Tracción & Densidad`), ejercicios prioritarios y cargas objetivo.
2. **Estado de Forma y Fatiga Inmediata (Tapering / ACWR):**
   - Saber si el cuerpo está en zona óptima de asimilación o si hay riesgo de sobrecarga aguda (ratio de Gabbett) de cara al 28 de Noviembre.
3. **Cuenta Atrás Psicológica:**
   - Visualizar claramente que estamos a T-12 días del Cross y el foco táctico de la semana.

### B. Elementos que generan ruido cognitivo o fricción:
- **8 Mini-Badges bajo el gráfico de volumen:** Mostrar semanas de hace mes y medio (`28 Sep 13.4k`, `05 Oct 19.2k`...) en un bloque de 8 píldoras apiñadas genera fatiga visual en móvil sin aportar valor a la sesión de hoy.
- **Doble botón "Ver Entreno":** En el Hero Card de Hoy hay un botón blanco grande "Ver Entreno ->" que fuerza un salto de línea en móvil. Al ser toda la tarjeta conceptualmente un acceso directo, un botón tan masivo roba espacio a las métricas del propio rodaje.
- **Sección "3 Sesiones Clave de Referencia" permanente en el Dashboard:** La marca del 10K de Ávila (38:26) y el 6x800m son hitos de calibración excelentes, pero tenerlos fijos en el dashboard diario junto al gráfico genera un scroll excesivo. Deben vivir en la pestaña de **Objetivos / Métricas**.

---

## 3. AUDITORÍA DETALLADA "SOBRA VS. FALTA"

| Componente | Estado Actual | Diagnóstico UI/UX | Acción Propuesta |
| :--- | :--- | :--- | :--- |
| **Header Superior** | Altura `h-20` (80px), incluye nombre completo, subtítulo, botón Perfil y botón Telegram. | **SOBRA:** En móvil satura el 12% superior de la pantalla. Los botones duplican el dock inferior y el sidebar. | **Simplificar a `h-14` (56px):** Monograma Logo + "AEGIS" + Badge de Fecha/Semana. Mover Telegram y Perfil exclusivamente a sus pestañas/dock. |
| **Dashboard: Gráfico Spline** | Curvas de Running y Gimnasio de 8 semanas + 8 mini-cajas de texto estático abajo. | **SOBRA:** Las 8 mini-cajas saturan la vista móvil y son ilegibles (10px). El rango de 8 semanas es demasiado amplio para el día a día. | **Refactorizar:** Reducir a las últimas 4 semanas + proyección del Cross. Eliminar las 8 cajas inferiores y sustituirlas por tooltips interactivos limpios al tocar los puntos. |
| **Dashboard: TSB vs ACWR** | Muestra `TSB -9.5` y `CTL 16.5 (ATL 26)` como texto complementario. | **FALTA:** No indica el ratio Agudo:Crónico (ACWR = 26/16.5 = 1.57), que es la métrica reina que exige el protocolo del coach para vigilar picos de fatiga antes del tapering. | **Incorporar Semáforo ACWR:** Visualizar el ratio con color semafórico (Verde 0.8-1.3, Naranja 1.3-1.5, Rosa Alerta >1.5). |
| **Gimnasio: Logger Serie a Serie** | Inputs de texto `<input type="text">` para Reps y Kilos, botón de eliminar de `w-6 h-6` (24x24px). | **CRÍTICO (FALLA DE USABILIDAD):** Imposible operar con dedos sudorosos o temblor muscular. Invoca el teclado alfanumérico en vez del teclado numérico (`inputmode="decimal"`). Touch target < 44px. | **Añadir Steppers Rápidos:** Botones táctiles grandes `[-2.5kg] [+2.5kg]` y `[-1] [+1 rep]`, touch targets de mínimo 48x48px, botón de check verde para confirmar serie completada. |
| **Gimnasio: Temporizador de Descanso** | No existe cronómetro entre series. | **FALTA:** Para un atleta con perfil de fibras rápidas, las pausas en series de fuerza y micro-intervalos son críticas para la recuperación de fosfágenos. | **Añadir "Quick Rest Timer":** Píldora flotante configurable (60s, 90s, 2 min) que vibra o suena al terminar el descanso. |
| **Objetivos: Matriz de Ritmos** | Tabla teórica con 1.500m, 10K, Media Maratón, Z2, Z1. | **DESFOCADA:** Muestra ritmos de distancias no prioritarias en lugar de desglosar el perfil táctico del **Cross del Soto** y de la **San Silvestre**. | **Centrar en los 2 Objetivos Reales:** Desglose del circuito de hierba/tierra del Soto (curvas, clavos, parciales a 3:30) y asfalto de San Silvestre (sub 3:35). |
| **Perfil: Monitor de Blindaje Articular** | Solo peso, altura, edad, FCR y calculadora de IMC. | **FALTA:** El protocolo exige monitorizar rodilla izquierda (derrame sinovial) e isquiotibial izquierdo (0-10 dolor). | **Check-in Articular Rápido:** Sliders táctiles 0-10 para Rodilla e Isquio que alerten inmediatamente al coach si hay reactividad. |

---

## 4. JERARQUÍA VISUAL, BALANCE CROMÁTICO Y WCAG AA

### A. Paleta Octet Luxury & Cohesión
- **Fondo Base (`#171821` River Styx):** Proporciona un contraste sobresaliente con el texto blanco (ratio > 15:1), ideal para visualización OLED nocturna.
- **Superficie de Tarjetas (`#21222d` / `#292631` Jaguar):** Excelente separación sutil mediante bordes de 1px con `rgba(255,255,255,0.06)` y `rgba(168,135,206,0.28)` en hover.
- **Acentos (`#fa769e` Candy Rose & `#9ca8f3` Periwinkle Blue):** Identidad visual sofisticada y premium, alejándose de los tópicos genéricos de apps deportivas.

### B. Deficiencias Detectadas de Accesibilidad y Contraste (WCAG AA):
1. **Contraste de Texto Secundario en Exteriores:**
   - El color de texto `--composers-magic: #A297A6` y `#7A7585` utilizado en tamaños de 10px y 11px (`text-[10px]`, `text-[11px]`) tiene un ratio de contraste de ~4.2:1 sobre `#21222d`. Bajo luz solar directa en la pista o el parque, estos textos resultan prácticamente invisibles.
   - **Corrección:** Subir el texto secundario a mínimo 12px y utilizar `#C4B9C8` o `#D1CAD5` (ratio > 6.5:1).
2. **Hero Card Legibilidad:**
   - El degradado rosa-lavanda (`#a887ce` a `#fa769e`) tiene zonas claras donde el texto blanco sobre píldoras oscuras semitransparentes (`bg-black/25`) pierde nitidez.
   - **Corrección:** Añadir un scrim de sombra o aumentar la opacidad del fondo de las píldoras a `bg-[#171821]/80`.

---

## 5. USABILIDAD MÓVIL Y ERGONOMÍA BAJO FATIGA

### A. Cumplimiento de Touch Targets (Objetivo: Mínimo 44x44px)
- **Dock Inferior Flotante (5 botones):** Cumple bien el área táctil horizontal, pero los iconos de 20px con etiqueta de 9px tienen poco espaciado inter-botón.
- **Botones de gestión en el Logger de Series:**
  - Botón eliminar serie: `w-6 h-6` (24x24px) ❌ **INCUMPLE**. Debe ser mínimo 40x40px o utilizar deslizamiento (swipe to delete).
  - Inputs de repeticiones y kilos: Altura de 32px (`py-1 text-xs`) ❌ **INSUFICIENTE**. Debe tener al menos 44px de altura.
- **Cuadrícula del Calendario Mensual:**
  - Celdas de días: En pantallas de 390px (iPhone estándar), cada día mide ~48px de ancho por 56px de alto. Cumple el mínimo táctil, pero los puntos de actividad (1.5px) son invisibles a la distancia de un brazo. Deben aumentarse a barras o píldoras de 4px de grosor.

### B. Ergonomía del Pulgar (Thumb Zone)
- En el diseño actual, el cambio de mes en el calendario (`< Noviembre 2026 >`) y los chips de selección de rutina de gimnasio (`Pierna 1`, `Torso Tracción`, etc.) se sitúan en el tercio superior de la pantalla, obligando a usar dos manos o forzar la hiperextensión del pulgar.
- **Propuesta:** Reorganizar los filtros y selectores primarios en la zona media-inferior o mediante carrusel horizontal con scroll táctil suave (*swipeable pills*).

---

## 6. PROPUESTA DE PROTOTIPO v10 — ESTRUCTURA QUIRÚRGICA POR PESTAÑA

### PESTAÑA 1: DASHBOARD (Ultra-Limpio & Focalizado)
1. **Header Compacto (56px):** Monograma Aero + "AEGIS COACH" + Badge de cuenta atrás sutil ("Cross Soto: 12d").
2. **Hero de la Sesión de Hoy (Card Activa Táctil):**
   - Click en cualquier punto abre directamente la vista del entreno o gimnasio.
   - Etiquetas claras: `35 min @ 4:55-5:10/km (Z1)` | `Rutina 2: Torso Tracción`.
   - Zapatilla asignada integrada con icono: `Asics Novablast 5`.
3. **Bloque Trilogía de Rendimiento (3 KPIs Refactorizados):**
   - **KPI 1: Volumen Semanal:** `30.0 km` objetivo (Progreso actual con barra Periwinkle `#9ca8f3`).
   - **KPI 2: ACWR & TSB (Fatiga):** `ACWR 1.2` (Óptimo) | `TSB -9.5` (Carga controlada).
   - **KPI 3: Blindaje Muscular (Gimnasio):** `3/4 sesiones` completadas (Barra Candy Rose `#fa769e`).
4. **Hero Competición: Cuenta Atrás Cross del Soto (28 Nov):**
   - Tarjeta destacada con número gigante `12 DÍAS`, objetivo `5.0 km @ 3:30/km (~17:30)`, terreno `Hierba/Tierra` y material obligatorio `Clavos 6mm`.
5. **Gráfico Semanal Compacto:**
   - 4 semanas (últimas 3 semanas reales + semana proyectada de competición).
   - Tooltips enriquecidos al toque en vez de 8 cajas inferiores apiñadas.

### PESTAÑA 2: ENTRENOS & CALENDARIO
1. **Segmented Control Ergonómico:** `Calendario Mensual` | `Próximos 14 Días (Microciclo)`.
2. **Calendario Optimizado:** Celdas con badges de color en lugar de micropuntos. Al tocar un día, el detalle emerge suavemente sin saltos bruscos de pantalla.
3. **Parciales de Vueltas Garmin FIT:** Formato tabla estilizada con ritmo codificado por color (Fucsia sub 3:30, Rosa sub 3:50, Verde Z1/Z2).

### PESTAÑA 3: GIMNASIO & REGISTRO SERIE A SERIE
1. **Selector de Rutinas en Carrusel Táctil:** 4 rutinas oficiales accesibles en la zona cómoda del pulgar.
2. **Logger con Ergonomía Antifatiga:**
   - Inputs con altura mínima de 44px e `inputmode="decimal"`.
   - Botón `[✓]` de confirmación grande que activa feedback visual esmeralda y guarda en LocalStorage + KV en segundo plano.
   - Botones rápidos de incremento `+2.5kg` para facilitar la sobrecarga progresiva sin teclear.
3. **Temporizador de Descanso Integrado:** Barra flotante de cuenta atrás al completar cada serie.
4. **Botón Flotante "Copiar para Garmin":** Sticky al final del scroll con confirmación táctil `¡Copiado!`.

### PESTAÑA 4: OBJETIVOS & ESTRATEGIA
1. **Cross Parque del Soto (28 Nov — 12 días):**
   - Ficha técnica completa: circuito, táctica de zancada en hierba, control de lactato (estrategia de micro-intervalos previa), calentamiento y clavos.
2. **San Silvestre (31 Dic — 45 días):**
   - Plan de asfalto: proyección sub 3:35/km (23:15 aprox.), placa de carbono y ritmo crucero.
3. **Matriz de Zonas de Fisiología:** Concentrada en los ritmos vigentes de Carlos basados en el 10K de Ávila (38:26).

### PESTAÑA 5: PERFIL & SALUD ARTICULAR
1. **Datos Fisiológicos:** Peso (63 kg), Altura (173 cm), FC Reposo (42 ppm), IMC (21.05 kg/m²).
2. **Semáforo de Blindaje Articular (NUEVO):**
   - Rodilla Izquierda: `0/10` (Sin derrame, sustitución activa sentadilla libre por Box Squat).
   - Isquiotibial Izquierdo: `0/10` (Blindado con Hip Thrust & RDL Unilateral).
   - Indicador de estado para feedback inmediato al coach.
