import os
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, ContextTypes, CommandHandler, MessageHandler, filters

from datetime import datetime
import pytz
import sys

# Set timezone to Malaysia
tz = pytz.timezone('Asia/Kuala_Lumpur')
now = datetime.now(tz)

# Run only between 7AM and 12PM
if now.hour < 7 or now.hour >= 12:
    sys.exit(0)


BOT_TOKEN = os.getenv("BOT_TOKEN")
SOURCE_CHANNEL_ID = int(os.getenv("SOURCE_CHANNEL_ID"))
DEST_CHANNEL_ID = int(os.getenv("DEST_CHANNEL_ID"))


# 2. Function to simulate receiving a form submission (replace with real logic later)
async def post_submission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This is a dummy function for demo — in your case, submission comes from Google Form
    keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("👍 Approve", callback_data="approve")]])
    await context.bot.send_message(
        chat_id=SOURCE_CHANNEL_ID,
        reply_markup=keyboard
    )

# 3. Handle the thumbs-up callback
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "approve":
        message_text = query.message.text  # Extract original message text

        # Re-send the message (instead of forwarding)
        await context.bot.send_message(
            chat_id=DEST_CHANNEL_ID,
            text=message_text
        )

        # Edit the original message to indicate it's been approved
        await query.edit_message_reply_markup(reply_markup=None)

# 4. Set up and run the bot
app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("submit", post_submission))  # For demo only
app.add_handler(CallbackQueryHandler(button_handler))

app.run_polling()
