import os


errors_list = [0, 1, 2, 3]
with open(f"{os.getcwd()}\\data\\links_new.txt", "r") as f:
    links = [row.strip() for row in f]

for item in errors_list:
    for link in links[int(item):int(item) + 1]:
        print(link)