import os
import time


path = "X:\Programs\Python\\test\\txts"

with open(f"{path}\\final_added.txt", "w") as final:
    final.write("")

n = 0

with open(f"{path}\\add.txt") as add, open(f"{path}\\all.txt") as all:
    added = add.readlines()
    all_links = all.readlines()
    for entry in added:
        entry = entry.replace("\n", "")
        for text in all_links:
            text = text.replace("\n", "")
            if text == entry:
                n = n + 1
            else:
                n = n + 0
        print(n)
        if n == 0:
            with open(f"{path}\\all.txt", "a") as all, open(f"{path}\\final_added.txt", "a") as final:
                final.write(entry + '\n')
                all.write(entry + '\n')
        n = 0