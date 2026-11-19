import os
import re
import requests
from PIL import Image, ImageDraw, ImageFont

os.makedirs('data/gym_images/processed', exist_ok=True)

# Image mapping for each routine (p1 to p4, 6 exercises each)
# Format: (routine_id, ex_num, img1_name, img2_name, ex_name_slug)
exercises = [
    # Rutina 1: Pierna 1
    (1, 1, 'p1_1__X31.jpg', 'p1_2__X34.jpg', 'sentadilla_barra'),
    (1, 2, 'p1_3__X38.jpg', 'p1_4__X39.jpg', 'prensa_45'),
    (1, 3, 'p1_5__X43.jpg', 'p1_6__X44.jpg', 'curl_femoral_tumbado'),
    (1, 4, 'p1_7__X48.jpg', 'p1_8__X49.jpg', 'extension_cuadriceps'),
    (1, 5, 'p1_9__X53.jpg', 'p1_10__X54.jpg', 'gemelos_barra'),
    (1, 6, 'p1_11__X58.jpg', 'p1_12__X59.jpg', 'rueda_abdominal'),

    # Rutina 2: Torso Tracción
    (2, 1, 'p2_1__X65.jpg', 'p2_2__X66.jpg', 'jalon_cerrado_v'),
    (2, 2, 'p2_3__X70.jpg', 'p2_4__X71.jpg', 'remo_dorian'),
    (2, 3, 'p2_5__X75.jpg', 'p2_6__X76.jpg', 'remo_gironda'),
    (2, 4, 'p2_7__X80.jpg', 'p2_8__X81.jpg', 'face_pull'),
    (2, 5, 'p2_9__X85.jpg', 'p2_10__X86.jpg', 'curl_inclinado_45'),
    (2, 6, 'p2_11__X90.jpg', 'p2_12__X91.jpg', 'biceps_scott'),

    # Rutina 3: Pierna 2
    (3, 1, 'p3_1__X43.jpg', 'p3_2__X44.jpg', 'hip_thrust'),
    (3, 2, 'p3_3__X97.jpg', 'p3_4__X98.jpg', 'peso_muerto_rumano'),
    (3, 3, 'p3_5__X102.jpg', 'p3_6__X103.jpg', 'prensa_pies_altos'),
    (3, 4, 'p3_7__X107.jpg', 'p3_8__X108.jpg', 'curl_femoral_hsr'),
    (3, 5, 'p3_9__X115.jpg', 'p3_10__X116.jpg', 'soleo_sentado'),
    (3, 6, 'p3_11__X120.jpg', 'p3_12__X121.jpg', 'pallof_granjero'),

    # Rutina 4: Torso Empuje
    (4, 1, 'p4_1__X127.jpg', 'p4_2__X128.jpg', 'press_banca_plano'),
    (4, 2, 'p4_3__X132.jpg', 'p4_4__X133.jpg', 'press_inclinado_mancuerna'),
    (4, 3, 'p4_5__X137.jpg', 'p4_6__X138.jpg', 'pec_deck'),
    (4, 4, 'p4_7__X142.jpg', 'p4_8__X143.jpg', 'elevaciones_laterales'),
    (4, 5, 'p4_9__X147.jpg', 'p4_10__X148.jpg', 'press_frances_z'),
    (4, 6, 'p4_11__X152.jpg', 'p4_12__X153.jpg', 'triceps_cuerda'),
]

# Process images into side-by-side composite
for r_id, ex_num, f1, f2, slug in exercises:
    path1 = os.path.join('data/gym_images/extracted', f1)
    path2 = os.path.join('data/gym_images/extracted', f2)
    
    im1 = Image.open(path1)
    im2 = Image.open(path2)
    
    # Combined side by side
    w = im1.width + im2.width + 4
    h = max(im1.height, im2.height)
    combined = Image.new('RGB', (w, h), (18, 24, 38)) # dark slate separator
    combined.paste(im1, (0, 0))
    combined.paste(im2, (im1.width + 4, 0))
    
    # Resize to width 720 for crisp mobile display while keeping size ~35kb
    combined.thumbnail((720, 360), Image.Resampling.LANCZOS)
    out_path = f'data/gym_images/processed/ex_{r_id}_{ex_num}.jpg'
    combined.save(out_path, format='JPEG', quality=85, optimize=True)
    print(f'Processed {slug} -> {out_path} ({os.path.getsize(out_path)} bytes)')

print('All 24 exercise images generated successfully!')
