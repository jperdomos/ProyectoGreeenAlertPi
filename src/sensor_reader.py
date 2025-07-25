# src/sensor_reader.py

import board
import adafruit_dht
from src. settings import DHT_PIN

# Inicializar el sensor DHT11 en el pin definido
dht_device = adafruit_dht.DHT11(getattr(board, f"D{DHT_PIN}"))

def leer_temperatura_humedad():
    try:
        temperatura = dht_device.temperature
        humedad = dht_device.humidity
        return temperatura, humedad
    except Exception as e:
        print("Error leyendo sensor:", e)
        return None, None

