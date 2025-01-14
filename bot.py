import logging
import os
import subprocess
import sys
from yt_dlp import YoutubeDL
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext, Update
import shutil

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_BOT_TOKEN:
    logger.error("TELEGRAM_BOT_TOKEN environment variable not set.")
    sys.exit(1)

# Define constants for quality options
VIDEO_QUALITIES = [
    ("Best (Video)", "best_video"),
    ("4320p (8K)", "4320"),
    ("2160p (UHD)", "2160"),
    ("1440p (4K)", "1440"),
    ("1080p (FHD)", "1080"),
    ("720p (HD)", "720"),
]
AUDIO_QUALITIES = [
    ("Best (Audio)", "best_audio"),
    ("320 kbps (Audio)", "320"),
    ("256 kbps (Audio)", "256"),
    ("160 kbps (Audio)", "160"),
    ("128 kbps (Audio)", "128"),
]

# Start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome! Please send me a YouTube URL.")

# Handle URL input
async def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()
    context.user_data["url"] = url
    keyboard = [
        [InlineKeyboardButton(label, callback_data=quality)]
        for label, quality in VIDEO_QUALITIES + AUDIO_QUALITIES
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Choose the quality:", reply_markup=reply_markup)

# Callback for quality selection
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    quality = query.data
    context.user_data["quality"] = quality
    url = context.user_data["url"]
    save_path = "./Video" if "video" in quality else "./Audio"
    os.makedirs(save_path, exist_ok=True)

    await query.edit_message_text(text="Downloading your file, please wait...")

    try:
        if "video" in quality or quality.isdigit():
            filename = download_video(url, save_path, quality.replace("best_video", "best"))
        else:
            filename = download_audio(url, save_path, quality.replace("best_audio", "best"))

        if filename and os.path.exists(filename):
            with open(filename, "rb") as file:
                if "video" in quality or quality.isdigit():
                    await query.message.reply_video(video=file)
                else:
                    await query.message.reply_audio(audio=file)
            os.remove(filename)
        else:
            await query.edit_message_text("Failed to download the requested file.")
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        await query.edit_message_text("An error occurred. Please try again.")

# Check for ffmpeg
def check_ffmpeg():
    if not shutil.which("ffmpeg"):
        logger.error("ffmpeg not found. Please install ffmpeg.")
        return False
    return True

# Update libraries
def check_updates():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "yt-dlp"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "ffmpeg"])
    except subprocess.CalledProcessError as e:
        logger.error(f"Error updating libraries: {e}")
        return False
    return True

# Video download
def download_video(url, save_path, quality):
    ydl_opts = {
        "format": f"bestvideo[height<={quality}]+bestaudio/best" if quality != "best" else "bestvideo+bestaudio/best",
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "ffmpeg_location": shutil.which("ffmpeg"),
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info_dict).replace(".webm", ".mp4")
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        return None

# Audio download
def download_audio(url, save_path, bitrate):
    ydl_opts = {
        "format": "bestaudio/best" if bitrate == "best" else f"bestaudio[abr<={bitrate}]",
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "postprocessors": [{"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": bitrate}],
        "ffmpeg_location": shutil.which("ffmpeg"),
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            return ydl.prepare_filename(info_dict).replace(".webm", ".mp3")
    except Exception as e:
        logger.error(f"Error downloading audio: {e}")
        return None

# Main
def main() -> None:
    if not check_ffmpeg():
        sys.exit(1)
    if not check_updates():
        sys.exit(1)

    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button))

    app.run_polling()

if __name__ == "__main__":
    main()
