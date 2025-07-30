from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler
import os

TOKEN = "8303573350:AAEXeHuN-Agnm6SMSaHAa4x5ee6zxoIM7fM"
bot = Bot(token=TOKEN)

app = Flask(__name__)
dispatcher = Dispatcher(bot, None, use_context=True)

# Comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="¡Hola! Bot activo en Render con Webhook.")

# Agrega tus otros comandos aquí
dispatcher.add_handler(CommandHandler("start", start))

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot activo"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

