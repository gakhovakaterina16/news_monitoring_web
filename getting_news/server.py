from celery import Celery
import psycopg2

from natasha import AddressExtractor
from natasha.markup import show_markup, show_json

from utils import find_address_in_news, links_list, write_to_db
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
    # Соединяемся с БД
    con = psycopg2.connect(
        database=settings.DB_NAME,
        user=settings.DB_USERNAME,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT
    )
    cur = con.cursor()

    # Загружаем список ссылок, чтобы сверяться с ним и не добавлять лишнего
    links = links_list(cur)    

    # Загружаем новости во временное хранилище
    temp_news_list = []
    for key in news_sites.keys():
        temp_news_list += get_news(key)

    # Инициализируем Наташу    
    extractor = AddressExtractor()
    
    for item in temp_news_list:
        # если ссылка есть в БД, то пропускаем
        if item['link'] in links:
            continue
        # анализируем текст на предмет наличия адресов
        if find_address_in_news(item, extractor, cur):            
            # Делаем запись в БД
            write_to_db(item, cur)
        else:
            # удаляем новости, в которых нет адресов
            temp_news_list.remove(item)

    # заканчиваем работу с БД
    con.commit()
    con.close()
    