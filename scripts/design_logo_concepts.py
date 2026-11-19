import os
from playwright.sync_api import sync_playwright

os.makedirs("cloudflare/public_exercises", exist_ok=True)
os.makedirs("scripts", exist_ok=True)

# =========================================================================
# CONCEPT 1: "The Aero-Aegis" (Kinetic Wing Shield & Apex Summit)
# =========================================================================
concept_1_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <defs>
    <!-- Cyan to Periwinkle Gradient (Speed & Protection) -->
    <linearGradient id="c1_blue" x1="20%" y1="0%" x2="80%" y2="100%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="40%" stop-color="#7B88FF"/>
      <stop offset="100%" stop-color="#5C6BC0"/>
    </linearGradient>

    <!-- Coral to Magenta Gradient (Kinetic Propulsion) -->
    <linearGradient id="c1_coral" x1="80%" y1="0%" x2="20%" y2="100%">
      <stop offset="0%" stop-color="#FF758C"/>
      <stop offset="45%" stop-color="#FF5E80"/>
      <stop offset="100%" stop-color="#E040FB"/>
    </linearGradient>

    <!-- Core Luminous Apex (White to Neon Coral) -->
    <linearGradient id="c1_core" x1="50%" y1="0%" x2="50%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="60%" stop-color="#FF5E80"/>
      <stop offset="100%" stop-color="#7B88FF"/>
    </linearGradient>

    <!-- Speed Bar Gradient -->
    <linearGradient id="c1_wing" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FF5E80"/>
    </linearGradient>

    <filter id="c1_glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="2.5" result="blur"/>
      <feComposite in="SourceGraphic" in2="blur" operator="over"/>
    </filter>
  </defs>

  <!-- Left Aero-Shield Shoulder & Flank (Fluid Dynamic Wing) -->
  <path d="M 50 10
           C 36 13, 19 24, 15 40
           C 11 55, 17 73, 33 84
           C 40 89, 47 92, 50 92
           C 44 85, 30 76, 26 62
           C 22 49, 27 36, 38 27
           C 44 22, 48 16, 50 10
           Z" 
        fill="url(#c1_blue)"/>

  <!-- Right Aero-Shield Shoulder & Flank (Kinetic Coral Wing) -->
  <path d="M 50 10
           C 64 13, 81 24, 85 40
           C 89 55, 83 73, 67 84
           C 60 89, 53 92, 50 92
           C 56 85, 70 76, 74 62
           C 78 49, 73 36, 62 27
           C 56 22, 52 16, 50 10
           Z" 
        fill="url(#c1_coral)"/>

  <!-- Propulsive 'A' Apex (The Runner's Summit) -->
  <path d="M 50 25
           C 52 25, 60 46, 64 62
           C 65 66, 61 68, 56 67
           C 53 62, 52 56, 50 56
           C 48 56, 47 62, 44 67
           C 39 68, 35 66, 36 62
           C 40 46, 48 25, 50 25
           Z" 
        fill="url(#c1_core)"
        filter="url(#c1_glow)"/>

  <!-- High-Speed Aerodynamic Cross-Wing (Forward Vector) -->
  <path d="M 23 57
           C 35 53, 65 53, 77 57
           C 67 61, 33 61, 23 57
           Z" 
        fill="url(#c1_wing)"/>
</svg>'''


# =========================================================================
# CONCEPT 2: "The Velocity Wing" (Fluid Monogram 'A')
# Athletic, sculptural, organic elegance. No boxy lines.
# =========================================================================
concept_2_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <defs>
    <!-- Left Ascender Gradient: Electric Indigo to Cyan -->
    <linearGradient id="c2_left" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#6366F1"/>
      <stop offset="50%" stop-color="#7B88FF"/>
      <stop offset="100%" stop-color="#38BDF8"/>
    </linearGradient>

    <!-- Right Wing & Crest Gradient: Coral Neón to Soft Magenta -->
    <linearGradient id="c2_right" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF758C"/>
      <stop offset="40%" stop-color="#FF5E80"/>
      <stop offset="100%" stop-color="#E040FB"/>
    </linearGradient>

    <!-- Kinetic Tape Gradient -->
    <linearGradient id="c2_cross" x1="0%" y1="50%" x2="100%" y2="50%">
      <stop offset="0%" stop-color="#7B88FF"/>
      <stop offset="50%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FF5E80"/>
    </linearGradient>

    <filter id="c2_softglow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-color="#FF5E80" flood-opacity="0.35"/>
    </filter>
  </defs>

  <!-- Left Dynamic Propulsion Stride (The Ascending Runner Blade) -->
  <path d="M 24 85
           C 20 81, 22 72, 28 56
           C 35 38, 44 23, 49 13
           C 51 9, 53 9, 54 13
           C 52 23, 44 42, 38 58
           C 33 71, 29 82, 26 86
           C 25 87, 24 87, 24 85
           Z" 
        fill="url(#c2_left)"/>

  <!-- Right Fluid Power Crest (The Aerodynamic Wing & Shield Contour) -->
  <path d="M 50 11
           C 56 18, 69 40, 77 58
           C 84 73, 83 83, 76 87
           C 70 90, 61 88, 56 81
           C 51 74, 49 64, 51 54
           C 52 50, 56 50, 58 53
           C 59 58, 60 67, 63 74
           C 66 80, 71 81, 74 78
           C 78 74, 76 64, 71 52
           C 65 38, 54 20, 50 11
           Z" 
        fill="url(#c2_right)"
        filter="url(#c2_softglow)"/>

  <!-- Forward Kinetic Ribbon (Breaking the Tape in Full Flight) -->
  <path d="M 14 58
           C 28 55, 48 54, 68 54
           C 80 54, 91 56, 94 58
           C 93 61, 80 62, 68 62
           C 48 62, 28 61, 14 58
           Z" 
        fill="url(#c2_cross)"/>
</svg>'''


# =========================================================================
# CONCEPT 3: "The Biomorphic Helix Shield" (Dual Laminar Vortices)
# Two continuous biomechanical ribbons that form a dynamic, open shield
# with forward momentum and tendon-like elasticity.
# =========================================================================
concept_3_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <defs>
    <linearGradient id="c3_cyan" x1="0%" y1="100%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="50%" stop-color="#7B88FF"/>
      <stop offset="100%" stop-color="#FFFFFF"/>
    </linearGradient>

    <linearGradient id="c3_pink" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FF5E80"/>
      <stop offset="55%" stop-color="#FF2A6D"/>
      <stop offset="100%" stop-color="#9C27B0"/>
    </linearGradient>

    <linearGradient id="c3_arrow" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FF5E80"/>
    </linearGradient>
  </defs>

  <!-- Left Continuous Biomechanical Arc (Foot-strike to Apex) -->
  <path d="M 28 84
           C 16 73, 12 55, 17 38
           C 22 23, 35 14, 49 11
           C 51 10, 52 12, 51 14
           C 39 19, 29 29, 25 43
           C 21 57, 26 71, 35 80
           C 42 87, 49 89, 52 90
           C 50 91, 46 91, 43 90
           C 37 89, 32 87, 28 84
           Z" 
        fill="url(#c3_cyan)"/>

  <!-- Right Continuous Kinetic Shield Arc (Apex to Push-off) -->
  <path d="M 51 11
           C 65 14, 78 23, 83 38
           C 88 55, 84 73, 72 84
           C 65 89, 58 91, 52 91
           C 54 88, 59 84, 63 80
           C 73 70, 77 56, 74 43
           C 70 29, 60 19, 49 14
           C 48 12, 49 10, 51 11
           Z" 
        fill="url(#c3_pink)"/>

  <!-- Interior Dynamic 'A' Chevron (Forward Heart & Biomechanical Core) -->
  <path d="M 50 26
           C 51 26, 58 43, 62 55
           C 63 58, 60 60, 56 59
           L 52 58
           C 51 61, 49 61, 48 58
           L 44 59
           C 40 60, 37 58, 38 55
           C 42 43, 49 26, 50 26
           Z" 
        fill="url(#c3_arrow)"/>

  <!-- Kinetic Stabilizer Wing -->
  <path d="M 30 63
           C 42 59, 58 59, 70 63
           C 60 67, 40 67, 30 63
           Z" 
        fill="#FFFFFF" 
        opacity="0.9"/>
</svg>'''


# =========================================================================
# CONCEPT 4: "The Alpha Aero" (Ultra-Minimalist Dual Foil Crest)
# =========================================================================
concept_4_svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" fill="none">
  <defs>
    <linearGradient id="c4_grad" x1="10%" y1="0%" x2="90%" y2="100%">
      <stop offset="0%" stop-color="#38BDF8"/>
      <stop offset="35%" stop-color="#7B88FF"/>
      <stop offset="70%" stop-color="#E040FB"/>
      <stop offset="100%" stop-color="#FF5E80"/>
    </linearGradient>
    <linearGradient id="c4_core" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#FFFFFF"/>
      <stop offset="100%" stop-color="#FF5E80"/>
    </linearGradient>
  </defs>

  <!-- Left Aerodynamic Carbon Foil -->
  <path d="M 28 82
           C 20 74, 16 58, 20 42
           C 24 26, 36 15, 48 11
           C 50 10, 51 11, 50 13
           C 40 19, 31 31, 28 44
           C 25 58, 29 70, 35 78
           C 36 80, 34 82, 32 82
           C 30 82, 29 82, 28 82
           Z" 
        fill="url(#c4_grad)"/>

  <!-- Right Aerodynamic Carbon Foil -->
  <path d="M 52 11
           C 64 15, 76 26, 80 42
           C 84 58, 80 74, 72 82
           C 71 82, 70 82, 68 82
           C 66 82, 64 80, 65 78
           C 71 70, 75 58, 72 44
           C 69 31, 60 19, 50 13
           C 49 11, 50 10, 52 11
           Z" 
        fill="url(#c4_grad)"/>

  <!-- Central Dynamic Apex Blade -->
  <path d="M 50 24
           C 51 24, 57 41, 61 52
           C 62 55, 59 57, 56 56
           L 52 55
           C 51 58, 49 58, 48 55
           L 44 56
           C 41 57, 38 55, 39 52
           C 43 41, 49 24, 50 24
           Z" 
        fill="url(#c4_core)"/>

  <!-- Kinetic Ground Diffuser -->
  <path d="M 37 77
           C 45 73, 55 73, 63 77
           C 59 81, 41 81, 37 77
           Z" 
        fill="#FF5E80"/>
</svg>'''


# Save to destination files
with open("cloudflare/public_exercises/logo_concept_1.svg", "w", encoding="utf-8") as f:
    f.write(concept_1_svg)

with open("cloudflare/public_exercises/logo_concept_2.svg", "w", encoding="utf-8") as f:
    f.write(concept_2_svg)

with open("cloudflare/public_exercises/logo_concept_3.svg", "w", encoding="utf-8") as f:
    f.write(concept_3_svg)

with open("cloudflare/public_exercises/logo_concept_4.svg", "w", encoding="utf-8") as f:
    f.write(concept_4_svg)

print("Updated concepts 1, 2, 3, 4 SVGs successfully.")
