from bs4 import BeautifulSoup

with open("piv0.html") as file:
    src = file.read()
soup = BeautifulSoup(src, "lxml")

# # GETTING AND PRINTING beer name
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

# # GETTING AND PRINTING beer region
# # TODO: Find out why \n appears (2 times!!!) here and in functions below
# for el in info:
#     information = el.find_all("li")
#     region = str(information[0].text).split(":")[1:]     # same idea like lines 19-22
#     region_corrected = ''                                           # will also appear in functions below
#     for reg in region:
#         region_corrected += reg
#     print(region_corrected)

# # GETTING AND PRINTING beer type
# for el in info:
#     information = el.find_all("li")
#     beer_type = str(information[3].text).split(":")[1:]
#     beer_type_corrected = ''
#     for ch in beer_type:
#         beer_type_corrected += ch
#     print(beer_type_corrected)

# # GETTING AND PRINTING beer style
# for el in info:
#     information = el.find_all("li")
#     beer_style = str(information[4].text).split(":")[1:]       # same idea like lines 19-22
#     beer_style_corrected = ''
#     for ch in beer_style:
#         beer_style_corrected += ch
#     print(beer_style_corrected)

# GETTING AND PRINTING beer strength
for el in info:
    information = el.find_all("li")
    beer_strength = str(information[6].text).split(":")[1:]       # same idea like lines 19-22
    beer_strength_corrected = ''
    for nums in beer_strength:
        beer_strength_corrected += nums.split("-")[1].replace("%", "")
    print(beer_strength_corrected)
