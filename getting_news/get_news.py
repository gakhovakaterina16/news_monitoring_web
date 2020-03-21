import requests
from bs4 import BeautifulSoup
from pprint import pprint

def get_html(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except(requests.RequestException, ValueError):
        return False

def get_feed():
    html = get_html('https://yandex.ru/news/region/moscow')
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        news_found = soup.find_all('div', class_='story story_view_normal story_noimage')
        result_news = []
        for item in news_found:
            title = item.find('h2').find('a').text
            link = item.find('h2').find('a')['href']
            text = item.find('div', class_='story__text').text
            info = item.find('div', class_='story__info').find('div', class_='story__date').text
            story_tuple = (title, link, text, info)
            result_news.append(story_tuple)
        return result_news

def get_post(url):
    html = get_html(url)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        source_link = soup.find('div', class_='doc__content').find('a')['href'] # ссылка на источник новости
        return source_link
        # Эта функция почему-то вырубается в какой-то момент


if __name__ == "__main__":
    NEWS_AGGREGATOR_URL = 'https://yandex.ru'
    feed = get_feed()
    
    for item in feed:
        url = NEWS_AGGREGATOR_URL + item[1]
        print(url) # ссылка новости на яндексе
        print()
        print(get_post(url)) # ссылка источика
        print('-------------------')
    