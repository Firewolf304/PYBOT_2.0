
import os
import random
import sys
import threading
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

from methods import log, readAuth, is_dev, tagsreader, parseDispaceList, tree
import json
import itertools

from methods.tools import nonasync_log

def __init__():
    print("i loaded")

async def mainvk(message : list, messagedata : Message, messanger:str, type:str, bot: Bot) -> None:
    f = open(str(Path(os.path.abspath(os.curdir), "tool", "info.json")), "r")
    f = json.loads(str(f.read()))
    if len(message) == 1:
        info = "Доступный список команд:\n"
        for i in f["TOOLS"]:
            info += str(i["FAQ"]) + "\n"
        info+="\n Более подробная информация: /help *command*"
        await messagedata.reply(info)
    elif len(message) == 2:
        try:
            id = -1
            for i in range(len(f["TOOLS"])):
                if str(f["TOOLS"][i]["NAME"]) == "/" + str(message[1]):
                    id = i
                    break
            if(id < 0):
                return
            info = "Информация о " + message[1] + ":\n"
            info += str(f["TOOLS"][i]["ADDICTIVE"]) + "\n"
            info += "Типы чата: " + str(f["TOOLS"][i]["TYPE_MESS"]) + "\n"
            info += "Блокировка: " + str(f["TOOLS"][i]["BLOCKED"]) + "\n"
            await messagedata.reply(info)
        except Exception as e:print(str(e))
    #print(os.path.abspath(os.curdir))
    #await messagedata.answer("Test helper")
    #await log("HELP " + messanger, 1, "END FUNC")

