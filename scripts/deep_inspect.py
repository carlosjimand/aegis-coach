import requests, base64, json

athlete_id = 'i690671'
api_key = '4cvqxm8a5intat925ttdcmpja'
auth_str = f'API_KEY:{api_key}'
b64_auth = base64.b64encode(auth_str.encode()).decode()
headers = {'Authorization': f'Basic {b64_auth}'}

print("=" * 60)
print("1. 4x1500m (i199898391) DETAILS & INTERVALS")
print("=" * 60)
r_int = requests.get('https://intervals.icu/api/v1/activity/i199898391/intervals', headers=headers)
if r_int.status_code == 200:
    intervals_data = r_int.json()
    intervals = intervals_data.get('icu_intervals', [])
    print(f"Total intervals: {len(intervals)}")
    for i, it in enumerate(intervals):
        dist = it.get('distance', 0)
        time_s = it.get('moving_time', 0)
        hr = it.get('average_heartrate')
        max_hr = it.get('max_heartrate')
        pace_sec = (time_s / (dist / 1000)) if dist > 0 else 0
        pace_str = f"{int(pace_sec // 60)}:{int(pace_sec % 60):02d}/km" if dist > 0 else "-"
        cad = it.get('average_cadence')
        label = it.get('label') or it.get('type') or ''
        print(f"Interval {i+1:02d}: Dist: {dist:6.1f}m | Time: {time_s//60}m {time_s%60:02d}s ({time_s:3d}s) | Pace: {pace_str} | HR: {hr} (max {max_hr}) | Cad: {cad} | {label}")

# Also check Garmin laps from activity stream or icu_lap_count
r_act = requests.get('https://intervals.icu/api/v1/activity/i199898391', headers=headers)
d_act = r_act.json()
print("icu_lap_count:", d_act.get('icu_lap_count'))

# Let's inspect strength activities
for act_id, name in [('i200171689', 'Torso Tracción (Oct 21)'), ('i201394798', 'Pierna 2 (Oct 23)')]:
    print("\n" + "=" * 60)
    print(f"STRENGTH ACTIVITY: {name} ({act_id})")
    print("=" * 60)
    r = requests.get(f'https://intervals.icu/api/v1/activity/{act_id}', headers=headers)
    d = r.json()
    print("Name:", d.get('name'))
    print("Description:", d.get('description'))
    print("Moving time (min):", (d.get('moving_time') or 0) / 60)
    print("Kg lifted:", d.get('kg_lifted'))
    
    r_s = requests.get(f'https://intervals.icu/api/v1/activity/{act_id}/intervals', headers=headers)
    if r_s.status_code == 200:
        sets = r_s.json().get('icu_intervals', [])
        print(f"Sets recorded ({len(sets)}):")
        for idx, s in enumerate(sets):
            print(f"  Set {idx+1:02d}: {s}")

# Let's inspect Hike Peñalara
print("\n" + "=" * 60)
print("HIKE PEÑALARA (i202337891)")
print("=" * 60)
r_hike = requests.get('https://intervals.icu/api/v1/activity/i202337891', headers=headers)
h = r_hike.json()
print(f"Dist: {h.get('distance')/1000:.2f} km")
print(f"Time: {h.get('moving_time')//60}m {h.get('moving_time')%60}s")
print(f"Elevation Gain: {h.get('total_elevation_gain')}m | Loss: {h.get('total_elevation_loss')}m")
print(f"Avg HR: {h.get('average_heartrate')} | Max HR: {h.get('max_heartrate')}")
print(f"Training Load: {h.get('icu_training_load')}")
