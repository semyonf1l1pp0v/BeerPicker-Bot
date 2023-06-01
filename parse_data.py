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


# GETTING AND PRINTING beer parameter based on variable param_num
# def parse_description(param_num):
#     for el in info:
#         information = el.find_all("li")
#         parameter = str(information[param_num].text).split(":")[1:]  # same idea like lines 19-22
#         parameter_corrected = ''  # will also appear in functions below
#         for par in parameter:
#             parameter_corrected += par.replace('\n', '')
#         print(parameter_corrected)


# parse_description(0)  # beer_region
# parse_description(3)  # beer_type
# parse_description(4)  # beer_style

# # GETTING AND PRINTING beer strength
# for el in info:
#     information = el.find_all("li")
#     beer_strength = str(information[6].text).split(":")[1:]       # same idea like lines 19-22
#     beer_strength_corrected = ''
#     for nums in beer_strength:
#         beer_strength_corrected += nums.split("-")[1].replace("%", "")
#     print(float(beer_strength_corrected))
