from requests import get 

from FallenRobot import pbot
from pyrogram import filters
from pyrogram.types import InputMediaPhoto

# credit to @NandhaBots

@pbot.on_message(filters.command("pinterest"))
async def pinterest(_, message):

     chat_id = message.chat.id

     try:
       query= message.text.split(None,1)[1]
     except:
         return await message.reply("Input image name for search 🔍")

     images = get(f"https://pinterest-api-one.vercel.app/?q={query}").json()

     media_group = []
     count = 0

     await message.reply("scaping images from pinterest...")

     for url in images:
          if count == 7:
              break        
          media_group.append(InputMediaPhoto(media=url))
          count += 1
          await message.edit("Scaped {count}")

     try:
        return await pbot.send_media_group(
                chat_id=chat_id, 
                media=media_group,
                reply_to_message_id=message.id)

     except Exception as e:
           return await message.reply(f"Error\n{e}")
          
     
     
