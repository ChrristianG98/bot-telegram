from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from flask import Flask
from threading import Thread

# Tu token de bot de Telegram
TOKEN = "8303573350:AAEXeHuN-Agnm6SMSaHAa4x5ee6zxoIM7fM"

# Lista global para guardar los números
numeros = []

# Inicia el bot con un mensaje
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("¡Hola! Envía números y usa /resultado para ver la suma, docenas y piezas. Usa /reset para comenzar de nuevo.")

# Agrega un número recibido
async def agregar_numero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        numero = int(update.message.text)
        numeros.append(numero)
        await update.message.reply_text(f"Número registrado: {numero}")
    except ValueError:
        await update.message.reply_text("Por favor, envía solo números enteros.")

# Muestra el resultado de la suma, docenas y piezas
async def resultado(update: Update, context: ContextTypes.DEFAULT_TYPE):
    suma = sum(numeros)
    docenas = suma // 12
    piezas = suma % 12
    await update.message.reply_text(
        f"Suma total: {suma}\nDocenas: {docenas}\nPiezas: {piezas}"
    )

# Reinicia la lista de números
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    numeros.clear()
    await update.message.reply_text("¡Registro reiniciado!")

# --- Configuración del bot de Telegram ---
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("resultado", resultado))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, agregar_numero))

# --- Servidor web para mantener vivo el bot ---
app_web = Flask('')

@app_web.route('/')
def home():
    return "El bot está activo"

def run():
    app_web.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()

# Ejecuta el bot
app.run_polling()
