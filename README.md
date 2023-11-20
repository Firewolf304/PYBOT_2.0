# Небольшая лекция по этой штуке

  <div id="header" align="left">
    <img src="https://media.giphy.com/media/R9cQo06nQBpRe/giphy.gif" width="400"/></div>
This is my shit

##### 
Это работает на библиотеке vkbottle, pathlib, requests (parse) и json. Основа данной штуки - динамическое импортирование библиотеки и чтение json из файла напрямую через open по классам "инструментариев". Для старта нужно заполнить auth.json подобным способом:

# Вот типо пример:
    { "data":
      [
        {
          "name": "vk",
          "tokens": ["vk1.a.fKWDiaDWlkand23123=-f=sf"]
        },
        {
          "name": "vk",
          "tokens": ["vk1.a.dawddawdawddwadddd=-f=sf"]
        },
      ]
    }    


А, да, эта хрень может вылететь из-за потери соединения, но vkbottle старается держать динамично от реквестов, запускаясь самостоятельно

# Run
    ========================
    Linux:
    - git clone https://github.com/Firewolf304/PYVK.git
    - sudo pip install vkbottle pathlib requests json
    - sudo python3 main.py
    
    Windows:
    - runas /noprofile /user:*your name* "pip install vkbottle pathlib requests json"
     or just "pip install vkbottle pathlib requests json"
    - python3.exe main.py
    ========================

# Commands и че за файлы
Все команды берутся из json файла /tool/info.json, который хранит данные о командах, т.е. можно с легкостью добавить команду на клиент бота без проблем, не останавливая его работу. Нужно лишь закинуть файлы и отредачить данные info.json, но остановимся на том, что есть на данный момент:

#####
    /help - помощь голове
    /adddev - добавление в DEV
    /info - информация о тэгах и пользователях
    /parse - парсер Dispace
    /all - спам all
    /set - установка тэга
    /deltag - удалить тэг
    /wakeup - пинг тега

Если Вы прочитали все это и даже че-то поняли, то я охуел с вас официально, поэтому расскажу микрохрень, которую Вы бы могли сами понять: эти команды можно также без проблем заблокировать в info.json, они даже не будут проверяться в каталоге

# My profiles
<div id="badges">
  <a href="https://vk.com/remonterblyat">
    <img src="https://img.shields.io/badge/VK account-blue?style=for-the-badge&logo=vk&logoColor=cyan" alt="VK"/>
  </a>
  <a href="https://github.com/Firewolf304">
    <img src="https://img.shields.io/badge/GitHub-black?style=for-the-badge&logo=GitHub&logoColor=white" alt="GitHub"/>
  </a>
</div>
