from os import makedirs
from threading import Thread
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from scrapy import Request
from scrapy.spiders import Spider

from SpiderHome.items import CSGXItem1, CSGXItem2


class ExampleSpider(Spider):
    name = 'CSGX'
    custom_settings = {
        'ITEM_PIPELINES': {
            'SpiderHome.pipelines.CSGXPipeline': 300,
        }
    }

    def start_requests(self):
        index = ['index', 'index_1', 'index_2']
        for i in range(3):
            url = 'http://www.szpl.gov.cn/xxgk/csgx/csgxjh/' + \
                index[i] + '.html'
            yield Request(url, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        tds = soup.find_all('td', attrs={'name': 'ColumnContent'})
        for td in tds:
            url = urljoin(response.url, td.find('a')['href'])
            yield Request(url, callback=self.parse1)

    def parse1(self, response):
        soup = BeautifulSoup(response.body, 'lxml')
        item1 = CSGXItem1()
        item2 = CSGXItem2()
        item1['Thead'] = item2['Thead'] = response.url.split('/')[-1][:-5]
        Title = soup.find('td', class_='titleorange03').get_text()
        if Title[-2:] != u'公告':
            return
        item2['Title'] = Title
        try:
            item2['Date'] = soup.find('div', class_='Custom_UnionStyle').find_all('p')[
                2].get_text().strip()
        except:
            return
        table = soup.find('table', class_='MsoNormalTable')
        if table is None:
            table = soup.find('div', class_='uion').find('table')
        trs = table.find_all('tr')
        item2['Notes'] = trs[-1].get_text()
        trs.pop()
        trs.reverse()
        trs.pop()
        for tr in trs:
            item1['Jurisdiction'] = tr.find_all('td')[1].get_text()
            item1['Street'] = tr.find_all('td')[2].get_text()
            item1['Cellname'] = tr.find_all('td')[3].get_text()
            item1['DeclarationBody'] = tr.find_all('td')[4].get_text()
            item1['ReconstructedArea'] = tr.find_all('td')[5].get_text()
            item1['Notes'] = tr.find_all('td')[6].get_text()
        yield item1
        div = soup.find('div', id='subFile')
        if div is None:
            div = soup.find('p', attrs={'target': '_blank'})
        ass = div.find_all('a')
        if len(ass) == 0:
            return
        makedirs('D:\\csgx\\' + Title)
        files = []
        for a in ass:
            file = {}
            if a['href'][:4] == 'href':
                href = a['href']
            else:
                href = urljoin(
                    response.url, a['href'])
            file['Name'] = a['href'].split('/')[-1]
            path = 'D:\\csgx\\' + Title + \
                '\\' + file['Name']
            file['Path'] = path
            files.append(file)
            thread = Thread(target=self.downloader, args=(href, path))
            thread.start()
        item2['Files'] = files
        yield item2

    def downloader(self, href, path):
        request = requests.get(href)
        fp = open(path, 'wb')
        if fp.writable():
            fp.write(request.content)
            fp.close()
            print(path)
