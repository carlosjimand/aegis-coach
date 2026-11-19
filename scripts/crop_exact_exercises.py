import os
import pdfplumber
from PIL import Image

os.makedirs('data/gym_images/exact_crops', exist_ok=True)

with pdfplumber.open('Rutinas_Gimnasio_Carlos_Visual.pdf') as pdf:
    for p_num in range(4):
        page = pdf.pages[p_num]
        p_img = Image.open(f'data/gym_images/page_{p_num+1}.png')
        scale_x = p_img.width / page.width
        scale_y = p_img.height / page.height
        
        # Sort images by row (top) then column (x0)
        imgs = sorted(page.images, key=lambda x: (round(x['top'], -1), x['x0']))
        # Each page has 6 exercises, 2 images per exercise:
        # Ex 1: imgs[0], imgs[1]
        # Ex 2: imgs[2], imgs[3]
        # Ex 3: imgs[4], imgs[5]
        # Ex 4: imgs[6], imgs[7]
        # Ex 5: imgs[8], imgs[9]
        # Ex 6: imgs[10], imgs[11]
        
        for ex_idx in range(6):
            im_a = imgs[ex_idx * 2]
            im_b = imgs[ex_idx * 2 + 1]
            
            # Bounding box enclosing both Inicio and Final
            x0 = min(im_a['x0'], im_b['x0'])
            top = min(im_a['top'], im_b['top'])
            x1 = max(im_a['x0'] + im_a['width'], im_b['x0'] + im_b['width'])
            bottom = max(im_a['top'] + im_a['height'], im_b['top'] + im_b['height'])
            
            # Convert to pixel coordinates
            crop_box = (
                int(x0 * scale_x),
                int(top * scale_y),
                int(x1 * scale_x),
                int(bottom * scale_y)
            )
            
            cropped = p_img.crop(crop_box)
            out_file = f'data/gym_images/exact_crops/ex_{p_num+1}_{ex_idx+1}.jpg'
            cropped.save(out_file, quality=90)
            print(f"Page {p_num+1} Ex {ex_idx+1}: {out_file} size={cropped.size}")

print("All exact crops completed!")
