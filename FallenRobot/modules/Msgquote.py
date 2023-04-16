import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
from FallenRobot import dispatcher
import telebot

bot_token = os.environ.get('TOKEN')
if bot_token is None:
    raise ValueError('Missing bot token. Set the TOKEN environment variable.')
    
TOKEN = os.environ.get('TOKEN')
bot = telebot.TeleBot(TOKEN)


# define the /q command handler
def quote_text(update, context):
    # get the message text to quote
    message_text = update.message.text.partition(' ')[2]
    
    # get the chat ID and message ID of the original message
    chat_id = update.message.chat_id
    message_id = update.message.reply_to_message.message_id if update.message.reply_to_message else None
    
    # create the quoted message
    quoted_message = f"> {message_text}"
    if message_id:
        quoted_message = f"[Reply to message](https://t.me/c/{chat_id}/{message_id})\n" + quoted_message
    
    # send the quoted message
    bot.send_message(chat_id=chat_id, text=quoted_message, parse_mode=telegram.ParseMode.MARKDOWN_V2)

# define the /qr command handler
def quote_reply(update, context):
    # get the chat ID and message ID of the original message
    chat_id = update.message.chat_id
    message_id = update.message.reply_to_message.message_id if update.message.reply_to_message else None
    
    # create the quoted message
    quoted_message = f"> {update.message.reply_to_message.text}"
    if message_id:
        quoted_message = f"[Reply to message](https://t.me/c/{chat_id}/{message_id})\n" + quoted_message
    
    # send the quoted message
    bot.send_message(chat_id=chat_id, text=quoted_message, parse_mode=telegram.ParseMode.MARKDOWN_V2)

# define the /q multi command handler
def quote_multi(update, context):
    # get the chat ID
    chat_id = update.message.chat_id
    
    # loop through each message ID to quote
    for message_text in context.args:
        message_id = message_text.partition(' ')[0]
        quoted_message = f"> {bot.get_message(chat_id=chat_id, message_id=message_id).text}"
        quoted_message = f"[Reply to message](https://t.me/c/{chat_id}/{message_id})\n" + quoted_message
        bot.send_message(chat_id=chat_id, text=quoted_message, parse_mode=telegram.ParseMode.MARKDOWN_V2)

# create a command handler for the /q command
quote_handler = CommandHandler('q', quote_text)

# create a command handler for the /qr command
quote_reply_handler = CommandHandler('qr', quote_reply)

# create a command handler for the /q multi command
quote_multi_handler = CommandHandler('q', quote_multi, pass_args=True)

# create an updater and add the handlers to it
updater = Updater(token='YOUR_TELEGRAM_BOT_TOKEN', use_context=True)
updater.dispatcher.add_handler(quote_handler)
updater.dispatcher.add_handler(quote_reply_handler)
updater.dispatcher.add_handler(quote_multi_handler)

# start the bot
updater.start_polling()
updater.idle()
