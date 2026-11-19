import requests, base64, json

athlete_id = 'i690671'
api_key = '4cvqxm8a5intat925ttdcmpja'
auth_str = f'API_KEY:{api_key}'
b64_auth = base64.b64encode(auth_str.encode()).decode()
headers = {'Authorization': f'Basic {b64_auth}'}

url = f'https://intervals.icu/api/v1/athlete/{athlete_id}/activities?oldest=2026-10-27&newest=2026-11-02'
r = requests.get(url, headers=headers)
activities = r.json()
print(f"Total activities found: {len(activities)}")

for a in activities:
    act_id = a.get('id')
    act_name = a.get('name')
    act_type = a.get('type')
    start_date = a.get('start_date_local')
    dist = (a.get('distance') or 0) / 1000.0
    moving_time = a.get('moving_time') or 0
    hr = a.get('average_heartrate')
    max_hr = a.get('max_heartrate')
    load = a.get('icu_training_load')
    
    det_url = f'https://intervals.icu/api/v1/activity/{act_id}'
    r_det = requests.get(det_url, headers=headers)
    det = r_det.json() if r_det.status_code == 200 else {}
    
    desc = det.get('description') or a.get('description') or ''
    
    print("\n" + "=" * 70)
    print(f"DATE: {start_date} | TYPE: {act_type} | NAME: {act_name}")
    print(f"ID: {act_id} | Dist: {dist:.2f} km | Time: {moving_time//60}m {moving_time%60}s | Avg HR: {hr} (Max: {max_hr}) | Load: {load}")
    if desc:
        print(f"--- Description / Notes ---\n{desc}")
    
    # Check intervals
    r_int = requests.get(f'https://intervals.icu/api/v1/activity/{act_id}/intervals', headers=headers)
    if r_int.status_code == 200:
        int_data = r_int.json()
        intervals = int_data.get('icu_intervals', [])
        if intervals:
            print(f"--- Laps / Intervals ({len(intervals)}) ---")
            for idx, it in enumerate(intervals):
                it_dist = it.get('distance', 0) or 0
                it_dur = it.get('elapsed_time', 0) or 0
                it_hr = it.get('average_heartrate')
                it_pace = (it_dur / (it_dist/1000))/60 if it_dist > 0 else 0
                m = int(it_pace)
                s = int((it_pace - m) * 60)
                pace_str = f"{m}:{s:02d}/km" if it_dist > 0 else "-"
                label = it.get('label') or it.get('type') or ''
                print(f"   Lap {idx+1:02d}: {it_dist:5.0f}m | {it_dur:4d}s ({it_dur//60}m {it_dur%60:02d}s) | Pace: {pace_str} | HR: {it_hr} | {label}")

# Also fetch wellness/fitness metrics
url_well = f'https://intervals.icu/api/v1/athlete/{athlete_id}/wellness?oldest=2026-10-25&newest=2026-11-02'
rw = requests.get(url_well, headers=headers)
if rw.status_code == 200:
    wells = rw.json()
    print("\n" + "=" * 70)
    print("--- WELLNESS / FITNESS METRICS (CTL / ATL / TSB) ---")
    for w in wells:
        print(f"{w.get('id')} | CTL: {w.get('ctl'):.1f} | ATL: {w.get('atl'):.1f} | TSB: {((w.get('ctl') or 0) - (w.get('atl') or 0)):.1f} | RHR: {w.get('restingHR')}")
