import grequests
import requests
import os
import json
import time
from bs4 import BeautifulSoup




def pagin():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36"
    }
    url = "https://mskins.net/ru/skins/latest"

    r = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    amount_of_skins = soup.find("span", class_="label green darken-4").text.strip()
    amount_of_skins = int(amount_of_skins.split(" ")[0])
    pages = amount_of_skins / 45
    pages = str(pages).split(".")[0]
    pages = int(pages) + 1
    return pages


def get_links(pages):
    print(pages)
    urls = []
    links = []
    for page in range(1, pages + 1):
        url = f"https://mskins.net/ru/skins/latest?page={page}"
        urls.append(url)

    reqs = [grequests.get(u) for u in urls]
    resp = grequests.map(reqs, size=16)
    errors = 0
    errors_list = []
    for r in enumerate(resp):
        try:
            soup = BeautifulSoup(r[1].text, "lxml")
            hrefs = soup.find_all("a")
            counter = 0
            for href in hrefs:
                link = href.get("href")
                if "/skin/" in str(link):
                    links.append(link)
                    counter += 1
            print(f"[INFO] Обработана страница {r[0]+1}  |  Ссылок найдено - {counter}  |  Всего ссылок - {len(links)}  |  {r[1]}")
            if counter == 0:
                errors_list.append(r[0]+1)
        except:
            errors += 1
            errors_list.append(r[0]+1)

    print(f"Ошибок - {errors}")
    print(f"Ошибки на страницах - {errors_list}")
    return links, errors_list


def error_handler(errors_list, links):
    urls = []
    for page in errors_list:
        url = f"https://mskins.net/ru/skins/latest?page={page}"
        urls.append(url)
    if not len(urls) == 0:
        reqs = [grequests.get(u) for u in urls]
        resp = grequests.map(reqs)
        errors = 0
        errors_list = []
        for r in enumerate(resp):
            try:
                soup = BeautifulSoup(r[1].text, "lxml")
                hrefs = soup.find_all("a")
                counter = 0
                for href in hrefs:
                    link = href.get("href")
                    if "/skin/" in str(link):
                        links.append(link)
                        counter += 1
                print(
                    f"[INFO] Обработана страница {r[0] + 1}  |  Ссылок найдено - {counter}  |  Всего ссылок - {len(links)}  |  {r[1]}")
                if counter == 0:
                    errors_list.append(r[0] + 1)
            except:
                errors += 1
                errors_list.append(r[0] + 1)

        print(f"Ошибок - {errors}")
        print(f"Ошибки на страницах - {errors_list}")
    return links, errors_list


def get_data():
    with open(f"{os.getcwd()}\\data\\links_new.txt", "r") as f:
        links = [row.strip() for row in f]

    data = []

    reqs = [grequests.get(u) for u in links]
    resp = grequests.map(reqs)
    errors = 0
    errors_list = []
    for r in enumerate(resp):

        try:
            soup = BeautifulSoup(r[1].text, "lxml")
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

            print(f"[INFO] Обработан скин {r[0] + 1}  |  {r[1]}", flush=True)
        except:
            errors += 1
            errors_list.append(r[0])

    print(f"Ошибок - {errors}")
    print(f"Ошибки на страницах - {errors_list}")
    return data, errors_list


def skins_errors_handler(data, errors_list):
    with open(f"{os.getcwd()}\\data\\links_new.txt", "r") as f:
        links = [row.strip() for row in f]

    error_links = []
    for item in errors_list:
        for link in links[int(item):int(item) + 1]:
            error_links.append(link)

    reqs = [grequests.get(u) for u in error_links]
    resp = grequests.map(reqs)
    errors = 0
    errors_list = []
    for r in enumerate(resp):
        try:
            soup = BeautifulSoup(r[1].text, "lxml")
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

            print(f"[INFO] Обработан скин {r[0] + 1}  |  {r[1]}")
        except:
            errors += 1
            errors_list.append(r[0] + 1)

    print(f"Ошибок - {errors}")
    print(f"Ошибки на страницах - {errors_list}")
    return data, errors_list


def main():
    # start_time = time.time()
    # output = get_links(pages=pagin())
    # links = output[0]
    # errors_list = output[1]
    # while not len(errors_list) == 0:
    #     errors_list = error_handler(errors_list=errors_list, links=links)[1]
    # print(f"Записано {len(links)} ссылок")
    #
    # with open(f"{os.getcwd()}\\data\\links_new.txt", "w") as f:
    #     for link in links:
    #         try:
    #             f.write(f"{link}\n")
    #         except:
    #             pass
    # print("Ссылки найдены за " + str(time.time() - start_time))


    start_time = time.time()
    output = get_data()
    data = output[0]
    errors_list = output[1]
    while not len(errors_list) == 0:
        errors_list = skins_errors_handler(data=data, errors_list=errors_list)[1]

    print(f"Записаны данные для {len(data)} скинов")

    with open(f"{os.getcwd()}\\data\\data_new.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print("Данные собраны за " + str(time.time() - start_time))


if __name__ == '__main__':
    main()
