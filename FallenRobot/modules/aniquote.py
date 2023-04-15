import requests
from telegram import ParseMode, Update
from FallenRobot.events import register
from telegram.ext import CallbackContext, run_async
from pyrogram import __version__ as pyrover
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as telever
from telethon import __version__ as tlhver

@pbot.on_message(filters.command("quote"))
@run_async
def quote(update: Update, context: CallbackContext):
    message = update.effective_message
    text = message.text.split(" ", 1)
    if len(text) == 1:
        r = requests.get("https://animechan.vercel.app/api/random").json()
        reply_text = f"**{r['quote']}**\n"
    else:
        variabla = text[1]
        r = requests.get(f"https://animechan.vercel.app/api/random").json()
        reply_text = f"**{r['quote']}**\n"
    message.reply_text(reply_text, parse_mode=ParseMode.MARKDOWN)
