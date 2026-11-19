import requests, base64

athlete_id = 'i690671'
api_key = '4cvqxm8a5intat925ttdcmpja'
auth_str = f'API_KEY:{api_key}'
b64_auth = base64.b64encode(auth_str.encode()).decode()
headers = {'Authorization': f'Basic {b64_auth}'}

# Check if intervals.icu has the original FIT file for download
for act_id in ['i200171689', 'i201394798']:
    r = requests.get(f'https://intervals.icu/api/v1/activity/{act_id}/file', headers=headers)
    print(f"File endpoint for {act_id}: status {r.status_code}, content-type: {r.headers.get('Content-Type')}, length: {len(r.content)}")
    if r.status_code == 200 and 'fit' in r.headers.get('Content-Type', '').lower():
        with open(f"scripts/{act_id}.fit", "wb") as f:
            f.write(r.content)
        print(f"Saved {act_id}.fit")
