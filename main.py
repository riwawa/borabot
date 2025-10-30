from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from commands.start import start
from commands.sugerir import conv_sugerir
from commands.listar import listar
from commands.votar import votar_inline, button_callback
from commands.resultado import resultado

from dotenv import load_dotenv
import os
import logging

load_dotenv()
token = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

app = ApplicationBuilder().token(token).build()

# /comandos
app.add_handler(CommandHandler('start', start))
app.add_handler(conv_sugerir)
app.add_handler(CommandHandler('listar', listar))
app.add_handler(CommandHandler('votar', votar_inline))
app.add_handler(CallbackQueryHandler(button_callback))
app.add_handler(CommandHandler('resultado', resultado))

print("Bot iniciado...")
app.run_polling()
