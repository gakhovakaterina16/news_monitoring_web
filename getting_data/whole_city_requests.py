from datetime import datetime
from pymongo import MongoClient
from pprint import pprint
import requests

import numpy as np

# Получение данных о 10 ближайших машинах по координатам
def get_data(latitude, longitude):
    response = requests.post('https://c-api.city-mobil.ru/getdrivers',
                        json={  "latitude": latitude,
                                "longitude": longitude,
                                "limit": 10,
                                "method": "getdrivers",
                                "radius": 5,
                                "tariff_group": [ 4, 5, 6 ],
                                "ver": "4.33.0"})
    return eval(response.text)

# Получение данных о машинах по всей Москве, запись в БД
def form_DB(min_lattitude, min_longitude, max_lattitude, max_longitude):
    
    # Массив координат
    lats_arr = np.arange(min_latitude, max_latitude, 0.0045)
    lons_arr = np.arange(min_longitude, max_longitude, 0.0045)
    #print(len(lats_arr), len(lons_arr), len(lats_arr) * len(lons_arr))

    # Создание БД
    client = MongoClient()
    db = client.test_taxi_data

    # Запрашиваем данные по координатам
    driver_ids_in_DB = []
    for lat in lats_arr:
        for lon in lons_arr:
            data = get_data(lat, lon)['drivers'] # получаем список словарей
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
                    post = {datetime.strftime(datetime.now()): {'lt':driver['lt'], 'ln':driver['ln']}}
                    driver_data['posts'].append(post)
                    db.drivers.insert_one(driver_data)
                elif driver['id'] in driver_ids_in_DB and ((min_latitude < driver['lt'] < max_latitude) or (min_longitude < driver['ln'] < max_longitude)):
                    pass # добавляем только время и координаты
                    '''
                    upd_posts = db.drivers.find({driver_id: driver['id']})
                    post = {datetime.now(): {'lt':driver['lt'], 'ln':driver['ln']}}
                    upd_posts.append(post)
                    db.drivers.update_one({driver_id: driver['id']}, {$set: {posts: upd_posts}})
                    '''
                else:
                    print("Unknown realm of human knowledge")
                    


                '''
                if driver['id'] not in driver_ids_in_DB and (min_latitude < driver['lt'] < max_latitude) or (min_longitude < driver['ln'] < max_longitude):
                    #try:
                        # добавляем id в список появившихся
                        driver_ids_in_DB.append(driver['id'])
                        # формируем запись в БД
                        driver_data = {}
                        driver_data['driver_id'] =  driver['id']
                        driver_data['color'] =  driver['CarColorCode']
                        driver_data['direction'] =  driver['direction']
                        driver_data['posts'] = []
                        post = {datetime.strftime(datetime.now()): {'lt':driver['lt'], 'ln':driver['ln']}}
                        driver_data['posts'].append(post)
                        db.drivers.insert_one(driver_data)
                    #except ValueError:
                    #    pass
                elif driver['id'] in driver_ids_in_DB:
                    try:
                        #??????????????????????????????
                        upd_posts = db.drivers.find({driver_id: driver['id']})
                        post = {datetime.now(): {'lt':driver['lt'], 'ln':driver['ln']}}
                        upd_posts.append(post)
                        #db.drivers.update_one({driver_id: driver['id']}, {$set: {posts: upd_posts}})
                    except ValueError:
                            pass
                else: pass
        except TypeError:
            pass
    print(len(driver_ids_in_DB))
    '''
    

if __name__ == "__main__":
    
    min_latitude = 55.13736
    min_longitude = 36.679533
    max_latitude = 56.028394
    max_longitude = 38.324735

    form_DB(min_latitude, min_longitude, max_latitude, max_longitude)

    