import json
import re
import requests

def update_kv(key, value):
    config_path = r'C:\Users\carlo\AppData\Roaming\xdg.config\.wrangler\config\default.toml'
    with open(config_path, 'r', encoding='utf-8') as f:
        text = f.read()

    token_match = re.search(r'oauth_token\s*=\s*"([^"]+)"', text)
    if not token_match:
        print("Could not find oauth_token")
        return False
        
    token = token_match.group(1)
    acc_id = '002d2d768548924ba8cbaae17182305c'
    kv_id = '2df7fe02551a4ae29074519b8206a301'
    url = f'https://api.cloudflare.com/client/v4/accounts/{acc_id}/storage/kv/namespaces/{kv_id}/values/{key}'
    headers = {'Authorization': f'Bearer {token}'}
    
    val_str = json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else str(value)
    r = requests.put(url, headers=headers, data=val_str.encode('utf-8'))
    print(f"KV PUT '{key}': status {r.status_code}")
    return r.status_code == 200

# Plan Maestro Bi-Semanal (14 Días: 16 al 29 Nov 2026)
plan_data = {
    "athlete": {
        "name": "Carlos Jiménez Andrino",
        "weight_kg": 63.0,
        "height_m": 1.73,
        "recent_milestone": "10K Ávila Monumental en 38:26 (3:50/km @ 1.070m altitud)"
    },
    "macrocycle": {
        "current_microcycle": "Bloque Pre-Milán & Afinamiento Cross del Soto (16 al 29 Nov)",
        "primary_objective": {
            "name": "Cross Popular Parque del Soto (Ávila)",
            "date": "2026-11-28",
            "distance_km": 5.0,
            "target_pace": "3:35 - 3:40/km (~18:00)",
            "surface": "Hierba / Tierra compacta (1.060m altitud)"
        },
        "secondary_objective": {
            "name": "San Silvestre",
            "date": "2026-12-31",
            "distance_km": 6.5,
            "target_pace": "Sub 3:35/km (Sub 23:15)"
        }
    },
    "days": [
        # ==========================================
        # SEMANA 1: PRE-MILÁN (16 al 22 Noviembre)
        # ==========================================
        {
            "date": "2026-11-16",
            "day_name": "Lunes",
            "display_date": "16 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": False,
                "session_type": "Rodaje Regenerativo Z1-Z2",
                "title": "Rodaje de Drenaje & Soltura Post-Fin de Semana",
                "duration_min": 35,
                "target_distance_km": 7.0,
                "target_pace": "4:55 - 5:10/km",
                "hr_zone": "Z1 (<145 ppm)",
                "warmup": "Movilidad articular de cadera y tobillo (5 min)",
                "main_work": "35 min continuos suaves en asfalto/tierra plana. Oxigenar piernas sin impacto articular duro tras el paintball y la fiesta.",
                "cooldown": "Caminar 3 min + estiramientos suaves de isquios y gemelos",
                "shoes_recommended": "Asics Novablast 5"
            },
            "gym": {
                "is_rest": False,
                "routine_id": 2,
                "routine_name": "Rutina 2 · Torso Tracción & Densidad (Pág 2 PDF)",
                "highlight_exercises": [
                    {"name": "Jalón Agarre Cerrado V", "load": "4 series x 4-6 reps @ 54 - 59 kg", "rir": "RIR 1"},
                    {"name": "Remo Dorian Unilateral", "load": "3 series x 6-8 reps @ 28 - 30 kg", "rir": "RIR 1"},
                    {"name": "Remo Gironda Amplio", "load": "3 series x 8-10 reps @ 36 kg", "rir": "RIR 1"},
                    {"name": "Face Pull en Polea Alta", "load": "3 series x 10-12 reps @ 23 - 27 kg", "rir": "RIR 2"},
                    {"name": "Curl Bíceps Mancuernas Inclinado", "load": "3 series x 8-10 reps @ 12 kg/mano", "rir": "RIR 1"},
                    {"name": "Rueda Abdominal", "load": "3 series x 8-10 reps", "rir": "RIR 1"}
                ],
                "knee_vmo_protocol": None
            }
        },
        {
            "date": "2026-11-17",
            "day_name": "Martes",
            "display_date": "17 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": True,
                "session_type": "Día de Trabajo en Madrid",
                "title": "Descanso Total de Carrera (Viaje Laboral)",
                "duration_min": 0,
                "target_distance_km": 0.0,
                "target_pace": "N/A",
                "hr_zone": "Reposo",
                "warmup": "Descanso de impacto",
                "main_work": "Día laboral en Madrid. Llegada a Ávila sobre las 19:30-20:00. Cero carrera para absorber el viaje y llegar fresco al VO2max del miércoles.",
                "cooldown": "Descanso y buena hidratación",
                "shoes_recommended": "Calzado casual cómodo"
            },
            "gym": {
                "is_rest": False,
                "routine_id": 4,
                "routine_name": "Rutina 4 · Torso Empuje en Ávila (Noche - 35 min)",
                "highlight_exercises": [
                    {"name": "Press de Banca Plano Máquina", "load": "3 series x 6 reps @ 30 kg/lado", "rir": "RIR 1-2"},
                    {"name": "Press Inclinado con Mancuernas (30°)", "load": "3 series x 8 reps @ 16 kg/mano", "rir": "RIR 1"},
                    {"name": "Pec Deck / Aperturas", "load": "3 series x 8 reps @ 59 - 66 kg", "rir": "RIR 1"},
                    {"name": "Tríceps Polea con Cuerda", "load": "3 series x 10 reps @ Nivel medio", "rir": "RIR 0-1"}
                ],
                "knee_vmo_protocol": None
            }
        },
        {
            "date": "2026-11-18",
            "day_name": "Miércoles",
            "display_date": "18 Nov",
            "is_key_session": True,
            "manual_status": "auto",
            "running": {
                "is_rest": False,
                "session_type": "Series VO2max en Terreno Firme",
                "title": "SESIÓN CLAVE PRE-MILÁN: 4 x 1.000m @ 3:30-3:32/km",
                "duration_min": 50,
                "target_distance_km": 9.5,
                "target_pace": "3:30 - 3:32 por 1.000m (Recuperación: 2' estático o trote)",
                "hr_zone": "Z4 / Z5 (174 - 186 ppm)",
                "warmup": "15 min trote progresivo Z1->Z2 + movilidad + 4 rectas vivas",
                "main_work": "4 x 1.000m en pista de atletismo o asfalto llano y limpio. Objetivo: clavar el ritmo objetivo en suelo firme sin derrapes de barro. Recuperación: 2 min para permitir aclaramiento parcial de lactato.",
                "cooldown": "10 min trote suave de vuelta a la calma",
                "shoes_recommended": "Nike Streakfly 2"
            },
            "gym": {
                "is_rest": True,
                "routine_id": None,
                "routine_name": "Descanso de Fuerza (Máxima Asimilación de VO2max)",
                "highlight_exercises": [],
                "knee_vmo_protocol": None
            }
        },
        {
            "date": "2026-11-19",
            "day_name": "Jueves",
            "display_date": "19 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": False,
                "session_type": "Rodaje Regenerativo Z1 + Rectas",
                "title": "Rodaje Suave Pre-Viaje (30') + 4 Progresiones",
                "duration_min": 30,
                "target_distance_km": 6.0,
                "target_pace": "5:00 - 5:15/km (Rectas sueltas)",
                "hr_zone": "Z1 (<140 ppm)",
                "warmup": "Movilidad dinámica",
                "main_work": "30 min muy fáciles para soltar piernas antes del viaje + 4 rectas de 80m sueltas sin fatiga.",
                "cooldown": "Estiramientos suaves de gemelos y sóleo",
                "shoes_recommended": "Asics Novablast 5"
            },
            "gym": {
                "is_rest": False,
                "routine_id": 3,
                "routine_name": "Rutina 3 · Pierna 2 Controlada (Pág 3 PDF - 40 min)",
                "highlight_exercises": [
                    {"name": "Hip Thrust con Barra en Banco", "load": "3 series x 6 reps @ 130 - 140 kg (control estricto, sin récord)", "rir": "RIR 2"},
                    {"name": "Peso Muerto Rumano Unilateral", "load": "3 series x 6 reps @ 20 - 22 kg/mano", "rir": "RIR 2"},
                    {"name": "Sóleo Sentado en Máquina", "load": "3 series x 8 reps @ 35 - 40 kg (pausa 2s)", "rir": "RIR 1"}
                ],
                "knee_vmo_protocol": "Spanish Squat isométrica con banda: 3 series x 35s"
            }
        },
        {
            "date": "2026-11-20",
            "day_name": "Viernes",
            "display_date": "20 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": True,
                "session_type": "Viaje a Milán (Vuelo)",
                "title": "Desplazamiento a Italia & Descanso de Entrenamiento",
                "duration_min": 0,
                "target_distance_km": 0.0,
                "target_pace": "N/A",
                "hr_zone": "Reposo",
                "warmup": "Movilidad de tobillo durante el viaje",
                "main_work": "Vuelo y llegada a Milán. Cero impacto de carrera. Disfrutar del viaje y caminar.",
                "cooldown": "Hidratación",
                "shoes_recommended": "Calzado casual cómodo"
            },
            "gym": {
                "is_rest": True,
                "routine_id": None,
                "routine_name": "Descanso de Fuerza (Viaje)",
                "highlight_exercises": [],
                "knee_vmo_protocol": None
            }
        },
        {
            "date": "2026-11-21",
            "day_name": "Sábado",
            "display_date": "21 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": True,
                "session_type": "Turismo Activo en Milán",
                "title": "Volumen Aeróbico Z1 Pasivo (Paseos)",
                "duration_min": 0,
                "target_distance_km": 0.0,
                "target_pace": "N/A",
                "hr_zone": "Caminata Z1 (<100 ppm)",
                "warmup": "Paseo continuo por la ciudad",
                "main_work": "Caminar 15.000 - 20.000 pasos. Excelente estímulo de capilarización y flujo sanguíneo sin impacto lesivo.",
                "cooldown": "Pies en alto al final del día en el hotel",
                "shoes_recommended": "Calzado cómodo de caminar"
            },
            "gym": {
                "is_rest": True,
                "routine_id": None,
                "routine_name": "Descanso Gimnasio",
                "highlight_exercises": [],
                "knee_vmo_protocol": None
            }
        },
        {
            "date": "2026-11-22",
            "day_name": "Domingo",
            "display_date": "22 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": True,
                "session_type": "Turismo Activo en Milán",
                "title": "Caminata & Asimilación Pre-Retorno",
                "duration_min": 0,
                "target_distance_km": 0.0,
                "target_pace": "N/A",
                "hr_zone": "Caminata Z1",
                "warmup": "Movilidad articular en el hotel (5 min)",
                "main_work": "Turismo activo a pie por Milán. Mantener la movilidad de tobillos y gemelos.",
                "cooldown": "Descanso y cena",
                "shoes_recommended": "Calzado cómodo de caminar"
            },
            "gym": {
                "is_rest": True,
                "routine_id": None,
                "routine_name": "Descanso Gimnasio",
                "highlight_exercises": [],
                "knee_vmo_protocol": None
            }
        },

        # ==========================================
        # SEMANA 2: COMPETICIÓN CROSS SOTO (23 al 29 Nov)
        # ==========================================
        {
            "date": "2026-11-23",
            "day_name": "Lunes",
            "display_date": "23 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": True,
                "session_type": "Regreso de Milán (Vuelo)",
                "title": "Descanso Total & Retorno a Ávila",
                "duration_min": 0,
                "target_distance_km": 0.0,
                "target_pace": "N/A",
                "hr_zone": "Reposo",
                "warmup": "Estiramientos suaves en casa",
                "main_work": "Vuelo y regreso de Milán. Descanso para disipar la fatiga de las caminatas y recuperar el sueño.",
                "cooldown": "Dormir bien e hidratarse",
                "shoes_recommended": "Calzado casual cómodo"
            },
            "gym": {
                "is_rest": True,
                "routine_id": None,
                "routine_name": "Descanso Gimnasio (Asimilación Viaje)",
                "highlight_exercises": [],
                "knee_vmo_protocol": None
            }
        },
        {
            "date": "2026-11-24",
            "day_name": "Martes",
            "display_date": "24 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": False,
                "session_type": "Reactivación Aeróbica Suave Z1",
                "title": "Rodaje de Reactivación Post-Milán (30-35') + 4 Rectas",
                "duration_min": 35,
                "target_distance_km": 6.5,
                "target_pace": "5:05 - 5:15/km",
                "hr_zone": "Z1 (<142 ppm)",
                "warmup": "Movilidad articular completa (tobillos y caderas)",
                "main_work": "30 min de trote regenerativo en tierra/asfalto plano + 4 rectas progresivas suaves de 80m en hierba para reconectar los receptores propioceptivos del pie.",
                "cooldown": "Caminar 2 min + soltar piernas",
                "shoes_recommended": "Asics Novablast 5"
            },
            "gym": {
                "is_rest": False,
                "routine_id": 2,
                "routine_name": "Rutina 2 · Torso Tracción Express Mantenimiento (25 min)",
                "highlight_exercises": [
                    {"name": "Jalón Agarre Cerrado V", "load": "3 series x 6 reps @ 50 kg (ligero, RIR 3)", "rir": "RIR 3"},
                    {"name": "Remo Dorian Unilateral", "load": "2 series x 8 reps @ 24 kg", "rir": "RIR 3"},
                    {"name": "Face Pull en Polea Alta", "load": "3 series x 12 reps @ 20 kg", "rir": "RIR 3"}
                ],
                "knee_vmo_protocol": "Activación isométrica suave de vasto medial: 2 series x 30s"
            }
        },
        {
            "date": "2026-11-25",
            "day_name": "Miércoles",
            "display_date": "25 Nov",
            "is_key_session": True,
            "manual_status": "auto",
            "running": {
                "is_rest": False,
                "session_type": "Afinamiento Neuromuscular Pre-Cross",
                "title": "AFINAMIENTO CLAVE PRE-CROSS: 3 x 500m @ Ritmo Cross",
                "duration_min": 40,
                "target_distance_km": 6.5,
                "target_pace": "1:45 - 1:47 por 500m (3:30 - 3:35/km) | Rec: 2'30\" amplia",
                "hr_zone": "Z4 / Ritmo Competición (sin fatiga residual)",
                "warmup": "15 min trote suave Z1 progresivo + ejercicios de técnica (skipping, zarpazo de tobillo) + 3 progresiones",
                "main_work": "3 x 500m clavando exactamente el ritmo de salida del cross (1:45-1:47). Recuperación amplia (2'30\" caminando y trote muy lento). Cero fatiga glucolítica: buscamos reclutamiento de fibras rápidas y confianza mecánica sin acumular lactato.",
                "cooldown": "8 min de trote muy suave de desasimilación",
                "shoes_recommended": "Zapatillas de clavos de cross (o Nike Streakfly 2)"
            },
            "gym": {
                "is_rest": True,
                "routine_id": None,
                "routine_name": "Descanso de Fuerza (Enfoque en Competición)",
                "highlight_exercises": [],
                "knee_vmo_protocol": None
            }
        },
        {
            "date": "2026-11-26",
            "day_name": "Jueves",
            "display_date": "26 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": True,
                "session_type": "Descanso Total Pre-Competición",
                "title": "Descanso Completo & Carga de Glucógeno",
                "duration_min": 0,
                "target_distance_km": 0.0,
                "target_pace": "N/A",
                "hr_zone": "Reposo",
                "warmup": "Movilidad de tobillo opcional",
                "main_work": "Cero impacto. Nutrición limpia con carbohidratos complejos (arroz, patata cocida, avena, pasta) + hidratación abundante con sales.",
                "cooldown": "Dormir 8 horas mínimo",
                "shoes_recommended": "Calzado casual cómodo"
            },
            "gym": {
                "is_rest": True,
                "routine_id": None,
                "routine_name": "Descanso Absoluto de Fuerza",
                "highlight_exercises": [],
                "knee_vmo_protocol": None
            }
        },
        {
            "date": "2026-11-27",
            "day_name": "Viernes",
            "display_date": "27 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": False,
                "session_type": "Activación Pre-Carrera (24h)",
                "title": "Activación Pre-Cross (15') + 4 Progresiones Vivas",
                "duration_min": 25,
                "target_distance_km": 4.0,
                "target_pace": "5:10/km trote + 4 rectas a ritmo de salida",
                "hr_zone": "Z1 (<135 ppm)",
                "warmup": "Movilidad dinámica de cadera y aductores",
                "main_work": "15 min muy suaves en hierba + 4 aceleraciones vivas de 60-80m con clavos puestos para chequear agarre del terreno y reactividad muscular.",
                "cooldown": "Soltar piernas. Revisar llave de clavos y apretar clavos de 6mm/9mm.",
                "shoes_recommended": "Clavos de cross (New Balance o Nike)"
            },
            "gym": {
                "is_rest": True,
                "routine_id": None,
                "routine_name": "Descanso de Gimnasio",
                "highlight_exercises": [],
                "knee_vmo_protocol": None
            }
        },
        {
            "date": "2026-11-28",
            "day_name": "Sábado",
            "display_date": "28 Nov",
            "is_key_session": True,
            "manual_status": "auto",
            "running": {
                "is_rest": False,
                "session_type": "COMPETICIÓN: CROSS POPULAR PARQUE DEL SOTO",
                "title": "¡DÍA D! CROSS POPULAR PARQUE DEL SOTO (5.000m)",
                "duration_min": 60,
                "target_distance_km": 8.5,
                "target_pace": "Km 1 @ 3:40/km -> Km 2-4 @ 3:35/km -> Km 5 @ sub 3:30/km",
                "hr_zone": "Z5 / VO2max de Competición",
                "warmup": "15 min trote progresivo + movilidad dinámica + 3 rectas de aceleración 20 min antes del pistoletazo.",
                "main_work": "5.000m oficiales en el circuito del Parque del Soto. Táctica: no suicidarse en los primeros 1.000m (3:40-3:42). Imponer ritmo de crucero en las zonas de curva y tierra (3:35). Desatar el cambio de mediofondista en el último km (sub 3:30/km). Objetivo de marca: 17:55 - 18:15.",
                "cooldown": "10 min de trote muy suave descalzo sobre el césped para descongestionar fascia y sóleos.",
                "shoes_recommended": "Zapatillas de clavos (6mm seco / 9mm húmedo o barro)"
            },
            "gym": {
                "is_rest": True,
                "routine_id": None,
                "routine_name": "Descanso de Fuerza (¡Celebración de Carrera!)",
                "highlight_exercises": [],
                "knee_vmo_protocol": None
            }
        },
        {
            "date": "2026-11-29",
            "day_name": "Domingo",
            "display_date": "29 Nov",
            "is_key_session": False,
            "manual_status": "auto",
            "running": {
                "is_rest": False,
                "session_type": "Regeneración Post-Competición Z1",
                "title": "Rodaje Regenerativo de Descarga Post-Cross",
                "duration_min": 35,
                "target_distance_km": 6.5,
                "target_pace": "5:15 - 5:30/km",
                "hr_zone": "Z1 (<138 ppm)",
                "warmup": "Movilidad articular muy suave",
                "main_work": "30-35 min de trote muy regenerativo en asfalto plano para barrer metabolitos y descargar la fascia. Si hay dolor o sobrecarga en sóleos por los clavos, sustituir por paseo suave.",
                "cooldown": "Estiramientos suaves y ducha de contrastes",
                "shoes_recommended": "Asics Novablast 5"
            },
            "gym": {
                "is_rest": True,
                "routine_id": None,
                "routine_name": "Descanso Gimnasio (Foam Roller y Movilidad)",
                "highlight_exercises": [],
                "knee_vmo_protocol": None
            }
        }
    ]
}

if __name__ == '__main__':
    with open('cloudflare/plan.json', 'w', encoding='utf-8') as f:
        json.dump(plan_data, f, ensure_ascii=False, indent=2)
    print("Saved cloudflare/plan.json with 14 days")
    update_kv("current_plan", plan_data)
