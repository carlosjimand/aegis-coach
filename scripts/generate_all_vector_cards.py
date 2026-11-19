import os
from PIL import Image, ImageDraw

assets_base = 'node_modules/@bryllim/workout-guide/assets'
output_dir = 'cloudflare/public_exercises'
os.makedirs(output_dir, exist_ok=True)

exercise_specs = {
    # Rutina 1: Pierna 1
    'ex_1_1': ('squat', 1, 3),
    'ex_1_2': ('leg-press', 3, 1),
    'ex_1_3': ('leg-extension', 1, 3),
    'ex_1_4': ('standing-calf-raise', 1, 3),
    'ex_1_5': ('bulgarian-split-squat', 2, 3),
    'ex_1_6': ('ab-wheel', 3, 1),

    # Rutina 2: Torso Tracción
    'ex_2_1': ('close-grip-lat-pulldown', 1, 3),
    'ex_2_2': ('one-arm-dumbbell-row', 1, 3),
    'ex_2_3': ('seated-row', 1, 3),
    'ex_2_4': ('face-pull', 1, 3),
    'ex_2_5': ('incline-dumbbell-curl', 1, 3),
    'ex_2_6': ('preacher-curl', 1, 3),

    # Rutina 3: Pierna 2
    'ex_3_1': ('hip-thrust', 3, 1),
    'ex_3_2': ('single-leg-romanian-deadlift', 1, 3),
    'ex_3_3': ('leg-press', 3, 1),
    'ex_3_4': ('seated-calf-raise', 1, 3),
    'ex_3_5': ('lying-leg-curl', 1, 3),
    'ex_3_6': ('hanging-leg-raise', 1, 3),

    # Rutina 4: Torso Empuje
    'ex_4_1': ('bench-press', 3, 1),
    'ex_4_2': ('incline-dumbbell-press', 1, 3),
    'ex_4_3': ('pec-deck', 1, 3),
    'ex_4_4': ('lateral-raise', 1, 3),
    'ex_4_5': ('tricep-pushdown', 2, 3),
    'ex_4_6': ('plank', 1, 2)
}

generated = []
for code, (folder, f_start, f_end) in exercise_specs.items():
    folder_path = os.path.join(assets_base, folder)
    img_start_path = os.path.join(folder_path, f'frame-{f_start}.png')
    img_end_path = os.path.join(folder_path, f'frame-{f_end}.png')

    if not os.path.exists(img_start_path) or not os.path.exists(img_end_path):
        print(f"ERROR: Missing files for {code} in {folder_path}")
        continue

    im_start = Image.open(img_start_path).convert('RGBA')
    im_end = Image.open(img_end_path).convert('RGBA')

    card = Image.new('RGBA', (600, 240), (20, 21, 34, 255))
    draw = ImageDraw.Draw(card)

    # Subtle vertical divider
    draw.line([(300, 20), (300, 220)], fill=(45, 47, 69, 255), width=1)

    # Resize frames
    s_resized = im_start.resize((210, 210), Image.Resampling.LANCZOS)
    e_resized = im_end.resize((210, 210), Image.Resampling.LANCZOS)

    card.paste(s_resized, (40, 15), s_resized)
    card.paste(e_resized, (350, 15), e_resized)

    # Central arrow pill
    draw.ellipse([284, 104, 316, 136], fill=(36, 38, 56, 255), outline=(255, 94, 128, 255), width=2)
    draw.line([(296, 120), (304, 120)], fill=(255, 94, 128, 255), width=2)
    draw.line([(301, 116), (305, 120)], fill=(255, 94, 128, 255), width=2)
    draw.line([(301, 124), (305, 120)], fill=(255, 94, 128, 255), width=2)

    out_file = os.path.join(output_dir, f'{code}.png')
    card.save(out_file, optimize=True)
    generated.append(code)

print(f"Generated {len(generated)} of {len(exercise_specs)} high-res vector cards!")
