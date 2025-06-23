import os
import logging
import asyncio
import threading
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
)

# === Logging ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === Load environment variables ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_A_CHANNEL_ID = int(os.getenv("SOURCE_A_CHANNEL_ID"))
DEST_A_CHANNEL_ID = int(os.getenv("DEST_A_CHANNEL_ID"))
SOURCE_B_CHANNEL_ID = int(os.getenv("SOURCE_B_CHANNEL_ID"))
DEST_B_CHANNEL_ID = int(os.getenv("DEST_B_CHANNEL_ID"))

# === Telegram Bot Logic ===
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

    except Exception as e:
        logging.error(f"Error in button_handler: {e}")

# === Async bot run ===
async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CallbackQueryHandler(button_handler))
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    await app.updater.idle()

# === Flask server for port binding ===
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running"

# === Main entrypoint ===
if __name__ == "__main__":
    threading.Thread(target=lambda: asyncio.run(run_bot())).start()
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
