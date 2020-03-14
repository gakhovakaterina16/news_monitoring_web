from datetime import datetime
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
    return eval(response.text)

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
    
    data = get_data(latitude, longitude)['drivers']
    driver_ids_in_DB = []
    drivers_data = []
    for driver in data:
        if driver['id'] not in driver_ids_in_DB and (min_latitude < driver['lt'] < max_latitude) or (min_longitude < driver['ln'] < max_longitude):
            try:


                driver_data = {}
                driver_data['driver_id'] =  driver['id']
                driver_data['color'] =  driver['CarColorCode']
                driver_data['direction'] =  driver['direction']
                driver_data['posts'] = []
                post = {datetime.now(): {'lt':driver['lt'], 'ln':driver['ln']}}
                driver_data['posts'].append(post)
                drivers_data.append(driver_data)
            except ValueError:
                pass
        elif driver['id'] in driver_ids_in_DB:
            pass

        

    #drivers.insert_many(data)
    pprint(drivers_data)