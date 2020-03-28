from celery import Celery

from m24_accidents import M24_accidents
from mosday_accidents import Mosday_accidents
from vm_accidents import VM_accidents


news_sites = {'m24.ru': M24_accidents, 'mosday.ru': Mosday_accidents, 'vm.ru': VM_accidents}

app = Celery('server', broker='redis://localhost:6379/0')

@app.task
def get_news(source_name):
    try:
        ScrapeClass = news_sites.get(source_name)
        source = ScrapeClass()
        results = source.get_feed()
        for val in results:
            val['text'] = source.get_post(val['link'])
            print(val)
    except KeyError:
        print("Данный источник недоступен")
        return False

if __name__ == "__main__":
    for key in news_sites.keys():
        get_news(key)
        