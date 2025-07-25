# data/alerta_estado.py

import json
import os

STATE_FILE = os.path.join(os.path.dirname(__file__), 'alerta_estado.json')


def get_alerta_estado():
    if not os.path.exists(STATE_FILE):
        return True  # Por defecto la alerta está activa
    with open(STATE_FILE, 'r') as f:
        data = json.load(f)
        return data.get("activo", True)


def set_alerta_estado(activo: bool):
    with open(STATE_FILE, 'w') as f:
        json.dump({"activo": activo}, f)


def reset_alerta():
    set_alerta_estado(True)
