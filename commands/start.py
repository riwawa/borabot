async def start(update, context):
    await update.message.reply_text(
        "Olá, eu sou o BoraBot! Vamos viajar.\n" 
        "Use /sugerir para sugestão de novos destinos."
    )
