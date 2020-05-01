from natasha import AddressExtractor

from utils import get_news, find_address_in_news
from parsers.m24_accidents import M24_accidents
from parsers.mosday_accidents  import Mosday_accidents
from parsers.vm_accidents import VM_accidents

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
            print(item)

if __name__ == "__main__":
    main()