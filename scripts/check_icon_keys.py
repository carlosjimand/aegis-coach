import re
import requests

config_path = r'C:\Users\carlo\AppData\Roaming\xdg.config\.wrangler\config\default.toml'
with open(config_path, 'r', encoding='utf-8') as f:
    text = f.read()

token = re.search(r'oauth_token\s*=\s*"([^"]+)"', text).group(1)
acc_id = '002d2d768548924ba8cbaae17182305c'
kv_id = '2df7fe02551a4ae29074519b8206a301'

url = f'https://api.cloudflare.com/client/v4/accounts/{acc_id}/storage/kv/namespaces/{kv_id}/keys?limit=100'
headers = {'Authorization': f'Bearer {token}'}
r = requests.get(url, headers=headers)
keys = [k['name'] for k in r.json().get('result', [])]
matching = [k for k in keys if 'icon' in k or 'fav' in k or 'logo' in k]
print('Matching icon/favicon keys in KV:', matching)
