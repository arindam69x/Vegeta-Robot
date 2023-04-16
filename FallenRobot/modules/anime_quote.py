import os
import requests
import logging
import telegram
from telegram.ext import CommandHandler, Updater

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Set up API variables
TOKEN = os.environ.get('TOKEN')
API_URL = "https://animechan.vercel.app/api/random"

# Define command handler
def quote_handler(update, context):
    # Get a random quote from the API
    response = requests.get(API_URL)
    data = response.json()
    quote = data['quote']
    character = data['character']
    anime = data['anime']
    message = f'"{quote}"\n- {character}, {anime}'

    # Send the quote to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=message)

# Set up the bot and add the command handler
def main():
    # Create the Updater and pass in the bot's API token
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add the quote command handler
    dp.add_handler(CommandHandler("quote", quote_handler))

    # Start the bot
    updater.start_polling()
    logger.info("Bot started polling.")

    # Run the bot until Ctrl-C is pressed or the process is stopped
    updater.idle()

if __name__ == '__main__':
    main()
