# import pandas as pd
# ds = pd.read_html("https://en.wikipedia.org/wiki/List_of_highest-grossing_films")
# pd.set_option('display.max_columns', None)
# ds[0].to_excel('movies.xlsx')

from bs4 import BeautifulSoup

with open("/Users/semenfilippov/Desktop/piv0.html") as file:
    src = file.read()
soup = BeautifulSoup(src, "lxml")

# # GETTING AND PRINTING NAMES
# # TODO: Use extracted value of volume to fill its column
# names = soup.find("div", class_="items-container").find_all("p", class_="title")
#
# for name in names:
#     beer_name = name.get("data-prodname")
#     print("")
#     beer_name_corr = str(beer_name).split(",")[0:-1]  # lines: 19-22: delete info about volume,
#     beer_name_fin = ''                                # like ", 0,44 л"
#     for s in beer_name_corr:                          # and leave only beer name
#         beer_name_fin += s
#     print(beer_name_fin)
# #

info = soup.find_all("ul", class_="list-description")

# # GETTING AND PRINTING REGION
# # TODO: Find out why \n appears (2 times!!!) here and in functions below
# for el in info:
#     region = el.find_all("li")
#     region_corrected = str(region[0].text).split(":")[1:]     # same idea like lines 19-22
#     region_fin = ''                                           # will also appear in functions below
#     for reg in region_corrected:
#         region_fin += reg
#     print(region_fin)

# # GETTING AND PRINTING beer_type
# for el in info:
#     beer_type = el.find_all("li")
#     beer_type_corrected = str(beer_type[3].text).split(":")[1:]
#     beer_type_fin = ''
#     for reg in beer_type_corrected:
#         beer_type_fin += reg
#     print(beer_type_fin)

# # GETTING AND PRINTING beer_style
# for el in info:
#     beer_style = el.find_all("li")
#     beer_style_corrected = str(beer_style[4].text).split(":")[1:]       # same idea like lines 19-22
#     beer_style_fin = ''
#     for reg in beer_style_corrected:
#         beer_style_fin += reg
#     print(beer_style_fin)

for el in info:
    beer_style = el.find_all("li")
    beer_style_corrected = str(beer_style[6].text).split(":")[1:]       # same idea like lines 19-22
    beer_style_fin = ''
    for reg in beer_style_corrected:
        beer_style_fin += reg.split("-")[1]
    print(beer_style_fin)
