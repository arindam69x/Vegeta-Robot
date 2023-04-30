import requests
from FallenRobot import pbot as app
from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


By @NandhaBots on telegram 

@app.on_message(filters.command("ud"))
async def urban(_, m):  
       global mm
       user_id = m.from_user.id
       if len(m.text.split()) == 1:
         return await m.reply("Enter the text for which you would like to find the definition.")
       text = m.text.split(None,1)[1]
       api = get(f"https://api.urbandictionary.com/v0/define?term={text}").json()
       mm = api["list"]
       if 0 == len(mm):
           return await m.reply("=> No results Found!")
       string = f"🔍 **Ward**: {mm[0]["word"]}\n\n📝 **Definition**: {mm[0]["definition"]}\n\n✏️ **Example**: {mm[0]["example"]}"
       return await m.reply(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('next', callback_data=f"nxt:1:{user_id}")]]), quote=True)
              
@app.on_callback_query(filters.regex("^nxt"))   
async def next(_, query):
       if not query.from_user.id == int(query.data.split(":")[-1]):
             return await query.answer("This is not for You!")
       num = int(query.data.split(":")[1])
       uwu = mm[num]
       if num == len(mm)-1:
       	  return await query.message.edit('=> No more definition could be found!')
       string = f"🔍 **Ward**: {uwu["word"]}\n\n📝 **Definition**: {uwu["definition"]}\n\n✏️ **Example**: {uwu["example"]}"
       return await query.message.edit(text=string, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('➡️ Next', callback_data=f"nxt:{num}")]]))
       
       
       



__help__ = """
» /ud (text) *:* Searchs the given text on Urban Dictionary and sends you the information.
"""
__mod_name__ = "Urban Dictionary"
__command_list__ = ["ud"]
__handlers__ = [UD_HANDLER]
