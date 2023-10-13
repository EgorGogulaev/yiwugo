import re
from collections import namedtuple

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup



def parse_data(str_html: str,) -> namedtuple:
    ProductInformation = namedtuple(typename="ProductInformation",
                                    field_names=["name", "price", "sort",
                                                 "descrition", "patterns",
                                                 "colours", "material", "meas",
                                                 "g_w", "place_of_origin",
                                                 "packing_qty", "cbm",
                                                 "n_w", "photos"])
    soup = BeautifulSoup(str_html, "lxml")
    try:
        name = soup.find("div", {"class": "pro-view-nav"}).find_all("span")[0].text.strip()
    except: name = None

    try:
        price = soup.find_all("font", {"class": "fontbold c-yellow font14px"})[-1].text.strip().replace("\n", '')
    except: price = None

    try:
        patterns = None
    except: patterns = None

    try:
        colours_list = []
        script_text = list(
            filter((lambda x: x.text.replace("\n", "").replace(" ", "").startswith("window.__INITIAL_STATE__")),
                   [scrpt_element for scrpt_element in soup.find_all("script")]))[0].text.replace("\\", '').replace(
            "\n", '').replace("#", '').replace("false", "False").replace("true", "True").replace(
            "window.__INITIAL_STATE__=", "").strip()[:-1]
        colour_text = script_text.split('"attrName":"colour"')[-1].split('"attrName":')[0]
        pattern = r'"attrValueName":"(.*?)"'
        colour_value = re.findall(pattern, colour_text)
        for value in colour_value:
            colours_list.append(value)
        colours = colours_list
    except: colours = None

    try:
        description = " ".join([descr.text for descr in soup.find("div", {"id": "pic"}).find_all("p")[:-1]]).replace("   ", " ").replace("  ", ' ').replace("  ", ' ').replace("\n", "").strip().replace("\\", "").replace("\xa0", "")
    except: description = None

    try:
        parameters_list_elements = soup.find("div", {"class": "cpms_guige"}).find_all("p")[1:]
    except: parameters_list_elements = None
    Sort = None
    Material = None
    MEAS = None
    G_W = None
    Place_of_origin = None
    Packing_qty = None
    CBM = None
    N_W = None
    if parameters_list_elements:
        try:
            Sort = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "Sort:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: Sort = None
        try:
            Material = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "Material:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: Material = None
        try:
            MEAS = list(filter((lambda x: x is not None), [parameter.text.strip() if parameter.find("span").text.strip() == "CTN Szie:" else None for parameter in parameters_list_elements]))[0].replace("\n", '').replace("   ", '').strip().replace("\\", "").replace("\xa0", "").replace("CTN Szie:", "")
        except: MEAS = None

        try:
            G_W = list(filter((lambda x: x is not None), [parameter.text.strip() if parameter.find("span").text.strip() == "G.W./CTN:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "").replace("G.W./CTN:", "")
        except: G_W = None
        try:
            Place_of_origin = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "Place of Origin:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: Place_of_origin = None
        try:
            Packing_qty = list(filter((lambda x: x is not None), [parameter.text.strip() if parameter.find("span").text.strip() == "QTY/CTN:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "").replace("QTY/CTN:", "")
        except: Packing_qty = None

        try:
            CBM = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "CBM:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: CBM = None
        try:
            N_W = list(filter((lambda x: x is not None), [parameter.find("span").find_next_sibling().text.strip() if parameter.find("span").text.strip() == "N.W.:" else None for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "")
        except: N_W = None

    # photos_bytes_list = []
    photos_links = []
    try:
        photo_elements = soup.find("div", {"id": "pic"}).find_all("img")
    except: photo_elements = None
    if photo_elements:
        for photo_element in photo_elements:
            if photo_element.get("src"):
                try:
                    photos_links.append(photo_element.get("src"))
                    # photo_bytes = download_photo(photo_element.get("src"))
                    # photos_bytes_list.append(photo_bytes)
                except Exception as ex:
                    print(f"photo ---> {ex}")
    # print(f"!!!|name - {name}|\n price - {price}|\n description - {description}|\n patterns - {patterns}|\n colours - {colours}|\n sort - {Sort}|\n material - {Material}| meas - {MEAS}|\n G.W. - {G_W}|\n place of origin - {Place_of_origin}|\n packing_qty - {Packing_qty}|\n cbm - {CBM}|!!!")
    return ProductInformation(name=name, price=price,
                              descrition=description, patterns=patterns,
                              colours=colours, sort=Sort,
                              material=Material, meas=MEAS, g_w=G_W,
                              place_of_origin=Place_of_origin,
                              packing_qty=Packing_qty, cbm=CBM,
                              n_w=N_W, photos=photos_links)


if __name__ == '__main__':

    response = requests.get("https://en.yiwugo.com/product/detail/950263926.html?spm=ZW4ueWl3dWdvLmNvbS9wcm9kdWN0L2RldGFpbC85MjkwOTgzMjkuaHRtbA==.ZW4ueWl3dWdvLmNvbS9wcm9kdWN0L2xpc3QuaHRtbD9jcGFnZT05Ng==#")
    data = parse_data(response.text)
    print(data)
