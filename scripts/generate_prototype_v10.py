import re
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_TS_PATH = os.path.join(BASE_DIR, 'cloudflare', 'src', 'index.ts')
PROTOTYPE_PATH = os.path.join(BASE_DIR, 'prototype', 'index.html')

with open(INDEX_TS_PATH, 'r', encoding='utf-8') as f:
    ts_content = f.read()

with open(os.path.join(BASE_DIR, 'cloudflare', 'plan.json'), 'r', encoding='utf-8') as f:
    plan_json = json.load(f)

with open(os.path.join(BASE_DIR, 'data', 'weekly_evolution.json'), 'r', encoding='utf-8') as f:
    weekly_evo = json.load(f)

with open(os.path.join(BASE_DIR, 'data', 'full_multi_month_calendar.json'), 'r', encoding='utf-8') as f:
    multi_month_calendar = json.load(f)

display_weeks = [w for w in weekly_evo if w['run_km'] > 0 or w['week_start'] >= '2026-09-28']
short_labels = {
    "2026-09-28": "28 Sep",
    "2026-10-05": "5 Oct",
    "2026-10-12": "12 Oct",
    "2026-10-19": "19 Oct",
    "2026-10-26": "26 Oct",
    "2026-11-02": "2 Nov",
    "2026-11-09": "9 Nov",
    "2026-11-16": "16 Nov"
}
for w in display_weeks:
    if w['week_start'] in short_labels:
        w['label'] = short_labels[w['week_start']]
display_weeks.append({
    "week_start": "2026-11-16",
    "week_end": "2026-11-22",
    "label": "16 Nov (Hoy)",
    "run_km": 30.0,
    "runs": 4,
    "pace_avg": "4:45/km",
    "gym_sessions": 3,
    "ctl": 16.5,
    "atl": 26.0,
    "tsb": -9.5,
    "is_projected": True
})
display_weeks.append({
    "week_start": "2026-11-23",
    "week_end": "2026-11-29",
    "label": "23 Nov (Cross)",
    "run_km": 20.0,
    "runs": 4,
    "pace_avg": "4:15/km",
    "gym_sessions": 2,
    "ctl": 17.0,
    "atl": 18.0,
    "tsb": -1.0,
    "is_projected": True
})

# Extract HTML template from index.ts
html_match = re.search(r'return `(<!DOCTYPE html>.*?)`;\s*\}', ts_content, re.DOTALL)
if not html_match:
    print("Could not match HTML in index.ts")
    exit(1)

raw_html = html_match.group(1)

# Perform literal substitutions from production index.ts
replacements = {
    "${todayISO}": "2026-11-16",
    "${primaryObj.name}": "Cross Popular Parque del Soto (Ávila)",
    "${primaryObj.date}": "2026-11-28",
    "${primaryObj.distance_km}": "5.0",
    "${primaryObj.target_pace}": "3:30 - 3:35/km (~17:30)",
    "${primaryObj.surface}": "Hierba / Tierra compacta (1.060m altitud)",
    "${daysRemaining}": "12",
    "${weeksRemaining}": "1.7",
    "${todayPlan.day_name.toUpperCase()}": "LUNES",
    "${todayPlan.date}": "2026-11-16",
    "${todayPlan.title}": "Rodaje de Drenaje & Soltura Post-Fin de Semana",
    "${todayPlan.running.title}": "Rodaje de Drenaje & Soltura Post-Fin de Semana",
    "${todayPlan.running.session_type}": "Rodaje Regenerativo Z1-Z2",
    "${todayPlan.running.duration_min}": "35",
    "${todayPlan.running.distance_km}": "7",
    "${todayPlan.running.pace_target}": "4:55 - 5:10/km",
    "${todayPlan.running.hr_target}": "Z1 (<145 ppm)",
    "${todayPlan.running.target_pace}": "4:55 - 5:10/km",
    "${todayPlan.running.hr_zone}": "Z1 (<145 ppm)",
    "${todayPlan.gym.routine_name}": "Rutina 2 · Torso Tracción & Densidad (Pág 2 PDF)",
    "${safeJsonStringify(planData.days || [])}": json.dumps(plan_json['days'], ensure_ascii=False),
    "${safeJsonStringify(WEEKLY_EVO_DATA)}": json.dumps(display_weeks, ensure_ascii=False),
    "${safeJsonStringify(CALENDAR_DATA_BY_MONTH)}": json.dumps(multi_month_calendar, ensure_ascii=False),
    "${JSON.stringify(planData.days || [])}": json.dumps(plan_json['days'], ensure_ascii=False),
    "${JSON.stringify(WEEKLY_EVO_DATA)}": json.dumps(display_weeks, ensure_ascii=False),
    "${JSON.stringify(CALENDAR_DATA_BY_MONTH)}": json.dumps(multi_month_calendar, ensure_ascii=False),
    '${env?.AEGIS_SECRET_KEY || ""}': "test-key"
}

proto_html = raw_html
for k, v in replacements.items():
    proto_html = proto_html.replace(k, str(v))

# Ternary dynamic expressions
proto_html = re.sub(r'\$\{todayPlan\.running\.is_rest\s*\?[^}]+\}', "'35 min &bull; 4:55 - 5:10/km &bull; Z1 (<145 ppm)'", proto_html)
proto_html = re.sub(r'\$\{todayPlan\.gym\.is_rest\s*\?[^}]+\}', "'Torso Tracción & Densidad'", proto_html)

# Clean up favicon placeholder
proto_html = proto_html.replace('href="\' + favicon_data_uri + \'"', 'href="/img/icon-192.png"')

with open(PROTOTYPE_PATH, 'w', encoding='utf-8') as f:
    f.write(proto_html)

print(f"Prototype v10 successfully rebuilt to {PROTOTYPE_PATH} ({len(proto_html)} chars)")
