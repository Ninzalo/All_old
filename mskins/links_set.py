import os


def set_links():
    with open(f"{os.getcwd()}\\data\\links.txt", "r") as f:
        links = [row.strip() for row in f]
        print(len(links))
        links = set(links)
        links = list(links)
        print(len(links))

    with open(f"{os.getcwd()}\\data\\links.txt", "w") as f:
        for link in links:
            f.write(f"{link}\n")


def main():
    set_links()


if __name__ == '__main__':
    main()