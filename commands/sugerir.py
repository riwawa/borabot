from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters
import json

IDEIA, TIPO, ORCAMENTO, DURACAO = range(4)
ARQUIVO_IDEIAS = "ideias.json"

# carregar ideias existentes
try:
    with open(ARQUIVO_IDEIAS, "r") as f:
        ideias = json.load(f)
except FileNotFoundError:
    ideias = []

async def start_sugerir(update, context):
    await update.message.reply_text("Qual ideia você quer sugerir?")
    return IDEIA

async def receber_ideia(update, context):
    context.user_data['texto'] = update.message.text
    await update.message.reply_text("Qual tipo de rolê? (comida / cultural / aventura / outro)")
    return TIPO

async def receber_tipo(update, context):
    context.user_data['tipo'] = update.message.text.lower()
    await update.message.reply_text("Qual o orçamento aproximado? (ex: baixo, médio, alto)")
    return ORCAMENTO

async def receber_orcamento(update, context):
    context.user_data['orcamento'] = update.message.text.lower()
    await update.message.reply_text("Qual a duração? (curta / longa / tarde / noite)")
    return DURACAO

async def receber_duracao(update, context):
    duracao = update.message.text.lower()
    usuario = update.effective_user.first_name

    ideia = {
        "usuario": usuario,
        "texto": context.user_data['texto'],
        "tipo": context.user_data['tipo'],
        "orcamento": context.user_data['orcamento'],
        "duracao": duracao
    }

    ideias.append(ideia)

    # salvar no arquivo
    with open(ARQUIVO_IDEIAS, "w") as f:
        json.dump(ideias, f, ensure_ascii=False, indent=2)

    await update.message.reply_text(f"Ideia registrada com sucesso! ✅\n{ideia}")
    return ConversationHandler.END

async def cancelar(update, context):
    await update.message.reply_text("Sugestão cancelada.")
    return ConversationHandler.END

conv_sugerir = ConversationHandler(
    entry_points=[CommandHandler("sugerir", start_sugerir)],
    states={
        IDEIA: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_ideia)],
        TIPO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_tipo)],
        ORCAMENTO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_orcamento)],
        DURACAO: [MessageHandler(filters.TEXT & ~filters.COMMAND, receber_duracao)],
    },
    fallbacks=[CommandHandler("cancelar", cancelar)]
)
