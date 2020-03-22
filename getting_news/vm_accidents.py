from bs4 import BeautifulSoup

from get_html import get_html

class vm_accidents():
    def get_feed():
        URL = 'https://vm.ru'
        html = get_html(URL + '/accidents')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_found = soup.find('div', class_='articles-list').find_all('div', class_='articles-list__item')
            #print(news_found)
            
            result_news = []
            for item in news_found:

                title = item.find('a').text.strip('\n\t ')
                link = URL + item.find('a')['href']
                published = item.find('ul')
                time = published.find('li', class_='articles-list__info articles-list__info--time').text.strip('\n\t')
                date = published.find('li', class_='articles-list__info articles-list__info--date').text.strip('\n\t')

                result_news.append((title, link, time, date))
            return result_news

    def get_post(url):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            text_blocks = soup.find('div', class_='single-article__main-content').find_all('p')
            text_blocks = text_blocks[:-1]
            news_text = ''
            for block in text_blocks:
                news_text += block.text + '\n'
            return news_text

if __name__ == "__main__":
    news = vm_accidents.get_feed()
    for item in news:
        print('----------------------')
        print(item)
        print()
        print(vm_accidents.get_post(item[1]))
    print('----------------------')
    print(len(news))