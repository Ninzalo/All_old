import os
import json


data = input("Введите текст сюда - ")

with open(f"{os.getcwd()}\\ответы.json", "w") as f:
    f.write(data)

with open(f"{os.getcwd()}\\ответы.json", "r", encoding='utf-8') as f:
    data = json.load(f)

with open(f"{os.getcwd()}\\ответы.json", "w") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)
