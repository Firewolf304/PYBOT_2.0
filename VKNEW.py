import os, random, threading, sys
import importlib.util as imp
from pathlib import Path
from typing import TYPE_CHECKING, Iterable, Type
import vkbottle_types.objects
from vkbottle.api import API
from vkbottle.bot import Bot, run_multibot, Message, MessageEvent, MessageEventMin
from vkbottle.dispatch.rules import ABCRule
from vkbottle.http import SingleAiohttpClient
from vkbottle.polling import BotPolling
from vkbottle import Callback, GroupEventType, GroupTypes, Keyboard, ShowSnackbarEvent, VKAPIError, UserEventType, \
    UserTypes, BotTypes, DocMessagesUploader
import logging
import asyncio

from vkbottle_types.events import GroupEventType, GroupTypes, UserEventType, bot_typings, bot_events
from vkbottle_types.objects import MessagesMessageActionStatus

from methods import log, readAuth, is_dev, tagsreader, parseDispaceList, tree, WorkTools, logo
import json
import itertools

from methods.tools import nonasync_log

if __name__ != "__main__":
    exit(0)
logging.disable(logging.DEBUG)

messanger = "vk"
f = open("auth.json", "r")
Authdata = json.loads(f.read())
f.close()

changename = False
messanger = "vk"
count = 0

def loadConfig():
    f = open("config.json", "r", encoding='utf-8')
    config = json.loads(f.read())
    f.close()
    return config

def loadTools():
    f = open(Path(os.path.abspath(os.curdir),"tool","info.json"), "r", encoding='utf-8')
    config = json.loads(f.read())
    f.close()
    return config

def writeConfig(data):
    f = open("config.json", 'w+', encoding='utf-8')
    f.write(str(data).replace("'", '"').replace(', ', ',\n'))
    f.close()


def vk_bot(messanger, apis):
    logo()
    async def replace(data, massive):
        for i in range(len(data["DATA_AUTH"])):
            if data["DATA_AUTH"][i][0] == str(massive[0]):
                data["DATA_AUTH"][i] = massive
        return data
    # rnd = random.randint(0,4)
    # await asyncio.sleep(rnd)
    user = ("user" + str(count))
    # bot = Bot(token=token)
    bot = Bot()

    @bot.on.chat_message()
    async def data(message: Message):



        try:
            load = loadTools()
            text = message.text.split(' ')
            await log(user="VK", type=5, text=message.text, messageid=str(message.message_id),
                      peer_id=str(message.peer_id), user_id=str(message.from_id))
            if(text[0][0] != '/'):
                return
            index = WorkTools(load).getIndex(text[0])
            if index > -1:
                await log("LOGGER chat", 1, "Loading module " + text[0])
                if not(WorkTools.CheckBlock(load["TOOLS"][int(index)])):
                    path = Path(os.path.abspath(os.curdir),  load["TOOLS"][int(index)]["PATH"].replace('\\', os.sep) )
                    spec = imp.spec_from_file_location("main"+messanger, path)
                    lib = imp.module_from_spec(spec)
                    spec.loader.exec_module(lib)
                    await log("LOGGER chat", 1,
                              "Success load the module " + text[0] + " -> " + str(load["TOOLS"][int(index)]["PATH"]))
                    await lib.mainvk(text, message, messanger, "chat" if bool("chat" in load["TOOLS"][int(index)]["TYPE_MESS"]) else "", bot)
                else:
                    await log("LOGGER chat", 1, "Function is blocked => " + text[0])
                    await message.reply("Function blocked")
        except Exception as e:
            try:
                if str(e) == "Flood control":
                    await message.answer("Stop flood")
                await message.answer(VKAPIError(e.code))
            except:
                await log("LOGGER", 3, "Detect error: " + str(e) + " in line ")


    @bot.on.private_message()
    async def data(message: Message):
        try:
            load = loadTools()
            text = message.text.split(' ')
            await log(user = "VK", type=5, text = message.text, messageid=str(message.message_id), peer_id=str(message.peer_id), user_id=str(message.from_id))
            if (text[0][0] != '/'):
                return
            index = WorkTools(load).getIndex(text[0])
            if index > -1:
                await log("LOGGER private", 1, "Loading module " + text[0])
                if not(WorkTools.CheckBlock(load["TOOLS"][int(index)])):
                    path = Path(os.path.abspath(os.curdir),  load["TOOLS"][int(index)]["PATH"].replace('\\', os.sep) )
                    spec = imp.spec_from_file_location("main"+messanger, path)
                    lib = imp.module_from_spec(spec)
                    spec.loader.exec_module(lib)
                    await log("LOGGER private", 1, "Success load the module " + text[0] + " -> " + str(load["TOOLS"][int(index)]["PATH"]))
                    await lib.mainvk(text, message, messanger, "private" if bool("private" in load["TOOLS"][int(index)]["TYPE_MESS"]) else "", bot)
                else:
                    await log("LOGGER private", 1, "Function is blocked => " + text[0])
                    await message.reply("Function blocked")
        except Exception as e:
            try:
                if str(e) == "Flood control":
                    await message.answer("Stop flood")
                await message.answer(VKAPIError(e.code))
            except:
                await log("LOGGER", 3, "Detect error: " + str(e) + " in line ")

    addtasks(bot, apis)  # отковыренная функция из vkbottle
    # run_multibot(bot, apis) # основа
    bot.loop_wrapper.run_forever()


def addtasks(bot, apis):
    polling_type: Type["ABCPolling"] = BotPolling
    for i, api_instance in enumerate(apis):
        nonasync_log("VK", 2, "Creating loop: " + str(i) + "| token = " + "'" +str(api_instance) + "'")
        polling = polling_type().construct(api_instance)
        api_instance.http_client = SingleAiohttpClient()
        bot.loop_wrapper.add_task(bot.run_polling(custom_polling=polling))


vk_bot(messanger, [API(token) for token in list(readAuth(Authdata, messanger))])
