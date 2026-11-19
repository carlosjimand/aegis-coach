import requests, base64

athlete_id = 'i690671'
api_key = '4cvqxm8a5intat925ttdcmpja'
auth_str = f'API_KEY:{api_key}'
b64_auth = base64.b64encode(auth_str.encode()).decode()
headers = {'Authorization': f'Basic {b64_auth}'}

r_int = requests.get('https://intervals.icu/api/v1/activity/i199898391/intervals', headers=headers)
intervals = r_int.json().get('icu_intervals', [])
print("INDEX | START -> END | DURATION | DIST (GPS) | PACE (GPS) | HR (AVG/MAX) | TYPE")
for i, it in enumerate(intervals):
    s = it.get('start_time', 0)
    e = it.get('end_time', 0)
    dur = it.get('elapsed_time', 0)
    dist = it.get('distance', 0)
    hr = it.get('average_heartrate')
    max_hr = it.get('max_heartrate')
    pace_sec = (dur / (dist / 1000)) if dist > 0 else 0
    pace = f"{int(pace_sec // 60)}:{int(pace_sec % 60):02d}/km" if dist > 0 else "-"
    typ = it.get('type')
    print(f"{i+1:02d}    | {s:4d}s -> {e:4d}s | {dur//60}m {dur%60:02d}s ({dur:3d}s) | {dist:6.1f}m | {pace:8s} | {hr:3d} / {max_hr:3d} | {typ}")
