import requests
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler

def joke(update: Update, context: CallbackContext):
    response = requests.get("https://official-joke-api.appspot.com/random_joke")
    if response.status_code == 200:
        data = response.json()
        setup = data['setup']
        punchline = data['punchline']
        update.message.reply_text(setup)
        context.job_queue.run_once(send_punchline, 5, context=[punchline, update.message.chat_id])
    else:
        update.message.reply_text("Sorry, something went wrong.")

def send_punchline(context):
    punchline, chat_id = context.job.context
    context.bot.send_message(chat_id=chat_id, text=punchline)

__help__ = """
Get a random joke by using the command /joke
"""

__mod_name__ = "Jokes"

JOKES_HANDLER = CommandHandler("joke", joke)

dispatcher.add_handler(JOKES_HANDLER)
