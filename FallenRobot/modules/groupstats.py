import telegram
from telegram.ext import CommandHandler, Updater
import os

# Function to count the number of messages in the group
def count_messages(update, context):
    chat_id = update.message.chat_id
    messages = context.bot.get_chat(chat_id).message_count
    context.bot.send_message(chat_id=chat_id, text=f"There have been {messages} messages sent in this group.")

# Function to get the most active members in the group
def active_members(update, context):
    chat_id = update.message.chat_id
    member_data = context.bot.get_chat(chat_id).get_members()
    sorted_data = sorted(member_data, key=lambda m: m.message_count, reverse=True)[:5]
    text = "Here are the 5 most active members in this group:\n"
    for i, member in enumerate(sorted_data):
        text += f"{i+1}. {member.user.first_name} - {member.message_count} messages\n"
    context.bot.send_message(chat_id=chat_id, text=text)

# Get the bot token from the Heroku config variable
TOKEN = os.environ.get('TOKEN')

# Set up the bot
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Add command handlers for the two functions
count_handler = CommandHandler("count", count_messages)
active_handler = CommandHandler("active", active_members)
dispatcher.add_handler(count_handler)
dispatcher.add_handler(active_handler)

# Start the bot
updater.start_polling()

# Add welcome message to the bot
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Welcome to the group!")
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.idle()
