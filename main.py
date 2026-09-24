import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
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

    # Simpan pilihan user sementara
    context.user_data["operator"] = operator
    context.user_data["nominal"] = nominal
    context.user_data["waiting_for_phone"] = True

    await query.edit_message_text(
        f"📱 Operator: {operator.title()}\n"
        f"💰 Nominal: Rp{int(nominal):,}\n\n"
        "Silakan masukkan nomor HP tujuan."
        .replace(",", ".")
    )

async def input_nomor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.user_data.get("waiting_for_phone"):
        return

    nomor_hp = update.message.text.strip()

    if not nomor_hp.isdigit():
        await update.message.reply_text(
            "❌ Nomor HP hanya boleh berisi angka.\n"
            "Silakan masukkan kembali nomor HP."
        )
        return

    if not nomor_hp.startswith("08"):
        await update.message.reply_text(
            "❌ Nomor HP harus diawali dengan 08.\n"
            "Silakan masukkan kembali nomor HP."
        )
        return

    if len(nomor_hp) < 10 or len(nomor_hp) > 13:
        await update.message.reply_text(
            "❌ Panjang nomor HP harus antara 10–13 digit.\n"
            "Silakan masukkan kembali nomor HP."
        )
        return

    operator = context.user_data["operator"]
    nominal = context.user_data["nominal"]

    context.user_data["nomor_hp"] = nomor_hp
    context.user_data["waiting_for_phone"] = False

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Konfirmasi",
                callback_data="confirm_transaction"
            ),
            InlineKeyboardButton(
                "❌ Batal",
                callback_data="cancel_transaction"
            ),
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"📋 Konfirmasi Transaksi\n\n"
        f"📱 Operator: {operator.title()}\n"
        f"💰 Nominal: Rp{int(nominal):,}\n"
        f"☎️ Nomor HP: {nomor_hp}\n\n"
        f"Apakah data sudah benar?"
        .replace(",", "."),
        reply_markup=reply_markup
    )

async def proses_konfirmasi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action = query.data

    if action == "confirm_transaction":
        operator = context.user_data.get("operator")
        nominal = context.user_data.get("nominal")
        nomor_hp = context.user_data.get("nomor_hp")

        await query.edit_message_text(
            f"✅ Transaksi Berhasil\n\n"
            f"📱 Operator: {operator.title()}\n"
            f"💰 Nominal: Rp{int(nominal):,}\n"
            f"☎️ Nomor HP: {nomor_hp}\n\n"
            f"Pulsa berhasil diproses (simulasi)."
            .replace(",", ".")
        )

        context.user_data.clear()

    elif action == "cancel_transaction":
        await query.edit_message_text(
            "❌ Transaksi dibatalkan.\n\n"
            "Ketik /produk untuk memulai transaksi baru."
        )

        context.user_data.clear()


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

    application.add_handler(
       MessageHandler(
           filters.TEXT & ~filters.COMMAND,
           input_nomor
       )
    )

    application.add_handler(
       CallbackQueryHandler(
           proses_konfirmasi,
           pattern="^(confirm_transaction|cancel_transaction)$"
       )
    )

    print("Telegram Pulsa Bot sedang berjalan...")

    # Menjalankan bot menggunakan long polling
    application.run_polling()


if __name__ == "__main__":
    main()