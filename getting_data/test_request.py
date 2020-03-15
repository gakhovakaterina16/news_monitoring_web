'''
Это черновик для функций запросов
'''

from datetime import datetime, timedelta
from pymongo import MongoClient
from pprint import pprint
import requests

def get_data(latitude, longitude):
    response = requests.post('https://c-api.city-mobil.ru/getdrivers',
                        json={  "latitude": latitude,
                                "longitude": longitude,
                                "limit": 100,
                                "method": "getdrivers",
                                "radius": 5,
                                "tariff_group": [ 4, 5, 6 ],
                                "ver": "4.33.0"})
    return eval(response.text)['drivers']

if __name__ == '__main__':

    min_latitude = 55.13736
    min_longitude = 36.679533
    max_latitude = 56.028394
    max_longitude = 38.324735

    latitude = 55.741891
    longitude = 37.615382
    #latitude = max_latitude
    #longitude = min_longitude

    #client = MongoClient()
    #db = client.test_taxi_data
    #drivers = db.drivers
    

    
    data = get_data(latitude, longitude)
    driver_ids_in_DB = []
    drivers_data = []
    for driver in data:
        if driver['id'] not in driver_ids_in_DB and ((min_latitude < driver['lt'] < max_latitude) or (min_longitude < driver['ln'] < max_longitude)):
            # добавляем id в список появившихся
            driver_ids_in_DB.append(driver['id'])
            # формируем запись в БД
            driver_data = {}
            driver_data['driver_id'] =  driver['id']
            driver_data['color'] =  driver['CarColorCode']
            driver_data['direction'] =  driver['direction']
            driver_data['car_type'] = driver['car_type']
            driver_data['posts'] = []
            post = {datetime.strftime(datetime.now(), '%d %m %Y %H:%M:%S'): {'lt':driver['lt'], 'ln':driver['ln']}}
            driver_data['posts'].append(post)
            drivers_data.append(driver_data)
        elif driver['id'] in driver_ids_in_DB and ((min_latitude < driver['lt'] < max_latitude) or (min_longitude < driver['ln'] < max_longitude)):
            post = {datetime.strftime(datetime.now(), '%d %m %Y %H:%M:%S'): {'lt':driver['lt'], 'ln':driver['ln']}}
            driver_data['posts'].append(post)

    
        

    #drivers.insert_many(data)
    pprint(drivers_data)

    '''
    current_date = datetime.now()
    period = timedelta(weeks=1)
    out_of_date = current_date - period

    print(current_date)
    print(period)
    print(out_of_date)
    '''