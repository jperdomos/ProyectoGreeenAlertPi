import sys
import os
import json
import RPi.GPIO as GPIO
import time
from src.settings import LED_PIN, BUZZER_PIN
from data.log_utils import guardar_alerta

# Ruta al archivo JSON que contiene el estado de alerta
STATE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'alerta_estado.json')

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUZZER_PIN, GPIO.OUT)
pwm_buzzer = GPIO.PWM(BUZZER_PIN, 1000)

def leer_estado_alerta():
    try:
        with open(STATE_FILE, 'r') as f:
            estado = json.load(f)
            return estado.get("activo", True)
    except (FileNotFoundError, json.JSONDecodeError):
        return True  # Por defecto, activo

def activar_alerta(temperatura, humedad, duracion=2):
    if not leer_estado_alerta():
        print("🚫 Alerta desactivada desde Telegram. No se activará LED ni buzzer.")
        return

    print("🚨 ¡Alerta activada! LED encendido y buzzer sonando (PWM).")
    GPIO.output(LED_PIN, GPIO.HIGH)
    pwm_buzzer.start(50)
    guardar_alerta(temperatura, humedad, "ACTIVA")

    end_time = time.time() + duracion
    while time.time() < end_time:
        pwm_buzzer.ChangeFrequency(1000)
        time.sleep(0.3)
        pwm_buzzer.ChangeFrequency(1500)
        time.sleep(0.3)

    pwm_buzzer.stop()
    GPIO.output(LED_PIN, GPIO.LOW)

def limpiar_gpio():
    pwm_buzzer.stop()
    GPIO.output(LED_PIN, GPIO.LOW)
    GPIO.cleanup()
