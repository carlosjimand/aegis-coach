import os
import json

def get_svg_wrapper(title, muscle_target, phase1_name, phase2_name, content_phase1, content_phase2):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 380" width="100%" height="100%">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#05161A"/>
      <stop offset="100%" stop-color="#072E33"/>
    </linearGradient>
    <linearGradient id="tealGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0F969C"/>
      <stop offset="100%" stop-color="#0C7075"/>
    </linearGradient>
    <linearGradient id="skin" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#F8D3B8"/>
      <stop offset="100%" stop-color="#E8B490"/>
    </linearGradient>
    <linearGradient id="skinShadow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#DE9E78"/>
      <stop offset="100%" stop-color="#C6835F"/>
    </linearGradient>
    <linearGradient id="plateGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#334155"/>
      <stop offset="50%" stop-color="#1E293B"/>
      <stop offset="100%" stop-color="#0F172A"/>
    </linearGradient>
    <linearGradient id="barChrome" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#64748B"/>
      <stop offset="50%" stop-color="#E2E8F0"/>
      <stop offset="100%" stop-color="#475569"/>
    </linearGradient>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- TARJETA BASE -->
  <rect width="800" height="380" rx="18" fill="url(#bgGrad)" stroke="#294D61" stroke-width="1.5" stroke-opacity="0.45"/>

  <!-- SUELO Y CUADRÍCULA SUTIL -->
  <line x1="30" y1="330" x2="770" y2="330" stroke="#294D61" stroke-width="2" stroke-dasharray="6 4" stroke-opacity="0.4"/>
  <rect x="30" y="331" width="740" height="1" fill="#0F969C" fill-opacity="0.2"/>

  <!-- DIVISOR CENTRAL CON CHEVRON -->
  <line x1="400" y1="45" x2="400" y2="330" stroke="#294D61" stroke-width="1" stroke-dasharray="4 6" stroke-opacity="0.3"/>
  <g transform="translate(400, 185)">
    <circle cx="0" cy="0" r="17" fill="#05161A" stroke="#0F969C" stroke-width="1.8" filter="url(#glow)"/>
    <path d="M-6 0 H6 M2 -4 L6 0 L2 4" stroke="#0F969C" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
  </g>

  <!-- BADGES SUPERIORES -->
  <g transform="translate(35, 24)">
    <rect width="145" height="26" rx="6" fill="#05161A" stroke="#294D61" stroke-width="1.2"/>
    <text x="72" y="17" fill="#6DA5C0" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 1 · {phase1_name}</text>
  </g>
  <g transform="translate(425, 24)">
    <rect width="160" height="26" rx="6" fill="#0C7075" fill-opacity="0.25" stroke="#0F969C" stroke-width="1.2"/>
    <circle cx="15" cy="13" r="3.5" fill="#0F969C" filter="url(#glow)"/>
    <text x="90" y="17" fill="#0F969C" font-family="-apple-system, sans-serif" font-size="10.5" font-weight="700" text-anchor="middle" letter-spacing="1">FASE 2 · {phase2_name}</text>
  </g>

  <!-- PIE DE TARJETA CON DIANA MUSCULAR -->
  <g transform="translate(400, 360)">
    <rect x="-210" y="-14" width="420" height="24" rx="12" fill="#05161A" fill-opacity="0.8" stroke="#294D61" stroke-width="1"/>
    <circle cx="-190" cy="-2" r="3" fill="#0F969C" filter="url(#glow)"/>
    <text x="0" y="2" fill="#94A3B8" font-family="-apple-system, sans-serif" font-size="11" font-weight="600" text-anchor="middle">
      {title} &bull; FOCO: <tspan fill="#0F969C" font-weight="700">{muscle_target}</tspan>
    </text>
  </g>

  <!-- CONTENIDO FASE 1 -->
  <g id="phase1-group">
    {content_phase1}
  </g>

  <!-- CONTENIDO FASE 2 -->
  <g id="phase2-group">
    {content_phase2}
  </g>
</svg>'''

print("Base SVG wrapper helper ready.")
