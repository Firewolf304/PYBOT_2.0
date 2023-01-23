import random
import threading
from typing import TYPE_CHECKING, Iterable, Type
import vkbottle_types.objects
from vkbottle.api import API
from vkbottle.bot import Bot, run_multibot, Message, MessageEvent, MessageEventMin
from vkbottle.dispatch.rules import ABCRule
from vkbottle.http import SingleAiohttpClient
from vkbottle.polling import BotPolling
from vkbottle import Callback, GroupEventType, GroupTypes, Keyboard, ShowSnackbarEvent, VKAPIError, UserEventType, \
    UserTypes, BotTypes
import logging
import asyncio

from vkbottle_types.events import GroupEventType, GroupTypes, UserEventType, bot_typings, bot_events
from vkbottle_types.objects import MessagesMessageActionStatus

from methods import log, readAuth, is_dev, tagsreader
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

messanger = "vk"

# apis = [API(token) for token in list(readAuth(Authdata, messanger))]
# log("VK", 1, "Taked tokens:" + ("\n" + str([str(x) for x in apis])))
count = 0


def loadConfig():
    f = open("config.json", "r", encoding='utf-8')
    config = json.loads(f.read())
    f.close()
    return config
def writeConfig(data):
    f = open("config.json", 'w+', encoding='utf-8')
    f.write(str(data).replace("'", '"').replace(', ', ',\n'))
    f.close()

