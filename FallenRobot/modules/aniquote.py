import requests
from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext, run_async
from FallenRobot.events import register

@run_async
def quote(update: Update, context: CallbackContext):
    r = requests.get("https://animechan.vercel.app/api/random").json()
    reply_text = f"**{r['quote']}** - {r['character']} ({r['anime']})"
    update.message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)

register(cmd="quote", func=quote)
