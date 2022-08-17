import vk_api
import requests
import datetime
from bs4 import BeautifulSoup
from vk_api.bot_longpoll import VkBotEventType, VkBotLongPoll
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


headers = {
"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36"
}

url = "https://www.gametracker.com/server_info/46.174.49.31:27284"
r = requests.get(url=url, headers=headers)
soup = BeautifulSoup(r.text, "lxml")
online = soup.find("table", class_="table_lst table_lst_stp")
online = online.find_all("a")
text = "123"
names = []
for item in online:
    name = item.text.strip()
    names.append(f"{name}")
    # print(name)
if online == None:
    online = "Игроков нет"
# text = f"{text}\n{str(names)}"
players = ""
for item in names:
    players = players + f"{item}\n"

text = f"{text}\n{str(players)}"

print(text)