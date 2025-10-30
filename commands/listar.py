from telegram.ext import CommandHandler
import json

ARQUIVO_IDEIAS = "ideias.json"

async def listar(update, context):
    try:
        with open(ARQUIVO_IDEIAS, "r") as f:
            ideias = json.load(f)
    except FileNotFoundError:
        ideias = []

    if not ideias:
        await update.message.reply_text("Nenhuma ideia registrada ainda.")
        return

    mensagens = []
    for idx, ideia in enumerate(ideias, start=1):
        msg = (
            f"{idx}️⃣ {ideia.get('texto', 'Sem texto')} 📝\n"
            f"   Usuário: {ideia.get('usuario', 'Desconhecido')}\n"
            f"   Tipo: {ideia.get('tipo', 'Não definido')}\n"
            f"   Orçamento: {ideia.get('orcamento', 'Não definido')}\n"
            f"   Duração: {ideia.get('duracao', 'Não definido')}\n\n"
        )
        mensagens.append(msg)

    resposta = "\n\n".join(mensagens)
    await update.message.reply_text(resposta)