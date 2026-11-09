
import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

TOKEN = os.environ["BOT_TOKEN"]
BASE_URL = os.environ["RENDER_EXTERNAL_URL"]
PORT = int(os.environ.get("PORT", 10000))

# Channel Details
CHANNEL_ID = "@proxpertquizbot"
CHANNEL_LINK = "https://t.me/proxpertquizbot"


async def is_member(user_id, context):
    try:
        member = await context.bot.get_chat_member(
            chat_id=CHANNEL_ID,
            user_id=user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except Exception as e:
        print(f"Verification Error: {e}")
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if await is_member(user.id, context):
        await update.effective_message.reply_text(
            f"Hello {user.first_name}! Welcome 🎉"
        )
        return

    keyboard = [
        [
            InlineKeyboardButton(
                "📢 JOIN CHANNEL",
                url=CHANNEL_LINK
            )
        ],
        [
            InlineKeyboardButton(
                "✅ VERIFY JOIN",
                callback_data="verify_join"
            )
        ]
    ]

    await update.effective_message.reply_text(
        "🔒 CHANNEL SUBSCRIPTION REQUIRED\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "Welcome to Proxpert Quiz Bot!\n\n"
        "To use this bot, please join our channel first.\n\n"
        "1️⃣ Click JOIN CHANNEL\n"
        "2️⃣ Join the channel\n"
        "3️⃣ Click VERIFY JOIN\n\n"
        "━━━━━━━━━━━━━━━━━━\n"
        "⚡ Join and unlock the bot!",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def verify_join(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    query = update.callback_query
    user = query.from_user

    if await is_member(user.id, context):
        await query.answer("✅ Verification Successful!")

        await query.edit_message_text(
            f"🎉 Hello {user.first_name}!\n\n"
            "Welcome to Proxpert Quiz Bot.\n"
            "Your subscription has been verified successfully. ✅"
        )

    else:
        await query.answer(
            "❌ Please join our channel first!",
            show_alert=True
        )


async def help_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.effective_message.reply_text(
        "https://t.me/proxpertquizbot"
    )


async def anything(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.effective_message.reply_text(
        "Contact admin - @abhitech"
    )


async def hello(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.effective_message.reply_text(
        "hii how are you"
    )


async def yt_cmd(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):
    await update.effective_message.reply_text(
        "https://t.me/VikasNCERT"
    )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("hello", hello))
app.add_handler(CommandHandler("yt", yt_cmd))
app.add_handler(CommandHandler("help", help_cmd))

app.add_handler(
    CallbackQueryHandler(
        verify_join,
        pattern="^verify_join$"
    )
)

app.add_handler(
    MessageHandler(filters.ALL, anything)
)

app.run_webhook(
    listen="0.0.0.0",
    port=PORT,
    url_path=TOKEN,
    webhook_url=f"{BASE_URL}/{TOKEN}",
)

