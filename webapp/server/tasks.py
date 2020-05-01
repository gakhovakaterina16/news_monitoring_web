from datetime import datetime

from natasha import AddressExtractor

from webapp.server.utils import get_news, find_address_in_news, get_coordinates
from webapp.model import db, News

from webapp.server.parsers.m24_accidents import M24_accidents
from webapp.server.parsers.mosday_accidents  import Mosday_accidents
from webapp.server.parsers.vm_accidents import VM_accidents

def main():
    news_sites = {'m24.ru': M24_accidents, 'mosday.ru': Mosday_accidents, 'vm.ru': VM_accidents}

    # Инициализируем Наташу
    extractor = AddressExtractor()
    
    # Ищем новости, проверяем на наличие адресов, загружаем во временное хранилище
    news_list = []
    for key in news_sites.keys():
        news_list += get_news(news_sites, key, extractor)

    for item in news_list:
        if find_address_in_news(item, extractor):
            #print(item)
            #print(item['location']['coordinates'][0][0], item['location']['coordinates'][0][1])
            
            record = News(
                title=item['title'],
                link=item['link'],
                date_and_time=datetime.strptime(item['time'] + ' ' + item['date'], '%H:%M %d.%m.%Y'),
                text=item['text'],
                address=item['location']['address'],
                street=item['location']['street'],
                lat=item['location']['coordinates'][0][0],
                lon=item['location']['coordinates'][0][1]
            )
            db.session.add(record)
            db.session.commit()
            
if __name__ == "__main__":
    main()