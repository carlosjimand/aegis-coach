import requests, base64, json

athlete_id = 'i690671'
api_key = '4cvqxm8a5intat925ttdcmpja'
auth_str = f'API_KEY:{api_key}'
b64_auth = base64.b64encode(auth_str.encode()).decode()
headers = {'Authorization': f'Basic {b64_auth}'}

# Check Pierna 1 (Oct 29)
url = f'https://intervals.icu/api/v1/athlete/{athlete_id}/activities?oldest=2026-10-29&newest=2026-10-31'
r = requests.get(url, headers=headers)
acts = r.json()
for a in acts:
    act_id = a.get('id')
    det = requests.get(f'https://intervals.icu/api/v1/activity/{act_id}', headers=headers).json()
    print("=" * 60)
    print(f"ACTIVITY: {det.get('start_date_local')} | {det.get('name')} | ID: {act_id}")
    print("Description:\n", det.get('description'))
    print(f"Time: {det.get('moving_time')}s | HR: {det.get('average_heartrate')} | Load: {det.get('icu_training_load')}")

# Check Almanzor Hike (Oct 31)
hike = requests.get('https://intervals.icu/api/v1/activity/i204607663', headers=headers).json()
print("=" * 60)
print("ALMANZOR HIKE (i204607663)")
print(f"Dist: {hike.get('distance')/1000:.2f} km")
print(f"Elapsed time: {hike.get('elapsed_time')//60} min | Moving time: {hike.get('moving_time')//60} min")
print(f"Elev Gain: {hike.get('total_elevation_gain')} m | Loss: {hike.get('total_elevation_loss')} m")
print(f"Avg HR: {hike.get('average_heartrate')} | Max HR: {hike.get('max_heartrate')}")
print(f"Load: {hike.get('icu_training_load')}")
print("Description:\n", hike.get('description'))

# Check Torso Tracción (Oct 30)
torso = requests.get('https://intervals.icu/api/v1/activity/i203757172', headers=headers).json()
print("=" * 60)
print("TORSO TRACCIÓN (Oct 30) (i203757172)")
print("Description:\n", torso.get('description'))

# Check Sunday Run (Nov 1)
run1 = requests.get('https://intervals.icu/api/v1/activity/i204607667', headers=headers).json()
run2 = requests.get('https://intervals.icu/api/v1/activity/i204607685', headers=headers).json()
print("=" * 60)
print("SUNDAY RUN PART 1 (i204607667)")
print(f"Dist: {run1.get('distance')}m | Time: {run1.get('moving_time')}s | HR: {run1.get('average_heartrate')}")
print("SUNDAY RUN PART 2 (i204607685)")
print(f"Dist: {run2.get('distance')}m | Time: {run2.get('moving_time')}s | HR: {run2.get('average_heartrate')} (max {run2.get('max_heartrate')}) | Elev Gain: {run2.get('total_elevation_gain')}m")
