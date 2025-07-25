# tui/interface.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import curses
import time
from datetime import datetime

from src.sensor_reader import leer_temperatura_humedad
from data.alert_state import get_alerta_estado, set_alerta_estado, reset_alerta
from src.settings import TEMP_UMBRAL, HUM_UMBRAL, LED_PIN
from src.alert_manager import activar_alerta
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

def dibujar_pantalla(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(1000)

    temp_umbral = TEMP_UMBRAL
    hum_umbral = HUM_UMBRAL

    while True:
        stdscr.clear()
        hora_actual = datetime.now().strftime("%H:%M:%S")

        temperatura, humedad = leer_temperatura_humedad()
        estado_alerta = get_alerta_estado()
        gpio_salida = GPIO.input(LED_PIN)

        # Estado de temperatura
        temp_estado = "NORMAL"
        temp_icon = "✅"
        if temperatura is not None and temperatura > temp_umbral:
            temp_estado = "ALTA"
            temp_icon = "🔥"

        # Estado de humedad
        hum_estado = "NORMAL"
        hum_icon = "✅"
        if humedad is not None and humedad < hum_umbral:
            hum_estado = "BAJA"
            hum_icon = "💧"

        # Activación automática de alerta
        if estado_alerta and temperatura is not None and humedad is not None:
            if temperatura > temp_umbral or humedad < hum_umbral:
                activar_alerta(temperatura, humedad)

        alerta_txt = "ALERTA ⚠️" if estado_alerta else "INACTIVA ❎"
        gpio_txt = "ON 🟥" if gpio_salida else "OFF 🟩"

        # Mostrar interfaz
        stdscr.addstr(0, 0, "╔═════════════════════════════════════╗")
        stdscr.addstr(1, 0, "║     🌿 GreenAlertPi – MONITOREO    ║")
        stdscr.addstr(2, 0, "╠═════════════════════════════════════╣")
        stdscr.addstr(3, 0, f"║ Hora:       {hora_actual:<24}║")
        stdscr.addstr(4, 0, f"║ Temp:       {temperatura:.1f}°C  [{temp_estado}] {temp_icon:<3}║" if temperatura is not None else "║ Temp:       ---                    ║")
        stdscr.addstr(5, 0, f"║ Humedad:    {humedad:.1f}%   [{hum_estado}] {hum_icon:<3}║" if humedad is not None else "║ Humedad:    ---                    ║")
        stdscr.addstr(6, 0, f"║ Estado:     {alerta_txt:<24}║")
        stdscr.addstr(7, 0, f"║ Umbral T:   {temp_umbral}°C                    ║")
        stdscr.addstr(8, 0, f"║ Umbral H:   {hum_umbral}%                     ║")
        stdscr.addstr(9, 0, f"║ Salida GPIO:  {gpio_txt:<22}║")
        stdscr.addstr(10, 0,"╚═════════════════════════════════════╝")

        stdscr.addstr(12, 0, "Teclas permitidas:")
        stdscr.addstr(14, 0, "    q: salir")
        stdscr.addstr(15, 0, "    ↑ ↓: cambiar umbrales")
        stdscr.addstr(16, 0, "    r: reset de alerta")

        key = stdscr.getch()
        if key == ord("q"):
            break
        elif key == curses.KEY_UP:
            temp_umbral += 1
            hum_umbral += 1
        elif key == curses.KEY_DOWN:
            temp_umbral = max(1, temp_umbral - 1)
            hum_umbral = max(1, hum_umbral - 1)
        elif key == ord("r"):
            reset_alerta()

        stdscr.refresh()

    curses.endwin()

if __name__ == "__main__":
    curses.wrapper(dibujar_pantalla)
