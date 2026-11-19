import os
from playwright.sync_api import sync_playwright

hip_thrust_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#05161A"/>
      <stop offset="100%" stop-color="#072E33"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F969C"/>
      <stop offset="100%" stop-color="#0C7075"/>
    </linearGradient>
    <linearGradient id="skinGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F5CBA7"/>
      <stop offset="100%" stop-color="#E5B28B"/>
    </linearGradient>
    <linearGradient id="barGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#94A3B8"/>
      <stop offset="50%" stop-color="#CBD5E1"/>
      <stop offset="100%" stop-color="#64748B"/>
    </linearGradient>
    <filter id="glowTeal" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- CARD BACKGROUND -->
  <rect width="800" height="380" rx="16" fill="url(#bgGrad)" stroke="#294D61" stroke-width="1.5" stroke-opacity="0.4"/>

  <!-- FLOOR GROUND LINE -->
  <line x1="40" y1="330" x2="760" y2="330" stroke="#294D61" stroke-width="1.5" stroke-dasharray="4 4" stroke-opacity="0.4"/>

  <!-- CENTER DIVIDER -->
  <line x1="400" y1="50" x2="400" y2="330" stroke="#294D61" stroke-width="1" stroke-dasharray="6 6" stroke-opacity="0.3"/>

  <!-- MOTION ARROW -->
  <g transform="translate(400, 190)">
    <circle cx="0" cy="0" r="16" fill="#072E33" stroke="#0F969C" stroke-width="1.5"/>
    <path d="M-6 0 H6 M2 -4 L6 0 L2 4" stroke="#0F969C" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- BADGES -->
  <g transform="translate(30, 22)">
    <rect width="130" height="24" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1"/>
    <text x="65" y="16" fill="#6DA5C0" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · INICIAL</text>
  </g>
  <g transform="translate(420, 22)">
    <rect width="150" height="24" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1"/>
    <circle cx="14" cy="12" r="3.5" fill="#0F969C" filter="url(#glowTeal)"/>
    <text x="84" y="16" fill="#0F969C" font-family="system-ui, -apple-system, sans-serif" font-size="10" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · BLOQUEO</text>
  </g>

  <!-- ==================== FASE 1: HIP THRUST INICIAL ==================== -->
  <!-- Bench 1 -->
  <rect x="70" y="210" width="48" height="95" rx="5" fill="#0E1E24" stroke="#294D61" stroke-width="1.5"/>
  <rect x="82" y="305" width="8" height="25" fill="#1E293B"/>
  <line x1="70" y1="330" x2="105" y2="330" stroke="#1E293B" stroke-width="3" stroke-linecap="round"/>

  <!-- Far Leg (Shadow depth) -->
  <path d="M175 270 Q 215 235 245 240 Q 252 285 255 320 L275 322 L275 330 L242 330 Z" fill="#C8926F" opacity="0.6"/>

  <!-- Torso & Hips Down -->
  <path d="M118 210 Q 140 240 168 275 Q 155 285 142 278 Q 120 245 108 220 Z" fill="#0F969C"/>
  <!-- Neck & Head -->
  <path d="M112 210 Q 106 198 100 190" stroke="#F5CBA7" stroke-width="9" stroke-linecap="round"/>
  <circle cx="96" cy="180" r="13" fill="#F5CBA7"/>
  <!-- Athletic Hair Ponytail -->
  <path d="M94 167 C 104 167 109 176 109 184 C 109 192 102 195 94 195 C 86 195 83 186 83 180 C 83 172 88 167 94 167 Z" fill="#1C1917"/>
  <path d="M86 182 Q 72 188 74 200 Q 82 200 89 188 Z" fill="#1C1917"/>

  <!-- Shorts -->
  <path d="M145 265 L 180 262 L 185 285 L 150 292 Z" fill="#05161A" stroke="#294D61" stroke-width="1"/>

  <!-- Near Thigh & Shin -->
  <path d="M178 268 Q 210 238 238 245 Q 248 285 250 320" stroke="#F5CBA7" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M178 268 Q 210 238 238 245 Q 248 285 250 320" stroke="#E5B28B" stroke-width="16" stroke-linecap="round" stroke-linejoin="round" fill="none"/>

  <!-- Near Shoe -->
  <path d="M238 320 L 268 320 Q 272 325 268 330 L 235 330 Z" fill="#1E293B"/>
  <rect x="235" y="327" width="35" height="3" rx="1" fill="#F1F5F9"/>
  <path d="M248 322 L 256 322" stroke="#0F969C" stroke-width="2" stroke-linecap="round"/>

  <!-- Arm Holding Bar -->
  <path d="M120 218 Q 142 245 168 265" stroke="#F5CBA7" stroke-width="9" stroke-linecap="round" fill="none"/>
  <!-- Hand -->
  <circle cx="168" cy="265" r="5.5" fill="#E5B28B"/>

  <!-- Barbell 1 on Pelvis -->
  <rect x="164" y="215" width="8" height="100" rx="2" fill="url(#barGrad)"/>
  <circle cx="168" cy="265" r="26" fill="#1E293B" stroke="#0F969C" stroke-width="2.5" opacity="0.9"/>
  <circle cx="168" cy="265" r="16" fill="#0F172A" stroke="#475569" stroke-width="1"/>
  <circle cx="168" cy="265" r="5" fill="#94A3B8"/>

  <!-- ==================== FASE 2: HIP THRUST BLOQUEO HORIZONTAL ==================== -->
  <!-- Bench 2 -->
  <rect x="440" y="210" width="48" height="95" rx="5" fill="#0E1E24" stroke="#294D61" stroke-width="1.5"/>
  <rect x="452" y="305" width="8" height="25" fill="#1E293B"/>
  <line x1="440" y1="330" x2="475" y2="330" stroke="#1E293B" stroke-width="3" stroke-linecap="round"/>

  <!-- Far Leg Fase 2 -->
  <path d="M575 208 L 650 208 L 650 320 L 675 320 L 675 328 L 642 328 Z" fill="#C8926F" opacity="0.6"/>

  <!-- Horizontal Torso -->
  <path d="M480 205 Q 525 205 570 205 L 565 228 Q 520 228 478 225 Z" fill="#0F969C"/>
  <!-- Neck & Tucked Head -->
  <path d="M478 208 Q 465 200 455 195" stroke="#F5CBA7" stroke-width="9" stroke-linecap="round"/>
  <circle cx="448" cy="186" r="13" fill="#F5CBA7"/>
  <!-- Athletic Hair Ponytail -->
  <path d="M446 173 C 456 173 461 182 461 190 C 461 198 454 201 446 201 C 438 201 435 192 435 186 C 435 178 440 173 446 173 Z" fill="#1C1917"/>
  <path d="M438 188 Q 424 194 426 206 Q 434 206 441 194 Z" fill="#1C1917"/>

  <!-- Shorts & Glute -->
  <path d="M540 202 L 585 202 Q 590 220 575 232 L 538 230 Z" fill="#05161A" stroke="#294D61" stroke-width="1"/>

  <!-- NEUROMUSCULAR GLOW: GLUTEUS MAXIMUS PEAK -->
  <ellipse cx="565" cy="215" rx="26" ry="16" fill="#0F969C" fill-opacity="0.4" filter="url(#glowTeal)"/>
  <path d="M548 215 Q 568 202 585 215" stroke="#6DA5C0" stroke-width="2" stroke-linecap="round" fill="none"/>

  <!-- Near Horizontal Thigh to Knee at 90 deg -->
  <path d="M575 212 L 655 212" stroke="#F5CBA7" stroke-width="18" stroke-linecap="round"/>
  <!-- Vertical Shin -->
  <path d="M655 212 L 655 320" stroke="#F5CBA7" stroke-width="15" stroke-linecap="round"/>

  <!-- Near Shoe Planted 90 deg -->
  <path d="M642 320 L 674 320 Q 678 325 674 330 L 638 330 Z" fill="#1E293B"/>
  <rect x="638" y="327" width="38" height="3" rx="1" fill="#F1F5F9"/>
  <path d="M650 322 L 660 322" stroke="#0F969C" stroke-width="2" stroke-linecap="round"/>

  <!-- Arm Holding Barbell at Top -->
  <path d="M485 212 Q 525 210 565 210" stroke="#F5CBA7" stroke-width="9" stroke-linecap="round" fill="none"/>
  <circle cx="565" cy="210" r="5.5" fill="#E5B28B"/>

  <!-- Barbell 2 at Peak Height -->
  <rect x="561" y="160" width="8" height="100" rx="2" fill="url(#barGrad)"/>
  <circle cx="565" cy="210" r="26" fill="#1E293B" stroke="#0F969C" stroke-width="2.5" opacity="0.9" filter="url(#glowTeal)"/>
  <circle cx="565" cy="210" r="16" fill="#0F172A" stroke="#475569" stroke-width="1"/>
  <circle cx="565" cy="210" r="5" fill="#94A3B8"/>

  <!-- BOTTOM CAPTION -->
  <text x="400" y="360" fill="#94A3B8" font-family="system-ui, -apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
    HIP THRUST CON BARRA &bull; FOCO NEUROMUSCULAR: <tspan fill="#0F969C" font-weight="700">GLÚTEO MAYOR &amp; CADENA POSTERIOR</tspan>
  </text>
</svg>'''

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ margin: 0; padding: 20px; background: #000; display: flex; justify-content: center; align-items: center; min-height: 100vh; }}
  svg {{ width: 800px; height: 380px; display: block; }}
</style>
</head>
<body>
{hip_thrust_svg}
</body>
</html>"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 840, "height": 420})
    page.set_content(html)
    page.screenshot(path='test_hip_thrust.png')
    browser.close()

print("Generated test_hip_thrust.png successfully!")
