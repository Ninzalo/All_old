import requests
import datetime
from bs4 import BeautifulSoup
from config import token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink, hitalic
from aiogram.dispatcher.filters import Text

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["АКб 2-1", "АКб 2-2"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Группа: ", reply_markup=keyboard, disable_notification=True)
    print("Пользователь подключился")


@dp.message_handler(Text(equals=["АКб 2-1", "АКб 2-2"]))
async def group(message: types.Message):
    global student_group
    if message.text == "АКб 2-1":
        student_group = str(1)
    elif message.text == "АКб 2-2":
        student_group = str(2)
    print(f"Выбрана группа: АКб 2-{student_group} | {message.from_user.id}")
    start_buttons = ["Англ 1", "Англ 2", "Назад"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Подгруппа по английскому: ", reply_markup=keyboard, disable_notification=True)
    return student_group


@dp.message_handler(Text(equals=["Англ 1", "Англ 2"]))
async def group(message: types.Message):
    global engl
    if message.text == "Англ 1":
        engl = 1
    if message.text == "Англ 2":
        engl = 2

    print(f"Выбрана подгруппа по англу: {engl} | {message.from_user.id}")
    engl = str(engl)
    start_buttons = ["Лабы 1", "Лабы 2", "Назад"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Подгруппа по лабораторным: ", reply_markup=keyboard, disable_notification=True)

@dp.message_handler(Text(equals=["Лабы 1", "Лабы 2"]))
async def subgroup(message: types.Message):
    global subgrp
    if message.text == "Лабы 1":
        subgrp = 3
    if message.text == "Лабы 2":
        subgrp = 4

    print(f"Выбрана подгруппа по лабам: {str(subgrp-2)} | {message.from_user.id}")
    # subgrp = str(subgrp)
    start_buttons = ["Сегодня", "Завтра", "Послезавтра", "Назад"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Расписание на: ", reply_markup=keyboard, disable_notification=True)




@dp.message_handler(Text(equals="Назад"))
async def start(message: types.Message):
    start_buttons = ["АКб 2-1", "АКб 2-2"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Группа: ", reply_markup=keyboard, disable_notification=True)


@dp.message_handler(Text(equals=["Время", "время"]))
async def start(message: types.Message):
    today = datetime.datetime.today()
    date = today + datetime.timedelta(hours=3)
    await message.answer(str(date), disable_notification=True)


@dp.message_handler(Text(equals=["Сегодня", "Завтра", "Послезавтра"]))
async def Schedule(message: types.Message):
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36"
    }

    try:
        url = f"https://sd.mstuca1.ru/d/full?fac=2&flow=63&grp={student_group}&lsubgrp={str(subgrp)}&esubgrp={engl}"
    except:
        await message.answer(
            f"Данные о группе, подгруппе по английскому и лабам не указаны\nНажмите \"Назад\" и укажите ваши данные")
        return

    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    articles_cards = soup.find_all("tr", style="height: 60px;")

    count_days = 0
    if message.text == "Сегодня":
        count_days = 0
    if message.text == "Завтра":
        count_days = 1
    if message.text == "Послезавтра":
        count_days = 2

    today = datetime.datetime.today()
    date = today + datetime.timedelta(days=count_days, hours=3)

    month = date.strftime('%m')
    if month == "01":
        month = "Янв"
    elif month == "02":
        month = "Фев"
    elif month == "03":
        month = "Мар"
    elif month == "04":
        month = "Апр"
    elif month == "05":
        month = "Май"
    elif month == "09":
        month = "Сен"
    elif month == "10":
        month = "Окт"
    elif month == "11":
        month = "Ноя"
    elif month == "12":
        month = "Дек"

    day = str(f"{date.strftime('%d')} {month} 20{date.strftime('%y')}")
    text = ""

    for article in articles_cards:
        try:
            article_titles = article.find_all("td")
            article_day = article.find("span", style="color: #000000;").text.strip()
            if article_day == day:
                print(f"Показано расписание на {article_day} | {message.from_user.id}")
                text = f"{str(article_day)}\n \n"
                for title in article_titles:
                    try:
                        lesson = title.find("b").text.strip()
                        name = title.find("small").text.strip()
                        place = title.find("u").text.strip()
                        href = "https://sd.mstuca1.ru/d/" + title.find("a").get("href")
                        lect_or_pr = title.get("class")

                        time_lp = "0"
                        try:
                            req = requests.get(url=href, headers=headers)

                            soup2 = BeautifulSoup(req.text, "lxml")
                            day_of_week = soup2.find_all("td")[-3].text.strip()

                            number = soup2.find("tr").text.strip()[12]

                            if number == "1":
                                time_lp = "8:30 - 10:00"
                            if number == "2":
                                time_lp = "10:10 - 11:40"
                            if number == "3":
                                time_lp = "12:40 - 14:10"
                            if number == "4":
                                time_lp = "14:20 - 15:50"
                            if number == "5":
                                time_lp = "16:20 - 17:50"
                            if number == "6":
                                time_lp = "18:00 - 19:30"
                        except:
                            pass

                        if "day_prctic" in lect_or_pr:
                            lect_or_pr = "ПРАКТИКА"
                        elif "day_lection" in lect_or_pr:
                            lect_or_pr = "ЛЕКЦИЯ"
                        else:
                            lect_or_pr = "ЛАБА"
                        text = text + f"{hitalic(time_lp)}\n{hbold(lect_or_pr)}\n{hitalic(lesson)}\n{hunderline(place)}\n\n"

                    except:
                        pass
        except:
            pass
    try:
        text = f"{day_of_week}\nАКб 2-{str(student_group)} | Лабы {str(subgrp-2)} | Англ {str(engl)}\n{text}"
    except:
        text = f"{text}АКб 2-{str(student_group)} | Лабы {str(subgrp-2)} | Англ {str(engl)}\nРасписания нет"
    await message.answer(str(text), disable_notification=True)


if __name__ == '__main__':
    executor.start_polling(dp)
