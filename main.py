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


def main():
    if not TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN tidak ditemukan di file .env")

    # Membuat aplikasi Telegram Bot
    application = Application.builder().token(TOKEN).build()

    # Jika user mengirim /start, jalankan function start()
    application.add_handler(
        CommandHandler("start", start)
    )

    print("Telegram Pulsa Bot sedang berjalan...")

    # Menjalankan bot menggunakan long polling
    application.run_polling()


if __name__ == "__main__":
    main()