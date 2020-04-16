from datetime import datetime
import re
import requests
#from collections import OrderedDict

import settings

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except(requests.RequestException, ValueError):
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


def links_list(cur):
    query = "SELECT src FROM news_locations"
    cur.execute(query)
    res = cur.fetchall()
    links = []
    for r in res:
        links.append(r[0])
    return links


def write_to_db(item, cur):
    dt_str = item['time'] + ' ' + item['date']
    query = '''INSERT INTO {table_name} (title, src, published, post, address, street, latitude, longitude) 
                    VALUES ('{title}', '{src}', '{published}', '{post}', '{address}', '{street}', {lat}, {lon})
            '''.format(table_name=settings.DB_TABLE_NAME, 
                        title=item['title'],
                        src=item['link'],
                        published=datetime.strptime(dt_str, '%H:%M %d.%m.%Y'),
                        post=item['text'],
                        address=item['location']['address'][0],
                        street=item['location']['street'],
                        lat=item['location']['coordinates'][0][0],
                        lon=item['location']['coordinates'][0][1])
    cur.execute(query)


def find_address_in_news(item, extractor, cur):
    for_record = False
    matches = extractor(item['text'])
    spans = [subject.span for subject in matches]
    facts = [subject.fact.as_json for subject in matches]
    address = extract_address(facts)
    # проверяем длину address, а не facts во избежание нахождения только площади возгорания
    if len(address) > 0:
        item['location'] = {'address': address,
                            'street': address[0].split(',')[1].strip()}
        # если улицы нет в БД, то ищем координаты
        query = "SELECT COUNT(*) FROM news_locations WHERE street = '{}'".format(item['location']['street'])
        street_in_database = bool(cur.execute(query)) 
        if not street_in_database:
            item['location']['coordinates'] = [get_coordinates(address) for address in address]
        # если есть - не ищем
        else:
            query = "SELECT latitude, longitude FROM news_locations where street = '{}'".format(item['location']['street'])
            cur.execute(query)
            item['location']['coordinates'] = [cur.fetchone()]
        for_record = True
    return for_record
        
