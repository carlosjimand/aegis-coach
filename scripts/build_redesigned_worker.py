import os
import re
import json
import subprocess

print("Iniciando generador de la Web App rediseñada...")

# Leer plan.json para asegurar datos maestros
with open('cloudflare/plan.json', 'r', encoding='utf-8') as f:
    plan_json = json.load(f)

print(f"Plan maestro cargado: {len(plan_json['days'])} días")
