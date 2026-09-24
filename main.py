import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# Membaca isi file .env
load_dotenv()

# Mengambil token Telegram dari .env
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Selamat datang di Telegram Pulsa Bot! 📱\n\n"
        "Bot ini merupakan simulator pembelian pulsa."
    )

async def produk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    keyboard = [
        [
            InlineKeyboardButton("Telkomsel", callback_data="telkomsel"),
            InlineKeyboardButton("Indosat", callback_data="indosat"),
        ],
        [
            InlineKeyboardButton("XL", callback_data="xl"),
            InlineKeyboardButton("Tri", callback_data="tri"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "📱 Pilih Operator",
        reply_markup=reply_markup
    )

async def pilih_operator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    operator = query.data

    keyboard = [
        [
            InlineKeyboardButton("Rp5.000", callback_data=f"nominal_5000_{operator}"),
            InlineKeyboardButton("Rp10.000", callback_data=f"nominal_10000_{operator}"),
        ],
        [
            InlineKeyboardButton("Rp20.000", callback_data=f"nominal_20000_{operator}"),
            InlineKeyboardButton("Rp50.000", callback_data=f"nominal_50000_{operator}"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        f"📱 Operator: {operator.title()}\n\n"
        "Pilih nominal pulsa:",
        reply_markup=reply_markup
    )

async def pilih_nominal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    await query.answer()

    data = query.data

    _, nominal, operator = data.split("_")

    await query.edit_message_text(
        f"📱 Operator: {operator.title()}\n"
        f"💰 Nominal: Rp{int(nominal):,}".replace(",", ".")
    )

def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di file .env")

    # Membuat aplikasi Telegram Bot
    application = Application.builder().token(TOKEN).build()

    # Jika user mengirim /start, jalankan function start()
    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("produk", produk)
    )

    application.add_handler(
        CallbackQueryHandler(
            pilih_operator,
            pattern="^(telkomsel|indosat|xl|tri)$"
        )
    )

    application.add_handler(
       CallbackQueryHandler(
           pilih_nominal,
           pattern="^nominal_"
       )
    )

    print("Telegram Pulsa Bot sedang berjalan...")

    # Menjalankan bot menggunakan long polling
    application.run_polling()


if __name__ == "__main__":
    main()