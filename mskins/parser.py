# soup = BeautifulSoup(r.text, "lxml")
# articles_cards = soup.find_all("tr", style="height: 60px;")


import json
import os
import random

import requests
import time
import datetime
import asyncio
import aiohttp
from bs4 import BeautifulSoup



links = []
data = []
errors_list = []
info = []


async def get_links(session, page):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36"
    }

    while True:
        try:
            async with session.get(url=page, headers=headers) as response:
                if "[200" in str(response):
                    try:
                        response_text = await response.text()
                        soup = BeautifulSoup(response_text, "lxml")
                        hrefs = soup.find_all("a")
                        counter = 0
                        for href in hrefs:
                            link = href.get("href")
                            if "/skin/" in str(link):
                                links.append(link)
                                counter += 1
                        if counter == 0:
                            errors_list.append(page)
                        else:
                            info.append(page)
                        print(f"[INFO] Обработана страница {page.split('page=')[1]}  |  Ссылок найдено - {counter}")
                    except:
                        errors_list.append(page)
                    break
                else:
                    time.sleep(random.randrange(1, 3))

        except:
            errors_list.append(page)

    return links, errors_list





async def gather_data():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36"
    }
    url = "https://mskins.net/ru/skins/latest"

    async with aiohttp.ClientSession() as session:
        r = await session.get(url=url, headers=headers)
        soup = BeautifulSoup(await r.text(), "lxml")
        amount_of_skins = soup.find("span", class_="label green darken-4").text.strip()
        amount_of_skins = int(amount_of_skins.split(" ")[0])
        pages = amount_of_skins / 45
        pages = str(pages).split(".")[0]
        pages = int(pages) + 1
        print(pages)
        tasks = []

        for page in range(1, pages + 1)[:100]:
            page = f"https://mskins.net/ru/skins/latest?page={page}"
            task = asyncio.create_task(get_links(session, page))
            tasks.append(task)
        links =  await asyncio.gather(*tasks)
        return links[0], links[1]


async def errors_handler(errors_list=None):
    urls = errors_list
    async with aiohttp.ClientSession() as session:
        tasks = []
        for url in urls:
            task = asyncio.create_task(get_links(session, page=url))
            tasks.append(task)
        errors_list.clear()
        await asyncio.gather(*tasks)


async def get_data(session, link):
    link = link.replace("\n", "")
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "onnection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36"
    }
    try:
        async with session.get(url=link, headers=headers) as response:
            response_text = await response.text()
            soup = BeautifulSoup(response_text, "lxml")
            name = soup.find("h1").text.strip().split(" ")[-1]

            views = "-"
            downloads = "-"
            format = "-"
            model = "-"
            image_src = "-"
            skin = "-"

            try:
                views = soup.find_all("span", class_="badge")[1].text.strip()
                downloads = soup.find_all("span", class_="badge")[2].text.strip()
                format = soup.find_all("span", class_="badge tooltipped")[0].text.strip()
                model = soup.find_all("span", class_="badge tooltipped")[1].text.strip()
            except:
                pass

            nickname_list = []
            try:
                nicknames = soup.find_all("div", class_="chip")
                for nickname in nicknames:
                    nickname = nickname.text.strip().replace("launch", "").strip()
                    nickname_list.append(nickname)
            except:
                pass

            try:
                image_src = f'https://mskins.net{soup.find("img", class_="responsive-img").get("src")}'
            except:
                pass

            try:
                skin = soup.find("a", class_="dw starting_download btn waves-effect waves-light cyan").get("href")
            except:
                pass

            # try:
            #     get_img = requests.get(image_src)
            #     with open(f"{os.getcwd()}\\photos\\{name}.png", "wb") as photo_file:
            #         photo_file.write(get_img.content)
            #     time.sleep(random.randrange(0, 1))
            #     get_skin = requests.get(skin)
            #     with open(f"{os.getcwd()}\\skins\\{name}.png", "wb") as skin_file:
            #         skin_file.write(get_skin.content)
            # except:
            #     pass

            try:
                 data.append(
                    {
                        "Name": name,
                        "Views": views,
                        "Downloads": downloads,
                        "Format": format,
                        "Model": model,
                        "Nicknames": nickname_list,
                        "Image": image_src,
                        "Skin": skin
                    }
                )
            except:
                pass


            print(f"Обработан скин {name}")

    except:
        pass


async def skin_parse():
    with open(f"{os.getcwd()}\\data\\links.txt", "r") as f:
        links = f.readlines()


    async with aiohttp.ClientSession() as session:
        tasks = []
        for link in links:
            task = asyncio.create_task(get_data(session, link))
            tasks.append(task)
        await asyncio.gather(*tasks)

        # 20000
        # Данные собраны за 593.609162569046
        # 19548
        # Данные собраны за 304.5216121673584


def main():

    if not os.path.exists(f"{os.getcwd()}\\photos"):
        os.mkdir(f"{os.getcwd()}\\photos")

    if not os.path.exists(f"{os.getcwd()}\\skins"):
        os.mkdir(f"{os.getcwd()}\\skins")

    if not os.path.exists(f"{os.getcwd()}\\data"):
        os.mkdir(f"{os.getcwd()}\\data")

    start_time = time.time()
    asyncio.run(gather_data())
    # errors_list = set(errors_list)
    # errors_list = list(errors_list)
    print(f"Ошибки в - {errors_list}")
    print(f"Ошибок всего - {len(errors_list)}")
    while not len(errors_list) == 0:
        asyncio.run(errors_handler(errors_list=errors_list))
    print(f"Количество информационных принтов - {len(info)}")
    print(len(links))
    print("Ссылки на скины найдены за " + str(time.time() - start_time))
    with open(f"{os.getcwd()}\\data\\links.txt", "w") as f:
        for link in links:
            try:
                f.write(f"{link}\n")
            except:
                pass


    # start_time = time.time()
    # asyncio.run(skin_parse())
    # with open(f"{os.getcwd()}\\data\\data.json", "w") as f:
    #     json.dump(data, f, indent=4, ensure_ascii=False)
    # print(len(data))
    # print("Данные собраны за " + str(time.time() - start_time))


if __name__ == '__main__':
    main()