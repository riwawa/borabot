from telegram.ext import ApplicationBuilder, CommandHandler
from commands.start import start
from commands.sugerir import conv_sugerir

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

print("Bot iniciado...")
app.run_polling()
