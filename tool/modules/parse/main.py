
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

async def mainvk(text, message : Message, messanger:str, type:str, bot: Bot) -> None:

    async def replace(data, massive):
        for i in range(len(data["DATA_AUTH"])):
            if data["DATA_AUTH"][i][0] == str(massive[0]):
                data["DATA_AUTH"][i] = massive
        return data

    if type == "private":
        if len(text) > 1:
            if text[1] == "add":
                if (len(text) > 3):
                    datasave = loadConfig()
                    if is_dev().ParseDispaceChecker(str(message.from_id)):
                        await message.answer("Аккаунт будет заменен")
                        datasave = await replace(datasave, [str(message.from_id), str(text[2]), str(text[3])])
                    else:
                        datasave["DATA_AUTH"].append([str(message.from_id), str(text[2]), str(text[3])])
                    writeConfig(datasave)
                    await message.answer("Данные сохранены")

                else:
                    await message.answer("Ошибка ввода")
            if (not (is_dev().ParseDispaceChecker(str(message.from_id)))):
                await message.reply("Вы не авторизированы в боте")
            else:
                if (text[1] == "tests"):
                    dae = is_dev().TakeAuthInfo(str(message.from_id))
                    await message.reply("INFO FOR " + str(message.from_id) + "\n" + await parseDispaceList.listTests(
                        await parseDispaceList.CheckTests(await parseDispaceList.connect(dae[1], dae[2]), dae[1],
                                                          "my_results"), dae[1]))
                elif (text[1] == "activetests"):
                    dae = is_dev().TakeAuthInfo(str(message.from_id))
                    await message.reply("INFO FOR " + str(message.from_id) + "\n" + await parseDispaceList.TakeActive(
                        await parseDispaceList.CheckTests(await parseDispaceList.connect(dae[1], dae[2]),
                                                          dae[1], "all"), dae[1]))
                elif (text[1] == "test"):
                    if len(text) > 1:
                        from vkbottle import DocUploader, API
                        import io
                        dae = is_dev().TakeAuthInfo(str(message.from_id))
                        f = io.BytesIO(b'test')
                        f.write(str(await tree(
                            await parseDispaceList.CheckTest(await parseDispaceList.connect(dae[1], dae[2]),
                                                             text[2], text[3], text[2]))).encode("utf-8"))

                        document = DocMessagesUploader(message.ctx_api.api_instance)  # Хуйня из под коня
                        doc = await document.upload(
                            str("Parse_for_" + str(message.from_id) + "_with_" + str(text[2]) + ".txt"), f,
                            peer_id=message.peer_id)
                        await message.reply(attachment=doc, message="Result info:")
                        # await message.answer(str(await tree(
                        #    await parseDispaceList.CheckTest(await parseDispaceList.connect(dae[1], dae[2]),
                        #                                     text[2], text[3], text[2]))))


                    else:
                        await message.answer("Использование: /parse test id code")

        else:
            await message.answer("Использование: /parse [add/tests/activetests/test]")
    elif type == "chat":
        if len(text) > 1:
            if (not (is_dev().ParseDispaceChecker(str(message.from_id)))):
                await message.answer("Вы не авторизированы в боте")
            else:
                if (text[1] == "tests"):
                    dae = is_dev().TakeAuthInfo(str(message.from_id))
                    await message.answer("INFO FOR " + str(message.from_id) + "\n" + await parseDispaceList.listTests(
                        await parseDispaceList.CheckTests(await parseDispaceList.connect(dae[1], dae[2]),
                                                          dae[1], "my_results"), dae[1]))
                elif (text[1] == "activetests"):
                    dae = is_dev().TakeAuthInfo(str(message.from_id))
                    await message.answer("INFO FOR " + str(message.from_id) + "\n" + await parseDispaceList.TakeActive(
                        await parseDispaceList.CheckTests(await parseDispaceList.connect(dae[1], dae[2]),
                                                          dae[1], "all"), dae[1]))
                elif (text[1] == "add"):
                    await message.answer("add работает исключительно в приватных сообщениях")
                elif (text[1] == "test"):
                    if len(text) > 1:
                        from vkbottle import DocUploader, API
                        import io
                        dae = is_dev().TakeAuthInfo(str(message.from_id))
                        f = io.BytesIO(b'test')
                        f.write(str(await tree(
                            await parseDispaceList.CheckTest(await parseDispaceList.connect(dae[1], dae[2]),
                                                             text[2], text[3], text[2]))).encode("utf-8"))

                        document = DocMessagesUploader(message.ctx_api.api_instance)  # Хуйня из под коня
                        doc = await document.upload(
                            str("Parse_for_" + str(message.from_id) + "_with_" + str(text[2]) + ".txt"), f,
                            peer_id=message.peer_id)
                        await message.reply(attachment=doc, message="Result info:")
                        # await message.answer(str(await tree(
                        #    await parseDispaceList.CheckTest(await parseDispaceList.connect(dae[1], dae[2]),
                        #                                     text[2], text[3], text[2]))))


                    else:
                        await message.answer("Использование: /parse test id code")
        else:
            await message.answer("Использование: /parse [add/tests/activetests/test]")
    #print(os.path.abspath(os.curdir))
    #await messagedata.answer("Test parse")
    #await log("HELP " + messanger, 1, "END FUNC")

