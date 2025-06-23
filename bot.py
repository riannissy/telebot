import os
import logging
import asyncio
from flask import Flask
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
)

# === Logging ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === Load environment variables safely ===
def get_env_var(key, default=None, required=True):
    value = os.getenv(key, default)
    if required and value is None:
        logging.error(f"❌ Environment variable '{key}' is missing.")
        exit(1)
    logging.info(f"✅ Loaded {key}: {value}")
    return value

BOT_TOKEN = get_env_var("BOT_TOKEN")
SOURCE_A_CHANNEL_ID = int(get_env_var("SOURCE_A_CHANNEL_ID"))
DEST_A_CHANNEL_ID = int(get_env_var("DEST_A_CHANNEL_ID"))
SOURCE_B_CHANNEL_ID = int(get_env_var("SOURCE_B_CHANNEL_ID"))
DEST_B_CHANNEL_ID = int(get_env_var("DEST_B_CHANNEL_ID"))

# === Telegram logic ===
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()
        data = query.data.split("|")
        if data[0] == "approve":
            source_id = int(data[1])
            dest_id = int(data[2])
            message_text = query.message.text
            await context.bot.send_message(chat_id=dest_id, text=message_text)
            await query.edit_message_reply_markup(reply_markup=None)
            logging.info(f"✅ Forwarded to {dest_id}")
    except Exception as e:
        logging.error(f"❌ Error: {e}")

# === Flask server ===
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running!"

# === Combined async runner ===
async def run_everything():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.initialize()
    await app.start()
    asyncio.create_task(app.updater.start_polling())

# === Entrypoint ===
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(run_everything())
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
