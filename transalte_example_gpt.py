import json


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import openai

import mapping_chinagoods as mc

def rephrase_product_name(property_: str, type_property: str, api_key: str):
    openai.api_key = api_key
    # initial_prompt = """
    #         Чат, помоги пожалуйста, я собрал карточки товаров с китайского сайта и мне нужно перевести их названия.
    #         Названия продуктов составлены неграмотно, мне нужно получить сокращенную интерпретацию наименования товара, оставив только название.
    #         После, нужно перевести название на русский язык, учитывая падежи, сколнения и наклонения.
    #         Дословного перевода не требуется, главное смысл.
    #         Избегай прилагательные, которые не будут способствовать продажам(например: "простой/простая")
    #         Вот пример:
    #         Ввод:
    #         Blowing bubbles nano adhesive strong nano double-sided tape transparent non-trace waterproof a large number of wholesale acrylic double-sided tape
    #
    #         Вывод:
    #         Прочный акриловый двухсторонний скотч
    #         """

    if type_property == "name":
        prompt = f"Прошу перевести следующее наименование товара с английского язка на русский язык, сделав сокращённую интерпретацию его смысла, чтобы избежать повторений и гарантировать правильное использование падежей, склонений и наклонений. Название товара должно быть понятным и грамотным, без дословного перевода. Вот текст наименования на английском языке: {property_}"
    elif type_property == "description":
        prompt = f"Прошу перевести следующее описание товара с иностранного языка на русский язык: {property_}"
    else:
        prompt = f"Прошу перевести следующую информацию о названии материала товара с иностранного языка на русский язык: {property_}"


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Укажите чат-модель, которую вы хотите использовать
        messages=[
            # {"role": "system", "content": initial_prompt},
            {"role": "user", "content": prompt}
        ]
    )

    rephrased_product_name = response['choices'][0]['message']['content'].split('.')[0]


    return rephrased_product_name

def translate_product_info(api_key: str):
    engine = create_engine("sqlite:///yiwugo.db")
    errors = []
    with sessionmaker(bind=engine)() as session:
        products = session.query(mc.Product).all()

        for idx, product in enumerate(products):
            print(idx + 1)
            try:
                name = product.name
                description = product.description
                material = product.material

                tr_name = rephrase_product_name(property_=name, type_property="name", api_key=api_key)
                tr_description = rephrase_product_name(property_=description, type_property="description", api_key=api_key)
                tr_material = rephrase_product_name(property_=material, type_property="material", api_key=api_key)


                new_row = mc.TranslatedProduct(
                    id=product.id,
                    site_id=product.site_id,
                    category=product.category,
                    sub_category=product.sub_category,
                    name=tr_name,
                    price=product.price,
                    description=tr_description,
                    patterns=product.patterns,
                    colours=product.colours,
                    sort=product.sort,
                    place_of_origin=product.place_of_origin,
                    material=tr_material,
                    packing_qty=product.packing_qty,
                    meas=product.meas,
                    cbm=product.cbm,
                    gw=product.gw,
                    nw=product.nw,
                )

                session.add(new_row)
                session.commit()
            except Exception as ex:
                print(ex)
                errors.append(product.id)




if __name__ == '__main__':
    api_key = ""
    translate_product_info(api_key)
