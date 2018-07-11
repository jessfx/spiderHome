import datetime
import json
import re

from bs4 import BeautifulSoup
from scrapy import FormRequest, Request
from scrapy.spiders import Spider

from SpiderHome.items import App_gdepbItem


class App_gdepbSpider(Spider):
    name = 'app_gdepb'
    custom_settings = {
        'ITEM_PIPELINES': {
            'SpiderHome.pipelines.AppGDEPBPipeline': 300,
        }
    }
    last_year = 2017
    last_week = 37
    op = 'Select'
    param = '{"queryParam": {"SkipResults": 0, "MaxResults": 0, "FiltByArea": true, "Parameter": {}}, "queryCondi": {"year": %d, "week": %d}}'
    url = 'http://www-app.gdepb.gov.cn/EQPublish/handlers/WaterWeekHandler.ashx'

    def start_requests(self):
        year = 2017
        week = 43
        while year >= self.last_year:
            if year == self.last_year and week < self.last_week:
                break
            formdata = {'op': self.op, 'param': self.param % (year, week)}
            yield FormRequest(self.url, formdata=formdata, callback=self.parse, meta={'year': year, 'week': week})
            week -= 1
            if week == 0:
                week = 52
                year -= 1

    # def start_requests(self):
    #     year = datetime.date.today().isocalendar()[0]
    #     week = datetime.date.today().isocalendar()[1] - 1
    #     formdata = {'op': self.op, 'param': self.param % (year, week)}
    # yield FormRequest(self.url1, formdata=formdata, callback=self.parse,
    # meta={'year': year, 'week': week, 'thread': 'app_week'})

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml', from_encoding='utf-8')
        txt = soup.find('p').get_text().strip()
        txt = re.sub('"FirstDay":new Date\(\d+\),', '', txt)
        json_obj = json.loads(txt)
        datas = json_obj['Data']
        for data in datas:
            item = App_gdepbItem()
            item['EntityId'] = data['EntityId']
            if response.meta['week'] >= 10:
                YearWeek = str(response.meta['year']) + \
                    str(response.meta['week'])
            else:
                YearWeek = str(response.meta['year']) + '0' +\
                    str(response.meta['week'])
            item['YearWeek'] = YearWeek
            item['SectionName'] = data['SectionName']
            item['WeekRange'] = data['WeekRange']
            item['WaterSysName'] = data['WaterSysName']
            item['RiverPartName'] = data['RiverPartName']
            item['OverItem'] = data['OverItem']
            if item['OverItem'] == '':
                item['OverItem'] = None
            item['LevelID'] = data['LevelID']
            if item['LevelID'] == 10 or item['LevelID'] is None:
                continue
            yield item
