import os
import threading
import logging
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler
)

# === Load Secrets ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_A_CHANNEL_ID = int(os.getenv("SOURCE_A_CHANNEL_ID"))
DEST_A_CHANNEL_ID = int(os.getenv("DEST_A_CHANNEL_ID"))
SOURCE_B_CHANNEL_ID = int(os.getenv("SOURCE_B_CHANNEL_ID"))
DEST_B_CHANNEL_ID = int(os.getenv("DEST_B_CHANNEL_ID"))

# === Logging ===
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# === Telegram Bot Logic ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is live!")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    try:
        data = query.data.split("|")
        if data[0] == "approve":
            source_id = int(data[1])
            dest_id = int(data[2])
            message_text = query.message.text
            await context.bot.send_message(chat_id=dest_id, text=message_text)
            await query.edit_message_reply_markup(reply_markup=None)
    except Exception as e:
        logging.error(f"Callback error: {e}")

def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

# === Flask for Render Port Ping ===
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Bot is running"

# === Main Entrypoint ===
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    web_app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
