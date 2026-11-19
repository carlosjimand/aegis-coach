import requests
import base64
import json
import pandas as pd

athlete_id = 'i690671'
api_key = '4cvqxm8a5intat925ttdcmpja'
auth_str = f'API_KEY:{api_key}'
b64_auth = base64.b64encode(auth_str.encode()).decode()
headers = {'Authorization': f'Basic {b64_auth}'}

# Fetch activities
url = f'https://intervals.icu/api/v1/athlete/{athlete_id}/activities?oldest=2026-09-01'
res = requests.get(url, headers=headers)
activities = res.json()

print(f"Total activities since Sept 1: {len(activities)}")

runs = [a for a in activities if a.get('type') == 'Run']
print(f"Total runs since Sept 1: {len(runs)}")

data = []
for r in runs:
    dist_km = r.get('distance', 0) / 1000.0
    sec = r.get('moving_time', 0)
    pace_sec = sec / dist_km if dist_km > 0 else 0
    m = int(pace_sec // 60)
    s = int(pace_sec % 60)
    pace_str = f"{m}:{s:02d}/km"
    
    data.append({
        'date': r.get('start_date_local')[:10],
        'time_str': r.get('start_date_local')[11:16],
        'name': r.get('name'),
        'distance_km': round(dist_km, 2),
        'duration_min': round(sec / 60.0, 1),
        'pace': pace_str,
        'pace_sec_km': round(pace_sec, 1),
        'avg_hr': r.get('average_heartrate'),
        'max_hr': r.get('max_heartrate'),
        'elevation_gain': r.get('total_elevation_gain'),
        'training_load': r.get('icu_training_load')
    })

df_runs = pd.DataFrame(data)
df_runs = df_runs.sort_values('date')
print("\nRecent Runs Detailed Analysis:")
print(df_runs.to_string(index=False))

# Check splits of Oct 6 and Oct 8
for target_date in ['2026-10-06', '2026-10-08', '2026-10-12']:
    target_acts = [a for a in activities if a.get('start_date_local', '').startswith(target_date) and a.get('type') == 'Run']
    for a in target_acts:
        act_id = a.get('id')
        det = requests.get(f'https://intervals.icu/api/v1/athlete/{athlete_id}/activities/{act_id}', headers=headers).json()
        print(f"\n--- Splits for {a.get('start_date_local')} ({a.get('name')}) ---")
        intervals = det if isinstance(det, list) else det.get('icu_intervals', [])
        for i, it in enumerate(intervals):
            dist = it.get('distance', 0)
            dur = it.get('elapsed_time', 0)
            p = (dur / (dist/1000))/60 if dist > 0 else 0
            mp = int(p)
            sp = int((p - mp)*60)
            hr = it.get('average_heartrate')
            print(f"  Split {i+1}: {dist:.0f}m in {dur:.0f}s ({mp}:{sp:02d}/km), HR: {hr}")



# Check athlete settings/zones in Intervals
url_profile = f'https://intervals.icu/api/v1/athlete/{athlete_id}'
p = requests.get(url_profile, headers=headers).json()
print("\nAthlete settings in Intervals.icu:")
for k in ['icu_resting_hr', 'icu_max_hr', 'icu_weight', 'icu_hr_zones', 'icu_pace_zones']:
    if k in p:
        print(f"  {k}: {p.get(k)}")
