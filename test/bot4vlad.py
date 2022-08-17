import requests
import aiogram
from bs4 import BeautifulSoup
# from config import token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text

# bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
# dp = Dispatcher(bot)

def parse():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36"
    }

    city = str(input("Введите город: "))

    if city == "Москва" or city == "москва":
        city = "moscow"
    elif city == "Щелково" or city == "щелково":
        city = "shchelkovo"
    elif city == "СПБ" or city == "спб" or city == "Санкт-Петербург":
        city = "saint_petersburg"

    url = f"https://world-weather.ru/pogoda/russia/{city}/"
    print(url)

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    weather = soup.find_all("ul", class_="tabs tabs-db")

    for item in weather:
        now = item.find_all("li", class_="tab-w current")
        for entry in now:
            now_temp = str(entry.find("div", class_="day-temperature")).split("°")[0].split(">")[-1]
            print(now_temp)


    #start_buttons = ""
    # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # keyboard.add(*start_buttons)

    # reply_markup = keyboard


parse()