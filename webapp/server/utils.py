import re

import requests

from .parsers.m24_accidents import M24_accidents
from .parsers.mosday_accidents  import Mosday_accidents
from .parsers.vm_accidents import VM_accidents


def get_news(news_sites, source_name, extractor):
    site_all_news = []
    try:
        ScrapeClass = news_sites.get(source_name)
        source = ScrapeClass()
        results = source.get_feed()
        for val in results:
            val['text'] = source.get_post(val['link'])
            if val['text']:
                matches = extractor(val['text'])
                spans = [item.span for item in matches]
                facts = [item.fact.as_json for item in matches]
                if facts:
                    val['location'] = facts
                    site_all_news.append(val)
        return site_all_news
    except KeyError:
        print("Данный источник недоступен")
        return False

def get_coordinates(address):
        url = 'http://search.maps.sputnik.ru/search/addr?q=' + address
        r = requests.get(url).json()
        lats = []
        lons = []
        # вытаскиваем координаты из json (их обычно ищется несколько) и считаем среднее
        for i in range(len(r['result']['address'])):
            for j in range(len(r['result']['address'][i]['features'])):
                for k in range(len(r['result']['address'][0]['features'][0]['geometry']['geometries'])):
                    lons.append(r['result']['address'][i]['features'][j]['geometry']['geometries'][0]['coordinates'][0])
                    lats.append(r['result']['address'][i]['features'][j]['geometry']['geometries'][0]['coordinates'][1])
        return sum(lats)/len(lats), sum(lons)/len(lons)


def extract_address(facts):
    '''
    Функция принимает список OrderedDict-ов facts от Наташи, формирует из них адреса в виде строк 
    "*название улицы/площади/др.* *улица/площадь/др.*, *номер дома*
    проверяет, прогоняет через re.match, удаляет дубликаты и возвращает список строк в виде
    "Москва, *название улицы/площади/др.* *улица/площадь/др.*, *номер дома*
    '''
    address_list = [] # список найденных в тексте адресов
    for i in range(len(facts)):
        # для каждого адреса в OrderedDict facts
        address = ''
        for j in range(len(facts[i]['parts'])):
            # структура адреса - несколько (обычно 2) OrderedDict-ов, содержащих ключи 
            # ('name', 'type') и ('number', 'type').
            # первый - это 'название улицы\площади и т.д., второй - чаще всего номер дома, может не содержать 'type'
            # остальные OrderedDict-ы это дополнительная информация, например, номер строения, их мы не учитываем
            try:
                if 'name' in facts[i]['parts'][j].keys():
                    address += facts[i]['parts'][j]['name'] + ' ' + facts[i]['parts'][j]['type']
                elif 'number' in facts[i]['parts'][j].keys():
                    address += ', ' + facts[i]['parts'][j]['number']
            # иногда падает, если не находит 'type'
            except KeyError:
                continue
        # проверяем, что это адрес, а не знаменитая 'площадь возгорания'
        if re.match(r'([А-Я]|\d*\-[а-я] [А-Я])', address):
            address_list.append('Москва, ' + address)
        # избавляемся от дублекатов адресов
        list(set(address_list))
    return address_list

def find_address_in_news(item, extractor):
    for_record = False
    matches = extractor(item['text'])
    spans = [subject.span for subject in matches]
    facts = [subject.fact.as_json for subject in matches]
    address = extract_address(facts)
    # проверяем длину address, а не facts во избежание нахождения только 'площади возгорания'
    if len(address) > 0:
        item['location'] = {'address': address,
                            'street': address[0].split(',')[1].strip()}
        # если улицы нет в БД, то ищем координаты
        #query = "SELECT COUNT(*) FROM news_locations WHERE street = '{}'".format(item['location']['street'])
        #street_in_database = bool(cur.execute(query)) 
        #if not street_in_database:
        item['location']['coordinates'] = [get_coordinates(address) for address in address]
        # если есть - не ищем
        #else:
        #    query = "SELECT latitude, longitude FROM news_locations where street = '{}'".format(item['location']['street'])
        #    cur.execute(query)
        #    item['location']['coordinates'] = [cur.fetchone()]
        for_record = True
    return for_record