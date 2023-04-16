import requests
import html

from telegram import Update, ParseMode
from telegram.ext import CommandHandler, CallbackContext

def quote(update: Update, context: CallbackContext):
    res = requests.get('https://animechan.vercel.app/api/random')
    if res.status_code == 200:
        data = res.json()
        quote = html.escape(data['quote'])
        anime = html.escape(data['anime'])
        character = html.escape(data['character'])
        message = f'<i>{quote}</i>\n\n<b>{anime}</b>\n{character}'
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, failed to fetch the quote. Please try again later.")
    

QUOTE_HANDLER = CommandHandler("quote", quote)

__help__ = f"""{__stats__()}
*Commands:*
- /quote: Get a random anime quote.
"""

__mod_name__ = "Anime Quotes"

__handlers__ = [
    QUOTE_HANDLER,
]
