import os
import uuid
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8780339717:AAEGqLrVWTIUpbyFE2l7LNgHnntWA9YninA"

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if "facebook.com" not in url:
        await update.message.reply_text("Gửi link Facebook hợp lệ.")
        return

    await update.message.reply_text("Đang tải video...")

    # tạo tên file ngẫu nhiên
    unique_id = str(uuid.uuid4())
    output_template = f"{unique_id}.%(ext)s"

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_template,
        'quiet': True
    }

    try:
        # tải video
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # tìm file vừa tải
        downloaded_file = None
        for file in os.listdir():
            if unique_id in file:
                downloaded_file = file
                break

        if downloaded_file is None:
            await update.message.reply_text("Không tìm thấy file video.")
            return

        # gửi video
        with open(downloaded_file, "rb") as video:
            await update.message.reply_video(video=video)

        # xóa file sau khi gửi xong
        os.remove(downloaded_file)

    except Exception as e:
        print("Lỗi chi tiết:", e)
        await update.message.reply_text("Lỗi khi tải video.")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

print("Bot đang chạy...")
app.run_polling()