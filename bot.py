import os
import logging
from telegram import Update, LabeledPrice
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters,
)

logging.basicConfig(level=logging.INFO)

TOKEN = os.getenv("BOT_TOKEN")

STAR_PACKS = {
    "10": 10,
    "50": 50,
    "100": 100,
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет!\nНапиши /buy чтобы купить Stars")

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Демо-инвойс (в реальном Stars надо настроить payments правильно)
    prices = [LabeledPrice(label="⭐ 10 Stars", amount=10)]
    await update.message.reply_text("⚠️ Покупка Stars требует корректной настройки платежей/инвойсов.\n"
                                    "Если ты делаешь Stars-бота — скажи, я настрою правильно под Telegram Stars.")

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.pre_checkout_query
    await query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Оплата прошла!")

def main():
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set (set it in Render Environment Variables)")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))

    app.run_polling()

if __name__ == "__main__":
    main()
