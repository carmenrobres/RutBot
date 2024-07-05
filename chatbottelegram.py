import logging
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from chatgpt_client import request_chat_gpt
from sheets_client import append_to_sheet1
from datetime import datetime

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="✨ Hola! Sóc la Ruth, la cara amiga que sempre trobes a la Plaça de la Virreina. Benvingut/da! 🌸 Si vols conèixer més sobre mi i els meus veïns, no dubtis en parlar-me. Estic aquí per escoltar-te i compartir la vida del nostre encantador barri. Pregunta'm el que vulguis, estic aquí per ajudar-te!")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    username = update.message.from_user.username
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    response = request_chat_gpt(user_message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

    # Log the user message, bot response, username, and timestamp to Google Sheets
    append_to_sheet1([username, user_message, response, timestamp])

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(start_handler)
    application.add_handler(echo_handler)

    application.run_polling()
