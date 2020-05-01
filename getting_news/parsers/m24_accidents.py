from bs4 import BeautifulSoup
from datetime import datetime

import requests

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except(requests.RequestException, ValueError):
        return False
        
                
class M24_accidents(object):
    def __init__(self):
        self.url = 'https://www.m24.ru'

    def get_feed(self):
        html = get_html(self.url + '/tag/происшествия')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_found = soup.find('div', class_='b-materials-list b-list_infinity').find('ul').find_all('li')
            
            result_news = []
            for item in news_found:
                news = item.find('p', class_='b-materials-list__title').find('a')

                title = news.text.strip('\n\t')
                link = self.url + news['href']
                time = item.find('span').text
                date = datetime.now().strftime('%d.%m.%Y')

                result_news.append({'title': title, 'link': link, 'time': time, 'date': date})
        return result_news

    def get_post(self, url):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            # есть страницы с разной разметкой, except - страницы с видео и парой абзацев
            try:
                text_blocks = soup.find('div', class_='js-mediator-article').find_all('p', class_='')
            except AttributeError:
                text_blocks = soup.find('div', class_='b-material-body').find_all('p', class_='')
            ##################################
            news_text = ''
            for block in text_blocks:
                news_text += block.text.replace('\xa0\n', '').strip('\n\t ') + '\n'
            return news_text


if __name__ == "__main__":
    m24_accidents = M24_accidents()

    news = m24_accidents.get_feed()
    for item in news:
        print('----------------------')
        print(item)
        print()
        print(m24_accidents.get_post(item['link']))
    print('----------------------')
    print(len(news))