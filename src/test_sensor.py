# src/test_sensor.py
from sensor_reader import leer_temperatura_humedad
import time

print("🔍 Iniciando prueba del sensor DHT11...\n")

while True:
    temperatura, humedad = leer_temperatura_humedad()
    if temperatura is not None and humedad is not None:
        print(f"🌡️ Temp: {temperatura}°C  |  💧 Humedad: {humedad}%")
    else:
        print("⚠️ Lectura fallida.")
    time.sleep(2)

