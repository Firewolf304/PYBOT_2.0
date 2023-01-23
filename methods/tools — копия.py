import vk_api
from pathlib import Path
import os
from datetime import datetime, date, time
from enum import Enum
import json
import random

class TypeMess(Enum):
    DEBUG = 1
    LOG = 2
    ERROR = 3
    WARNING = 4
    MESSAGE = 5
class TypeUser(Enum):
    USER = 1
    DEV = 2
f = open(str(Path(os.path.abspath(os.curdir), "config.json")), "r")
conf = json.loads(f.read()) #using Path
f.close()



class readAuth:
    def __init__(self, data, messanger):
        self.data = data
        self.messanger = messanger
    def __iter__(self):
        for i in self.data["data"]:
            if str(i["name"]) ==  self.messanger:
                for x in i["tokens"]:
                    yield x
class tagsreader:
    def __init__(self):
        f = open(str(Path(os.path.abspath(os.curdir), "methods", "tags.json")), "r")
        data = json.loads(f.read())  # using Path
        self.data = data
        f.close()
    def __iter__(self):
        for i in self.data["TAGS"]:
            yield i
    def __len__(self):
        return self.data["TAGS"]
    def __str__(self):
        return '{"LEN":' + str(self.__len__()) + ', "ITERS":' + self.__iter__() + '}'
    def takeusers(self, tagname) -> iter:
        for i in self.data["TAGS"]:
            if str(i["NAME"]) == str(tagname):
                return i["USERS_ID"]
    def return_idTag(self, tag) -> int:
        for i in range(len(self.data["TAGS"])):
            if str(tag) == str(self.data["TAGS"][i]):
                return i
    def writedata(self, newdata):
        f = open(str(Path(os.path.abspath(os.curdir), "methods", "tags.json")), "w+")
        data = json.loads(f.read())  # using Path
        self.data = data
        f.close()
    def edittag(self, tag, new_user_id) -> None:
        self.data["TAGS"][self.return_idTag(tag)]["USERS_ID"].append(new_user_id)
        self.writedata(self.data)
    def getTags(self, user_id: int) -> iter:
        info = []
        for i in self.data["TAGS"]:
            if user_id in i["USERS_ID"]:
                info.append(str(i["NAME"]))
        return info




class is_dev:
    def __init__(self):
        f = open(str(Path(os.path.abspath(os.curdir), "config.json")), "r")
        data = json.loads(f.read())  # using Path
        f.close()
        self.data = data["DEVS"]
    def permission_level(self, user_id: str) -> int:
        """ This method return integer of level """
        for i in self.data:
            if str(i[0]) == str(user_id):
                return i[1]
        return -1
    def is_dev(self, user_id) -> bool:
        for i in self.data:
            if str(i[0]) == str(user_id):
                return True
        return False

    def checkPer(self, user_id: str, change_id: str) -> bool:
        if self.permission_level(user_id) > self.permission_level(change_id):
            return True
        else:
            return False





async def log(user = "", type = "", text = "", username = "", messageid = "", peer_id="", user_id = ""):
    """Функция вывода: | 1 - DEBUG | 2 - LOG | 3 - ERROR | 4 - WARNING | 5 - MESSAGE | (дополняется). Функция использует файл config.json. При messageid дополнить peer_id"""
    #print("123")
    global conf
    f = open(str(Path(os.path.abspath(os.curdir), "config.json")), "r")
    conf = json.loads(f.read())  # using Path
    f.close()
    try:
        if bool(int(conf["USE"])):
            try:
                for i in conf["TYPES"].keys():

                    #print(bool(int(conf["TYPES"][i].va)), conf["TYPES"][i], i)
                    if(str(i) == str(TypeMess(type).name) and not(bool(int(conf["TYPES"][i])))):
                        return 0

                info = "[" + str(datetime.now()) + "] " + TypeMess(type).name + " [" + user + "]: "

                if(len(str(username))):
                    info+= "'" + str(username) + "' "
                if (len(str(user_id))):
                    info += "[" + str(user_id) + "] "
                if(len(str(messageid)) > 0 and len(str(peer_id)) == 0):
                    info += '[' + str(messageid) + ']' + " >> "
                elif (len(str(messageid)) == 0 and len(str(peer_id)) > 0):
                    info += '[' + str(peer_id) + ']' + " >> "
                elif (len(str(messageid)) > 0 and len(str(peer_id)) > 0):
                    info += '[' + str(peer_id) + ":" + str(messageid) + ']' + " >> "
                info += str(text)
                print(info)




            except Exception as e:
                print("[" + str(datetime.now()) + "] " + TypeMess(1).name + " [" + user + "]: Error, ignoring... " + str(e))
                print("[" + str(datetime.now()) + "] " + TypeMess(type).name + " [" + user + "]: " + str(text))
    except Exception as e:
        print("[" + str(datetime.now()) + "] " + TypeMess(1).name + " [" + user + "]: Error read config in USE, ignoring...")

