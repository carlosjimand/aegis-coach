import openpyxl
import json
from datetime import datetime

wb = openpyxl.load_workbook('data/historial_entrenamientos_carlos.xlsx', data_only=True)
ws_act = wb['Actividades_Detalle']
ws_laps = wb['Series_y_Parciales']
ws_gym = wb['Fuerza_Gym']

# Map laps by activity ID
laps_by_act = {}
for r in ws_laps.iter_rows(min_row=2, values_only=True):
    if not r[0]: continue
    act_id = str(r[0])
    laps_by_act.setdefault(act_id, []).append({
        'lap': r[3],
        'dist_m': round(float(r[4]), 1) if r[4] is not None else 0,
        'time_s': r[5],
        'time_str': str(r[6]),
        'pace': str(r[7]),
        'hr_avg': int(r[8]) if r[8] is not None else 0,
        'hr_max': int(r[9]) if r[9] is not None else 0
    })

# Map gym sets by date
gym_by_date = {}
for r in ws_gym.iter_rows(min_row=2, values_only=True):
    if not r[0]: continue
    d = str(r[0])[:10]
    gym_by_date.setdefault(d, []).append({
        'exercise': str(r[1]),
        'set': r[2],
        'reps': r[3],
        'load': str(r[4])
    })

# Group activities by date
acts_by_date = {}
for r in ws_act.iter_rows(min_row=2, values_only=True):
    if not r[0]: continue
    act_id = str(r[0])
    d = str(r[1])[:10]
    t = str(r[3])
    name = str(r[4])
    dist = float(r[5]) if r[5] is not None else 0.0
    dur = float(r[6]) if r[6] is not None else 0.0
    pace = str(r[7])
    hr_avg = int(r[8]) if r[8] is not None else 0
    notes = str(r[12]) if r[12] is not None else ''

    acts_by_date.setdefault(d, []).append({
        'id': act_id,
        'type': t,
        'name': name,
        'dist_km': dist,
        'duration_min': dur,
        'pace': pace,
        'hr_avg': hr_avg,
        'notes': notes,
        'laps': laps_by_act.get(act_id, [])
    })

months_meta = {
    "2026-09": {"year": 2026, "month": 9, "month_name": "Septiembre 2026", "days_in_month": 30, "first_day_weekday": 1},
    "2026-10": {"year": 2026, "month": 10, "month_name": "Octubre 2026", "days_in_month": 31, "first_day_weekday": 3},
    "2026-11": {"year": 2026, "month": 11, "month_name": "Noviembre 2026", "days_in_month": 30, "first_day_weekday": 6},
    "2026-12": {"year": 2026, "month": 12, "month_name": "Diciembre 2026", "days_in_month": 31, "first_day_weekday": 1}
}

# Upcoming planned days in Nov
with open('cloudflare/plan.json', 'r', encoding='utf-8') as f:
    plan_data = json.load(f)
planned_days = {d['date']: d for d in plan_data.get('days', [])}

