import pdfplumber

with pdfplumber.open('Rutinas_Gimnasio_Carlos_Visual.pdf') as pdf:
    for p_num in range(4):
        p = pdf.pages[p_num]
        print(f"=== PAGE {p_num+1} IMAGES ===")
        imgs = sorted(p.images, key=lambda x: (round(x['top'], -1), x['x0']))
        for idx, img in enumerate(imgs):
            name = img.get('name') or img.get('stream', {}).get('name')
            print(f"Img {idx+1}: top={img['top']:.1f}, x0={img['x0']:.1f}, w={img['width']:.1f}, h={img['height']:.1f}, obj={img.get('object_type')}, stream={img.get('id')}")