async def send(messanger = "", message = "", isReply = False, isWithoutForward = 0, reply_to = "", chat_id = "", data = dict({})):
    """messanger = "", message = "", isReply = False, reply_to = 0, message_id = "", chat_id = "", data = dict({})"""
    if messanger == "vk":
        vk = data["vk"]
        event = data["event"]
        try:
            log(data["user"], 1, data)
            if isReply:
                #mes = vk.messages.getById(message_ids=event['object']['conversation_message_id'])
                #log(data["user"], 1, mes)
                vk.messages.send(peer_id=event.object["peer_id"], message=message,
                forward=json.dumps({'peer_id': event.object["peer_id"], 'conversation_message_ids': reply_to, 'is_reply': isWithoutForward}),
                                 random_id=random.randint(0, 9999999), attachment=data["attachment"])
    #forward=str({"owner_id": int(event.object["from_id"]), "peer_id": event.object["peer_id"], "conversation_message_ids": event.object["conversation_message_id"], "message_ids": "", "is_reply": 0}).replace("'", '"'),

            else:
                vk.messages.send(peer_id=event.object["peer_id"], message=message, random_id=random.randint(0, 9999999), attachment = data["attachment"])
        except Exception as e:
            log(data["user"], 1, "Error send: " + str(e))


    elif messanger == "telegram":pass


def nonasync_log(user = "", type = "", text = "", username = "", messageid = "", peer_id="", user_id = ""):
    """Функция вывода: | 1 - DEBUG | 2 - LOG | 3 - ERROR | 4 - WARNING | 5 - MESSAGE | (дополняется). Функция использует файл config.json. При messageid дополнить peer_id"""
    #print("123")
    global conf
    f = open(str(Path(os.path.abspath(os.curdir), "config.json")), "r")
    conf = json.loads(f.read())  # using Path
    f.close()
    try:
        if bool(int(conf["USE"])):
            try:
                for i in conf["TYPES"].keys():

                    #print(bool(int(conf["TYPES"][i].va)), conf["TYPES"][i], i)
                    if(str(i) == str(TypeMess(type).name) and not(bool(int(conf["TYPES"][i])))):
                        return 0

                info = "[" + str(datetime.now()) + "] " + TypeMess(type).name + " [" + user + "]: "

                if(len(str(username))):
                    info+= "'" + str(username) + "' "
                if (len(str(user_id))):
                    info += "[" + str(user_id) + "] "
                if(len(str(messageid)) > 0 and len(str(peer_id)) == 0):
                    info += '[' + str(messageid) + ']' + " >> "
                elif (len(str(messageid)) == 0 and len(str(peer_id)) > 0):
                    info += '[' + str(peer_id) + ']' + " >> "
                elif (len(str(messageid)) > 0 and len(str(peer_id)) > 0):
                    info += '[' + str(peer_id) + ":" + str(messageid) + ']' + " >> "
                info += str(text)
                print(info)




            except Exception as e:
                print("[" + str(datetime.now()) + "] " + TypeMess(1).name + " [" + user + "]: Error, ignoring... " + str(e))
                print("[" + str(datetime.now()) + "] " + TypeMess(type).name + " [" + user + "]: " + str(text))
    except Exception as e:
        print("[" + str(datetime.now()) + "] " + TypeMess(1).name + " [" + user + "]: Error read config in USE, ignoring...")