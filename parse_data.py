from bs4 import BeautifulSoup
import csv

with open("piv0.html") as file:
    src = file.read()
soup = BeautifulSoup(src, "lxml")

# TODO:
'''
name + 
region + 
type + 
style +
strength +
price with discount +
without discount +
volume +
availability ? (maybe later)
'''

names = soup.find("div", class_="items-container").find_all("p", class_="title")


# GETTING AND PRINTING beer volume
# def parse_beer_volume():
#     for name in names:
#         beer_volume = name.get("data-prodname")
#         beer_volume_corr_dig = str(str(beer_volume).split(",")[-1]).split(' ')[1].split('\n')
#         for digit in beer_volume_corr_dig:
#             if float(digit) > 50.0:
#                 digit = float(digit) / 1000.0
#             print(float(digit))
#
#
# # GETTING AND PRINTING beer name
# def parse_beer_name():
#     for name in names:
#         beer_name = name.get("data-prodname")
#         beer_name_corr = str(beer_name).split(",")[0:-1]  # lines: 19-22: delete info about volume,
#         beer_name_fin = ''  # like ", 0,44 л"
#         for s in beer_name_corr:  # and leave only beer name
#             beer_name_fin += s
#         print(beer_name_fin)


info = soup.find_all("ul", class_="list-description")


# GETTING AND PRINTING beer parameter based on variable param_num
def parse_description(param_num):
    descr = []
    for el in info:
        information = el.find_all("li")
        parameter = str(information[param_num].text).split(":")[1:]  # same idea like lines 19-22
        parameter_corrected = ''  # will also appear in functions below
        for par in parameter:
            parameter_corrected += par.replace('\n', '')
            descr.append(parameter_corrected)
    return descr


print(parse_description(0))  # beer_region
# parse_description(3)  # beer_type
# parse_description(4)  # beer_style

# # GETTING AND PRINTING beer strength
# def parse_beer_strength():
#     for el in info:
#         information = el.find_all("li")
#         beer_strength = str(information[6].text).split(":")[1:]  # same idea like lines 19-22
#         beer_strength_corrected = ''
#         for nums in beer_strength:
#             beer_strength_corrected += nums.split("-")[1].replace("%", "")
#         print(float(beer_strength_corrected))
#
#
# left_tablet_price = soup.find_all("div", class_="left-tablet")
#
#
# # GETTING AND PRINTING beer_price with and without discount
# def parse_price(http_class, price_class):
#     for el in left_tablet_price:
#         price_old = el.find(http_class, class_=price_class)
#         if price_old:
#             print(int(str(price_old.text)[0:-4]))
#         else:
#             print(int(str(el.find("div", class_="price").text)[0:-4]))


#
#
# parse_price("div", 'price-old')  # price without discount
# parse_price("div", 'price')  # price with discount

def save_data(filename):
    with open(filename+'.csv', 'w', newline='', encoding='utf-8-sig') as fileout:
        writer = csv.writer(fileout, delimiter=' ')
        writer.writerow(("Название", "Тип", "Стиль", "Регион", "Цена со скидкой", "Цена без скидки", "Объем"))
        writer.writerow(parse_description(0))

save_data('output')