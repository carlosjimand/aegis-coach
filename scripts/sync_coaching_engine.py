import requests
from urllib3.util import Retry
from requests.adapters import HTTPAdapter
import base64
import json
import os
import io
import fitparse
from datetime import datetime, timedelta
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# Athlete Credentials
ATHLETE_ID = os.getenv('ATHLETE_ID', 'i690671')
API_KEY = os.getenv('INTERVALS_API_KEY', '4cvqxm8a5intat925ttdcmpja')
AUTH_STR = f'API_KEY:{API_KEY}'
B64_AUTH = base64.b64encode(AUTH_STR.encode()).decode()
HEADERS = {'Authorization': f'Basic {B64_AUTH}'}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_DIR, exist_ok=True)
EXCEL_PATH = os.path.join(DATA_DIR, 'historial_entrenamientos_carlos.xlsx')

# Robust requests session with retry backoff and timeouts
session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504],
    raise_on_status=False
)
adapter = HTTPAdapter(max_retries=retries)
session.mount('https://', adapter)
session.mount('http://', adapter)

DEFAULT_TIMEOUT = (5.0, 25.0)

def fetch_activities(oldest_date='2026-08-15', newest_date=None):
    if newest_date is None:
        newest_date = datetime.now().strftime('%Y-%m-%d')
    url = f'https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/activities?oldest={oldest_date}&newest={newest_date}'
    r = session.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    if r.status_code == 200:
        return r.json()
    print(f"Error fetching activities: {r.status_code} {r.text}")
    return []

def fetch_activity_detail(act_id):
    url = f'https://intervals.icu/api/v1/activity/{act_id}'
    r = session.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    return r.json() if r.status_code == 200 else {}

def fetch_activity_intervals(act_id):
    url = f'https://intervals.icu/api/v1/activity/{act_id}/intervals'
    r = session.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    return r.json() if r.status_code == 200 else {}

def fetch_activity_fit_laps(act_id):
    url = f'https://intervals.icu/api/v1/activity/{act_id}/file'
    r = session.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    if r.status_code != 200:
        return None
    try:
        fit = fitparse.FitFile(io.BytesIO(r.content))
        laps = list(fit.get_messages('lap'))
        if not laps:
            return None
        res = []
        for l in laps:
            d = {f.name: f.value for f in l}
            tt = d.get('total_timer_time') or d.get('total_elapsed_time') or 0
            td = d.get('total_distance') or 0
            sp = d.get('avg_speed')
            pace = '-'
            if sp and sp > 0:
                s_km = 1000.0 / sp
                pace = f"{int(s_km // 60)}:{int(s_km % 60):02d}/km"
            res.append({
                'dist_m': round(td, 1),
                'time_s': int(round(tt)),
                'pace': pace,
                'avg_hr': d.get('avg_heart_rate'),
                'max_hr': d.get('max_heart_rate')
            })
        return res
    except Exception:
        return None

def fetch_wellness(oldest_date='2026-08-15', newest_date=None):
    if newest_date is None:
        newest_date = datetime.now().strftime('%Y-%m-%d')
    url = f'https://intervals.icu/api/v1/athlete/{ATHLETE_ID}/wellness?oldest={oldest_date}&newest={newest_date}'
    r = session.get(url, headers=HEADERS, timeout=DEFAULT_TIMEOUT)
    return r.json() if r.status_code == 200 else []

