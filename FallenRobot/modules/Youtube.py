import telebot
from pytube import YouTube
import os

bot_token = os.environ.get('TOKEN')
if bot_token is None:
    raise ValueError('Missing bot token. Set the TOKEN environment variable.')

@bot.message_handler(commands=['yt'])
def download_video(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Do you want to download a video or audio? Please type 'video' or 'audio'.")
    bot.register_next_step_handler(msg, process_type_step)

def process_type_step(message):
    chat_id = message.chat.id
    user_choice = message.text.lower()
    if user_choice == 'video':
        msg = bot.send_message(chat_id, "Please enter the video link:")
        bot.register_next_step_handler(msg, process_video_step)
    elif user_choice == 'audio':
        msg = bot.send_message(chat_id, "Please enter the video link:")
        bot.register_next_step_handler(msg, process_audio_step)
    else:
        bot.send_message(chat_id, "Invalid input. Please type 'video' or 'audio'.")
        bot.register_next_step_handler(msg, process_type_step)

def process_video_step(message):
    chat_id = message.chat.id
    link = message.text
    try:
        video = YouTube(link)
        stream = video.streams.get_highest_resolution()
        stream.download()
        bot.send_message(chat_id, "Video downloaded successfully!")
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}")

def process_audio_step(message):
    chat_id = message.chat.id
    link = message.text
    try:
        video = YouTube(link)
        stream = video.streams.filter(only_audio=True).first()
        stream.download()
        bot.send_message(chat_id, "Audio downloaded successfully!")
    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}")

bot.polling()
