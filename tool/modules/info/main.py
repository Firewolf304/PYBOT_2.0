
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

from methods import log, readAuth, is_dev, tagsreader, parseDispaceList, tree, loadConfig, writeConfig
import json
import itertools

from methods.tools import nonasync_log

def __init__():
    print("i loaded")

async def mainvk(message, messagedata : Message, messanger:str, type:str, bot: Bot) -> None:
    def returnData(id: int):
        info = "Информация о пользователе:\n"
        info += "ID user: " + str(id) + "\n"
        info += "Tags: " + str(tagsreader().getTags(id))
        return info

    if len(message) == 1:
        if messagedata.reply_message:
            await messagedata.answer(returnData(messagedata.reply_message.from_id))
        elif len(messagedata.fwd_messages) > 0:
            await messagedata.answer(returnData(messagedata.fwd_messages[0].from_id))
        else:
            await messagedata.answer(returnData(messagedata.from_id))
    elif len(message) == 2:
        if(message[1]) == "tags":
            info = "Теги:\n"
            info += str(list(tagsreader().list())).replace("[","").replace("]","")
            await messagedata.answer(info)
    elif len(message) == 3:
        if message[1] == "tag":
            info = "Информация о теге\n"
            info += message[2] + " users: " + str(tagsreader().takeusers(str(message[2])))
            await messagedata.answer(info)


    #print(os.path.abspath(os.curdir))
    #await messagedata.answer("Test helper")
    #await log("HELP " + messanger, 1, "END FUNC")


