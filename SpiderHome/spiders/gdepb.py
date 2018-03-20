import re

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import Spider
from requests import get
import scrapy
import logging

from SpiderHome.items import GdepbItem


class GdepbSpider(Spider):

    name = 'gdepb'
    custom_settings = {
        'ITEM_PIPELINES': {
            'SpiderHome.pipelines.GDEPBPipeline': 300,
        }
    }

    def start_requests(self):
        url = 'http://pub.gdepb.gov.cn/pub/pubcatalogwry/extranet_pub_documents_list_left.jsp?page=1&catalog='
        yield Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        url = 'http://pub.gdepb.gov.cn/pub/pubcatalogwry/extranet_pub_documents_list_left.jsp?page=%d&catalog='
        count = int(
            soup.find_all('span', class_='arrow')[-2]['onclick'][-4:-1])
        for i in range(1, count + 1):
            yield Request(url % i, callback=self.first_parse)

    def first_parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        url = 'http://pub.gdepb.gov.cn/pub/pubcatalogwry/extranet_pub_document_view.jsp?docId=%d&kwStr='
        for a in soup.find_all('a'):
            yield Request(url % (int(re.findall('\\d+', a['href'])[0])), callback=self.second_parse)

    def second_parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        item = GdepbItem()
        item['thread'] = 'cate3'
        item['body'] = soup.get_text()
        yield item
        if soup.find('span', class_='sr') is not None and soup.find('span', class_='sr').get_text() != '监察执法\信访、投诉案件':
            item['thread'] = 'cate2'
        else:
            item['thread'] = 'cate1'
        item['title'] = soup.find_all('tr', class_='trS')[3].find(
            'span', class_='sr').get_text().strip()
        item['time'] = soup.find_all('tr', class_='trS')[1].find_all(
            'span', class_='sr')[1].get_text().strip()
        item['cate'] = soup.find_all('tr', class_='trS')[0].find(
            'span', class_='sr').get_text().strip()
        item['body'] = soup.find('div', class_='content').get_text().strip()
        if re.search('投诉对象：', soup.get_text()) is None:
            item['thread'] = 'cate1'
        else:
            count1 = re.search('投诉对象：', soup.get_text()).span()[1]
            count2 = re.search('投诉对象地址：', soup.get_text()).span()[0]
            count3 = re.search('投诉对象地址：', soup.get_text()).span()[1]
            count4 = re.search('办理结果', soup.get_text()).span()[0]
            item['obj'] = soup.get_text()[count1:count2]
            item['location'] = soup.get_text()[count3:count4]
        search_txt = ['水污染', '污水', '废水', '污染河流', '污染水', '水环境污染', '河流污染']
        for i in range(len(search_txt)):
            if re.search(search_txt[i], soup.get_text().strip()) is not None:
                item['thread'] = 'water' + item['thread']
                break
        doc_urls = soup.find('div', class_='content').find_all('a')
        doc_locs = []
        for a in doc_urls:
            try:
                doc_name = a.get_text().strip()
                doc_path = 'D:\\gdepb\\' + item['title'] + '\\'
                doc_loc = doc_loc + doc_path
                fp = open(doc_loc, "w")
                r = get(a['href'], timeout=6)
                fp.write(r.content())
                fp.close()
            except:
                self.logger.info(msg="download file error")
        yield item
