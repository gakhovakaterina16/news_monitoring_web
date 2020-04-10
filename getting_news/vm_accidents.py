from bs4 import BeautifulSoup
from datetime import datetime

from utils import get_html

class VM_accidents(object):
    def __init__(self):
        self.url = 'https://vm.ru'

    def get_feed(self):
        html = get_html(self.url + '/accidents')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_found = soup.find('div', class_='articles-list').find_all('div', class_='articles-list__item')
            
            result_news = []
            for item in news_found:

                title = item.find('a').text.replace('\xa0\n', '').strip('\n\t ')
                link = self.url + item.find('a')['href']
                published = item.find('ul')
                time = published.find('li', class_='articles-list__info articles-list__info--time').text.strip('\n\t')
                # приведение даты к общему виду (имеем '25 марта' --> '25.03.2020')
                # 'str(int(' нужно для того, если однозначное число отобразится как 1, а не 01
                day = str(int(published.find('li', class_='articles-list__info articles-list__info--date').text.strip('\n\t')[0:2]))
                month_and_year = datetime.now().strftime('.%m.%Y')
                date = day + month_and_year

                result_news.append({'title': title, 'link': link, 'time': time, 'date': date})
            return result_news

    def get_post(self, url):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            text_blocks = soup.find('div', class_='single-article__main-content').find_all('p')
            text_blocks = text_blocks[:-1]
            news_text = ''
            for block in text_blocks:
                news_text += block.text.replace('\xa0', '').strip('\n\t ') + '\n'
            return news_text

if __name__ == "__main__":
    vm_accidents = VM_accidents()

    news = vm_accidents.get_feed()
    for item in news:
        print('----------------------')
        print(item)
        print()
        print(vm_accidents.get_post(item['link']))
    print('----------------------')
    print(len(news))