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

# === Flask server ===
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "✅ Bot is running!"

# === Logging ===
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# === Load environment variables ===
def get_env_var(key, required=True):
    value = os.getenv(key)
    if required and value is None:
        logging.error(f"❌ Missing env var: {key}")
        exit(1)
    logging.info(f"✅ Loaded {key}")
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
            dest_id = int(data[2])
            message_text = query.message.text
            await context.bot.send_message(chat_id=dest_id, text=message_text)
            await query.edit_message_reply_markup(reply_markup=None)
            logging.info(f"✅ Forwarded to {dest_id}")
    except Exception as e:
        logging.error(f"❌ Button handler error: {e}")

# === Run Telegram bot as a background coroutine ===
async def run_bot():
    logging.info("🚀 Starting Telegram bot...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()  # NOTE: not blocking, works in create_task

# === Main asyncio loop ===
def start_all():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(run_bot())
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    start_all()
