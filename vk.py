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
    UserTypes, BotTypes, DocMessagesUploader
import logging
import asyncio

from vkbottle_types.events import GroupEventType, GroupTypes, UserEventType, bot_typings, bot_events
from vkbottle_types.objects import MessagesMessageActionStatus

from methods import log, readAuth, is_dev, tagsreader, parseDispaceList, tree
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


    @bot.on.private_message()
    async def data(message: Message):
        try:
            await log("VK: " + str(message.group_id), 5, str(message.text), peer_id=message.peer_id,
                      user_id=message.from_id, messageid=str(message.message_id))
            text = message.text.split(' ')
            if (text[0] == "/parse"):
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
                        if(text[1] == "tests"):
                            dae = is_dev().TakeAuthInfo(str(message.from_id))
                            await message.reply("INFO FOR " + str(message.from_id) + "\n" + await parseDispaceList.listTests( await parseDispaceList.CheckTests( await parseDispaceList.connect( dae[1], dae[2] ), dae[1], "my_results"), dae[1]) )
                        elif (text[1] == "activetests") :
                            dae = is_dev().TakeAuthInfo(str(message.from_id))
                            await message.reply("INFO FOR " + str(message.from_id) + "\n" + await parseDispaceList.TakeActive(
                                    await parseDispaceList.CheckTests(await parseDispaceList.connect(dae[1], dae[2]),
                                                                          dae[1], "all"), dae[1]))
                        elif (text[1] == "test") :
                            if len(text) > 1:
                                from vkbottle import DocUploader, API
                                import io
                                dae = is_dev().TakeAuthInfo(str(message.from_id))
                                f = io.BytesIO(b'test')
                                f.write(str(await tree(
                                    await parseDispaceList.CheckTest(await parseDispaceList.connect(dae[1], dae[2]),
                                                                     text[2], text[3], text[2]))).encode("utf-8"))

                                document = DocMessagesUploader(message.ctx_api.api_instance)    #Хуйня из под коня
                                doc = await document.upload(str("Parse_for_" + str(message.from_id) + "_with_"+str(text[2]) + ".txt"), f, peer_id=message.peer_id)
                                await message.reply(attachment=doc,message="Result info:")
                                #await message.answer(str(await tree(
                                #    await parseDispaceList.CheckTest(await parseDispaceList.connect(dae[1], dae[2]),
                                #                                     text[2], text[3], text[2]))))


                            else:
                                await message.answer("Использование: /parse test id code")

                else:
                    await message.answer("Использование: /parse [add/tests/activetests/test]")
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
                        await message.answer( returnData(message.from_id) )
            elif (text[0] == "/help"):
                await message.reply("Help (беседа/лс):\n"
                                    " • (+/-) /changename - изменение название чата (требуется dev и адм. группы). Параметры:\n"
                                    "   (+/-) 1. list - список доступных названий\n"
                                    "   (+/-) 2. change [id] - изменить название беседы\n"
                                    "   (+/-) 3. *nothing* - изменить название беседы по рандому\n"
                                    " • (+/-) /adddev - добавление в dev (требуется dev > 2). Параметры:\n"
                                    "   (+/-) 1. *forward/reply* *nothing* - простое добавление в dev (ставит по умолчанию 0)\n"
                                    "   (+/-) 2. *forward/reply* (user id) change *number*- изменение статуса dev на значение *number*\n"
                                    " • (+/+) /info - информация о пользователе\n"
                                    " • (+/+) /parse - парсинг dispace (требуется авторизация dispace). Параметры:\n"
                                    "   (-/+) 1. add *login* *password* - авторизация dispace\n"
                                    "   (+/+) 2. tests - список пройденных тестов (название/id/code)"
                                    "   (+/+) 3. activetests - список активных тестов\n"
                                    "   (+/+) 4. test *id* *code* - получение парс-файла о пройденном тесте")
        except Exception as e:
            try:
                if str(e) == "Flood control":
                    await message.answer("Stop flood")
                await message.answer(VKAPIError(e.code))
            except:
                await log("LOGGER", 3, "Detect error: " + str(e))
    @bot.on.chat_message()
    async def data(message: Message):
        global changename
        try:
            #print(is_dev().permission_level(message.from_id))
            await log("VK: " + str(message.group_id), 5, str(message.text), peer_id=message.peer_id,
                      user_id=message.from_id, messageid=str(int(message.message_id)))
            try:
                await log("VK: " + str(message.group_id), 2, str(message.action.type), peer_id=message.peer_id,
                          user_id=message.from_id, messageid=str(int(message.message_id)))
                if changename and (message.action.type == MessagesMessageActionStatus.CHAT_INVITE_USER or message.action.type == MessagesMessageActionStatus.CHAT_KICK_USER or message.action.type == MessagesMessageActionStatus.CHAT_INVITE_USER_BY_LINK or message.action.type == MessagesMessageActionStatus.CHAT_INVITE_USER_BY_MESSAGE_REQUEST):
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
                    elif text[1] == "enable":
                        changename = not(changename)
                        await message.answer("Enable changename is " + str(changename))

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
                    message.from_id) > 2):
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
            elif (text[0] == "/all" and is_dev().is_dev(message.from_id) and is_dev().permission_level(message.from_id) > 2 and 0):
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
                        await message.answer( returnData(message.from_id) )
            elif (text[0] == "/tag"):
                if(len(text) > 1):
                    pass
            elif (text[0] == "/parse"):
                if len(text) > 1:
                    if (not (is_dev().ParseDispaceChecker(str(message.from_id)))):
                        await message.answer("Вы не авторизированы в боте")
                    else:
                        if (text[1] == "tests"):
                            dae = is_dev().TakeAuthInfo(str(message.from_id))
                            await message.answer("INFO FOR " + str(message.from_id) + "\n" + await parseDispaceList.listTests(
                                await parseDispaceList.CheckTests(await parseDispaceList.connect(dae[1], dae[2]),
                                                                  dae[1], "my_results"), dae[1]))
                        elif (text[1] == "activetests") :
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

            elif (text[0] == "/help"):
                await message.reply("Help (беседа/лс):\n"
                                    " • (+/-) /changename - изменение название чата (требуется dev и адм. группы). Параметры:\n"
                                    "   (+/-) 1. list - список доступных названий\n"
                                    "   (+/-) 2. change [id] - изменить название беседы\n"
                                    "   (+/-) 3. *nothing* - изменить название беседы по рандому\n"
                                    " • (+/-) /adddev - добавление в dev (требуется dev > 2). Параметры:\n"
                                    "   (+/-) 1. *forward/reply* *nothing* - простое добавление в dev (ставит по умолчанию 0)\n"
                                    "   (+/-) 2. *forward/reply* (user id) change *number*- изменение статуса dev на значение *number*\n"
                                    " • (+/+) /info - информация о пользователе\n"
                                    " • (+/+) /parse - парсинг dispace (требуется авторизация dispace). Параметры:\n"
                                    "   (-/+) 1. add *login* *password* - авторизация dispace\n"
                                    "   (+/+) 2. tests - список пройденных тестов (название/id/code)"
                                    "   (+/+) 3. activetests - список активных тестов\n"
                                    "   (+/+) 4. test *id* *code* - получение парс-файла о пройденном тесте")
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
