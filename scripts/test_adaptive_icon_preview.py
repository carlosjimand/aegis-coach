from PIL import Image, ImageDraw
import os

def test_adaptive_masks():
    icon_path = 'cloudflare/public_exercises/icon-512.png'
    im = Image.open(icon_path).convert('RGBA')
    w, h = im.size

    # 1. Circle Mask (Android standard circle launcher)
    circle_mask = Image.new('L', (w, h), 0)
    draw_c = ImageDraw.Draw(circle_mask)
    draw_c.ellipse((0, 0, w, h), fill=255)
    
    circle_im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    circle_im.paste(im, (0, 0), circle_mask)
    
    # 2. Squircle Mask (Samsung OneUI / Android Squircle)
    squircle_mask = Image.new('L', (w, h), 0)
    draw_s = ImageDraw.Draw(squircle_mask)
    draw_s.rounded_rectangle((0, 0, w, h), radius=int(w * 0.22), fill=255)
    
    squircle_im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    squircle_im.paste(im, (0, 0), squircle_mask)

    # Save preview image with both side by side on dark gray background
    preview = Image.new('RGBA', (w * 2 + 60, h + 60), (30, 30, 35, 255))
    preview.paste(squircle_im, (20, 30), squircle_im)
    preview.paste(circle_im, (w + 40, 30), circle_im)

    preview_path = 'C:/Users/carlo/.gemini/antigravity/brain/d4e37e51-1f92-46c9-9a99-dcfde448f82c/android_launcher_mask_preview.png'
    preview.save(preview_path)
    print(f"Saved adaptive icon mask preview to {preview_path}!")

if __name__ == '__main__':
    test_adaptive_masks()
