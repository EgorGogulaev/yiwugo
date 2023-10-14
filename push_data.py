# import time
#
# import openai
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import mapping_chinagoods as mc
#
#
# # Задайте свой API-ключ OpenAI
# api_key = "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"
# openai.api_key = api_key
# # Функция для перефразирования названия товара
# def rephrase_product_name(product_name):
#   # Создайте запрос к API ChatGPT
#   initial_prompt = """
#           Чат, помоги пожалуйста, я собрал карточки товаров с китайского сайта и мне нужно перевести их названия.
#           Названия продуктов составлены неграмотно, мне нужно получить сокращенную интерпретацию наименования товара, оставив только название.
#           После, нужно перевести название на русский язык, учитывая падежи, сколнения и наклонения.
#           Дословного перевода не требуется, главное смысл.
#           Избегай прилагательные, которые не будут способствовать продажам(например: "простой/простая")
#           Вот пример:
#           Ввод:
#           Blowing bubbles nano adhesive strong nano double-sided tape transparent non-trace waterproof a large number of wholesale acrylic double-sided tape
#
#           Вывод:
#           Прочный акриловый двухсторонний скотч
#           """
#
#   response = openai.ChatCompletion.create(
#       model="gpt-3.5-turbo",  # Укажите чат-модель, которую вы хотите использовать
#       messages=[
#           {"role": "system", "content": initial_prompt},
#           {"role": "user", "content": f"Прошу перевести следующее наименование товара с английского язка на русский язык, сделав сокращённую интерпретацию его смысла, чтобы избежать повторений и гарантировать правильное использование падежей, склонений и наклонений. Название товара должно быть понятным и грамотным, без дословного перевода. Вот текст наименования на английском языке: {product_name}"}
#       ]
#   )
#
#   # Получите ответ от API ChatGPT
#   rephrased_product_name = response['choices'][0]['message']['content'].split('.')[0]
#
#   # Верните перефразированное название товара
#   return rephrased_product_name
#
#
#
# if __name__ == '__main__':
#     lst = [
#         "Blowing bubbles nano adhesive strong nano double-sided tape transparent non-trace waterproof a large number of wholesale acrylic double-sided tape",
#         "Kneadle nano adhesive blowing bubble transparent double-sided tape non-trace nano tape wholesale waterproof magic paste high viscosity",
#         "Advertising frame",
#         "Yi La Bao exhibition frame aluminum alloy plastic steel advertising frame frame X exhibition frame easy",
#         "Pull net frame, aluminum pull net",
#         "2 mm pet chain, suitable for small pets.",
#         "Carved belt for women with skirt Korean everything sweet decorative thin waist chain Metal chain sweater dress accessories",
#         "Table skirt protective skirt",
#         "Baofeng BF-UV5R/5RA/5RB/5RC TYTF8 walkie-talkie leather sleeve silicone sleeve",
#         "Plastic box glass chess leisure puzzle black and white chess stationery 2 yuan Xu Sheng friends department store wholesale",
#         "Colorful tail pet cleaning supplies Nail clippers Xu Shengyou small products Pet supplies department store",
#         "Silver simple glass European home wall clock wall stick clock mirror circular clock atmosphere digital mirror personality wall clock cross-border hot selling living room decoration clock foreign trade clock pack flannel wood household wall clock",
#         "Three heat sensitive label paper 100x100150 Heat sensitive paper self-adhesive sticker EPost fba label printing paper",
#         "Corner Clip Triangle Clip Right Angle Clip Ins Wind Stapler Protection Book Corner Little Clip Roll Storage Fantastic",
#         "Macaron Color Labor-Saving Handheld Stapler Small No. 10 Convenient Binding Stapler Durable All-Metal Book Stapler",
#         "Cross-border supply of Europe and the United States light luxury gold turquoise waist chain with skirt, suit chain belt chain pants chain accessories women",
#         "Table skirt protective skirt",
#         "Baofeng BF-UV5R/5RA/5RB/5RC TYTF8 walkie-talkie leather sleeve silicone sleeve",
#         "Plastic box glass chess leisure puzzle black and white chess stationery 2 yuan Xu Sheng friends department store wholesale",
#         "Multi-voice high-power walkie-talkie wireless outdoor hand-held waterproof civil mobile station site self-driving tour walkie-talkie",
#         "Factory Direct Sales Logo Custom Metal Color Mini Stapler 24/6/6 Stitching Needle"
#     ]
#     res = []
#     for idx, i in enumerate(lst):
#
#         print(idx + 1)
#         r = rephrase_product_name(
#             product_name=i
#         )
#         res.append(r)
#         time.sleep(15)
#     print(res)



