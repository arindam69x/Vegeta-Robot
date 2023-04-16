import requests
import random
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler
from FallenRobot import dispatcher

def animequote(update: Update, context: CallbackContext):
    response = requests.get('https://animechan.vercel.app/api/random')
    data = response.json()
    quote = data['quote']
    anime = data['anime']
    character = data['character']
    message = f'"{quote}"\n\n- {character} ({anime})'
    update.message.reply_text(message)

ANIMEQUOTE_HANDLER = CommandHandler('quote', animequote)

dispatcher.add_handler(ANIMEQUOTE_HANDLER)
