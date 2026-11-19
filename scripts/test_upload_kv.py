import re
import requests

config_path = r'C:\Users\carlo\AppData\Roaming\xdg.config\.wrangler\config\default.toml'
with open(config_path, 'r', encoding='utf-8') as f:
    text = f.read()

token = re.search(r'oauth_token\s*=\s*"([^"]+)"', text).group(1)
acc_id = '002d2d768548924ba8cbaae17182305c'
kv_id = '2df7fe02551a4ae29074519b8206a301'

with open('data/gym_images/processed/test_lat_pulldown.jpg', 'rb') as f:
    img_bytes = f.read()

url = f'https://api.cloudflare.com/client/v4/accounts/{acc_id}/storage/kv/namespaces/{kv_id}/values/img_test_lat'
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'image/jpeg'
}
r = requests.put(url, headers=headers, data=img_bytes)
print('Upload status:', r.status_code, r.text[:200])
