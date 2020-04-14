from bs4 import BeautifulSoup

from utils import get_html

class Mosday_accidents(object):
    def __init__(self):
        self.url = 'http://mosday.ru/news'

    def get_feed(self):
        html = get_html(self.url + '/tags.php?accident')
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_found = soup.find('body')
            news_found = news_found.find('table', width="100%", height="500", cellpadding="0", cellspacing="0", border="0")
            news_found = news_found.find_all('td')[27] # здесь и далее время от времени сбивается индекс нужного элемента, раньше был 29
            news_found = news_found.find('table')
            news_found = news_found.find('table')
            news_found = news_found.find_all('font', face="Arial", size="2", color="#666666", style="font-size:13px")
            #print(news_found)

            result_news = []
            for item in news_found:
                title = item.find('font', size="3", style="font-size:16px").find('a').text
                link = self.url + '/' + item.find('font', size="3", style="font-size:16px").find('a')['href']
                date = item.find('b').text
                time = item.text[12:16]
                
                result_news.append({'title': title, 'link': link, 'time': time, 'date': date})
            return result_news

    def get_post(self, url):
        html = get_html(url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            text_blocks = soup.find('body')
            text_blocks = text_blocks.find('table', width="100%", height="500", cellpadding="0", cellspacing="0", border="0")
            text_blocks = text_blocks.find_all('td')[27] # тот же индекс
            text_blocks = text_blocks.find('div').find('table').find('article').find('div', itemprop="text")
            text_blocks = text_blocks.find_all('p')
            #print(text_blocks)

            news_text = ''
            for block in text_blocks:
                news_text += block.text.replace('\xa0\n', '').strip('\n\t ') + '\n'
            return news_text


if __name__ == "__main__":
    mosday_accidents = Mosday_accidents()

    news = mosday_accidents.get_feed()    
    for item in news:
        print('----------------------')
        print(item)
        print()
        print(mosday_accidents.get_post(item['link']))
    print('----------------------')
    print(len(news))
    #print(mosday_accidents.get_post('http://mosday.ru/news/item.php?2282246&tags=accident'))
    