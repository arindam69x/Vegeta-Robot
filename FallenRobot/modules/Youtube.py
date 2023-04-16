import requests
import os

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, ConversationHandler
from FallenRobot import Dispatcher

YTCHOICE, YTLINK = range(2)

def yt_choice(update: Update, context: CallbackContext):
    update.message.reply_text("Do you want to download a video or audio?\n"
                              "Enter 1️⃣ for Video\n"
                              "Enter 2️⃣ for Audio")
    return YTCHOICE


def yt_link(update: Update, context: CallbackContext):
    choice = update.message.text
    context.user_data['choice'] = choice

    update.message.reply_text("Enter the YouTube video link.")
    return YTLINK


def yt_receive_link(update: Update, context: CallbackContext):
    link = update.message.text
    choice = context.user_data['choice']
    vid_format = 'mp4' if choice == '1' else 'mp3'

    r = requests.get(f'https://www.y2mate.com/mates/{os.environ.get("Y2MATE_API_KEY")}/analyze/ajax',
                     headers={
                         'referer': 'https://www.y2mate.com/youtube-downloader',
                         'sec-fetch-dest': 'empty',
                         'sec-fetch-mode': 'cors',
                         'sec-fetch-site': 'same-origin',
                         'x-requested-with': 'XMLHttpRequest',
                     },
                     params={
                         'url': link,
                         'q_auto': 0,
                         'ajax': 1
                     })

    data = r.json()

    title = data['title']
    thumb = data['image']
    filesize = data['filesize']
    filesize = filesize/(1024*1024)
    update.message.reply_text(f"Title: {title}\n"
                              f"Size: {filesize:.2f} MB\n\n"
                              f"Processing download...")
    time.sleep(1.5)

    r = requests.get(f'https://www.y2mate.com/mates/{os.environ.get("Y2MATE_API_KEY")}/convert',
                     headers={
                         'referer': 'https://www.y2mate.com/youtube-downloader',
                         'sec-fetch-dest': 'empty',
                         'sec-fetch-mode': 'cors',
                         'sec-fetch-site': 'same-origin',
                         'x-requested-with': 'XMLHttpRequest',
                     },
                     params={
                         'type': 'youtube',
                         'vid': data['vid'],
                         'mp3': vid_format,
                         'quality': data['fquality'],
                         'auto': 0,
                         'ajax': 1
                     })

    download_data = r.json()

    download_url = download_data['result'][0]['url']
    update.message.reply_text(f"Title: {title}\n"
                              f"Size: {filesize:.2f} MB\n\n"
                              f"Sending {vid_format.upper()}...")

    if choice == '1':
        context.bot.send_video(update.message.chat_id, video=download_url, thumb=thumb, caption=title)
    elif choice == '2':
        context.bot.send_audio(update.message.chat_id, audio=download_url, thumb=thumb, title=title)

    return ConversationHandler.END


def yt_cancel(update: Update, context: CallbackContext):
    update.message.reply_text("Download cancelled.")
    return ConversationHandler.END


yt_handler = ConversationHandler(
    entry_points=[CommandHandler('yt', yt_choice)],
    states={
        YTCHOICE: [CommandHandler('cancel', yt_cancel), yt_link],
        YTLINK: [CommandHandler('cancel', yt_cancel), CommandHandler('yt', yt_receive_link)],
    },
    fallback