full_calendar = {}
for m_key, meta in months_meta.items():
    activities_dict = {}
    for day in range(1, meta["days_in_month"] + 1):
        date_str = f"{m_key}-{day:02d}"
        acts = acts_by_date.get(date_str, [])
        gym_sets = gym_by_date.get(date_str, [])
        
        # If we have real completed activities from Excel
        if acts or gym_sets:
            dots = []
            has_run = any(a['type'] in ['Run', 'VirtualRun'] for a in acts)
            has_gym = any(a['type'] == 'WeightTraining' for a in acts) or len(gym_sets) > 0
            has_hike = any(a['type'] in ['Hike', 'Ride'] for a in acts)

            if has_run: dots.append("run")
            if has_gym: dots.append("gym")
            if has_hike: dots.append("mountain")

            run_acts = [a for a in acts if a['type'] in ['Run', 'VirtualRun']]
            hike_acts = [a for a in acts if a['type'] in ['Hike', 'Ride']]
            gym_acts = [a for a in acts if a['type'] == 'WeightTraining']

            total_km = sum(a['dist_km'] for a in acts)
            total_dur = sum(a['duration_min'] for a in acts)
            
            title = ""
            act_type = ""
            pace_str = "-"
            hr_str = "-"
            ai_comment = ""
            notes_text = ""

            if run_acts:
                primary = max(run_acts, key=lambda x: x['dist_km'])
                title = primary['name']
                act_type = "Running" + (" + Gym" if has_gym else "")
                pace_str = primary['pace']
                hr_str = f"{primary['hr_avg']} ppm" if primary['hr_avg'] else "-"
                notes_text = primary['notes']
                if '6x800' in primary['name']:
                    ai_comment = "Series de 6x800m cross con clavos de 6mm en terreno mojado. Parciales exactos de vueltas Garmin: 2:53, 2:56, 2:55, 3:05, 3:10, 3:01 (recuperación clavada a 90s)."
                elif '10k' in primary['name'].lower():
                    ai_comment = "HITO HISTÓRICO: 10K Ávila Monumental oficial en 38:26 (3:50/km) a 1.070m de altitud con viento y desniveles duros."
                elif '4x1500' in primary['name']:
                    ai_comment = "Series de 4x1500m clavando ritmo objetivo con recuperación de 2'30\"."
                elif '3x2000' in primary['name']:
                    ai_comment = "Series largas de 3x2000m @ 4:00/km preparando la base de umbral anaeróbico."
                else:
                    ai_comment = f"Sesión de {primary['dist_km']:.1f} km a ritmo {primary['pace']} con FC media de {primary['hr_avg']} ppm."
            elif hike_acts:
                primary = hike_acts[0]
                title = primary['name']
                act_type = "Outdoor / Senderismo"
                pace_str = "-"
                hr_str = f"{primary['hr_avg']} ppm"
                notes_text = primary['notes']
                ai_comment = f"Entrenamiento aeróbico en altitud ({primary['name']}): {primary['dist_km']} km con aclimatación hipóxica."
            elif gym_acts or gym_sets:
                title = gym_acts[0]['name'] if gym_acts else "Sesión de Gimnasio"
                act_type = "Gimnasio & Fuerza"
                pace_str = "-"
                hr_str = f"{gym_acts[0]['hr_avg']} ppm" if gym_acts and gym_acts[0]['hr_avg'] else "-"
                notes_text = gym_acts[0]['notes'] if gym_acts else ""
                ai_comment = "Sesión de sobrecarga progresiva y blindaje neuromuscular registrada en Garmin/Aegis."

            all_laps = []
            for a in run_acts:
                all_laps.extend(a['laps'])

            activities_dict[date_str] = {
                "dots": dots,
                "title": title,
                "type": act_type,
                "km": round(total_km, 2),
                "time": f"{int(total_dur)} min" if total_dur > 0 else "-",
                "pace": pace_str,
                "hr": hr_str,
                "ai": ai_comment,
                "notes": notes_text.strip(),
                "laps": all_laps[:14],
                "gym_sets": gym_sets[:10]
            }
        elif date_str in planned_days:
            # Planned upcoming day
            p = planned_days[date_str]
            r = p['running']
            g = p['gym']
            dots = []
            if not r['is_rest']: dots.append("run")
            if not g['is_rest']: dots.append("gym")
            if r['is_rest'] and g['is_rest']: dots.append("mountain")

            activities_dict[date_str] = {
                "dots": dots,
                "title": r['title'] if not r['is_rest'] else (g['routine_name'] if not g['is_rest'] else "Descanso / Asimilación"),
                "type": ("Running" if not r['is_rest'] else "") + (" + Gym" if not g['is_rest'] and not r['is_rest'] else ("Gimnasio" if not g['is_rest'] else "Descanso")),
                "km": r.get('target_distance_km', 0.0),
                "time": f"{r.get('duration_min', 0)} min" if r.get('duration_min') else "-",
                "pace": r.get('target_pace', '-'),
                "hr": r.get('hr_zone', '-'),
                "ai": f"{r.get('main_work', '')} {g.get('routine_name', '')}".strip(),
                "notes": f"Calzado recomendado: {r.get('shoes_recommended', '-')}",
                "laps": [],
                "gym_sets": []
            }
        elif m_key == "2026-11" and day == 28:
            activities_dict["2026-11-28"] = {
                "dots": ["run"],
                "title": "CROSS POPULAR PARQUE DEL SOTO (5 KM)",
                "type": "COMPETICIÓN",
                "km": 5.0,
                "time": "17:30 obj",
                "pace": "3:30/km",
                "hr": "Z5 Máxima",
                "ai": "OBJETIVO PRIMARIO: 5 km en tierra/hierba @ 3:30/km (~17:30). Clavos de 6 mm obligatorios.",
                "notes": "Parque del Soto (Ávila). Circuito con giros y barro.",
                "laps": [],
                "gym_sets": []
            }

    # December target
    if m_key == "2026-12":
        activities_dict["2026-12-31"] = {
            "dots": ["run"],
            "title": "SAN SILVESTRE 2026 (6.5 KM)",
            "type": "COMPETICIÓN",
            "km": 6.5,
            "time": "Sub 23:15 obj",
            "pace": "Sub 3:35/km",
            "hr": "Z5 Máxima",
            "ai": "OBJETIVO SECUNDARIO: Asfalto urbano a ritmo de 3:34/km para despedir el año con marca personal.",
            "notes": "Objetivo de cierre de año en pico de forma tras el Cross del Soto.",
            "laps": [],
            "gym_sets": []
        }

    full_calendar[m_key] = {
        "year": meta["year"],
        "month": meta["month"],
        "month_name": meta["month_name"],
        "days_in_month": meta["days_in_month"],
        "first_day_weekday": meta["first_day_weekday"],
        "activities": activities_dict
    }

with open('data/full_multi_month_calendar.json', 'w', encoding='utf-8') as f:
    json.dump(full_calendar, f, indent=2, ensure_ascii=False)

print("Saved complete multi-month calendar successfully!")
for m, d in full_calendar.items():
    print(f"Month {m}: {len(d['activities'])} active/planned days")
