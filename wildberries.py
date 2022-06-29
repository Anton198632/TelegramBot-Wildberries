from typing import List
import asyncio
import aiohttp
import requests

WB_URL = 'https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?spp=0&regions=83,75,64,4,38,30,33,70,71,22,31,66,68,40,82,48,1,69,80&stores=117673,122258,122259,125238,125239,125240,507,3158,117501,120602,120762,6158,121709,124731,130744,159402,2737,117986,1733,686,132043&pricemarginCoeff=1.0&reg=0&appType=1&offlineBonus=0&onlineBonus=0&emp=0&locale=ru&lang=ru&curr=rub&couponsGeo=12,3,18,15,21&dest=-1029256,-102269,-2162196,-1257786&nm='


# 'https://wbxcatalog-ru.wildberries.ru/nm-2-card/catalog?locale=ru&lang=ru&curr=rub&nm='


class Socks:
    DICT_WH = [
        {'id': 121709, 'description': 'Электросталь КБТ'},
        {'id': 120762, 'description': 'Электросталь'},
        {'id': 1193, 'description': 'Хабаровск'},
        {'id': 119408, 'description': 'СЦ Очаково'},
        {'id': 117986, 'description': 'Казань'},
        {'id': 116433, 'description': 'Домодедово'},
        {'id': 2737, 'description': 'Санкт-Петербург'},
        {'id': 686, 'description': 'Новосибирск'},
        {'id': 1699, 'description': 'Краснодар'},
        {'id': 3158, 'description': 'Коледино'},
        {'id': 507, 'description': 'Подольск'},
        {'id': 1733, 'description': 'Екатеринбург'},
    ]

    def __init__(self, id: int, qty: int):

        if str(id)[0:3] == '122':
            self.wh = 'Свой склад'
        else:
            data = [s for s in self.DICT_WH if s['id'] == id]
            description = str(id)
            if data is not None and len(data) > 0:
                description = [s for s in self.DICT_WH if s['id'] == id][
                    0].get('description')
            self.wh = description
        self.qty = qty

    def get_wh(self) -> str:
        return self.wh

    def get_qty(self) -> int:
        return self.qty


class Product:
    def __init__(self, id_: int, name: str, brand: str, socks: List[Socks],
                 price: {}, rating: int, feedbacks: int):
        self.__id = id_
        self.__name = name
        self.__brand = brand
        self.__socks = socks
        self.__price = price
        self.__rating = rating
        self.__feedbacks = feedbacks

    def build_result(self) -> str:

        result_text = '<b>{}:</b> <a href="https://www.wildberries.ru/catalog/{}/detail.aspx">{} ({})</a>\n' \
            .format(self.__id, self.__id, self.__name, self.__brand)

        qty_all = 0
        for s in self.__socks:
            qty_all += s.get_qty()
            result_text += '{} - <b>{}</b>\n'.format(s.get_wh(),
                                                     s.get_qty())

        if qty_all == 0:
            result_text += 'нет в наличии\n\n'
        else:
            result_text += '<b>ВСЕГО - {}</b>\n'.format(qty_all)

        result_text += 'Цена / cо скидкой (скидка) - <b>{} / {} ({}%)</b>\n' \
            .format(float(self.__price.get('price')) / 100,
                    float(self.__price.get('sale_price')) / 100,
                    self.__price.get('sale'))

        result_text += 'Рейтинг - <b>{}</b>\n'.format(self.__rating)
        result_text += 'Отзывы - <b>{}</b>\n'.format(self.__feedbacks)

        result_text += "______________________\n"

        return result_text


class WildberriesParser:
    def __init__(self):
        pass

    def parse(self, article_ids: list) -> list:

        result_data = []

        for article_id in article_ids:
            response = requests.get('{}{}'.format(WB_URL, str(article_id)))
            result: dict = response.json()

            products = result.get('data').get('products')
            if products is None or len(products) == 0:
                result_data.append(None)

            if len(products) == 0:
                continue

            name = products[0].get('name')
            brand = products[0].get('brand')

            price = products[0].get('priceU')
            sale = products[0].get('sale')
            sale_price = products[0].get('salePriceU')
            price_pr = {'price': price, 'sale': sale, 'sale_price': sale_price}

            rating = products[0].get('rating')

            feedbacks = products[0].get('feedbacks')

            socks: dict = products[0].get('sizes')[0].get('stocks')
            res_socks = []
            for s in socks:
                res_socks.append(Socks(s.get('wh'), s.get('qty')))

            product = Product(
                id_=article_id,
                name=name,
                brand=brand,
                socks=res_socks,
                price=price_pr,
                rating=rating,
                feedbacks=feedbacks
            )

            result_data.append(product)

        return result_data
