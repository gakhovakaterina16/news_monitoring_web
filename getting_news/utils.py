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
    #try:
        url = 'http://search.maps.sputnik.ru/search/addr?q=' + address
        r = requests.get(url).json()
        lats = []
        lons = []
        for i in range(len(r['result']['address'])):
            for j in range(len(r['result']['address'][i]['features'])):
                for k in range(len(r['result']['address'][0]['features'][0]['geometry']['geometries'])):
                    lons.append(r['result']['address'][i]['features'][j]['geometry']['geometries'][0]['coordinates'][0])
                    lats.append(r['result']['address'][i]['features'][j]['geometry']['geometries'][0]['coordinates'][1])
        return sum(lats)/len(lats), sum(lons)/len(lons)

def extract_address(facts):
    address_list = []
    for i in range(len(facts)):
        address = 'Москва, '
        for j in range(len(facts[i]['parts'])):
            if 'name' in facts[i]['parts'][j].keys():
                address += facts[i]['parts'][j]['name'] + ' ' + facts[i]['parts'][j]['type']
            elif 'number' in facts[i]['parts'][j].keys():
                address += ', ' + facts[i]['parts'][j]['number']
        address_list.append(address)
    return address_list


if __name__ == "__main__":
    #o = [OrderedDict([('parts', [OrderedDict([('name', 'Юных Ленинцев'), ('type','улица')]), OrderedDict([('number', '54'), ('type', 'дом')]), OrderedDict([('type', 'строение')])])])]
    o = [OrderedDict([('parts', [OrderedDict([('name', '1-й Карачаровской'), ('type', 'улица')]), OrderedDict([('number', '8'), ('type', 'дом')])])]), OrderedDict([('parts', [OrderedDict([('name', 'возгорания составляет'), ('type', 'площадь')]), OrderedDict([('number', '950')])])])]
    
    
    print(extract_address(o))
        