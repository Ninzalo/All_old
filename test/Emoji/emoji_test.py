import emoji

while True:
    name = input('Введите текст ')
    # text = [
    #     "!", "!tg", "!bttv", "!inst", "!обзор", "!тг", "!knifex",
    #     "\\", "/", ":", "*", "?", '"', "<", ">", "|",
    #     "ブ", "ラ", "チ", "シ", "ュ", "キ", "ン", "の", "攻", "撃", "ャ",
    #     "💢", "👼🏼", "🧀", "🔴", "😎", "❤", "🍑", "💦", "✖", "😏", "🌚", "😜", "😋", "😉", "😵",
    #     "👏", "😸", "😹", "❌", "🧠", "😂", "🤫", "🔫", "🎯", "🧒", "🏀", "🤯", "🎬", "❓",
    #     "🐗", "👉🏻", "🤡", "👽", "👷", "🐥", "🥵", "😍", "🧔", "🏻", "🐵", "😨", "🤢", "❗️",
    #     "😱", "😡", "🐄", "🧡", "😴", "💗", "🤔", "🐀", "✨", "😄", "😁", "🛑", "🤪", "🤙",
    #     "✈", "💓", "😯", "☝", "☝️", "ү", "😇", "☢️", "😈", "🦷", "👉", "👌", "👼", "😭",
    #     "🤣", "🔥", "💜", "😳", "💩", "🥺", "♥", "ニ", "ー", "🤤", "₴", "🤵", "🍷", "✊", "😘",
    #     "🐶", "5️⃣", "🦔", "🍇", "🥶", "🐾", "🔪", "🍸", "🙋", "♿", "😲",
    #     "Название отсутствует", "IRL", "стрим", "Стрим", "КАТАЕМСЯ",
    #     "хуй", "пизд", "дцп", "хохол", "пид", "gay", "геи", "гей", "nig", "негр",
    #     "ЕБАТЬ", "ебать", "Ебать", "ебанный", "ебаный"
    # ]
    # for item in text:
    #     if ":" in emoji.demojize(item):
    #         print(f"{item} - Yes")
    #     else:
    #         print(f"{item} - No")

    words = [
        "!", "!tg", "!bttv", "!inst", "!обзор", "!тг", "!knifex",
        "\\", "/", ":", "*", "?", '"', "<", ">", "|",
        "ブ", "ラ", "チ", "シ", "ュ", "キ", "ン", "の", "攻", "撃", "ャ",
        # "💢", "👼🏼", "🧀", "🔴", "😎", "❤", "🍑", "💦", "✖", "😏", "🌚", "😜", "😋", "😉", "😵",
        # "👏", "😸", "😹", "❌", "🧠", "😂", "🤫", "🔫", "🎯", "🧒", "🏀", "🤯", "🎬", "❓",
        # "🐗", "👉🏻", "🤡", "👽", "👷", "🐥", "🥵", "😍", "🧔", "🏻", "🐵", "😨", "🤢", "❗️",
        # "😱", "😡", "🐄", "🧡", "😴", "💗", "🤔", "🐀", "✨", "😄", "😁", "🛑", "🤪", "🤙",
        # "✈", "💓", "😯", "☝", "☝️", "ү", "😇", "☢️", "😈", "🦷", "👉", "👌", "👼", "😭",
        # "🤣", "🔥", "💜", "😳", "💩", "🥺", "♥", "ニ", "ー", "🤤", "₴", "🤵", "🍷", "✊", "😘",
        # "🐶", "5️⃣", "🦔", "🍇", "🥶", "🐾", "🔪", "🍸", "🙋", "♿", "😲",
        "Название отсутствует", "IRL", "стрим", "Стрим", "КАТАЕМСЯ",
        "хуй", "пизд", "дцп", "хохол", "пид", "gay", "геи", "гей", "nig", "негр",
        "ебать", "ебанный", "ебаный"
    ]

    is_ok = True

    for i in words:
        if i.lower() in name.lower():
            is_ok = False

    # if is_ok:

    if ":" not in emoji.demojize(name) and is_ok:
        print(f"{name} - Загружаем")
    else:
        print(f"{name} - No")