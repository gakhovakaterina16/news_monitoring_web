from celery import Celery
from pprint import pprint

from natasha import AddressExtractor
from natasha.markup import show_markup, show_json

from m24_accidents import M24_accidents
from mosday_accidents import Mosday_accidents
from vm_accidents import VM_accidents


news_sites = {'m24.ru': M24_accidents, 'mosday.ru': Mosday_accidents, 'vm.ru': VM_accidents}

app = Celery('server', broker='redis://localhost:6379/0')

@app.task
def get_news(source_name):
    site_all_news = []
    try:
        ScrapeClass = news_sites.get(source_name)
        source = ScrapeClass()
        results = source.get_feed()
        for val in results:
            val['text'] = source.get_post(val['link'])
            #print(val)
            site_all_news.append(val)
        return site_all_news
    except KeyError:
        print("Данный источник недоступен")
        return False

if __name__ == "__main__":
    # Загружаем новости во временное хранилище
    pseudo_db = []
    for key in news_sites.keys():
        pseudo_db += get_news(key)

    # Инициализируем Наташу    
    extractor = AddressExtractor()
    
    for item in pseudo_db:
        text = item['text']
        matches = extractor(text)
        spans = [item.span for item in matches]
        facts = [item.fact.as_json for item in matches]

        if len(facts) > 0:
            item['location'] = facts
        else:
            # что-то не так, ничего не удаляется
            pseudo_db.remove(item)

    print(pseudo_db)