import unicodedata
from pathlib import Path
import os
from datetime import datetime, date, time
from enum import Enum
import json
import random
#from main import Dirs

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
print()
#f = open(Dirs().GetDirFromMain("config.json"))
conf = json.loads(f.read()) #using Path
f.close()

def logo():
    print("""         
   KM                       ,ok0KNWW
         KM               :NMMMMMMMM
       KM  ..             WMMMMMMMMM
   KM      KM             WMMMMMMMMM
   KM    KM               WMMMMMMMMM
   KM  KM  ..             WMMMMMMMMM
   KM  ..  KM   VK bot    WMMMMMMMMM
   KM  KM  KM     by      WMMMMMMMMM
   KMNXWM  KM Firewolf304 WMMMMMMMMK
   KMMMMMKONM             WMMMMMMMW
   KMMMMMMMMM             WMMMMMMM x
   lMMMMMMMMM             WMMMMMN xK
    MMMMMMMMMl           ,WMMMP dXM:
    lMMMMMMMMx .        ,,,aaadXMMd
     lNMMMMMMW: XOxolcclodOKMMMMWc
       lXMMMMMNc lMMMMMMMMMMMMNo.
         llONMMM0c lMMMMMMNOo'
              'lMN;. lMWl'
              
              \n""")


def loadConfig():
    f = open("config.json", "r", encoding='utf-8')
    config = json.loads(f.read())
    f.close()
    return config
def writeConfig(data):
    f = open("config.json", 'w+', encoding='utf-8')
    f.write(str(data).replace("'", '"').replace(', ', ',\n'))
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
        f = open(str(Path(os.path.abspath(os.curdir), "methods", "tags.json")), "r", encoding="utf-8")
        data = json.loads(f.read())  # using Path
        self.data = data
        f.close()
    def __iter__(self):
        for i in self.data["TAGS"]:
            yield i
    def __len__(self):
        return self.data["TAGS"]
    def __str__(self) -> iter:
        return '{"LEN":' + str(self.__len__()) + ', "ITERS":' + self.__iter__() + '}'
    def takeusers(self, tagname) -> iter:
        for i in self.data["TAGS"]:
            if str(i["NAME"]) == str(tagname):
                return i["USERS_ID"]
    def list(self) -> iter:
        for i in self.data["TAGS"]:
            yield str(i["NAME"])
    def return_idTag(self, tag:str) -> int:
        for i in range(len(self.data["TAGS"])):
            if tag == str(self.data["TAGS"][i]["NAME"]):
                return i
        return -1
    def loaddata(self):
        f = open(str(Path(os.path.abspath(os.curdir), "methods", "tags.json")), "r")
        self.data = json.loads(f.read())  # using Path
        f.close()
    def writedata(self):
        f = open(str(Path(os.path.abspath(os.curdir), "methods", "tags.json")), "w+")
        f.write(str(self.data).replace("'", '"'))
        f.close()
    def edittags(self, tag:str, new_user_id:str) -> bool:
        if self.is_securecopy(new_user_id, tag):

            if self.return_idTag(tag) < 0:
                self.addtag(tag)
            self.data["TAGS"][self.return_idTag(tag)]["USERS_ID"].append(new_user_id)
            self.writedata()
            return True
        else:
            return False
    def getTags(self, user_id: int) -> iter:
        info = []
        for i in self.data["TAGS"]:
            nonasync_log("TESTER", 1, str(user_id) + " " + str() + str(i))
            if str(user_id) in i["USERS_ID"]:
                info.append(str(i["NAME"]))
        return info
    def addtag(self, tag:str):
        self.data["TAGS"].append( json.loads( """{"NAME": "%s","USERS_ID": []}""" % tag ))
        self.writedata()
    def is_securecopy(self, user_id:str, tag:str):
        for i in self.getTags(int(user_id)):
            if i == tag:
                return False
        return True



class is_dev:
    def __init__(self):
        f = open(str(Path(os.path.abspath(os.curdir), "config.json")), "r", encoding="utf-8")
        data = json.loads(f.read())  # using Path
        f.close()
        self.data = data["DEVS"]
        self.parse = data["DATA_AUTH"]
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

    def ParseDispaceChecker(self, user_id:str) -> bool:
        #format: ["user_id", "login", "password"]
        for i in self.parse:
            if str(i[0]) == user_id:
                return True
        return False
    def TakeAuthInfo(self, user_id:str) -> bool:
        #format: ["user_id", "login", "password"]
        for i in self.parse:
            if str(i[0]) == user_id:
                return i
        return False
    #def addforParse(self, user_id:str, login:str, password:str):






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
                print("[" + str(datetime.now()) + "] " + TypeMess(4).name + " [" + user + "]: Error, ignoring... " + str(e))
                print("[" + str(datetime.now()) + "] " + TypeMess(type).name + " [" + user + "]: " + str(text))
    except Exception as e:
        print("[" + str(datetime.now()) + "] " + TypeMess(4).name + " [" + user + "]: Error read config in USE, ignoring...")

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