import requests
import os
from dotenv import load_dotenv
load_dotenv()
access_token = os.getenv('access_token')


def test_push():

    sku_type = "0"  # CONSTANTA
    name = "Pet nail clippers"
    type_id = "1"
    price = "31"
    description = "商品标价为不含税价格，如需开票请联系客服 装箱数量：1000/个（请尽量按装箱数下单）尺寸：如图(手工测量略有误差）材质：EVA 重量：小号20中号29大号36特大号44g颜色：半透明商家编码：C2101是否可印logo：否重量：35g 计抛重量：g包装：无小包装数：1个箱规：由于批次和测量方式不同 数据略有误差 介意者慎拍若需要原图图片做详情 请联系客服哦  上架商品是否有货？如果没货怎么办？我们所有产品都是现货销售，页面显示可拍的宝贝都是有货的，请您放心购买。由于商品种类较多，每天销量较大未能及时下架造成的缺货情况，请您谅解，我们会通过电话或者旺旺与您取得联系并处理。我们已经付款，什么时候发货，要多久可以收到货？由于每天发货量比较大，我们会在您付款成功后24-28小时内按付款顺序发货，运送时间会因为距离、天气以及不确定因素影响。如果收到货产品有质量问题和缺货的情况怎么办？如果收到货后货品有缺货或质量问题，请在三天内及时联系售后客服，有质量问题的，请您收到货后及时拍下图片并发给客服。我收到货了，不过不是很喜欢，是否可以退换？如果您对产品不满意、不喜欢，在没有使用过，不影响二次销售的情况下可以退换，运费自理。以下情况不退换A退回的产品包装损毁或不完整，产品配件或相关资料不齐；B未经授权擅自修理或改装；C未按正常方法使用或贮存；D超出售后服务期限的商品；E季节性产品超期不予退还（如夏天的风扇冬天的保暖贴）；F对于我们公司已经下架的产品恕不退换"


    response = requests.post(
        f"https://chinazar.com/api.php/shop.product.add?name={name}&type_id={type_id}&access_token=cf5dabdda340010353432323d9c490ef&format=json", )

    print(response.status_code)
    print(response.json())

def push_goods():

    """
        sku_type POST Необязательно
        Способ выбора модификаций товара на витрине: 0 — по наименованиям артикулов, 1 — по значениям характеристик. Значение по умолчанию — 0.
    
    """
    
    BASE_URL = 'https://chinazar.com/api.php/'
    method = "shop.product.add"

    FULL_URL = f"{BASE_URL}{method}?access_token={access_token}"
    
    name = "Pet nail clippers"
    type_id = 1
    sku_type = 1 # CONSTANTA ТУТ СТАВИМ 1 TODO Понять логику почему 
    price = "31"
    description = "商品标价为不含税价格，如需开票请联系客服 装箱数量：1000/个（请尽量按装箱数下单）尺寸：如图(手工测量略有误差）材质：EVA 重量：小号20中号29大号36特大号44g颜色：半透明商家编码：C2101是否可印logo：否重量：35g 计抛重量：g包装：无小包装数：1个箱规：由于批次和测量方式不同 数据略有误差 介意者慎拍若需要原图图片做详情 请联系客服哦  上架商品是否有货？如果没货怎么办？我们所有产品都是现货销售，页面显示可拍的宝贝都是有货的，请您放心购买。由于商品种类较多，每天销量较大未能及时下架造成的缺货情况，请您谅解，我们会通过电话或者旺旺与您取得联系并处理。我们已经付款，什么时候发货，要多久可以收到货？由于每天发货量比较大，我们会在您付款成功后24-28小时内按付款顺序发货，运送时间会因为距离、天气以及不确定因素影响。如果收到货产品有质量问题和缺货的情况怎么办？如果收到货后货品有缺货或质量问题，请在三天内及时联系售后客服，有质量问题的，请您收到货后及时拍下图片并发给客服。我收到货了，不过不是很喜欢，是否可以退换？如果您对产品不满意、不喜欢，在没有使用过，不影响二次销售的情况下可以退换，运费自理。以下情况不退换A退回的产品包装损毁或不完整，产品配件或相关资料不齐；B未经授权擅自修理或改装；C未按正常方法使用或贮存；D超出售后服务期限的商品；E季节性产品超期不予退还（如夏天的风扇冬天的保暖贴）；F对于我们公司已经下架的产品恕不退换"

    headers = {
        "Content-Type": "application/json"
    }
    params = {
                'name': name,
                'type_id': type_id,
                "sku_type": sku_type
            }

    response = requests.post(
        FULL_URL, data=params
    )

    print()

if __name__ == "__main__":
    push_goods()