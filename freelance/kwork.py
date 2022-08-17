import json

from bs4 import BeautifulSoup
import requests
import random
import time
import os



def kwork():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 YaBrowser/21.9.2.169 Yowser/2.5 Safari/537.36",
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
    }

    cards = []

    while True:
        url = r"https://kwork.ru/projects?c=41&attr=211"
        r = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(r.text, "lxml")
        final = soup.find("div", class_="project-list js-project-list")
        final = final.find_all("div", class_="card__content pb5")
        for item in final:
            try:
                card = f"Kwork - {item.find('div', class_='wants-card__header-title first-letter breakwords pr250').find('a').text.strip()}"
                if not card in cards:
                    print(card)
                    cards.append(card)
            except:
                pass
        # print(cards)

        url = r"https://freelance.habr.com/tasks?categories=development_bots"
        r = requests.get(url=url, headers=headers)

        soup = BeautifulSoup(r.text, "lxml")
        article = soup.find_all("li", class_="content-list__item")
        for item in article:
            try:
                card = f"Habr  - {item.find('div', class_='task__title').text.strip()}"
                if not card in cards:
                    print(card)
                    cards.append(card)
            except:
                pass


        # time.sleep(random.randrange(60, 120))
        time.sleep(random.randrange(2, 5))

def main():
    kwork()


if __name__ == '__main__':
    main()
