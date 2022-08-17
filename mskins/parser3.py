import aiohttp
import asyncio
import os
import time
import random
import json
from bs4 import BeautifulSoup



async def get_link_tasks(session):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.85 YaBrowser/21.11.0.1996 Yowser/2.5 Safari/537.36"
    }
    url = "https://mskins.net/ru/skins/latest"

    r = await session.get(url=url, headers=headers)
    soup = BeautifulSoup(await r.text(), "lxml")
    return soup


async def session_creation():
    async with aiohttp.ClientSession() as session:
        data = await get_link_tasks(session)
        return data


def main():
    data = asyncio.run(session_creation())
    print(data)


if __name__ == '__main__':
    main()
