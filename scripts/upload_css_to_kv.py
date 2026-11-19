import os
import re
import requests

config_path = r'C:\Users\carlo\AppData\Roaming\xdg.config\.wrangler\config\default.toml'
with open(config_path, 'r', encoding='utf-8') as f:
    text = f.read()

token = re.search(r'oauth_token\s*=\s*"([^"]+)"', text).group(1)
acc_id = '002d2d768548924ba8cbaae17182305c'
kv_id = '2df7fe02551a4ae29074519b8206a301'

with open('cloudflare/public_exercises/compiled_tailwind.css', 'r', encoding='utf-8') as f:
    css_content = f.read()

url = f'https://api.cloudflare.com/client/v4/accounts/{acc_id}/storage/kv/namespaces/{kv_id}/values/css_app'
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'text/css; charset=utf-8'
}
r = requests.put(url, headers=headers, data=css_content.encode('utf-8'))
print(f'Uploaded compiled_tailwind.css to KV key "css_app": status {r.status_code} ({len(css_content)} chars)')
