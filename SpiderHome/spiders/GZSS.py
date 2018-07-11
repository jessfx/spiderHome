# encoding: utf-8
import datetime
import re
import urllib

import pymongo
import requests
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import Spider

from SpiderHome.items import GzssItem


class GzssSpider(Spider):
    response = requests.get('http://cri.gz.gov.cn/')
    soup = BeautifulSoup(response.content, 'lxml', from_encoding='utf-8')
    count = int(soup.find('div', attrs={'style': 'font-size:xx-large'}).string)
    count1 = 0
    name = 'GZSS'
    start_urls = 'http://cri.gz.gov.cn/Search/Result?page='
    custom_settings = {
        'ITEM_PIPELINES': {
            'SpiderHome.pipelines.GzssPipeline': 300,
        },
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:7.0.1) Gecko/20100101 Firefox/7.7',
        'DEPTH_LIMIT': 1,
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS': 1,
    }

    def start_requests(self):
        count = 1
        while self.count1 <= self.count:
            yield Request(
                self.start_urls + str(count), callback=self.first_parse)
            count = count + 1

    def first_parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        for div in soup.find_all('div', class_='inner-results'):
            if self.count1 > self.count:
                return
            day = div.find('p').string.split('   ')[-2][-10:]
            print(day)
            url = urllib.parse.urljoin('http://cri.gz.gov.cn/',
                                       div.find('a')['href'])
            yield Request(url, callback=self.second_parse)
            self.count1 += 1

    def second_parse(self, response):
        web = BeautifulSoup(response.body, 'lxml')
        item = GzssItem()
        item['Thread'] = response.url.strip().split('=')[1].split('&')[0]
        item['Name'] = web.find(
            'th', text=re.compile('名称')).nextSibling.nextSibling.string.strip()
        if (web.find('th', text=re.compile('法定代表人')) is not None):
            item['LegalRepresentative'] = web.find(
                'th',
                text=re.compile('法定代表人')).nextSibling.nextSibling.text.strip()
        else:
            item['LegalRepresentative'] = 'None'
        item['Code'] = web.find(
            'th',
            text=re.compile('社会信用代码')).nextSibling.nextSibling.text.strip()
        item['MainCategory'] = web.find(
            'th',
            text=re.compile('主营项目类别')).nextSibling.nextSibling.text.strip()
        if (web.find('th', text=re.compile('注册资本')) is not None):
            item['RegisteredCapital'] = web.find(
                'th',
                text=re.compile('注册资本')).nextSibling.nextSibling.text.strip()
        else:
            item['RegisteredCapital'] = 'None'
        if (web.find('th', text=re.compile('负责人')) is not None):
            item['Head'] = web.find(
                'th',
                text=re.compile('负责人')).nextSibling.nextSibling.text.strip()
        else:
            item['Head'] = 'None'
        if (web.find('th', text=re.compile('经营者')) is not None):
            item['Operators'] = web.find(
                'th',
                text=re.compile('经营者')).nextSibling.nextSibling.text.strip()
        else:
            item['Operators'] = 'None'
        item['CommercialBodyType'] = web.find(
            'th',
            text=re.compile('商事主体类型')).nextSibling.nextSibling.text.strip()
        item['EstablishmentDate'] = web.find(
            'th', text=re.compile('成立日期')).nextSibling.nextSibling.text.strip()
        item['OperatingPeriod'] = web.find(
            'th', text=re.compile('营业期限')).nextSibling.nextSibling.text.strip()
        item['IssuanceDate'] = web.find(
            'th', text=re.compile('核发日期')).nextSibling.nextSibling.text.strip()
        item['RegistrationAuthority'] = web.find(
            'th', text=re.compile('登记机关')).nextSibling.nextSibling.text.strip()
        item['State'] = web.find(
            'th', text=re.compile('状态')).nextSibling.nextSibling.text.strip()
        item['Notes'] = web.find(
            'th', text=re.compile('备注')).nextSibling.nextSibling.text.strip()
        item['BusinessScope'] = []
        item['BusinessScope'].append(
            web.find_all(
                'span', class_="color-red")[0].text.strip() + web.find_all(
                    'span', class_="color-red")[0]
            .nextSibling.nextSibling.strip())
        item['LicenseScope'] = []
        item['LicenseScope'].append(
            web.find_all(
                'span', class_="color-red")[1].text.strip() + web.find_all(
                    'span', class_="color-red")[1]
            .nextSibling.nextSibling.strip())
        item['RegistrationNumber'] = web.find(id='RegNo').text
        item['Home'] = web.find(id="OperationSite").text.strip()
        pdf_links = web.find_all(
            'a', href=re.compile(r'/Detail/GetFile\?code=.'))
        item['doc_urls'] = []
        for link in pdf_links:
            pdf_url = urllib.parse.urljoin(r'http://cri.gz.gov.cn/',
                                           link['href'])
            item['doc_urls'].append(pdf_url)
            print('get pdf_url')
        yield item
