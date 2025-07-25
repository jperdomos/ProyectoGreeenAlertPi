import csv
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'alert_log.csv')

def inicializar_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["timestamp", "temperatura", "humedad", "estado_alerta"])

def guardar_alerta(temperatura, humedad, estado_alerta):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, mode='a', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([timestamp, temperatura, humedad, estado_alerta])