def format_pace(time_seconds, dist_meters):
    if not dist_meters or dist_meters <= 0 or not time_seconds:
        return "-"
    pace_sec = time_seconds / (dist_meters / 1000.0)
    m = int(pace_sec // 60)
    s = int(pace_sec % 60)
    return f"{m}:{s:02d}/km"

def build_excel_ledger():
    print("Sincronizando con Intervals.icu...")
    activities = fetch_activities()
    print(f"Total actividades recuperadas: {len(activities)}")
    wellness_data = fetch_wellness()
    
    # Sort activities by date
    activities = sorted(activities, key=lambda x: x.get('start_date_local', ''))
    
    act_rows = []
    interval_rows = []
    strength_rows = []
    
    for a in activities:
        act_id = a.get('id')
        name = a.get('name')
        typ = a.get('type')
        start_date = a.get('start_date_local', '')
        date_str = start_date[:10] if start_date else ''
        time_str = start_date[11:16] if len(start_date) >= 16 else ''
        dist_m = a.get('distance') or 0
        dist_km = round(dist_m / 1000.0, 2)
        moving_s = a.get('moving_time') or 0
        m_mins = round(moving_s / 60.0, 1)
        pace = format_pace(moving_s, dist_m) if typ in ['Run', 'VirtualRun'] else "-"
        avg_hr = a.get('average_heartrate')
        max_hr = a.get('max_heartrate')
        load = a.get('icu_training_load') or 0
        elev_gain = round(a.get('total_elevation_gain') or 0, 1)
        
        # Get details for description
        det = fetch_activity_detail(act_id)
        desc = det.get('description') or a.get('description') or ''
        
        act_rows.append({
            'ID': act_id,
            'Fecha': date_str,
            'Hora': time_str,
            'Tipo': typ,
            'Nombre': name,
            'Distancia (km)': dist_km,
            'Tiempo (min)': m_mins,
            'Ritmo Medio': pace,
            'FC Media': avg_hr,
            'FC Máxima': max_hr,
            'Desnivel + (m)': elev_gain,
            'Carga (Load)': load,
            'Notas / Descripción': desc
        })
        
        # Parse intervals if Run (Prefer raw Garmin FIT laps if available)
        if typ in ['Run', 'VirtualRun']:
            fit_laps = fetch_activity_fit_laps(act_id)
            if fit_laps and len(fit_laps) > 1:
                for idx, fl in enumerate(fit_laps):
                    t_sec = fl['time_s']
                    interval_rows.append({
                        'Actividad ID': act_id,
                        'Fecha': date_str,
                        'Actividad': name,
                        'Lap / Intervalo': idx + 1,
                        'Distancia (m)': fl['dist_m'],
                        'Tiempo (s)': t_sec,
                        'Tiempo (min:seg)': f"{t_sec//60}:{t_sec%60:02d}",
                        'Ritmo (/km)': fl['pace'],
                        'FC Media': fl['avg_hr'],
                        'FC Máx': fl['max_hr'],
                        'Tipo': 'Garmin Lap'
                    })
            else:
                int_data = fetch_activity_intervals(act_id)
                intervals = int_data.get('icu_intervals', [])
                for idx, it in enumerate(intervals):
                    it_dist = it.get('distance') or 0
                    it_time = it.get('elapsed_time') or it.get('moving_time') or 0
                    it_hr = it.get('average_heartrate')
                    it_max_hr = it.get('max_heartrate')
                    it_pace = format_pace(it_time, it_dist)
                    interval_rows.append({
                        'Actividad ID': act_id,
                        'Fecha': date_str,
                        'Actividad': name,
                        'Lap / Intervalo': idx + 1,
                        'Distancia (m)': round(it_dist, 1),
                        'Tiempo (s)': it_time,
                        'Tiempo (min:seg)': f"{it_time//60}:{it_time%60:02d}",
                        'Ritmo (/km)': it_pace,
                        'FC Media': it_hr,
                        'FC Máx': it_max_hr,
                        'Tipo': it.get('type', '')
                    })
                
        # Parse strength if notes exist
        if typ == 'WeightTraining' and desc:
            lines = desc.split('\n')
            current_exercise = ''
            for line in lines:
                line_s = line.strip()
                if not line_s: continue
                if line_s.startswith('*') or line_s.startswith('-') or line_s.startswith('#'):
                    current_exercise = line_s.lstrip('*#- ').strip()
                elif 'x' in line_s.lower() and ('kg' in line_s.lower() or 'reps' in line_s.lower() or 'peso' in line_s.lower()):
                    strength_rows.append({
                        'Fecha': date_str,
                        'Actividad ID': act_id,
                        'Sesión': name,
                        'Ejercicio': current_exercise or 'General',
                        'Detalle Set': line_s
                    })
    
    # Wellness summary
    well_rows = []
    for w in sorted(wellness_data, key=lambda x: x.get('id', '')):
        well_rows.append({
            'Fecha': w.get('id'),
            'CTL (Fitness)': round(w.get('ctl') or 0, 1),
            'ATL (Fatiga)': round(w.get('atl') or 0, 1),
            'TSB (Forma)': round((w.get('ctl') or 0) - (w.get('atl') or 0), 1),
            'FC Reposo': w.get('restingHR'),
            'Peso (kg)': w.get('weight')
        })
        
    df_act = pd.DataFrame(act_rows)
    df_int = pd.DataFrame(interval_rows)
    df_str = pd.DataFrame(strength_rows)
    df_well = pd.DataFrame(well_rows)
    
    # Build Excel with openpyxl
    wb = openpyxl.Workbook()
    # remove default sheet
    wb.remove(wb.active)
    
    # Style definitions
    header_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    zebra_fill = PatternFill(start_color="F2F5F8", end_color="F2F5F8", fill_type="solid")
    border_thin = Border(
        left=Side(style='thin', color='D9D9D9'),
        right=Side(style='thin', color='D9D9D9'),
        top=Side(style='thin', color='D9D9D9'),
        bottom=Side(style='thin', color='D9D9D9')
    )
    
    def add_sheet_from_df(title, df):
        ws = wb.create_sheet(title=title)
        ws.views.sheetView[0].showGridLines = True
        
        # Headers
        cols = list(df.columns)
        ws.append(cols)
        for col_num in range(1, len(cols) + 1):
            cell = ws.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            
        # Rows
        for r_idx, row in df.iterrows():
            row_data = list(row)
            ws.append(row_data)
            current_row = ws.max_row
            is_zebra = (r_idx % 2 == 1)
            for c_idx in range(1, len(cols) + 1):
                c = ws.cell(row=current_row, column=c_idx)
                c.border = border_thin
                if is_zebra:
                    c.fill = zebra_fill
                # Alignment
                val = c.value
                if isinstance(val, (int, float)):
                    c.alignment = Alignment(horizontal="right", vertical="center")
                else:
                    c.alignment = Alignment(horizontal="left", vertical="center")
                    
        # Auto column width
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 10), 45)
        ws.row_dimensions[1].height = 28
        return ws

    add_sheet_from_df("Actividades_Detalle", df_act)
    add_sheet_from_df("Series_y_Parciales", df_int)
    add_sheet_from_df("Fuerza_Gym", df_str)
    add_sheet_from_df("Fitness_y_Salud", df_well)
    
    # Add Sheet: Proximos_Objetivos
    ws_obj = wb.create_sheet(title="Proximos_Objetivos")
    ws_obj.views.sheetView[0].showGridLines = True
    obj_data = [
        ["Fecha", "Objetivo / Competición", "Distancia", "Terreno / Altitud", "Ritmo Objetivo", "Tiempo Target", "Estado"],
        ["08/11/2026", "10K Media Maratón Ávila Monumental", "10.00 km", "Asfalto / Adoquín (1.070m)", "3:50/km", "38:26 (Oficial)", "COMPLETADO (ÉXITO)"],
        ["28/11/2026", "Cross Popular Parque del Soto", "5.00 km", "Hierba / Tierra (1.060m)", "3:30/km", "17:30", "EN PREPARACIÓN (D-19)"],
        ["31/12/2026", "San Silvestre", "6.50 km", "Asfalto rápido", "Sub 3:35/km", "Sub 23:15", "OBJETIVO CUMBRE FIN DE AÑO"]
    ]
    for row in obj_data:
        ws_obj.append(row)
    for col_num in range(1, len(obj_data[0]) + 1):
        c = ws_obj.cell(row=1, column=col_num)
        c.fill = header_fill
        c.font = header_font
        c.alignment = Alignment(horizontal="center", vertical="center")
    for r in range(2, len(obj_data) + 1):
        for col_num in range(1, len(obj_data[0]) + 1):
            c = ws_obj.cell(row=r, column=col_num)
            c.border = border_thin
            c.alignment = Alignment(horizontal="left", vertical="center")
            if "COMPLETADO" in str(c.value):
                c.fill = PatternFill(start_color="D9EAD3", end_color="D9EAD3", fill_type="solid")
            elif "PREPARACIÓN" in str(c.value):
                c.fill = PatternFill(start_color="FFF2CC", end_color="FFF2CC", fill_type="solid")
    for col in ws_obj.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws_obj.column_dimensions[col_letter].width = max(max_len + 3, 14)
    ws_obj.row_dimensions[1].height = 28

    wb.save(EXCEL_PATH)
    print(f"Excel generado exitosamente en: {EXCEL_PATH}")

if __name__ == '__main__':
    build_excel_ledger()
