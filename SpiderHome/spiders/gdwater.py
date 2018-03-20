# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from re import findall, sub
from time import sleep

from bs4 import BeautifulSoup as BS
from scrapy import Request
from scrapy.http import FormRequest
from scrapy.spiders import Spider

from SpiderHome.items import GdwaterItem


class GdwaterSpider(Spider):
    name = 'gdwater'
    custom_settings = {
        'ITEM_PIPELINES': {
            'SpiderHome.pipelines.GdwaterPipeline': 300,
        },
    }
    count = 0
    day1 = datetime(2017, 10, 25, 0, 0)
    day2 = datetime(2017, 7, 1, 0, 0)
    form = {
        '__EVENTVALIDATION': '',
        '__VIEWSTATE': '',
        'btn_query': '查询',
        'ddl_addvcd': '',
        'hidsearch': '',  # 81000880，81000755
        'txt_search': '飞来峡',
        'txt_time1': (day1 - timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
        'txt_time2': day1.strftime("%Y-%m-%d %H:%M")
    }
    url = 'http://www.gdwater.gov.cn:9001/Report/WaterReport.aspx'

    def start_requests(self):
        yield Request(self.url, callback=self.parse)

    def parse(self, response):
        soup = BS(response.body, 'lxml', from_encoding='utf-8')
        self.form['__EVENTVALIDATION'] = soup.find(
            'input', id='__EVENTVALIDATION')['value']
        self.form['__VIEWSTATE'] = soup.find(
            'input', id='__VIEWSTATE')['value']
        while self.day1 > self.day2:
            self.form['txt_time2'] = self.day1.strftime("%Y-%m-%d %H:%M")
            #print(self.day1.strftime("%Y-%m-%d %H:%M"))
            self.day1 = self.day1 - timedelta(hours=1)
            self.form['txt_time1'] = self.day1.strftime("%Y-%m-%d %H:%M")
            yield FormRequest(
                url=self.url, formdata=self.form, callback=self.second_parse, meta={'txt_time2': self.form['txt_time2']})

    def second_parse(self, response):
        print('in')
        soup = BS(response.body, 'lxml')
        div = soup.find('div', id='LeftTree')
        tbody1 = div.find('tbody')
        trs = tbody1.find_all('tr')
        self.count += 1
        trs.reverse()
        trs.pop()
        for tr in trs:
            tds = tr.find_all('td')
            item = GdwaterItem()
            item['thread'] = 'river'
            item['city'] = tds[0].get_text().strip()
            item['county'] = tds[1].get_text().strip()
            item['site'] = tds[2].get_text().strip()
            item['time'] = tds[3].get_text().strip()
            try:
                item['water_level'] = float(tds[4].get_text().strip())
            except:
                item['water_level'] = None
            item['warning_level'] = tds[5].get_text().strip()
            item['water_potemtial'] = tds[6].get_text().strip()
            print(response.meta['txt_time2'])
            print(self.count)
            yield item
        div = soup.find('div', id='RightTree')
        trs = div.find_all('tr')
        trs.reverse()
        trs.pop()
        trs.pop()
        for tr in trs:
            tds = tr.find_all('td')
            item = GdwaterItem()
            item['thread'] = 'Reservoir'
            item['city'] = tds[0].get_text().strip()
            item['county'] = tds[1].get_text().strip()
            item['site'] = tds[2].get_text().strip()
            item['time'] = tds[3].get_text().strip()
            item['water_level'] = float(tds[4].get_text().strip())
            try:
                item['flood_limit_water_level'] = float(
                    tds[5].get_text().strip())
            except:
                item['flood_limit_water_level'] = None
            print(response.meta['txt_time2'])
            print(self.count)
            yield item
