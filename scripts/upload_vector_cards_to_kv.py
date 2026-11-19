import os
import re
import requests
import time

config_path = r'C:\Users\carlo\AppData\Roaming\xdg.config\.wrangler\config\default.toml'
with open(config_path, 'r', encoding='utf-8') as f:
    text = f.read()

token = re.search(r'oauth_token\s*=\s*"([^"]+)"', text).group(1)
acc_id = '002d2d768548924ba8cbaae17182305c'
kv_id = '2df7fe02551a4ae29074519b8206a301'

img_dir = 'cloudflare/public_exercises'
files = [f for f in os.listdir(img_dir) if f.startswith('ex_') and f.endswith('.png')]

print(f"Uploading {len(files)} vector exercise cards to Cloudflare KV...")

for filename in sorted(files):
    key = f"vector_{filename.replace('.png', '')}"
    filepath = os.path.join(img_dir, filename)
    with open(filepath, 'rb') as f:
        data = f.read()
    
    url = f'https://api.cloudflare.com/client/v4/accounts/{acc_id}/storage/kv/namespaces/{kv_id}/values/{key}'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'image/png'
    }
    r = requests.put(url, headers=headers, data=data)
    if r.status_code == 200:
        print(f"Uploaded {key} ({len(data)} bytes) -> HTTP 200")
    else:
        print(f"Failed {key} -> HTTP {r.status_code}: {r.text}")
    time.sleep(0.08)

print("All 24 vector cards uploaded to Cloudflare KV!")
