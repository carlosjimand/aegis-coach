import os
from playwright.sync_api import sync_playwright

# CONCEPT 1B: Sculpted Aero Shield (Broader athletic shoulders, wing intake, apex core)
svg_c1b = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <defs>
    <linearGradient id="c1b_blue" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#7B88FF"/>
      <stop offset="100%" stop-color="#4F46E5"/>
    </linearGradient>
    <linearGradient id="c1b_coral" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF758C"/>
      <stop offset="50%" stop-color="#FF5E80"/>
      <stop offset="100%" stop-color="#D946EF"/>
    </linearGradient>
    <linearGradient id="c1b_core" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#FF5E80"/>
      <stop offset="100%" stop-color="#7B88FF"/>
    </linearGradient>
    <linearGradient id="c1b_wing" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FF5E80"/>
    </linearGradient>
  </defs>

  <!-- Left Sculpted Shoulder & Flank (Aggressive Aero Wing) -->
  <path d="M 50 14
           C 38 12, 22 18, 16 32
           C 11 48, 16 68, 32 82
           C 40 88, 47 92, 50 93
           C 44 86, 28 76, 25 61
           C 22 47, 28 34, 40 26
           C 44 23, 48 18, 50 14
           Z" 
        fill="url(#c1b_blue)"/>

  <!-- Right Sculpted Shoulder & Flank (Kinetic Downforce Wing) -->
  <path d="M 50 14
           C 62 12, 78 18, 84 32
           C 89 48, 84 68, 68 82
           C 60 88, 53 92, 50 93
           C 56 86, 72 76, 75 61
           C 78 47, 72 34, 60 26
           C 56 23, 52 18, 50 14
           Z" 
        fill="url(#c1b_coral)"/>

  <!-- Propulsive 'A' Apex (Runner's Summit Vector) -->
  <path d="M 50 26
           C 52 26, 61 46, 65 62
           C 66 66, 62 68, 57 67
           C 54 62, 53 56, 50 56
           C 47 56, 46 62, 43 67
           C 38 68, 34 66, 35 62
           C 39 46, 48 26, 50 26
           Z" 
        fill="url(#c1b_core)"/>

  <!-- Aerodynamic Tape-Breaking Horizon Crossbar -->
  <path d="M 22 57
           C 35 53, 65 53, 78 57
           C 68 61, 32 61, 22 57
           Z" 
        fill="url(#c1b_wing)"/>
</svg>'''

# CONCEPT 2B: Streamlined Velocity Monogram 'A' (Cleaner negative space, razor precision at 24px)
svg_c2b = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <defs>
    <linearGradient id="c2b_leftLeg" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#4F46E5"/>
      <stop offset="50%" stop-color="#7B88FF"/>
      <stop offset="100%" stop-color="#38BDF8"/>
    </linearGradient>
    <linearGradient id="c2b_rightWing" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF758C"/>
      <stop offset="45%" stop-color="#FF5E80"/>
      <stop offset="100%" stop-color="#D946EF"/>
    </linearGradient>
    <linearGradient id="c2b_cross" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#7B88FF"/>
      <stop offset="40%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FF5E80"/>
    </linearGradient>
    <filter id="c2b_dropGlow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3.5" flood-color="#FF5E80" flood-opacity="0.3"/>
    </filter>
  </defs>

  <!-- Left Dynamic Propulsion Stride (The Ascending Runner Blade) -->
  <path d="M 22 86
           C 18 82, 20 73, 27 56
           C 34 38, 43 23, 49 12
           C 51 8, 53 8, 54 12
           C 51 23, 43 43, 37 60
           C 32 73, 28 83, 24 87
           C 23 88, 22 88, 22 86
           Z" 
        fill="url(#c2b_leftLeg)"/>

  <!-- Right Fluid Power Wing (Sweeps Down with Dynamic Aerodynamic Taper) -->
  <path d="M 50 11
           C 57 19, 70 42, 78 60
           C 85 75, 83 84, 76 87
           C 69 90, 60 86, 56 78
           C 52 70, 52 60, 57 52
           C 60 48, 64 50, 65 54
           C 66 61, 65 71, 70 76
           C 74 80, 77 77, 78 72
           C 80 64, 76 53, 71 42
           C 64 28, 54 18, 50 11
           Z" 
        fill="url(#c2b_rightWing)"
        filter="url(#c2b_dropGlow)"/>

  <!-- Forward Kinetic Tape-Breaking Ribbon -->
  <path d="M 12 58
           C 26 55, 48 54, 70 54
           C 82 54, 93 56, 96 58
           C 95 61, 82 62, 70 62
           C 48 62, 26 61, 12 58
           Z" 
        fill="url(#c2b_cross)"/>
</svg>'''

# Save and update
with open("cloudflare/public_exercises/logo_concept_1.svg", "w", encoding="utf-8") as f:
    f.write(svg_c1b)

with open("cloudflare/public_exercises/logo_concept_2.svg", "w", encoding="utf-8") as f:
    f.write(svg_c2b)

print("Updated concept 1 and concept 2 SVGs.")
