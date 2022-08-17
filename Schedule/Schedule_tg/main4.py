import requests
import datetime
import os
import json
from bs4 import BeautifulSoup
from config import token
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.markdown import hbold, hunderline, hcode, hlink, hitalic
from aiogram.dispatcher.filters import Text

bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

if not os.path.exists(f'{os.getcwd()}\\Data'):
    os.mkdir(f'{os.getcwd()}\\Data')
if not os.path.exists(f'{os.getcwd()}\\Data\\data.json'):
    with open(f'{os.getcwd()}\\Data\\data.json', "w") as f:
        f.write(r"[]")


@dp.message_handler(commands="start")
async def start(message: types.Message):
    start_buttons = ["АКб 2-1", "АКб 2-2"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Группа: ", reply_markup=keyboard, disable_notification=True)
    print(f"Пользователь {message.from_user.id} подключился")
    with open(f'{os.getcwd()}\\Data\\data.json', "r") as f:
        data = json.load(f)
        user_exists = 0
        for item in data:
            if item["ID"] == message.from_user.id:
                user_exists += 1
        if user_exists == 0:
            print("Новый пользователь")
            new_user = {
                "ID": message.from_user.id,
                "Group": 1,
                "LSubgroup": 3,
                "ESubgroup": 1
            }
            data.append(new_user)

    with open(f'{os.getcwd()}\\Data\\data.json', "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@dp.message_handler(Text(equals=["АКб 2-1", "АКб 2-2"]))
async def group(message: types.Message):
    global student_group
    if message.text == "АКб 2-1":
        student_group = 1
    elif message.text == "АКб 2-2":
        student_group = 2
    print(f"Выбрана группа: АКб 2-{student_group}")

    with open(f'{os.getcwd()}\\Data\\data.json', "r") as f:
        data = json.load(f)
        user_exists = 0
        for item in data:
            if item["ID"] == message.from_user.id:
                item["Group"] = student_group
                user_exists += 1
        if user_exists == 0:
            print("Новый пользователь")
            new_user = {
                "ID": message.from_user.id,
                "Group": student_group,
                "LSubgroup": 3,
                "ESubgroup": 1
            }
            data.append(new_user)

    with open(f'{os.getcwd()}\\Data\\data.json', "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    start_buttons = ["Англ 1", "Англ 2", "Назад"]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer("Подгруппа по английскому: ", reply_markup=keyboard, disable_notification=True)
    return student_group


@dp.message_handler(Text(equals=["Англ 1", "Англ 2"]))
async def egroup(message: types.Message):
    global engl
    if message.text == "Англ 1":
        engl = 1
    if message.text == "Англ 2":
        engl = 2

    print(f"Выбрана подгруппа по англу: {engl}")

    with open(f'{os.getcwd()}\\Data\\data.json', "r") as f:
        data = json.load(f)
        user_exists = 0
        for item in data:
            if item["ID"] == message.from_user.id:
                item["ESubgroup"] = engl
                user_exists += 1
        if user_exists == 0:
            print("Новый пользователь")
            new_user = {
                "ID": message.from_user.id,
                "Group": 1,
                "LSubgroup": 3,
                "ESubgroup": engl
            }
            data.append(new_user)

    with open(f'{os.getcwd()}\\Data\\data.json', "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

    print(f"Выбрана подгруппа по лабам: {str(subgrp-2)}")

    with open(f'{os.getcwd()}\\Data\\data.json', "r") as f:
        data = json.load(f)
        user_exists = 0
        for item in data:
            if item["ID"] == message.from_user.id:
                item["LSubgroup"] = subgrp
                user_exists += 1
        if user_exists == 0:
            print("Новый пользователь")
            new_user = {
                "ID": message.from_user.id,
                "Group": 1,
                "LSubgroup": subgrp,
                "ESubgroup": 1
            }
            data.append(new_user)

    with open(f'{os.getcwd()}\\Data\\data.json', "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    subgrp = str(subgrp)
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
    today = str(datetime.datetime.today())
    await message.answer(today, disable_notification=True)


@dp.message_handler(Text(equals=["Мои данные", "мои данные"]))
async def start(message: types.Message):

    # try:
    #     with open(f'{os.getcwd()}\\Data\\{message.from_user.id}.json', 'r') as f:
    #         json_data = json.load(f)
    #     my_data = f"Имя - {message.from_user.username} | id - {message.from_user.id}\nАКб 2-{json_data['Group']} | Лабы {json_data['LSubgroup']-2} | Англ {json_data['ESubgroup']}"
    # except:
    #     my_data = f"Вы еще не указали свои данные"

    try:
        with open(f'{os.getcwd()}\\Data\\data.json', "r") as f:
            data = json.load(f)
            user_exists = 0
            for item in data:
                if item["ID"] == message.from_user.id:
                    user_exists += 1
                    my_data = f"Имя - {message.from_user.username} | id - {message.from_user.id}\nАКб 2-{item['Group']} | Лабы {item['LSubgroup'] - 2} | Англ {item['ESubgroup']}"
            if user_exists == 0:
                print("Новый пользователь")
                new_user = {
                    "ID": message.from_user.id,
                    "Group": 1,
                    "LSubgroup": 3,
                    "ESubgroup": 1
                }
                data.append(new_user)

        with open(f'{os.getcwd()}\\Data\\data.json', "w") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except:
        my_data = "Попробуйте еще раз"

    await message.answer(my_data, disable_notification=True)


@dp.message_handler(Text(equals=["Сегодня", "Завтра", "Послезавтра"]))
async def Schedule(message: types.Message):


    with open(f'{os.getcwd()}\\Data\\data.json', "r") as f:
        data = json.load(f)
        user_exists = 0
        for item in data:
            if item["ID"] == message.from_user.id:
                user_exists += 1
        if user_exists == 0:
            print("Новый пользователь")
            new_user = {
                "ID": message.from_user.id,
                "Group": 1,
                "LSubgroup": 3,
                "ESubgroup": 1
            }
            data.append(new_user)
            update_user = r"Нажмите кнопку 'Назад' и измените свои данные"
            await message.answer(update_user, disable_notification=True)


    with open(f'{os.getcwd()}\\Data\\data.json', "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    for user in data:
        if user["ID"] == message.from_user.id:

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.2.381 Yowser/2.5 Safari/537.36"
            }

            url = f"https://sd.mstuca1.ru/d/full?fac=2&flow=63&grp={str(user['Group'])}&lsubgrp={str(user['LSubgroup'])}&esubgrp={str(user['ESubgroup'])}"
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
            date = today + datetime.timedelta(days=count_days, hours=0)

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
                        day_of_week = article_titles[1].text.strip()

                        if day_of_week == "Пн":
                            day_of_week = "Понедельник"
                        elif day_of_week == "Вт":
                            day_of_week = "Вторник"
                        elif day_of_week == "Ср":
                            day_of_week = "Среда"
                        elif day_of_week == "Чт":
                            day_of_week = "Четверг"
                        elif day_of_week == "Пт":
                            day_of_week = "Пятница"
                        elif day_of_week == "Сб":
                            day_of_week = "Суббота"
                        elif day_of_week == "Вс":
                            day_of_week = "Воскресенье"
                        else:
                            day_of_week = ""


                        print(f"Показано расписание на {article_day}")
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
                                    # day_of_week = soup2.find_all("td")[-3].text.strip()

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
                # text = f"{day_of_week}\nАКб 2-{json_data['Group']} | Лабы {json_data['LSubgroup']-2} | Англ {json_data['ESubgroup']}\n{text}"
                # print(f"{day_of_week} | АКб 2-{json_data['Group']} | Лабы {json_data['LSubgroup']-2} | Англ {json_data['ESubgroup']} | {message.from_user.id} | {date}")
                text = f"{day_of_week}\nАКб 2-{user['Group']} | Лабы {user['LSubgroup'] - 2} | Англ {user['ESubgroup']}\n{text}"
                print(f"{day_of_week} | АКб 2-{user['Group']} | Лабы {user['LSubgroup'] - 2} | Англ {user['ESubgroup']} | {message.from_user.id} | {date}")
            except:
                text = f"{text}Расписания нет"

            start_buttons = ["Сегодня", "Завтра", "Послезавтра", "Назад"]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*start_buttons)

            await message.answer(text, reply_markup=keyboard, disable_notification=True)


if __name__ == '__main__':
    executor.start_polling(dp)
