import logging
import aiohttp
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext
from youtube_dl import YoutubeDL
from FallenRobot import dispatcher

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the states of the conversation
VIDEO, AUDIO = range(2)

# Define the callback functions for the conversation
def video_callback(update: Update, context: CallbackContext) -> int:
    # Send a message to the user
    update.message.reply_text('Please enter the URL of the video you want to download.')

    # Set the state of the conversation to VIDEO
    return VIDEO

def audio_callback(update: Update, context: CallbackContext) -> int:
    # Send a message to the user
    update.message.reply_text('Please enter the URL of the video you want to extract audio from.')

    # Set the state of the conversation to AUDIO
    return AUDIO

def video_url(update: Update, context: CallbackContext) -> int:
    # Get the URL from the user's message
    url = update.message.text

    # Download the video using youtube_dl
    ydl_opts = {'outtmpl': 'video.mp4'}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Send the video to the user
    with open('video.mp4', 'rb') as video_file:
        update.message.reply_video(video=video_file)

    # End the conversation
    return ConversationHandler.END

def audio_url(update: Update, context: CallbackContext) -> int:
    # Get the URL from the user's message
    url = update.message.text

    # Download the audio using youtube_dl
    ydl_opts = {'outtmpl': 'audio.mp3', 'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}]}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Send the audio to the user
    with open('audio.mp3', 'rb') as audio_file:
        update.message.reply_audio(audio=audio_file)

    # End the conversation
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    # Send a message to the user indicating that the conversation has been canceled
    update.message.reply_text('Conversation canceled.')

    # End the conversation
    return ConversationHandler.END

def youtube_handler(update: Update, context: CallbackContext) -> None:
    # Start the conversation
    update.message.reply_text('Do you want to download a video or extract audio? Type /cancel to stop.')

    # Set up the ConversationHandler
    yt_handler = ConversationHandler(
        entry_points=[CommandHandler('yt', video_callback)],
        states={
            VIDEO: [MessageHandler(Filters.text & ~Filters.command, video_url)],
            AUDIO: [MessageHandler(Filters.text & ~Filters.command, audio_url)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Add the ConversationHandler to the dispatcher
    updater.dispatcher.add_handler(yt_handler)

