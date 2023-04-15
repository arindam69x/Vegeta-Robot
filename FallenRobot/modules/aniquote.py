import requests
from telegram import ParseMode, Update
from telegram.ext import CallbackContext, run_async

from FallenRobot import dispatcher
from FallenRobot.modules.disable import DisableAbleCommandHandler


@run_async
def quote(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(" ", 1)
    if len(text) == 1:
        r = requests.get("https://animechan.vercel.app/api/random").json()
        reply_text = f"**{resp['quote']}**\n"
    else:
        variabla = text[1]
        r = requests.get(f"https://animechan.vercel.app/api/random").json()
        reply_text = f"**{resp['quote']}**\n"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
