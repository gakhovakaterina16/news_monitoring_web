from pymongo import MongoClient
#from pprint import pprint
import requests

def get_data():
    response = requests.post('https://c-api.city-mobil.ru/getdrivers',
                        json={  "latitude": 55.741891,
                                "longitude": 37.615382,
                                "limit": 10,
                                "method": "getdrivers",
                                "radius": 5,
                                "tariff_group": [ 4, 5, 6 ],
                                "ver": "4.33.0"})
    return eval(response.text)

if __name__ == '__main__':

    client = MongoClient()
    db = client.test_taxi_data
    drivers = db.drivers

    data = get_data()['drivers']
    drivers.insert_many(data)
    #pprint(data)