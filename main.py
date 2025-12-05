import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

# تنظیمات لاگ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ====================
# منوی اصلی
# ====================

def get_main_menu():
    keyboard = [
        [InlineKeyboardButton("شروع 🚀", callback_data="start_now")],
        [
            InlineKeyboardButton("راهنما ℹ️", callback_data="help"),
            InlineKeyboardButton("درباره من 👤", callback_data="about")
        ],
        [InlineKeyboardButton("خدافظ 👋", callback_data="goodbye")]
    ]
    return InlineKeyboardMarkup(keyboard)

# ====================
# منوی با دکمه برگشت
# ====================

def get_back_menu(callback_data="main_menu"):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("برگشت ↩️", callback_data=callback_data)]
    ])

# ====================
# هندلرهای دستورات
# ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "🌟 سلام! من ربات هوشمند شما هستم!\n\n"
        "از دکمه‌های زیر استفاده کن تا شروع کنیم 👇"
    )
    await update.message.reply_text(welcome_text, reply_markup=get_main_menu())

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📖 راهنما:\n/start — نمایش منوی اصلی\n/help — نمایش این راهنما\n/about — اطلاعات درباره ربات\n«خدافظ» — خداحافظی دوستانه!",
        reply_markup=get_back_menu()
    )

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 ربات هوشمند\nنسخه: 1.0\nساخته‌شده توسط alitavv ❤️",
        reply_markup=get_back_menu()
    )

# ====================
# هندلر کلیک روی دکمه‌ها
# ====================

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "main_menu":
        welcome_text = (
            "🌟 سلام! من ربات هوشمند شما هستم!\n\n"
            "از دکمه‌های زیر استفاده کن تا شروع کنیم 👇"
        )
        await query.edit_message_text(text=welcome_text, reply_markup=get_main_menu())

    elif query.data == "start_now":
        await query.edit_message_text(
            "🔥 عالی! حالا می‌تونیم کار کنیم!\n\nدستورات رو امتحان کن یا فقط یه متن بفرست.",
            reply_markup=get_back_menu()
        )

    elif query.data == "help":
        await query.edit_message_text(
            "📖 راهنما:\n/start — منوی اصلی\n/help — این صفحه\n/about — درباره ما\n«خدافظ» — خداحافظی دوستانه!",
            reply_markup=get_back_menu()
        )

    elif query.data == "about":
        await query.edit_message_text(
            "🤖 ربات هوشمند\nنسخه: 1.0\nساخته‌شده توسط alitavv ❤️",
            reply_markup=get_back_menu()
        )

    elif query.data == "goodbye":
        await query.edit_message_text("خداحافظ! حتماً دوباره بیا 👋\nمن همیشه اینجام تا دوباره بیایی 💙")

# ====================
# هندلر پیام‌های متنی
# ====================

async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower().strip()
    
    if "سلام" in text or "های" in text or "hi" in text:
        await update.message.reply_text("👋 سلام دوست عزیز! چطور می‌تونم کمکت کنم؟")
    elif "خوبی" in text:
        await update.message.reply_text("عالیم! ممنون که پرسیدی 😊")
    elif "مرسی" in text or "تشکر" in text:
        await update.message.reply_text("خواهش می‌کنم! همیشه اینجام 🤗")
    elif "خدافظ" in text or "خداحافظ" in text or "بای" in text:
        await update.message.reply_text("خداحافظ! حتماً دوباره بیا 👋\nمن همیشه اینجام 💙")
    else:
        await update.message.reply_text("متاسفانه متوجه نشدم! 🤔\nمی‌تونی از دستورات استفاده کنی یا فقط 'سلام' بفرستی.")

# ====================
# خطای عمومی
# ====================

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error("Exception while handling an update:", exc_info=context.error)

# ====================
# راه‌اندازی ربات
# ====================

def main():
    TOKEN = os.environ.get("BOT_TOKEN")
    if not TOKEN:
        raise ValueError("❌ متغیر محیطی BOT_TOKEN تنظیم نشده!")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))

    app.add_error_handler(error_handler)

    print("✅ ربات در حال راه‌اندازی است...")
    
    PORT = int(os.environ.get("PORT", 8000))
    WEBHOOK_URL = os.environ.get("WEBHOOK_URL")
    
    if WEBHOOK_URL:
        app.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            webhook_url=f"{WEBHOOK_URL}/{TOKEN}"
        )
    else:
        app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()