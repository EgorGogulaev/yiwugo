import winsound
import json
import time

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import lxml


def get_products_links(dict_with_categories: dict):
    dict_with_products = {}
    for category in list(dict_with_categories):
        dict_with_products[category] = {}
        for sub_category in list(dict_with_categories[category]):
            if not dict_with_products[category].get(sub_category, None):
                dict_with_products[category][sub_category] = []

            response = requests.get(dict_with_categories[category][sub_category])
            if "帐号密码" in response.text:
                print("fucking china shit on page")
                time.sleep(210)
                response = requests.get(dict_with_categories[category][sub_category])
                if "帐号密码" in response.text:
                    print("fucking china shit on page again")
                    time.sleep(300)
                    response = requests.get(dict_with_categories[category][sub_category])
                    if "帐号密码" in response.text:
                        print("fucking china shit on page again 🤦‍♂️")
                        time.sleep(300)
                        response = requests.get(dict_with_categories[category][sub_category])

            print(f'sub category: "{sub_category}" ---> ', response.status_code)

            soup = BeautifulSoup(response.text, 'lxml')
            try:
                max_page = int(soup.find('input', {"id": "sumpage"}).get("value"))
            except: max_page = 1

            for page_num in range(1, max_page + 1):
                response = requests.get(dict_with_categories[category][sub_category] + f"&cpage={page_num}")
                print(f'sub category: "{sub_category}" | page: №{page_num} ---> ', response.status_code)

                page_soup = BeautifulSoup(response.text, 'lxml')

                product_inf_elements = page_soup.find_all("div", {"class": "product_inf"})
                for product_inf_element in product_inf_elements:
                    try:
                        product_link = product_inf_element.find("p").find("span").find("a").get("href")
                        dict_with_products[category][sub_category].append(product_link)
                    except: pass

    with open('products.json', 'w', encoding='utf-8') as outfile:
        json.dump(dict_with_products, outfile)


if __name__ == '__main__':
    import utils
    try:
        get_products_links(utils.categories)
    except Exception as ex:
        winsound.Beep(400, 10000)