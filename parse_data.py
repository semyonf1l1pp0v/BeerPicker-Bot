import random
import re
from time import sleep

import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://winestyle.ru/beer/all/'

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

FILENAME = 'output'


# GETTING beer volume
def parse_beer_volume(names):
    volumes = []
    for name in names:
        beer_volume = name.get("data-prodname")
        beer_volume_corr_dig = str(str(beer_volume).split(",")[-1]).split(' ')[1].split('\n')
        for digit in beer_volume_corr_dig:
            try:
                if float(digit) > 50.0:
                    digit = float(digit) / 1000.0
                volumes.append(float(digit))
            except ValueError:
                volumes.append(0)
    return volumes


# GETTING beer name
def parse_beer_name(names):
    reg = []
    for name in names:
        beer_name = name.get("data-prodname")
        beer_name_corr = str(beer_name).split(",")[0:-1]  # lines: 31-33: delete info about volume,
        beer_name_fin = ''  # like ", 0,44 л"
        for s in beer_name_corr:  # and leave only beer name
            beer_name_fin += s
        reg.append(beer_name_fin)
    return reg


# GETTING beer parameter based on variable
def parse_description(soup, info):
    information = soup.find_all("li")
    descr = ""
    for item in information:
        name = item.find("span", class_="name")
        if name and name.text.strip() == info:
            descr_links = item.find_all("a")
            descr = ", ".join(str(link.text).lower() for link in descr_links)
    return descr


# GETTING beer strength
def parse_beer_strength(info):
    strengths = []
    for el in info:
        information = el.find_all("li")
        beer_strength = None
        for item in information:
            if "Крепость" in str(item):
                beer_strength = str(item.text)
                break
        if beer_strength is not None:
            match = re.search(r'\d+(\.\d+)?%', beer_strength)
            if match:
                strength = float(match.group(0).rstrip('%'))
                strengths.append(strength)
            else:
                strengths.append(None)
        else:
            strengths.append(None)
    return strengths


# GETTING beer_price with and without discount
def parse_price(left_tablet_price, http_tag, http_class):
    costs = []
    for el in left_tablet_price:
        price_old = el.find(http_tag, class_=http_class)
        if price_old:
            costs.append(int(str(str(price_old.text).replace(' ', '')[0:-4]).replace('—', '0')))  # beer with no price
        else:
            costs.append(int(str(str(el.find("div", class_="price").text).replace(' ', '')[0:-4]).replace('—', '0')))
    return costs


def parse_image_link(links):
    links_list = []
    for link in links:
        links_list.append(link.find("img").get("src"))
    return links_list


# SAVING data to csv file
def save_data(filename, names, info_list, left_tablet_price, image_link):
    with open(filename, mode='a', encoding='utf-8-sig') as fileout:
        writer = csv.writer(fileout, delimiter=';')
        for i, name in enumerate(parse_beer_name(names)):
            writer.writerow((
                name,
                parse_description(soup=BeautifulSoup(str(info_list[i]), "lxml"), info="Регион:"),
                parse_description(soup=BeautifulSoup(str(info_list[i]), "lxml"), info="Пиво:"),
                parse_description(soup=BeautifulSoup(str(info_list[i]), "lxml"), info="Стиль:"),
                parse_beer_strength(info=info_list)[i],
                parse_price(left_tablet_price=left_tablet_price, http_tag="div", http_class='price')[i],
                parse_price(left_tablet_price=left_tablet_price, http_tag="div", http_class='price-old')[i],
                parse_beer_volume(names)[i],
                parse_image_link(image_link)[i]
            ))


def print_output_headers(filename):
    with open(filename + '.csv', mode='w', encoding='utf-8-sig') as fileout:
        writer = csv.writer(fileout, delimiter=';')
        writer.writerow(
            ("Название", "Регион", "Тип", "Стиль", "Крепость", "Цена со скидкой", "Цена без скидки", "Объем", "Изображение"))


def get_pages_count():
    with requests.Session() as session:
        req = session.get(url=URL, headers=HEADERS)
    soup = BeautifulSoup(req.text, "lxml")
    beer_count_soup = soup.find("div", class_="main-title-container").find("span", class_="small").text
    beer_count = int(beer_count_soup.strip().split(' ')[-1])
    return beer_count // 20 + 1


def parser():
    pages_to_parse = get_pages_count()
    page = '?page='
    print_output_headers(filename=FILENAME)
    for i in range(pages_to_parse):
        print(f"Парсим страницу №{i+1}")
        while True:
            try:
                with requests.Session() as session:
                    proxy_tor = f"socks5://127.0.0.1:{random.randint(9052, 9139)}"
                    proxies = {"https": proxy_tor}
                    req = session.get(url=(URL + page + str(i + 1)), headers=HEADERS, proxies=proxies, timeout=10)
                    soup = BeautifulSoup(req.text, "lxml")
                    names = soup.find("div", class_="items-container").find_all("p", class_="title")
                    info = soup.find_all("ul", class_="list-description")
                    left_tablet_price = soup.find_all("div", class_="left-tablet")
                    image_links = soup.find_all("a", class_="img-block")
                    save_data(FILENAME + '.csv', names, info, left_tablet_price, image_links)
                    print(f"Спарсили страницу №{i+1}")
                    break
            except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout,
                    AttributeError):
                print("\nНе удалось подключиться к прокси-серверу, попробуем другой\n")
            sleep(random.randrange(4, 6))


def main():
    parser()


if __name__ == '__main__':
    main()
