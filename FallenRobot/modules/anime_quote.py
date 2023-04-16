import os
import telegram
from telegram.ext import Updater, CommandHandler
import requests

# Define a function that gets a random anime quote from the API
def get_anime_quote():
    response = requests.get('https://animechan.vercel.app/api/random')
    if response.status_code == 200:
        data = response.json()
        return f"{data['quote']} - {data['character']} ({data['anime']})"
    else:
        return "Oops, something went wrong while trying to fetch an anime quote :(" 

# Define a function that handles the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm an anime quote bot. Type /quote to get a random anime quote.")

# Define a function that handles the /quote command
def quote(update, context):
    quote = get_anime_quote()
    context.bot.send_message(chat_id=update.effective_chat.id, text=quote)

# Set up the Telegram bot
TOKEN = os.environ['6150409031:AAF31Y9CsAnYgvLcALZpi23JXgYuBt5lsqw']
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Register the handlers for the /start and /quote commands
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
quote_handler = CommandHandler('quote', quote)
dispatcher.add_handler(quote_handler)

# Start the bot
if __name__ == '__main__':
    updater.start_polling()
