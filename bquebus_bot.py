import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)

GEMINI_KEY = "AIzaSyCe7_poNdZrqa0lKohMO4w9g2xLS_4Spqc"
TG_TOKEN   = "8803923099:AAHkxB5lvrtuZZTR5gvnbp-ZxsuBdPpa7cA"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""Eres BqueBus, un asistente experto en el transporte público de Barranquilla, Colombia.

Tu misión es ayudar a los usuarios a moverse por la ciudad de forma fácil, rápida y económica.

Ayudas con:
- Rutas de bus entre dos puntos de la ciudad
- Cómo usar el Transmetro (BRT) correctamente
- Tarifas y horarios aproximados
- Dónde esperar el transporte (paradas, portales)
- Combinación de rutas cuando es necesario
- Consejos de seguridad y zonas a evitar
- Diferencia entre bus, buseta, colectivo y Transmetro

Datos clave que conoces:
- Tarifa bus urbano: $2.500 COP aprox
- Tarifa Transmetro: $2.800 COP aprox
- Transmetro cubre: Portal del Prado (norte), La Castellana, Murillo, Ciudad Jardín, Portal Sur (sur)
- Estaciones Transmetro principales: Portal del Prado, Calle 72, Calle 84, Olaya, Las Américas, Portal Sur
- Rutas urbanas populares: 1, 2, 3, 4, 5, 7, 8, 10, 11, 14, 15, 17, 20, 21
- Barrios principales: El Prado, Manga, Riomar, Villa Santos, Boston, El Centro, Soledad, Malambo, Suroccidente, La Victoria, Los Andes, El Silencio, Ciudadela 20 de Julio
- Horario general buses: 5:00am - 11:00pm
- Transmetro: 5:00am - 10:00pm (lunes a sábado), 6:00am - 9:00pm (domingo)
- Empresas de buses: Coodetrans, Transcaribe, Metrocar, entre otras

Estilo de respuesta:
- Siempre en español, amigable y cercano
- Respuestas cortas y claras (máximo 3-4 párrafos)
- Usa emojis ocasionalmente para hacerlo más visual 🚌
- Si no tienes certeza de una ruta exacta, da orientación general y sugiere confirmar con el conductor
- Siempre ofrece alternativas (más rápida vs más económica)
- Si el usuario da una ubicación, ayúdalo con el transporte más cercano"""
)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy *BqueBus* 🚌\n\n"
        "Tu guía de transporte en Barranquilla. Cuéntame:\n\n"
        "• ¿Dónde estás?\n"
        "• ¿A dónde quieres ir?\n\n"
        "¡Y te digo cómo llegar! 💪",
        parse_mode="Markdown"
    )

async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🗺️ *Cómo usar BqueBus:*\n\n"
        "Solo escríbeme cosas como:\n\n"
        "➡️ _Estoy en El Prado y quiero ir al Centro_\n"
        "➡️ _¿Cómo llego a la Zona Franca?_\n"
        "➡️ _¿Cuánto cuesta el Transmetro?_\n"
        "➡️ _¿A qué hora sale el último bus de Soledad?_\n\n"
        "¡Pregunta lo que necesites! 😊",
        parse_mode="Markdown"
    )

async def handle(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    await update.message.chat.send_action("typing")
    try:
        chat = model.start_chat()
        resp = chat.send_message(msg)
        await update.message.reply_text(resp.text)
    except Exception as e:
        await update.message.reply_text(
            "Lo siento, tuve un problema respondiendo. Intenta de nuevo en un momento 🙏"
        )
        logging.error(f"Error: {e}")

app = ApplicationBuilder().token(TG_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))

print("🚌 BqueBus Bot activo...")
app.run_polling()
