import openpyxl
from datetime import datetime, timedelta

wb = openpyxl.load_workbook('data/historial_entrenamientos_carlos.xlsx', data_only=True)
ws = wb['Actividades_Detalle']

activities = []
for row in ws.iter_rows(min_row=2, values_only=True):
    act_id, fecha, hora, tipo, nombre, dist, tiempo, ritmo = row[:8]
    if fecha:
        dt = datetime.strptime(str(fecha)[:10], '%Y-%m-%d')
        dist = float(dist) if dist and dist != '-' else 0.0
        tiempo = float(tiempo) if tiempo and tiempo != '-' else 0.0
        activities.append({'date': dt, 'type': str(tipo), 'name': str(nombre), 'dist': dist, 'time': tiempo, 'pace': str(ritmo)})

# Group by week (Monday to Sunday)
weeks = {}
for act in activities:
    monday = act['date'] - timedelta(days=act['date'].weekday())
    monday_str = monday.strftime('%Y-%m-%d')
    if monday_str not in weeks:
        weeks[monday_str] = {'run_km': 0.0, 'run_time': 0.0, 'gym_count': 0, 'other_time': 0.0, 'runs': 0}
    
    t = act['type'].lower()
    if 'run' in t:
        weeks[monday_str]['run_km'] += act['dist']
        weeks[monday_str]['run_time'] += act['time']
        weeks[monday_str]['runs'] += 1
    elif 'weight' in t or 'gym' in t:
        weeks[monday_str]['gym_count'] += 1
    else:
        weeks[monday_str]['other_time'] += act['time']

# Also get Fitness (CTL, ATL, TSB) from Fitness_y_Salud
ws_fit = wb['Fitness_y_Salud']
fit_data = {}
for row in ws_fit.iter_rows(min_row=2, values_only=True):
    f_date, ctl, atl, tsb = row[:4]
    if f_date:
        fit_data[str(f_date)[:10]] = {'ctl': ctl, 'atl': atl, 'tsb': tsb}

weekly_summary = []
for w, data in sorted(weeks.items()):
    avg_pace_min = (data['run_time'] / data['run_km']) if data['run_km'] > 0 else 0
    m = int(avg_pace_min)
    s = int((avg_pace_min - m) * 60)
    # Sunday date
    sun_dt = datetime.strptime(w, '%Y-%m-%d') + timedelta(days=6)
    sun_str = sun_dt.strftime('%Y-%m-%d')
    f_stats = fit_data.get(sun_str, {'ctl': '-', 'atl': '-', 'tsb': '-'})
    
    weekly_summary.append({
        'week_start': w,
        'week_end': sun_str,
        'label': f"{datetime.strptime(w, '%Y-%m-%d').strftime('%d %b')}",
        'run_km': round(data['run_km'], 1),
        'runs': data['runs'],
        'pace_avg': f"{m}:{s:02d}/km" if data['run_km'] > 0 else "-",
        'gym_sessions': data['gym_count'],
        'ctl': f_stats.get('ctl', '-'),
        'atl': f_stats.get('atl', '-'),
        'tsb': f_stats.get('tsb', '-')
    })

import json
print(json.dumps(weekly_summary, indent=2))
with open('data/weekly_evolution.json', 'w', encoding='utf-8') as f:
    json.dump(weekly_summary, f, indent=2, ensure_ascii=False)
