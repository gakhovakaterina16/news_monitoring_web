from bs4 import BeautifulSoup

from get_html import get_html

class mosday_accidents():
    def get_feed():
        URL = 'http://mosday.ru/news'
        html = get_html(URL + '/tags.php?accident')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_found = soup.find('body')
            news_found = news_found.find('table', width="100%", height="500", cellpadding="0", cellspacing="0", border="0")
            news_found = news_found.find_all('td')[26]
            news_found = news_found.find('table')
            news_found = news_found.find('table')
            news_found = news_found.find_all('font', face="Arial", size="2", color="#666666", style="font-size:13px")

            result_news = []
            for item in news_found:
                title = item.find('font', size="3", style="font-size:16px").find('a').text
                link = URL + '/' + item.find('font', size="3", style="font-size:16px").find('a')['href']
                date = item.find('b').text
                time = item.text[12:16]
                
                result_news.append((title, link, time, date))
            return result_news
                   

    def get_post(url):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            text_blocks = soup.find('body')
            text_blocks = text_blocks.find('table', width="100%", height="500", cellpadding="0", cellspacing="0", border="0")
            text_blocks = text_blocks.find_all('td')[26]
            text_blocks = text_blocks.find('div').find('table').find('article').find('div', itemprop="text")
            text_blocks = text_blocks.find_all('p')

            news_text = ''
            for block in text_blocks:
                news_text += block.text + '\n'
            return news_text


if __name__ == "__main__":
    news = mosday_accidents.get_feed()
    
    for item in news:
        print('----------------------')
        print(item)
        print()
        print(mosday_accidents.get_post(item[1]))
    print('----------------------')
    print(len(news))
    