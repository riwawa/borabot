from telegram.ext import CommandHandler
import json

ARQUIVO_IDEIAS = "ideias.json"
ARQUIVO_VOTOS = "votos.json"

async def resultado(update, context):
    # carregar ideias
    try:
        with open(ARQUIVO_IDEIAS, "r") as f:
            ideias = json.load(f)
    except FileNotFoundError:
        await update.message.reply_text("Nenhuma ideia registrada ainda.")
        return

    # carregar votos
    try:
        with open(ARQUIVO_VOTOS, "r") as f:
            votos = json.load(f)
    except FileNotFoundError:
        votos = {}

    if not votos:
        await update.message.reply_text("Ainda não houve votos.")
        return

    # contar votos
    contagem = {}
    for escolha in votos.values():
        contagem[escolha] = contagem.get(escolha, 0) + 1

    # ordenar do mais votado
    ranking = sorted(contagem.items(), key=lambda x: x[1], reverse=True)

    mensagem = "resultado da votação:\n\n"
    for idx, (escolha, qtde) in enumerate(ranking, start=1):
        ideia = ideias[escolha]
        mensagem += f"{idx}️⃣ {ideia['texto']} ({qtde} votos) - {ideia['tipo']}, {ideia['orcamento']}, {ideia['duracao']}\n"

    await update.message.reply_text(mensagem)
