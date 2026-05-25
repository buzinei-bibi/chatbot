import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ==========================
# carregar .env
# ==========================
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("telegram_bot_token")
GROQ_API_KEY = os.getenv("groq_api_key")

# ==========================
# validação
# ==========================
# modelo Groq
# ==========================
chat = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    api_key=GROQ_API_KEY
)

# ==========================
# função de conversa
# ==========================
def conversar(pergunta: str) -> str:
    resposta = chat.invoke([
        ("system", "você é um assistente útil e objetivo."),
        ("human", pergunta)
    ])
    return resposta.content

# ==========================
# comandos Telegram
# ==========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("bot online 🚀")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        pergunta = update.message.text
        resposta = conversar(pergunta)
        await update.message.reply_text(resposta)
    except Exception as e:
        await update.message.reply_text(f"Erro: {str(e)}")

# ==========================
# main
# ==========================
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    print("bot iniciado...")
    app.run_polling()

# ==========================
# executar
# ==========================
if __name__ == "__main__":
    main()