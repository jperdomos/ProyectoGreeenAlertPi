# telegram/bot_handler.py
import json
import sys
import csv
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))


from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from sensor_reader import leer_temperatura_humedad
from config import BOT_TOKEN, CHAT_ID

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'alert_log.csv')
STATE_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'alerta_estado.json')

def guardar_estado_alerta(activo: bool):
    with open(STATE_FILE, 'w') as f:
        json.dump({"activo": activo}, f)

def leer_estado_alerta():
    if not os.path.exists(STATE_FILE):
        return True  # Activo por defecto
    with open(STATE_FILE, 'r') as f:
        estado = json.load(f)
    return estado.get("activo", True)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 ¡Hola! Soy tu bot de monitoreo GreenAlertPi.")

async def estado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    temperatura, humedad = leer_temperatura_humedad()
    if temperatura is None or humedad is None:
        await update.message.reply_text("⚠️ No se pudo leer el sensor.")
    else:
        mensaje = f"🌡️ Temp: {temperatura}°C\n💧 Humedad: {humedad}%"
        await update.message.reply_text(mensaje)

async def desactivar_alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    guardar_estado_alerta(False)
    await update.message.reply_text("🔕 Alerta desactivada temporalmente.")

async def activar_alerta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    guardar_estado_alerta(True)
    await update.message.reply_text("🔔 Alerta activada.")

async def historial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(LOG_FILE):
        await update.message.reply_text("📂 No hay historial disponible.")
        return

    with open(LOG_FILE, newline='') as f:
        reader = csv.reader(f)
        next(reader, None)  # Saltar encabezado
        filas = list(reader)[-5:]  # Últimos 5 registros

    if not filas:
        await update.message.reply_text("📂 No hay registros de alerta.")
        return

    mensaje = "📋 *Últimos registros de alerta:*\n"
    for row in filas:
        timestamp, temp, hum, estado = row
        mensaje += f"🕒 {timestamp}\n🌡️ {temp}°C | 💧 {hum}% | Estado: {estado}\n\n"

    await update.message.reply_text(mensaje, parse_mode="Markdown")

# Esta función la puede usar el sistema principal para leer el estado
def get_alerta_estado():
    return leer_estado_alerta()

# Enviar alerta desde el bot
async def enviar_alerta(context: ContextTypes.DEFAULT_TYPE, mensaje: str):
    await context.bot.send_message(chat_id=CHAT_ID, text=mensaje)


# Iniciar bot
def iniciar_bot():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("estado", estado))
    app.add_handler(CommandHandler("desactivar", desactivar_alerta))
    app.add_handler(CommandHandler("activar", activar_alerta))
    app.add_handler(CommandHandler("historial", historial))

    print("🤖 Bot ejecutándose...")
    app.run_polling()

if __name__ == "__main__":
    iniciar_bot()