class parseDispaceList:
    import requests

    async def takeJsonTest(json, id: str) -> dict:
        for i in json["tests"]:
            if str(i["test"]["id"]) == id:
                return i
        return {}
    async def shortInfo(json, id: str) -> dict:
        for i in json["tests"]:
            if str(i["test"]["id"]) == id:
                return {"test_id":i["test"]["id"], "code":str(i["my_results"]).split("=-=")[0], "name":i["test"]["name"], "author":i["author"], "result":str(i["my_results"]).split("=-=")[3] + "/" + str(i["my_results"]).split("=-=")[4]}
        return {}
    async def listTests(json, login):
        mess = ""
        for i in json["tests"]:
            mess += "ID - " + str(i["test"]["id"]) + "\nCode - "+ str(i["my_results"]).split("=-=")[0] + "\nName - " + str(i["test"]["name"]) + "\nResult - " + str(i["my_results"]).split("=-=")[3] + "/" + str(i["my_results"]).split("=-=")[4] + "\n---------------------\n"
        return mess
    async def TakeActive(json, login):
        mess = ""
        for i in json["tests"]:
            mess += "ID - " + str(i["test"]["id"]) + "\nDate from - " + str(i["timeacc"]).split("~^~")[0] +"\nDate to - " + str(i["timeacc"]).split("~^~")[1] + "\nName - " + str(i["test"]["name"]) + "\nAuthor - "+ str(i["author"]) + "\nAttempts - "+ str(i["attempts"]) + "\n---------------------\n"
        return mess
    async def CheckTests(sess : requests.Session, login, action:str):
        """Это json-returner, который скидывает инфу о тесте (action дополняет запрос: my_results/all"""
        import json
        data = {
            "action": "get_tests",
            "discipline_id": str(action),
            "start": "false",
            "filter": "",
            "orderby": "",
            "test_group_id": "-1",
        }
        try:
            response = sess.post('https://dispace.edu.nstu.ru/ditest/index',
                                 headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                                 data=data)
            listTests = json.loads(response.text)
            if (len(listTests["error"]) != 0):
                raise ConnectionError("The site fucked you :/")
        except ConnectionError as e:
            return ("Error parse: " + str(e))
        except Exception as e:
            await log(login, 3, "ERROR PARSE: unlucky try: " + str(e))
            return "Error parse: unlucky trying"
        return listTests
    async def CheckTest(sess:requests.Session, id:str, code:str, login:str):
        """Это json-returner, который скидывает инфу о тесте"""
        import json
        data = {
            "action": "get_results",
            "score_id": code,
            "test_id": id
        }
        print(data)
        try:
            response = sess.post('https://dispace.edu.nstu.ru/ditest/index/result',data=data)
            info = json.loads( unicodedata.normalize('NFD', str(response.text)) )

            try:
                if (len(info["error"]) != 0):
                    raise ConnectionError("The site fucked you :/")
            except ConnectionError as e:
                return ("Error parse: " + str(e) + " " + str(info))
            except Exception: pass
        except Exception as e:
            log(login, 3, "ERROR PARSE: unlucky try: " + str(e))
            return "Error parse: unlucky trying"
        return info

    async def connect(login : str, password : str):
        """Это data-returner, который позволяет сразу авторизировать и выкинуть данные кукисов с токенами"""
        import json, datetime
        import requests
        sess = requests.Session()
        await log(login, 2, "Getting json auth... with => " + login + " " + password)
        params = {
            'realm': '/ido',
            'goto': 'https://dispace.edu.nstu.ru/user/proceed?login=openam&password=auth',
        }
        try:
            r = sess.get('https://dispace.edu.nstu.ru/')
            r = sess.post('https://login.nstu.ru/ssoservice/json/authenticate', params=params, cookies=sess.cookies,
                          headers=sess.headers)
            r = sess.post(
                'https://login.nstu.ru/ssoservice/json/authenticate?realm=/ido&goto=https://dispace.edu.nstu.ru/user/proceed?login=openam&password=auth')
            auth = json.loads(r.text)  # инфа авторизации
        except Exception as e:
            await log(login, 3, "Error getting auth instructions: " + str(e) + "\n=======REQUETS=======\n" + r.text)
            return "Error getting data\nStatus code: -1\nTime: " + str(datetime.datetime.now())
        auth["callbacks"][0]["input"][0]["value"] = login
        auth["callbacks"][1]["input"][0]["value"] = password
        try:
            r = sess.post("https://login.nstu.ru/ssoservice/json/authenticate", json=auth, cookies=sess.cookies)
            tokeninfo = json.loads(r.text)
            sess.cookies.set("NstuSsoToken", tokeninfo["tokenId"])
        except Exception as e:
            await log(login, 3,
                "Error get token info (the server may have sent false information, the receipt code has been changed or you are banned :D): " + str(
                    e) + "\n=======REQUETS=======\n" + r.text)
            return "Error get token info (the server may have sent false information, the receipt code has been changed or you are banned :D):\nStatus code: -2\nTime: " + str(datetime.datetime.now())

        try:
            r = sess.post('https://login.nstu.ru/ssoservice/json/ido/users', params={'_action': 'idFromSession', },
                          cookies=sess.cookies, headers=sess.headers, json=json.loads("{}"))

            check = json.loads(r.text)
        except Exception as e:
            await log(login, 3, "Error getting account info: " + str(e) + "\n\n=======REQUETS=======\n" + r.text)
            return "Error getting account info\nStatus code: -3\nTime: " + str(datetime.datetime.now())
        await log(login + " SERVER NSTU", 1,
            "Received account info: " + "\n==============================CHECK AUTH==============================\n" + str(
                check) + "\n==============================CHECk AUTH==============================\n\n")
        try:
            r = sess.get("https://login.nstu.ru/ssoservice/json/ido/users/%s" % check['id'],
                         cookies=sess.cookies)  # юзать только GET, иначе жопа с bad request

            authData = json.loads(r.text)
            await log(login + " SERVER NSTU", 1,
                "Received account info: " + "\n==============================AUTH INFO==============================\n" + str(
                    authData) + "\n==============================AUTH INFO==============================")
            await log(login, 2  , "Welcome to your account %s " % str(authData['cn'][0]))

        except Exception as e:
            await log(login, 3, "Error filling _action, or the server has changed codes: " + str(
                e) + "\n\n=======REQUETS=======\n" + r.text)
            return "Error filling _action, or the server has changed codes\nStatus code: -4\nTime: " + str(datetime.datetime.now())
        try:
            r = sess.post("https://login.nstu.ru/ssoservice/json/users", params={'_action': 'validateGoto'},
                          json=json.loads(
                              '{"goto":"https://dispace.edu.nstu.ru/user/proceed?login=openam&password=auth"}'))
            # r = sess.post("https://login.nstu.ru/ssoservice/json/users?_action=validateGoto",json=json.loads({"goto":"https://dispace.edu.nstu.ru/user/proceed?login=openam&password=auth"}) )
            await log(login, 1, "_action info: " + r.text)
            r = sess.post("https://dispace.edu.nstu.ru/user/proceed?login=openam&password=auth")
            if ("<!DOCTYPE html" in r.text):
                raise ConnectionError("BAD REQUEST: this is piss of shit")
            elif ("code" in json.loads(r.text)):
                if (json.loads(r.text)["code"] > 200):
                    raise ImportError("BAD REQUEST: " + str(json.loads(r.text)["message"]))
        except ImportError as e:
            await log(login, 4, "Something wrong with goto :/ : " + str(
                e) + "\n\n=======REQUETS=======\n" + r.text + "\n=======REQUETS=======\n")
        except ConnectionError as e:
            await log(login, 4, "Something wrong with goto :/ : " + str(e))
        return sess


