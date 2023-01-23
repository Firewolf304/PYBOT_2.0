
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

async def mainvk(message, messagedata : Message, messanger:str, type:str, bot: Bot) -> None:
    if type == "private":
        pass
    elif type == "chat":
        if len(message) == 2 and message[1].isnumeric():
            try:
                for i in range(int(message[1])):
                    await messagedata.answer("@all")
            except Exception as e:
                try:
                    if e.code > -1:
                        await log("LOGGER", 1, "STOP SPAM")
                except Exception:
                    pass
        elif len(message) == 1:
            for i in range(int(4)):
                await messagedata.answer("@all")
    #print(os.path.abspath(os.curdir))
    #await messagedata.answer("Test helper")
    #await log("HELP " + messanger, 1, "END FUNC")

