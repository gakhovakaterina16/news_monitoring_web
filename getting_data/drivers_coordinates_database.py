'''
Пока работает скрипт, заполняется БД.
Предполагается, что он будет работать все время.

!!!
NB: Нужно дописать автоматическое удаление устаревших данных.
!!!
'''

from datetime import datetime, timedelta
from pymongo import MongoClient
from pprint import pprint
import requests

import numpy as np

# Получение данных о 10 ближайших машинах по координатам
def get_data(latitude, longitude):
    '''
    Функция запрашивает данные о ближайших к (latitude, longitude) 
    10 свободных водителях с 'https://c-api.city-mobil.ru/getdrivers'.
    Возвращает список словарей  типа : {'CarColorCode': '000000',
                                        'car_type': 'comfort_plus',
                                        'direction': 4,
                                        'id': '40b8eda224fd07dc308f1eba8ec7b0d1',
                                        'ln': 37.6274738,
                                        'lt': 55.7379757}
    '''
    response = requests.post('https://c-api.city-mobil.ru/getdrivers',
                        json={  "latitude": latitude,
                                "longitude": longitude,
                                "limit": 10,
                                "method": "getdrivers",
                                "radius": 5,
                                "tariff_group": [ 4, 5, 6 ],
                                "ver": "4.33.0"})
    return eval(response.text)['drivers']

# Получение данных о машинах по всей Москве, запись в БД
def form_DB(min_lattitude, min_longitude, max_lattitude, max_longitude):
    '''
    Функция делает запросы из точек с координатами, лежащими в заданом диапазоне и формирует из них БД.
    Запись в БД имеет вид: {
                            "_id": {
                                "$oid": "5e6cb0482ed23c86e5a9c235"
                            },
                            "driver_id": "36c8320dc184c411e0bab22770b6b38a",
                            "color": "000000",
                            "direction": {
                                "$numberInt": "0"
                            },
                            "posts": [{
                                "14 03 2020 13:22:00": {
                                    "lt": {
                                        "$numberDouble": "55.1418298"
                                    },
                                    "ln": {
                                        "$numberDouble": "37.4531165"
                                        }
                                    }
                                }]
                            }
    
    Предполагается, что чем больше раз будет запущена функция, тем более полными будут данные.
    '''
    
    # Массив координат
    lats_arr = np.arange(min_latitude, max_latitude, 0.0045) # шаг 0.0045 ~ 500 м
    lons_arr = np.arange(min_longitude, max_longitude, 0.0045)

    # Создание БД
    client = MongoClient()
    db = client.test_taxi_data

    # Запрашиваем данные по координатам
    driver_ids_in_DB = []
    for lat in lats_arr:
        for lon in lons_arr:
            data = get_data(lat, lon) # получаем список словарей
            # Проверяем, есть ли уже в БД запись с id и находится ли в пределах города
            for driver in data:
                if driver['id'] not in driver_ids_in_DB and ((min_latitude < driver['lt'] < max_latitude) or (min_longitude < driver['ln'] < max_longitude)):
                    # добавляем id в список появившихся
                    driver_ids_in_DB.append(driver['id'])
                    # формируем запись в БД
                    driver_data = {}
                    driver_data['driver_id'] =  driver['id']
                    driver_data['color'] =  driver['CarColorCode']
                    driver_data['direction'] =  driver['direction']
                    driver_data['posts'] = []
                    post = {datetime.strftime(datetime.now(), '%d %m %Y %H:%M:%S'): {'lt':driver['lt'], 'ln':driver['ln']}}
                    driver_data['posts'].append(post)
                    db.drivers.insert_one(driver_data)
                elif driver['id'] in driver_ids_in_DB and ((min_latitude < driver['lt'] < max_latitude) or (min_longitude < driver['ln'] < max_longitude)):
                    post = {datetime.strftime(datetime.now(), '%d %m %Y %H:%M:%S'): {'lt':driver['lt'], 'ln':driver['ln']}}
                    db.drivers.driver['id'].posts.insert_one(post)
                
                
    # Удаляем устаревшие данные
    '''
    current_date = datetime.now()
    period = datetime.timedelta(weeks=1)
    out_of_date = current_date - period
    #????????????????????????
    '''


if __name__ == "__main__":
    
    min_latitude = 55.13736
    min_longitude = 36.679533
    max_latitude = 56.028394
    max_longitude = 38.324735

    #form_DB(min_latitude, min_longitude, max_latitude, max_longitude)

    while True:
        form_DB(min_latitude, min_longitude, max_latitude, max_longitude)

    