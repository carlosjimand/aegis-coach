import json
import pandas as pd
import openpyxl

wb = openpyxl.load_workbook('data/historial_entrenamientos_carlos.xlsx')

# Extract activities
ws_act = wb['Actividades_Detalle']
activities = []
for row in ws_act.iter_rows(min_row=2, values_only=True):
    if row[0]:
        activities.append({
            'id': row[0],
            'fecha': str(row[1]),
            'hora': str(row[2]),
            'tipo': str(row[3]),
            'nombre': str(row[4]),
            'dist_km': float(row[5] or 0),
            'tiempo_min': float(row[6] or 0),
            'ritmo': str(row[7]),
            'fc_media': row[8],
            'fc_max': row[9],
            'desnivel': row[10],
            'load': row[11],
            'notas': str(row[12] or '')
        })

print(f"Total activities loaded from Excel: {len(activities)}")

# Extract wellness
ws_well = wb['Fitness_y_Salud']
wellness = []
for row in ws_well.iter_rows(min_row=2, values_only=True):
    if row[0]:
        wellness.append({
            'fecha': str(row[0]),
            'ctl': float(row[1] or 0),
            'atl': float(row[2] or 0),
            'tsb': float(row[3] or 0),
            'rhr': row[4],
            'peso': row[5]
        })

print(f"Total wellness days: {len(wellness)}")

# Save to json for embedding
with open('data/dashboard_data.json', 'w', encoding='utf-8') as f:
    json.dump({'activities': activities, 'wellness': wellness}, f, indent=2)

print("Saved data/dashboard_data.json")
