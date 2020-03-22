from bs4 import BeautifulSoup

from get_html import get_html

class m24():
    def get_feed():
        URL = 'https://www.m24.ru'
        html = get_html(URL + '/news')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_found = soup.find('div', class_='b-materials-list b-list_infinity').find('ul').find_all('li')
            
            result_news = []
            for item in news_found:
                news = item.find('p', class_='b-materials-list__title b-materials-list__title_news')

                title = news.find('a').text.strip('\n\t')
                link = URL + news.find('a')['href']
                time = news.find('span').text

                result_news.append((title, link, time))
            return result_news
            
    def get_post(url):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            text_blocks = soup.find('div', class_='js-mediator-article').find_all('p', class_='')
            news_text = ''
            for block in text_blocks:
                news_text += block.text + '\n'
            return news_text


if __name__ == "__main__":
    news = m24.get_feed()
    for item in news:
        print('----------------------')
        print(item)
        print()
        print(m24.get_post(item[1]))
    print('----------------------')
    print(len(news))
