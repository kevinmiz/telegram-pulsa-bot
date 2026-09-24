import os

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


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
    await update.message.reply_text(
        "📱 Daftar Operator\n\n"
        "1. Telkomsel\n"
        "2. Indosat\n"
        "3. XL\n"
        "4. Tri\n\n"
        "Silakan pilih operator."
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

    print("Telegram Pulsa Bot sedang berjalan...")

    # Menjalankan bot menggunakan long polling
    application.run_polling()


if __name__ == "__main__":
    main()