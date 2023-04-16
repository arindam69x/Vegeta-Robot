import requests
import html

from telegram import Update, ChatPermissions
from telegram.ext import CallbackContext, CommandHandler

from FallenRobot import dispatcher


def quote(update: Update, context: CallbackContext):
    url = "https://animechan.vercel.app/api/random"
    response = requests.get(url)
    if response.status_code == 200:
        quote_data = response.json()
        quote_text = html.unescape(quote_data["quote"])
        context.bot.send_message(chat_id=update.effective_chat.id, text=quote_text)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I couldn't get a quote right now.")


dispatcher.add_handler(CommandHandler('quote', quote))
