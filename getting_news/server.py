from datetime import datetime

from celery import Celery
import psycopg2

from natasha import AddressExtractor
from natasha.markup import show_markup, show_json

from utils import extract_address, get_coordinates
from m24_accidents import M24_accidents
from mosday_accidents  import Mosday_accidents
from vm_accidents import VM_accidents
import settings


news_sites = {'m24.ru': M24_accidents, 'mosday.ru': Mosday_accidents, 'vm.ru': VM_accidents}

app = Celery('server', broker='redis://localhost:6379/0')

@app.task
def get_news(source_name):
    site_all_news = []
    try:
        ScrapeClass = news_sites.get(source_name)
        source = ScrapeClass()
        results = source.get_feed()
        extractor = AddressExtractor()
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

if __name__ == "__main__":
    # соединяемся с БД
    con = psycopg2.connect(
        database=settings.DB_NAME,
        user=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT
    )
    cur = con.cursor()

    # Загружаем новости во временное хранилище
    temp_news_list = []
    for key in news_sites.keys():
        temp_news_list += get_news(key)

    # Инициализируем Наташу    
    extractor = AddressExtractor()
    
    for item in temp_news_list:
        text = item['text']
        matches = extractor(text)
        spans = [item.span for item in matches]
        facts = [item.fact.as_json for item in matches]
        address = extract_address(facts)
        # проверяем длину address, а не facts во избежание нахождения только площади возгорания
        if len(address) > 0:
            item['location'] = {'address': address,
                                'street': address[0].split(',')[1]}
                                #'coordinates': [get_coordinates(address) for address in extract_address(facts)]}
            # если улицы нет в БД, то ищем координаты
            item['location']['coordinates'] = [get_coordinates(address) for address in address]
            # если нет - ищем координаты
            #############
            # делаем запись в БД
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
        else:
            temp_news_list.remove(item)
            # не делаем запись в БД

    # заканчиваем работу с БД
    con.commit()
    con.close()

    for item in temp_news_list:
        print('----------------------')
        print(item['title'])
        print(item['link'])
        print(item['time'], item['date'])
        print()
        print(item['text'])
        print()
        print(item['location'])

    
    print('----------------------')
    n = len(temp_news_list)
    print(len(temp_news_list))
    