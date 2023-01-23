import vkbottle
from vkbottle import Bot
import asyncio
from random import randint
from vkbottle.bot import Message
import logging
from methods.tools import is_dev


test = 741685046
token = "" # AUTH !!!
logging.disable(logging.DEBUG)
fuckid = 266968806
fraze = [
    "Нахуй иди"
]

bot = Bot(token = token)

active = True
@bot.on.chat_message()
async def chat(message: Message):
    global active
    try:
        rnd = int(randint(0, len(fraze) * 10000) / 10000)
        try:
            detect = message.dict()
            if (detect['attachments'][0]['sticker']['sticker_id'] == 51563 or detect['attachments'][0]['sticker'][
                'sticker_id'] == 77727 or detect['attachments'][0]['sticker']['sticker_id'] == 56397):
                await bot.api.messages.send(peer_id=message.peer_id, sticker_id=51563, random_id=rnd)
        except: pass
        
        if is_dev().is_dev(message.from_id) and message.text == "/active":
            active = not(active)
            await message.answer("Active changed on " + str(active))
        
        if message.from_id == fuckid and active:

            await message.reply(fraze[rnd])
            await bot.api.messages.delete(spam=False, peer_id=message.peer_id, group_id=message.group_id ,cmids=[message.conversation_message_id], delete_for_all=True)
        

    except Exception as e :print(e)
bot.run_forever()
