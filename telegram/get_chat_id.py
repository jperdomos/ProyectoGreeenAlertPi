# telegram/get_chat_id.py

from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from config import BOT_TOKEN

async def recibir_mensaje(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    print(f"📩 chat_id: {chat_id}")
    await update.message.reply_text(f"Tu chat_id es: {chat_id}")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_mensaje))
print("✅ Envía un mensaje al bot para obtener tu chat_id.")
app.run_polling()
