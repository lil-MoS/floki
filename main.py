import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# توکن ربات تلگرام
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# تنظیمات لاگ‌گیری
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ایجاد اپلیکیشن Flask
app = Flask(__name__)

# ایجاد اپلیکیشن ربات تلگرام
application = Application.builder().token(TOKEN).build()

# هندلر دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("سلام! به ربات من خوش آمدید.")

# افزودن هندلر به ربات تلگرام
application.add_handler(CommandHandler("start", start))

# Endpoint برای دریافت آپدیت‌های تلگرام
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    """این متد، آپدیت‌های تلگرام را از طریق webhook دریافت می‌کند."""
    json_data = request.get_json()
    update = Update.de_json(json_data, application.bot)
    application.update_queue.put(update)
    return "OK"

# اجرای Flask در سرور
if __name__ == "__main__":
    # تنظیم Webhook
    application.bot.set_webhook(url=f"https://your-domain.com/{TOKEN}")
    # اجرای سرور Flask
    app.run(host="0.0.0.0", port=5000)
