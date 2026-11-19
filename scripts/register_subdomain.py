import re
import requests

config_path = r'C:\Users\carlo\AppData\Roaming\xdg.config\.wrangler\config\default.toml'
with open(config_path, 'r', encoding='utf-8') as f:
    text = f.read()

token_match = re.search(r'oauth_token\s*=\s*"([^"]+)"', text)
if token_match:
    token = token_match.group(1)
    print("OAuth token extracted successfully.")
    acc_id = '002d2d768548924ba8cbaae17182305c'
    url = f'https://api.cloudflare.com/client/v4/accounts/{acc_id}/workers/subdomain'
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    candidates = ['uranuslabs', 'carlos-aegis', 'aegis-coach', 'carlosgomez-coach']
    for cand in candidates:
        r = requests.put(url, headers=headers, json={'subdomain': cand})
        print(f"Candidate '{cand}': status={r.status_code}, response={r.text}")
        if r.status_code == 200:
            print(f"SUCCESS! Registered subdomain: {cand}.workers.dev")
            break
else:
    print("Could not find oauth_token in default.toml")
