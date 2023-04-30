import requests
from FallenRobot import pbot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


#By @NandhaBots on telegram 

@app.on_message(filters.command("ud"))
async def urban(_, m):  
       global mm
       user_id = m.from_user.id
       if len(m.text.split()) == 1:
         return await m.reply("Enter the text for which you would like to find the definition.")
       text = m.text.split(None,1)[1]
       api = requests.get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
       mm = api["list"]
       if 0 == len(mm):
           return await m.reply("=> No results Found!")
       string = f"🔍 **Ward**: {mm[0].get('word')}\n\n📝 **Definition**: {mm[0].get('definition')}\n\n✏️ **Example**: {mm[0].get('example')}"
       return await m.reply(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('next', callback_data=f"udnxt:1:{user_id}")]]), quote=True)
              
@app.on_callback_query(filters.regex("^udnxt"))   
async def next(_, query):
       user_id = query.from_user.id
       if not user_id == int(query.data.split(":")[-1]):
             return await query.answer("This is not for You!")
       num = int(query.data.split(":")[1])+1
       uwu = mm[num]
       if num == len(mm)-1:
       	  return await query.message.edit('=> No more definition could be found!')
       string = f"🔍 **Ward**: {uwu.get('word')}\n\n📝 **Definition**: {uwu.get('definition')}\n\n✏️ **Example**: {uwu.get('example')}"
       return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('➡️ Next', callback_data=f"udnxt:{num}:{user_id}")]]))
       
       
       



__help__ = """
» /ud (text) *:* Searchs the given text on Urban Dictionary and sends you the information.
"""
__mod_name__ = "Urban Dictionary"

