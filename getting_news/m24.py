from bs4 import BeautifulSoup
from datetime import datetime

from utils import get_html

class M24(object):
    def __init__(self):
        self.url = 'https://www.m24.ru'

    def get_feed(self):
        html = get_html(self.url + '/news')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_found = soup.find('div', class_='b-materials-list b-list_infinity').find('ul').find_all('li')
            
            result_news = []
            for item in news_found:
                news = item.find('p', class_='b-materials-list__title b-materials-list__title_news')

                title = news.find('a').text.strip('\n\t')
                link = self.url + news.find('a')['href']
                time = news.find('span').text
                date = datetime.now().strftime('%d.%m.%Y')

                result_news.append({'title': title, 'link': link, 'time': time, 'date': date})
            return result_news
            
    def get_post(self, url):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            text_blocks = soup.find('div', class_='js-mediator-article').find_all('p', class_='')
            news_text = ''
            for block in text_blocks:
                news_text += block.text + '\n'
            return news_text


if __name__ == "__main__":
    m24 = M24()
    
    news = m24.get_feed()
    for item in news:
        print('----------------------')
        print(item)
        print()
        print(m24.get_post(item['link']))
    print('----------------------')
    print(len(news))
    