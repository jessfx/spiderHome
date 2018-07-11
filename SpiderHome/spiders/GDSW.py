import json
from datetime import datetime

from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import Spider

from SpiderHome.items import GdswItem

# 监测站点数据爬虫1


class GdswSpider(Spider):
    name = 'GDSW'
    start_urls = [
        'http://www.gdsw.gov.cn/live/CACHE/RTDATA/ZZ/SSWZ.js',
        'http://www.gdsw.gov.cn/live/CACHE/RTDATA/RR/large_reservoir.js',
        'http://www.gdsw.gov.cn/live/CACHE/RTDATA/RR/middle_reservoir.js'
    ]
    custom_settings = {
        'ITEM_PIPELINES': {
            'SpiderHome.pipelines.GdswPipeline': 300,
        }
    }

    def start_requests(self):
        yield Request(self.start_urls[0], callback=self.parse)
        yield Request(self.start_urls[1], callback=self.parse1)
        yield Request(self.start_urls[2], callback=self.parse1)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'html.parser', from_encoding='gbk')
        text = str(soup).split('\n')[0].split('=')[-1].strip()
        r = open(
            'D:\workspace\scrapy spider\SpiderHome\SpiderHome\spiders\data.json',
            'w')
        r.write(text)
        r.close()
        jsonobj = json.load(
            open('D:\workspace\scrapy spider\SpiderHome\SpiderHome\spiders\data.json', 'r'))
        for obj in jsonobj:
            item = GdswItem()
            item['thread'] = 'river'
            item['tm'] = obj.get('tm', None)
            if item['tm'] > datetime.today().strftime("%Y-%m-%d %H:%M"):
                continue
            item['stnm'] = obj.get('stnm', None)
            item['stcd'] = obj.get('stcd', None)
            item['hnnm'] = obj.get('hnnm', None)
            if obj['tend'] == '4':
                item['tend'] = '落'
            elif obj['tend'] == '5':
                item['tend'] = '涨'
            elif obj['tend'] == '6':
                item['tend'] = '平'
            else:
                item['tend'] = None
            item['rvnm'] = obj.get('rvnm', None)
            item['z'] = obj.get('z', None)
            item['q'] = obj.get('q', None)
            yield item

    def parse1(self, response):
        soup = BeautifulSoup(response.body, 'html.parser', from_encoding='gbk')
        text = str(soup).split('\n')[0].split('=')[-1].strip()
        r = open(
            'D:\workspace\scrapy spider\SpiderHome\SpiderHome\spiders\data1.json',
            'w')
        r.write(text)
        r.close()
        jsonobj = json.load(
            open(
                'D:\workspace\scrapy spider\SpiderHome\SpiderHome\spiders\data1.json',
                'r'))
        for obj in jsonobj:
            item = GdswItem()
            item['thread'] = 'reservoir'
            item['tm'] = obj.get('tm', None)
            if item['tm'] > datetime.today().strftime("%Y-%m-%d %H:%M"):
                continue
            item['stnm'] = obj.get('stnm', None)
            item['stcd'] = obj.get('stcd', None)
            item['hnnm'] = obj.get('hnnm', None)
            if obj['tend'] == '4':
                item['tend'] = '落'
            elif obj['tend'] == '5':
                item['tend'] = '涨'
            elif obj['tend'] == '6':
                item['tend'] = '平'
            else:
                item['tend'] = None
            item['rvnm'] = obj.get('rvnm', None)
            item['z'] = obj.get('z', None)
            item['q'] = obj.get('q', None)
            yield item
