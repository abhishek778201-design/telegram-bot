import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]
BASE_URL = os.environ["RENDER_EXTERNAL_URL"]  # Render sets this automatically
PORT = int(os.environ.get("PORT", 10000))


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.effective_user.first_name
    await update.effective_message.reply_text(f"Hello {name} Welcome")


async def anything(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text("Contact admin - @abhitech")


app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, anything))

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url=f"{BASE_URL}/{TOKEN}",
)
