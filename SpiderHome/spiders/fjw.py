from datetime import date
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import CrawlSpider

from SpiderHome.items import FjwItem


class FjwSpider(CrawlSpider):
    custom_settings = {
        'ITEM_PIPELINES': {
            'SpiderHome.pipelines.fjwPipeline': 300,
        },
        'DOWNLOAD_DELAY': 4
    }
    name = 'fjw'
    update_flag = True
    start_urls = []  # 初始url，也就是入口urls
    fb = open(
        r'D:\workspace\scrapy spider\SpiderHome\SpiderHome\first_url.txt')
    for url in fb.readlines():
        start_urls.append(url.replace('\n', '--e-1'))
    fb.close()

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)
            self.update_flag = True

    def parse(self, response):
        print(response.url)
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='urf-8')
        next_page_url = urljoin(response.url[:-1],
                                '--e-' + (str)((int)(response.url[-1]) + 1))
        yield Request(next_page_url, callback=self.parse)

    def second_parse(self, response):
        soup = BeautifulSoup(response.body, "lxml", from_encoding='utf-8')
        item = FjwItem()
        item['update_time'] = soup.find(
            'div', class_='fr').string[:-3]  # 获取更新时间
        if item['update_time'] != (str)(
                date.today()):  # 与今天的日期进行比较，若不同，则把update_flag标识设置为false，并跳出
            self.update_flag = False
            return
        item['url'] = response.url
        item['relateId'] = soup.find(
            'input', attrs={'id': 'relateId'})['value']
        item['city'] = soup.find(
            'input', attrs={'id': 'shle_city'}).get_text()  # 获取城市
        item['title'] = soup.find(
            'h1', attrs={'name': 'hl_area'}).get_text()  # 获取标题
        item['region'] = soup.find(
            'input', attrs={'id': 'shle_region'}).get_text()  # 取区域
        item['district_name'] = soup.find(
            'input', attrs={'id': 'shle_region'}).get_text()  # 获取街道
        item['house_desc'] = soup.find(
            'div', class_='text').get_text()  # 获取房子简介
        item['house_infor'] = soup.find('ol').get_text().replace('\n',
                                                                 ' ')  # 获取房子信息
        item['contact'] = soup.find(
            'span', class_='k1 sp0').get_text()  # 获取联系人
        item['phone_number'] = soup.find(
            'span', class_='k1 sp1').get_text()  # 获取联系人电话
        item['img_urls'] = soup.find_all('img', class_='lazy')  # 获取图片下载地址
        if len(item['img_urls']) != 0:
            item['img_path'] = item['relateId']
        yield item
