import requests

from telegram import Update, ParseMode
from telegram.ext import CallbackContext, CommandHandler

from FallenRobot import dispatcher


def jokes(update: Update, context: CallbackContext):
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        joke = f"<b>{data['setup']}</b>\n\n{data['punchline']}"
        context.bot.send_message(chat_id=update.effective_chat.id, text=joke, parse_mode=ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Oops, something went wrong. Please try again later.")


jokes_handler = CommandHandler("jokes", jokes)
dispatcher.add_handler(jokes_handler)

