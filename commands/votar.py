from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackQueryHandler, CommandHandler
import json
import os

ARQUIVO_IDEIAS = "ideias.json"
ARQUIVO_VOTOS = "votos.json"

# garante que os arquivos existam
if not os.path.exists(ARQUIVO_IDEIAS):
    with open(ARQUIVO_IDEIAS, "w") as f:
        json.dump([], f)

if not os.path.exists(ARQUIVO_VOTOS):
    with open(ARQUIVO_VOTOS, "w") as f:
        json.dump({}, f)

async def votar_inline(update, context):
    # carregar ideias
    with open(ARQUIVO_IDEIAS, "r") as f:
        ideias = json.load(f)

    if not ideias:
        await update.message.reply_text("Nenhuma ideia registrada ainda.")
        return

    # criar botões
    keyboard = [
        [InlineKeyboardButton(f"{idx+1}. {i['texto']}", callback_data=str(idx))]
        for idx, i in enumerate(ideias)
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Escolha uma ideia para votar:", reply_markup=reply_markup)

async def button_callback(update, context):
    query = update.callback_query
    await query.answer()

    escolha = int(query.data)
    usuario = str(query.from_user.id)

    # carregar votos
    with open(ARQUIVO_VOTOS, "r") as f:
        votos = json.load(f)

    # registrar ou atualizar voto
    votos[usuario] = escolha

    # salvar votos
    with open(ARQUIVO_VOTOS, "w") as f:
        json.dump(votos, f, ensure_ascii=False, indent=2)

    # carregar ideias para mostrar o texto correto
    with open(ARQUIVO_IDEIAS, "r") as f:
        ideias = json.load(f)

    await query.edit_message_text(
        f"Você votou na ideia: {ideias[escolha].get('texto', 'Ideia sem texto')} ✅"
    )

# Handlers prontos para adicionar no main.py
handler_command = CommandHandler("votar", votar_inline)
handler_callback = CallbackQueryHandler(button_callback)
