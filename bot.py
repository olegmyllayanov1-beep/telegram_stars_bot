from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    LabeledPrice
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters
)

# 🔴 ВСТАВЬ СЮДА СВОЙ ТОКЕН
TOKEN = "8594677794:AAGVthZDbk0Hyhph7jF-NwgYlDFsJryx-eo"

STAR_PACKS = {
    "10": 10,
    "50": 50,
    "100": 100
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет!\n\n"
        "⭐ Здесь можно купить Telegram Stars\n"
        "Нажми /buy"
    )

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("⭐ 10 Stars", callback_data="buy_10")],
        [InlineKeyboardButton("⭐ 50 Stars", callback_data="buy_50")],
        [InlineKeyboardButton("⭐ 100 Stars", callback_data="buy_100")]
    ]
    await update.message.reply_text(
        "Выбери пакет:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    stars = query.data.split("_")[1]

    prices = [
        LabeledPrice(
            label=f"{stars} Telegram Stars",
            amount=STAR_PACKS[stars]
        )
    ]

    await query.message.reply_invoice(
        title=f"Покупка {stars} ⭐",
        description="Telegram Stars",
        payload=f"stars_{stars}",
        provider_token="",   # ⭐ ОБЯЗАТЕЛЬНО ПУСТО
        currency="XTR",      # ⭐ ОБЯЗАТЕЛЬНО XTR
        prices=prices
    )

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stars = update.message.successful_payment.total_amount
    await update.message.reply_text(
        f"✅ Оплата успешна!\nТы купил ⭐ {stars}"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("buy", buy))
    app.add_handler(CallbackQueryHandler(on_callback))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(
        MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment)
    )

    app.run_polling()

if __name__ == "__main__":
    main()