text = ""
time = 0
async def tree(json) -> str:
    global text, time
    text = ""
    time = 0
    def f1(js, count):
        global text, time
        #print(type(js), count, time)
        if type(js) is dict:
            mass = list(js)
            for i in range(len(mass)):
                if count != 0:
                    text += "\n"
                    for k in range(count):
                        text += "│" + (" " * 2)
                    #text += "\n│" + (" " * count * 2)
                else:
                    text += "\n"
                #text += str(time) + " " + str( bool(count < 1) ) +" " + str( bool(isinstance(type(js[mass[i]]), (bool, str, int))))  +" " + str(bool( i+1 < len(mass) ))+" " + str(type(js[mass[i]]))
                text += (str("├──") if (count < 1 or isinstance(js[mass[i]], (bool, str, int))) and i+1 < len(mass) else str("└──")) + "'" + str(mass[i]) + "'"
                f1(js[mass[i]], count+1)
        elif type(js) is list:
            for j in js:
                mass = list(j)
                for i in range(len(mass)):
                    if count != 0:
                        text += "\n"
                        for k in range(count):
                            text += "│" + (" " * 2)
                    else:
                        text += "\n"
                    #text += str(time) + " " + str( bool(count < 1) ) +" " + str( bool(isinstance(j[mass[i]], (bool, str, int))))  +" " + str(bool( i+1 < len(mass) )) +" " + str(type(j[mass[i]]))
                    text += (str("├──") if (count < 1 or isinstance(j[mass[i]], (bool, str, int, dict, list))) and i+1 < len(mass) else str("└──")) + "'" + str(mass[i]) + "'"
                    f1(j[mass[i]], count+1)
        else:
            text += str(" => ") + "'" + str(js) + "'"
        time += 1
    f1(json,0)
    return text


class WorkTools:
    def __init__(self, config):
        self.config = config
    def __str__(self):
        return self.config
    def CheckBlock(FuncDataJson : dict):
        return bool(int(FuncDataJson["BLOCKED"]))
    def getIndex(self, name:str) -> int:
        for i in range( len(self.config["TOOLS"]) ):
            if self.config["TOOLS"][i]["NAME"] == name:
                return i
        return -1