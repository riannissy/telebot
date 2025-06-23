
import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    ContextTypes,
)

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Load environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_A_CHANNEL_ID = int(os.getenv("SOURCE_A_CHANNEL_ID"))
DEST_A_CHANNEL_ID = int(os.getenv("DEST_A_CHANNEL_ID"))
SOURCE_B_CHANNEL_ID = int(os.getenv("SOURCE_B_CHANNEL_ID"))
DEST_B_CHANNEL_ID = int(os.getenv("DEST_B_CHANNEL_ID"))

# Handle button press (Approve)
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    try:
        await query.answer()

        # Parse callback data: "approve|source_id|dest_id"
        data = query.data.split("|")
        if data[0] == "approve":
            source_id = int(data[1])
            dest_id = int(data[2])
            message_text = query.message.text

            # Forward the approved message
            await context.bot.send_message(chat_id=dest_id, text=message_text)

            # Remove the button from the original message
            await query.edit_message_reply_markup(reply_markup=None)

    except Exception as e:
        logging.error(f"Error in button_handler: {e}")

# Initialize and run bot
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CallbackQueryHandler(button_handler))
app.run_polling()
