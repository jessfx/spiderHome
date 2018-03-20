from scrapy import Request
from bs4 import BeautifulSoup
from scrapy.spider import Spider


class LagouSpider(Spider):

    name = 'lagou'
    header = {
        'Accept': 'application/javascript, */*; q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3',
        'Host': 'webapi.amap.com',
        'Referer': '',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}
    header1 = {
        'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US, en; q=0.8, zh-Hans-CN; q=0.5, zh-Hans; q=0.3',
        'Connection': 'Keep-Alive',
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

    def start_requests(self):
        url = 'https://www.lagou.com/zhaopin/Python/%d/'
        for i in range(1, 31):
            yield Request(url % i, callback=self.parse, headers=self.header1)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        list1 = soup.find('div', class_='s_position_list ').find_all(
            'a', class_='position_link')
        for a in list1:
            header1 = self.header
            header1['Referer'] = a['href']
            yield Request(a['href'], callback=self.parse1)

    def parse1(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        print(soup.find('dd', class_='job-advantage').get_text())
        yield None
