# -*- coding: utf-8 -*-
import multiprocessing
import os

import parse_type
import pymysql
import requests

from SpiderHome.store import GDSWDB, GZSSDB, GdsqDB, CSGHDB1, CSGHDB2, GDEPBDB, GdszDB


class GdsqPipeline(object):
    def process_item(self, item, spider):
        spec = {'station': item['station'], 'time': item['time']}
        GdsqDB.djriver.update(spec, {'$set': dict(item)}, upsert=True)
        return None


class GdwaterPipeline(object):
    def process_item(self, item, spider):
        spec = {
            'city': item['city'],
            'county': item['county'],
            'site': item['site'],
            'time': item['time']
        }
        thread = item.get('thread', None)
        item.pop('thread')
        GdsqDB[thread].update(spec, {'$set': dict(item)}, upsert=True)
        return None


class GdswPipeline(object):
    def process_item(self, item, spider):
        spec = {'tm': item['tm'], 'stcd': item['stcd'], 'stnm': item['stnm']}
        print(item['tm'])
        thread = item.get('thread', None)
        item.pop('thread')
        GDSWDB[thread].update(spec, {'$set': dict(item)}, upsert=True)
        return item


class fjwPipeline(object):
    def process_item(self, item, spider):
        # 数据库的配置信息
        conn = pymysql.Connect(
            host='127.0.0.1',  # 主机ip
            port=3306,  # 端口
            user='root',  # 用户名
            passwd='',  # 密码
            db='gdfj',  # 数据库名字
            charset='utf8')
        cursor = conn.cursor()  # get the cursor
        cursor.execute(
            "INSERT INTO fjw (url,city,title,region,district_name,\
                house_desc,house_infor,contact,phone_number,update_time) \
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
            (item['url'], item['city'], item['title'], item['region'],
             item['district_name'], item['house_desc'], item['house_infor'],
             item['contact'], item['phone_number'], item['update_time']))
        conn.commit()
        cursor.close()
        conn.close()
        return

    '''
        item['url']
        item['city']
        item['title']
        item['region']
        item['district_name']
        item['house_desc']
        item['house_infor']
        item['contact']
        item['phone_number']
        item['update_time']
    '''


class GzssPipeline(object):
    def process_item(self, item, spider):
        spec = {"Thread": item["Thread"]}
        GZSSDB.Gzss.update(spec, {'$set': dict(item)}, upsert=True)
        if len(item['doc_urls']) != 0:
            downloader = multiprocessing.Process(
                target=self.downloader, args=(item, ))
            downloader.start()
        return None

    def downloader(self, item):
        count = 0
        path = u'E:\\gzss\\' + item['Name'] + item['EstablishmentDate']
        for url in item['doc_urls']:
            try:
                r = requests.get(url)
            except:
                pass
            if r.status_code == 200:
                if not os.path.exists(path):
                    os.makedirs(path)
                try:
                    name = item['Thread'] + '(' + str(count) + ').'
                    dest = os.path.join(path, name)
                    docm = open(dest, "wb")
                    docm.write(r.content)
                    docm.close()
                    new_name = name + parse_type.filetype(dest)
                    new_dest = os.path.join(path, new_name)
                    os.rename(dest, new_dest)
                except:
                    continue
                count += 1
            else:
                pass
        item['doc_path'] = path
        spec = {"Thread": item['Thread']}
        GZSSDB.Gzss.update(spec, {'$set': dict(item)}, upsert=True)


class CSGXPipeline(object):
    def process_item(self, item, spider):
        if item.get('Jurisdiction') is not None:
            spec = {}
            CSGHDB1[item['Thead']].update(spec, {'$set': item}, upsert=True)
        else:
            spec = {}
            CSGHDB2[item['Thead']].update(spec, {'$set': item}, upsert=True)


class GDEPBPipeline(object):
    def process_item(self, item, spider):
        thread = item['thread']
        item.pop('thread')
        spec = {'title': item['title']}
        GDEPBDB[thread].update(spec, {'$set': item}, upsert=True)
        return None


class AppGDEPBPipeline(object):
    def process_item(self, item, spider):
        spec = item
        GdszDB.app_week.update(spec, {'$set': dict(item)}, upsert=True)