def vk_bot(messanger, apis):
    # rnd = random.randint(0,4)
    # await asyncio.sleep(rnd)
    user = ("user" + str(count))
    # bot = Bot(token=token)
    bot = Bot()
    @bot.on.chat_message()
    async def data(message: Message):
        try:
            #print(is_dev().permission_level(message.from_id))
            await log("VK: " + str(message.group_id), 5, str(message.text), peer_id=message.peer_id,
                      user_id=message.from_id, messageid=str(int(message.message_id)))
            try:
                await log("VK: " + str(message.group_id), 2, str(message.action.type), peer_id=message.peer_id,
                          user_id=message.from_id, messageid=str(int(message.message_id)))
                if message.action.type == MessagesMessageActionStatus.CHAT_INVITE_USER or message.action.type == MessagesMessageActionStatus.CHAT_KICK_USER or message.action.type == MessagesMessageActionStatus.CHAT_INVITE_USER_BY_LINK or message.action.type == MessagesMessageActionStatus.CHAT_INVITE_USER_BY_MESSAGE_REQUEST:
                    number = int((await message.ctx_api.messages.get_conversation_members(peer_id=message.peer_id)).count)
                    await log("LOGGER", 1, "Detect " + str(number) + " users")

                    rnd = int(random.randint(0, len(loadConfig()["CHAT_NAMES"]) * 100000) / 100000)
                    if len(loadConfig()["CHAT_NAMES"][rnd]) > 1:
                        number = eval(str(loadConfig()["CHAT_NAMES"][rnd][1]))
                    await log("LOGGER", 1, "data: " + str(loadConfig()))
                    await message.ctx_api.messages.edit_chat(chat_id=message.chat_id,
                                                             title=str(number) + " " + str(
                                                                 str(loadConfig()["CHAT_NAMES"][rnd][0])))
                    pass
            except Exception as e:
                try:
                    if e.code > -1:
                        await log("VK: " + str(message.group_id), 3, str(e), peer_id=message.peer_id,
                                  user_id=message.from_id)
                except Exception:
                    pass
            text = message.text.split(' ')
            if (text[0] == "/changename" and is_dev().is_dev(message.from_id)):
                if len(text) > 1:
                    if text[1].isnumeric():
                        if (int(text[1]) < len(loadConfig()["CHAT_NAMES"])):
                            number = int((await message.ctx_api.messages.get_conversation_members(peer_id=message.peer_id)).count)
                            await log("LOGGER", 1, "Detect " + str(number) + " users")
                            if len(loadConfig()["CHAT_NAMES"][int(text[1])]) > 1:
                                number = eval(str(loadConfig()["CHAT_NAMES"][int(text[1])][1]))
                                #print(str(loadConfig()["CHAT_NAMES"][int(text[1])][1]))
                            await log("LOGGER", 1, "data: " + str(loadConfig()))
                            await message.ctx_api.messages.edit_chat(chat_id=message.chat_id,
                                                                     title=str(number) + " " + str( str(loadConfig()["CHAT_NAMES"][int(text[1])][0])))
                    elif text[1] == "list":
                        info = "Available titles:\n"
                        count = 0
                        for i in loadConfig()["CHAT_NAMES"]:
                            info += str(count) + " => '" + str(i[0]) + "'\n"
                            count += 1

                        await message.answer(info)
                else:
                    number = int((await message.ctx_api.messages.get_conversation_members(peer_id=message.peer_id)).count)
                    await log("LOGGER", 1, "Detect " + str(number) + " users")

                    rnd = int(random.randint(0, len(loadConfig()["CHAT_NAMES"]) * 100000) / 100000)
                    if len(loadConfig()["CHAT_NAMES"][rnd]) > 1:
                        number = eval(str(loadConfig()["CHAT_NAMES"][rnd][1]))
                    await log("LOGGER", 1, "data: " + str(loadConfig()))
                    await message.ctx_api.messages.edit_chat(chat_id=message.chat_id,
                                                             title=str(number) + " " + str(str(loadConfig()["CHAT_NAMES"][rnd][0])))

                pass

            elif (text[0] == "/adddev" and is_dev().is_dev(message.from_id) and is_dev().permission_level(
                    message.from_id) > 1):
                datasave = loadConfig()
                if(len(text) == 1):

                    try:
                        if message.reply_message:
                            datasave["DEVS"].append([message.reply_message.from_id, 0])
                            await message.answer("Loaded new dev")
                    except Exception: pass

                    if len(message.fwd_messages) > 0:
                        datasave["DEVS"].append([message.fwd_messages[0].from_id, 0])
                        await message.answer("Loaded new dev")



                elif(len(text) == 2):
                    datasave["DEVS"].append([str(text[1]), 0])
                    await message.answer("Loaded new dev")
                    pass
                elif(len(text) == 3):
                    #access =  or  # доступ по ID из is_dev
                    #print(is_dev().checkPer(str(message.from_id) , str(text[1])) , is_dev().checkPer(str(message.from_id) , str(text[2])), access)
                    if(str(text[1]).isnumeric() and str(text[2]).isnumeric()   ):
                        #проверка DEV
                        if is_dev().checkPer(str(message.from_id) , str(text[1]) ):
                            for i in range(len(datasave["DEVS"])):
                                if str(datasave["DEVS"][i][0]) == str(text[1]):
                                    datasave["DEVS"][i][1] = int(text[2])
                                    await message.answer("User " + text[1] + " has been changed")
                                    break


                        else:
                            await message.answer("Low permissions")
                    elif(text[1] == "change" and str(text[2]).isnumeric()):
                        # проверка DEV
                        if is_dev().checkPer(str(message.from_id) , str(text[2])):
                            try:
                                if message.reply_message:
                                    for i in range(len(datasave["DEVS"])):
                                        if str(datasave["DEVS"][i][0]) == str(message.reply_message.from_id):
                                            datasave["DEVS"][i][1] = int(text[2])
                                            await message.answer("User " + str(message.reply_message.from_id) + " has been changed")
                                            break

                            except Exception: pass
                            if len(message.fwd_messages) > 0:
                                for i in range(len(datasave["DEVS"])):
                                    if str(datasave["DEVS"][i][0]) == str(message.fwd_messages[0].from_id):
                                        datasave["DEVS"][i][1] = int(text[2])
                                        await message.answer("User " + str(message.fwd_messages[0].from_id) + " has been changed")
                                        break
                        else:
                            await message.answer("Low permissions")



                await log("LOGGER", 1, "EDIT CONFIG")
                writeConfig(datasave)


                pass
            elif (text[0] == "/all" and is_dev().is_dev(message.from_id) and is_dev().permission_level(message.from_id) > 2):
                if len(text) == 2 and text[1].isnumeric():
                    try:
                        for i in range(int(text[1])):
                            await message.answer("@all")
                    except Exception as e:
                        try:
                            if e.code > -1:
                                await log("LOGGER", 1, "STOP SPAM")
                        except Exception:pass
                elif len(text) == 1:
                    for i in range(int(4)):
                        await message.answer("@all")
                pass
            elif (text[0] == "/info"):
                def returnData(id:int):
                    info = "Информация о пользователе:\n"
                    info += "ID user: " + str(id) + "\n"
                    info += "Tags: " + str(tagsreader().getTags(id))
                    return info
                if len(text) == 1:
                    check = False
                    try:
                        if message.reply_message:
                            await message.answer( returnData(message.reply_message.from_id) )
                            pass
                    except Exception as e:check = True
                    if len(message.fwd_messages) > 0:
                        await message.answer( returnData(message.fwd_messages[0].from_id) )
                    elif check and len(message.fwd_messages) == 0:
                        print(3)
                        await message.answer( returnData(message.from_id) )



        except Exception as e:
            try:
                if str(e) == "Flood control":
                    await message.answer("Stop flood")
                await message.answer(VKAPIError(e.code))
            except:
                await log("LOGGER", 3, "Detect error: " + str(e))



        # log("VK: " + str(message.group_id), 2)
        # for i in bot.polling.listen():
        #    log("VK: " + str(message.group_id), 2, i)

    # @bot.on.raw_event(UserEventType.MESSAGE_NEW, dataclass=bot_events.MessageNew)
    # async def join(event: bot_events.MessageNew):
    #    try:
    #        log("VK: " + str("gr"), 2, str(event.object))
    #    except Exception as e:
    #        log("VK: " + str("gr"), 2, str(e))

    addtasks(bot, apis)  # отковыренная функция из vkbottle
    # run_multibot(bot, apis) # основа
    bot.loop_wrapper.run_forever()


def addtasks(bot, apis):
    polling_type: Type["ABCPolling"] = BotPolling
    for i, api_instance in enumerate(apis):
        nonasync_log("VK", 2, "Creating loop: " + str(i) + "| token = " + str(api_instance))
        polling = polling_type().construct(api_instance)
        api_instance.http_client = SingleAiohttpClient()
        bot.loop_wrapper.add_task(bot.run_polling(custom_polling=polling))


vk_bot(messanger, [API(token) for token in list(readAuth(Authdata, messanger))])
