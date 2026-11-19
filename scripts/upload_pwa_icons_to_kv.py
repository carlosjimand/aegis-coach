import os
import re
import requests

config_path = r'C:\Users\carlo\AppData\Roaming\xdg.config\.wrangler\config\default.toml'
with open(config_path, 'r', encoding='utf-8') as f:
    text = f.read()

token = re.search(r'oauth_token\s*=\s*"([^"]+)"', text).group(1)
acc_id = '002d2d768548924ba8cbaae17182305c'
kv_id = '2df7fe02551a4ae29074519b8206a301'

icons_to_upload = [
    ('icon-512.png', 'img_icon-512', 'image/png'),
    ('icon-192.png', 'img_icon-192', 'image/png'),
    ('apple-touch-icon.png', 'img_apple-touch-icon', 'image/png'),
    ('favicon-64.png', 'img_favicon_png', 'image/png'),
    ('favicon-32.png', 'img_favicon_32', 'image/png'),
    ('favicon.ico', 'img_favicon', 'image/x-icon')
]

for filename, kv_key, content_type in icons_to_upload:
    filepath = os.path.join('cloudflare/public_exercises', filename)
    with open(filepath, 'rb') as f:
        data = f.read()
    
    url = f'https://api.cloudflare.com/client/v4/accounts/{acc_id}/storage/kv/namespaces/{kv_id}/values/{kv_key}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': content_type
    }
    r = requests.put(url, headers=headers, data=data)
    print(f'Uploaded {filename} -> {kv_key} ({len(data)} bytes): status {r.status_code}')
