import random
from time import sleep

import requests
from bs4 import BeautifulSoup
import csv

# TODO: parse data from all pages

URL = 'https://winestyle.ru/beer/all/'

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

FILENAME = 'output'


# req = requests.get(url=URL, headers=HEADERS)
# soup = BeautifulSoup(req.text, "lxml")
# names = soup.find("div", class_="items-container").find_all("p", class_="title")

# with open("piv0.html") as file:
#     src = file.read()
# soup = BeautifulSoup(src, "lxml")
#
# names = soup.find("div", class_="items-container").find_all("p", class_="title")


#
#
# GETTING beer volume
def parse_beer_volume(names):
    volumes = []
    for name in names:
        beer_volume = name.get("data-prodname")
        beer_volume_corr_dig = str(str(beer_volume).split(",")[-1]).split(' ')[1].split('\n')
        for digit in beer_volume_corr_dig:
            if float(digit) > 50.0:
                digit = float(digit) / 1000.0
            volumes.append(float(digit))
    return volumes


#
#
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


#
#
# info = soup.find_all("ul", class_="list-description")
#
#
# GETTING beer parameter based on variable param_num
def parse_description(info, param_num):
    descr = []
    for el in info:
        information = el.find_all("li")
        parameter = str(information[param_num].text).split(":")[1:]  # same idea like lines 19-22
        parameter_corrected = ''  # will also appear in functions below
        for par in parameter:
            parameter_corrected += par.replace('\n', '')
            descr.append(parameter_corrected)
    return descr


# print(parse_description(0))  # beer_region
# parse_description(3)  # beer_type
# parse_description(4)  # beer_style
#
# GETTING beer strength
def parse_beer_strength(info):
    strengths = []
    for el in info:
        information = el.find_all("li")
        beer_strength = str(information[6].text).split(":")[1:]  # same idea like lines 19-22
        beer_strength_corrected = ''
        for nums in beer_strength:
            beer_strength_corrected += nums.split("-")[1].replace("%", "")
        strengths.append(float(beer_strength_corrected))
    return strengths


# left_tablet_price = soup.find_all("div", class_="left-tablet")
#
#
# GETTING beer_price with and without discount
def parse_price(left_tablet_price, http_tag, http_class):
    costs = []
    for el in left_tablet_price:
        price_old = el.find(http_tag, class_=http_class)
        if price_old:
            costs.append(int(str(price_old.text)[0:-4]))
        else:
            costs.append(int(str(el.find("div", class_="price").text)[0:-4]))
    return costs


#
#
# SAVING data to csv file
def save_data(filename, name, info, left_tablet_price):
    with open(filename, mode='a', encoding='utf-8-sig') as fileout:
        writer = csv.writer(fileout, delimiter=';')
        for i in range(len(parse_beer_name(names=name))):
            writer.writerow((
                parse_beer_name(names=name)[i],
                parse_description(info=info, param_num=0)[i],
                parse_description(info=info, param_num=3)[i],
                parse_description(info=info, param_num=4)[i],
                parse_beer_strength(info=info)[i],
                parse_price(left_tablet_price=left_tablet_price, http_tag="div", http_class='price')[i],
                parse_price(left_tablet_price=left_tablet_price, http_tag="div", http_class='price-old')[i],
                parse_beer_volume(names=name)[i]
            ))


def parser():
    pages_to_parse = int(input("Сколько страниц будем парсить?: "))
    page = '?page='
    with open(FILENAME + '.csv', mode='w', encoding='utf-8-sig') as fileout:
        writer = csv.writer(fileout, delimiter=';')
        writer.writerow(
            ("Название", "Регион", "Тип", "Стиль", "Крепость", "Цена со скидкой", "Цена без скидки", "Объем"))
    for i in range(pages_to_parse):
        print("Парсим страницу №" + str(i + 1))
        req = requests.get(url=(URL + page + str(i)), headers=HEADERS)
        soup = BeautifulSoup(req.text, "lxml")
        names = soup.find("div", class_="items-container").find_all("p", class_="title")
        info = soup.find_all("ul", class_="list-description")
        left_tablet_price = soup.find_all("div", class_="left-tablet")
        save_data(FILENAME + '.csv', names, info, left_tablet_price)
        sleep(random.randrange(2, 4))
