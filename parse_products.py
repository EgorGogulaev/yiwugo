import asyncio
import random
import re
import winsound
import time
import json
from collections import namedtuple

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import lxml

import aiohttp
import aiohttp_proxy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import mapping_chinagoods as mc


def parse_data(str_html: str, ) -> namedtuple:
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
    except:
        name = None

    try:
        price = soup.find_all("font", {"class": "fontbold c-yellow font14px"})[-1].text.strip().replace("\n", '')
    except:
        price = None

    try:
        patterns = None
    except:
        patterns = None

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
    except:
        colours = None

    try:
        description = " ".join([descr.text for descr in soup.find("div", {"id": "pic"}).find_all("p")[:-1]]).replace(
            "   ", " ").replace("  ", ' ').replace("  ", ' ').replace("\n", "").strip().replace("\\", "").replace(
            "\xa0", "")
    except:
        description = None

    try:
        parameters_list_elements = soup.find("div", {"class": "cpms_guige"}).find_all("p")[1:]
    except:
        parameters_list_elements = None
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
            Sort = list(filter((lambda x: x is not None), [
                parameter.find("span").find_next_sibling().text.strip() if parameter.find(
                    "span").text.strip() == "Sort:" else None for parameter in parameters_list_elements]))[
                0].strip().replace("\\", "").replace("\xa0", "")
        except:
            Sort = None
        try:
            Material = list(filter((lambda x: x is not None), [
                parameter.find("span").find_next_sibling().text.strip() if parameter.find(
                    "span").text.strip() == "Material:" else None for parameter in parameters_list_elements]))[
                0].strip().replace("\\", "").replace("\xa0", "")
        except:
            Material = None
        try:
            MEAS = list(filter((lambda x: x is not None),
                               [parameter.text.strip() if parameter.find("span").text.strip() == "CTN Szie:" else None
                                for parameter in parameters_list_elements]))[0].replace("\n", '').replace("   ",
                                                                                                          '').strip().replace(
                "\\", "").replace("\xa0", "").replace("CTN Szie:", "")
        except:
            MEAS = None

        try:
            G_W = list(filter((lambda x: x is not None),
                              [parameter.text.strip() if parameter.find("span").text.strip() == "G.W./CTN:" else None
                               for parameter in parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0",
                                                                                                                 "").replace(
                "G.W./CTN:", "")
        except:
            G_W = None
        try:
            Place_of_origin = list(filter((lambda x: x is not None), [
                parameter.find("span").find_next_sibling().text.strip() if parameter.find(
                    "span").text.strip() == "Place of Origin:" else None for parameter in parameters_list_elements]))[
                0].strip().replace("\\", "").replace("\xa0", "")
        except:
            Place_of_origin = None
        try:
            Packing_qty = list(filter((lambda x: x is not None), [
                parameter.text.strip() if parameter.find("span").text.strip() == "QTY/CTN:" else None for parameter in
                parameters_list_elements]))[0].strip().replace("\\", "").replace("\xa0", "").replace("QTY/CTN:", "")
        except:
            Packing_qty = None

        try:
            CBM = list(filter((lambda x: x is not None), [
                parameter.find("span").find_next_sibling().text.strip() if parameter.find(
                    "span").text.strip() == "CBM:" else None for parameter in parameters_list_elements]))[
                0].strip().replace("\\", "").replace("\xa0", "")
        except:
            CBM = None
        try:
            N_W = list(filter((lambda x: x is not None), [
                parameter.find("span").find_next_sibling().text.strip() if parameter.find(
                    "span").text.strip() == "N.W.:" else None for parameter in parameters_list_elements]))[
                0].strip().replace("\\", "").replace("\xa0", "")
        except:
            N_W = None

    # photos_bytes_list = []
    photos_links = []
    try:
        photo_elements = soup.find("div", {"id": "pic"}).find_all("img")
    except:
        photo_elements = None
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


def save_data(category: str, sub_category: str, product_id: str, product_information: namedtuple, idx: int, ):
    engine = create_engine("sqlite:///yiwugo.db")
    with sessionmaker(bind=engine)() as session:
        product_object = mc.Product(
            site_id=str(product_id.split("/")[-1].split(".html")[0]),
            category=category,
            sub_category=sub_category,
            name=product_information.name,
            price=product_information.price,
            description=product_information.descrition.replace("u002", '/') if product_information.descrition and \
                                                                               "style =" not in product_information.descrition and \
                                                                               "< strong >" not in product_information.descrition and \
                                                                               "< span" not in product_information.descrition and \
                                                                               "< br" not in product_information.descrition else None,
            patterns=", ".join(
                product_information.patterns) if product_information.patterns and \
                                                 "style =" not in product_information.patterns and \
                                                 "< strong >" not in product_information.patterns and \
                                                 "< span" not in product_information.patterns and \
                                                 "< br" not in product_information.patterns else None,
            colours=", ".join(
                product_information.colours).replace("u002", '/') if product_information.colours else None,
            sort=product_information.sort,
            place_of_origin=product_information.place_of_origin,
            material=product_information.material,
            packing_qty=product_information.packing_qty,
            meas=product_information.meas,
            cbm=product_information.cbm,
            gw=product_information.g_w,
            nw=product_information.n_w,
        )
        session.add(product_object)
        session.commit()
        for photo_bytes in product_information.photos:
            photo_object = mc.Photo(photo=photo_bytes,
                                    product=product_object.id)
            session.add(photo_object)
            session.commit()
        iter_time = time.time()
        print(
            f"<<<|||product #{idx + 1}||| id=>{product_id}.>>>")


async def fetch_product(session, product_id, url, headers):
    try:
        response = await session.get(url=url, headers=headers)
        if "帐号密码" in await response.text(encoding="utf-8"):
            print("fucking china shit on page")
            await asyncio.sleep(210)
            response = await session.get(url=url, headers=headers)
            if "帐号密码" in await response.text(encoding="utf-8"):
                print("fucking china shit on page again")
                await asyncio.sleep(300)
                response = await session.get(url=url, headers=headers)
                if "帐号密码" in await response.text(encoding="utf-8"):
                    print("fucking china shit on page again 🤦‍♂️")
                    await asyncio.sleep(300)
                    response = await session.get(url=url, headers=headers)
        product_information = parse_data(await response.text(encoding="utf-8"))
        return product_information
    except Exception as e:
        print(f"Error fetching product {product_id}: {e}")
        return None


async def get_product_information(headers: dict, idx_start_categoty: int, idx_end_category: int,
                                  idx_start_sub_category: int, idx_end_sub_category: int,
                                  proxy: aiohttp_proxy.ProxyConnector | None, unicue_products: list[str],
                                  process_num: int) -> None:
    with open("products.json", 'r', encoding="utf-8") as file:
        categories_with_products_dict = json.load(file)

    async with aiohttp.ClientSession(connector=proxy) if proxy else aiohttp.ClientSession() as session:
        for idx_category, category in enumerate(
                list(categories_with_products_dict)[
                idx_start_categoty:idx_end_category if idx_end_category != -1 else len(
                    list(categories_with_products_dict))]):
            for idx_sub_category, sub_category in enumerate(list(categories_with_products_dict[category])[idx_start_sub_category:idx_end_sub_category if idx_end_sub_category != -1 else len(list(categories_with_products_dict[category]))]):
                print(sub_category)
                list_product_ids = categories_with_products_dict[category][sub_category]
                start_time = time.time()
                for idx, product_url in enumerate(list_product_ids):
                    # try:
                        if product_url not in unicue_products:
                            unicue_products.append("https:" + product_url)
                            print(f"{product_url} ---> P ---> №{process_num}")
                            await asyncio.sleep(random.uniform(0.5, 1))
                            url = f"https:{product_url}"

                            product_information = await fetch_product(session, product_url, url, headers)
                            if product_information:
                                save_data(category, sub_category, product_url, product_information, idx)

                    # except Exception as ex:
                    #     print(
                    #         f"{ex} ||| {idx_category}->{category} ||| {idx_sub_category}->{sub_category} ||| https:{product_url}")
                    #     continue


async def main():
    list_proxy = [
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@45.128.130.134:7002"),
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@149.126.199.81:9858"),
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@149.126.241.247:9858"),
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@149.126.227.194:9858"),
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@149.126.241.241:9858"),
        aiohttp_proxy.ProxyConnector.from_url("https://user135727:5ryz31@149.126.199.197:9858"),
    ]
    headers = {
        'user-agent': UserAgent().random,
    }

    unicue_products = []
    try:
        task_0 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=0, idx_end_category=1, idx_start_sub_category=0,
                                    idx_end_sub_category=10, proxy=None,
                                    unicue_products=unicue_products, process_num=1))
        task_1 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=0, idx_end_category=1,
                                    idx_start_sub_category=10, idx_end_sub_category=20,
                                    proxy=list_proxy[0], unicue_products=unicue_products, process_num=2))
        task_2 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=0, idx_end_category=1,
                                    idx_start_sub_category=20, idx_end_sub_category=30,
                                    proxy=list_proxy[1], unicue_products=unicue_products, process_num=3))
        task_3 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=0, idx_end_category=1,
                                    idx_start_sub_category=30, idx_end_sub_category=-1,
                                    proxy=list_proxy[2], unicue_products=unicue_products, process_num=4))
        task_4 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=1, idx_end_category=-1,
                                    idx_start_sub_category=0, idx_end_sub_category=7,
                                    proxy=list_proxy[3], unicue_products=unicue_products, process_num=5))
        task_5 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=1, idx_end_category=-1,
                                    idx_start_sub_category=7, idx_end_sub_category=14,
                                    proxy=list_proxy[4], unicue_products=unicue_products, process_num=6))
        task_6 = asyncio.create_task(
            get_product_information(headers=headers, idx_start_categoty=1, idx_end_category=-1,
                                    idx_start_sub_category=14, idx_end_sub_category=-1,
                                    proxy=list_proxy[5], unicue_products=unicue_products, process_num=7))
        tasks = [task_0, task_1, task_2, task_3, task_4, task_5, task_6]

        await asyncio.gather(*tasks)

    except Exception as ex:
        print(ex)
        winsound.Beep(500, 10000)


if __name__ == '__main__':
    asyncio.run(main())
