import logging
import os
import subprocess
import sys
from yt_dlp import YoutubeDL
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext, Defaults

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

# Define the start command handler
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text('Welcome! Please send me the YouTube URL.')

# Define the message handler for YouTube URL
async def handle_message(update: Update, context: CallbackContext) -> None:
    url = update.message.text
    context.user_data['url'] = url
    keyboard = [
        [InlineKeyboardButton("Best (Video)", callback_data='best_video'), InlineKeyboardButton("4320p (8K)", callback_data='4320')],
        [InlineKeyboardButton("2160p (4K)", callback_data='2160'), InlineKeyboardButton("1080p (FHD)", callback_data='1080')],
        [InlineKeyboardButton("720p (HD)", callback_data='720'), InlineKeyboardButton("Best (Audio)", callback_data='best_audio')],
        [InlineKeyboardButton("320 kbps (Audio)", callback_data='320'), InlineKeyboardButton("256 kbps (Audio)", callback_data='256')],
        [InlineKeyboardButton("160 kbps (Audio)", callback_data='160'), InlineKeyboardButton("128 kbps (Audio)", callback_data='128')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose the quality:', reply_markup=reply_markup)

# Define the callback query handler for quality selection
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    context.user_data['quality'] = query.data
    await query.edit_message_text(text="Processing your request...")

    # Interact with your existing script
    url = context.user_data['url']
    quality = context.user_data['quality']
    save_path = './Video' if 'video' in quality else './Audio'

    if 'video' in quality or quality in ['4320', '2160', '1440', '1080', '720']:
        filename = download_video(url, save_path, quality.replace('best_video', 'best'))
    else:
        filename = download_audio(url, save_path, quality.replace('best_audio', 'best'))

    if filename:
        # Check file size
        file_size = os.path.getsize(filename)
        if file_size > 50 * 1024 * 1024:  # 50 MB
            await query.edit_message_text(text="The file you requested is larger than 50 MB. Please try a lower resolution, or visit my site: https://utube.bayt.cc to download from there")
        else:
            # Send the file to the user
            with open(filename, 'rb') as file:
                if 'video' in quality or quality in ['4320', '2160', '1440', '1080', '720']:
                    await query.message.reply_video(video=file, timeout=360)
                else:
                    await query.message.reply_audio(audio=file, timeout=3600)
    else:
        await query.edit_message_text(text="There was an error processing your request.")

def check_ffmpeg():
    ffmpeg_path = '/usr/bin/ffmpeg'
    if not os.path.exists(ffmpeg_path):
        print("Error: ffmpeg not found")
        return False
    return True

def check_updates():
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'yt-dlp'])
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'ffmpeg'])
    except subprocess.CalledProcessError as e:
        print(f"Error updating libraries: {e}")
        return False
    return True

def download_video(url, save_path, quality):
    ydl_opts = {
        'format': f'bestvideo[height<={quality}]+bestaudio/best[height<={quality}]' if quality != 'best' else 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'ffmpeg_location': '/usr/bin/ffmpeg',  # Default location for ffmpeg in the container
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
    }
    with YoutubeDL(ydl_opts) as ydl:
        try:
            info_dict = ydl.extract_info(url, download=True)
        except TypeError as e:
            if 'float_or_none() missing 1 required positional argument: \'v\'' in str(e):
                def float_or_none_wrapper(v, scale=None):
                    try:
                        return float(v) * scale if scale else float(v)
                    except (TypeError, ValueError):
                        return None
                info_dict = ydl.extract_info(url, download=True, float_or_none=float_or_none_wrapper)
            else:
                raise e
        return ydl.prepare_filename(info_dict).replace('.webm', '.mp4')

def download_audio(url, save_path, bitrate):
    ydl_opts = {
        'format': 'bestaudio/best' if bitrate == 'best' else f'bestaudio[abr<={bitrate}]',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': bitrate,
        }],
        'ffmpeg_location': '/usr/bin/ffmpeg'  # Default location for ffmpeg in the container
    }
    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict).replace('.webm', '.mp3')

def main() -> None:
    # Check if ffmpeg and updates are available
    if not check_ffmpeg():
        return

    if not check_updates():
        return

    # Increase the timeout settings
    defaults = Defaults(timeout=120)  # Set the timeout to 120 seconds

    application = Application.builder().token(TELEGRAM_BOT_TOKEN).defaults(defaults).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling()

if __name__ == '__main__':
    main()
