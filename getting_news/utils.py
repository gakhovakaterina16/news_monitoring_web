import re
import requests
from collections import OrderedDict
from pprint import pprint

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
        if re.match(r'([А-Я]|[\d*\- А-Я])', address):
            address_list.append('Москва, ' + address)
        # избавляемся от дублекатов адресов
        list(set(address_list))
    return address_list


if __name__ == "__main__":
    #o = [OrderedDict([('parts', [OrderedDict([('name', 'Юных Ленинцев'), ('type','улица')]), OrderedDict([('number', '54'), ('type', 'дом')]), OrderedDict([('type', 'строение')])])])]
    o = [OrderedDict([('parts', [OrderedDict([('name', '1-й Карачаровской'), ('type', 'улица')]), OrderedDict([('number', '8'), ('type', 'дом')])])]), OrderedDict([('parts', [OrderedDict([('name', 'возгорания составляет'), ('type', 'площадь')]), OrderedDict([('number', '950')])])])]
    address_list = extract_address(o)
    print(address_list)
    #print('-------------------------------')


        