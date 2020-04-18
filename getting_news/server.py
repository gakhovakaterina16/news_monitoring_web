from celery import Celery
import psycopg2

from natasha import AddressExtractor
from natasha.markup import show_markup, show_json

from utils import find_address_in_news, get_news, links_list, write_to_db
from m24_accidents import M24_accidents
from mosday_accidents  import Mosday_accidents
from vm_accidents import VM_accidents
import settings

celery_app = Celery('server', broker='redis://localhost:6379/0')
#celery_app.conf.beat_schedule = {
#    'add-every-30-seconds': {
#        'task': 'server.main',
#        'schedule': 30.0
#    },
#}
celery_app.conf.timezone = 'UTC'

@celery_app.task
def main():
    news_sites = {'m24.ru': M24_accidents, 'mosday.ru': Mosday_accidents, 'vm.ru': VM_accidents}

    # Инициализируем Наташу
    extractor = AddressExtractor()

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
        temp_news_list += get_news(news_sites, key, extractor)
    
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

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=0), main.s())

if __name__ == "__main__":
    main.delay()