# -*- coding: utf-8 -*-

"""
慕课网spider
"""
import json

import pymongo
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class MoocPipeline(object):
    """
    慕课网数据爬取，保存在本地文件中
    """

    def __init__(self):
        # 打开文件
        self.file = open('data.json', 'w', encoding='utf-8')

    # 处理数据
    def process_item(self, item, spider):
        # 读取item中的数据
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        self.file.write(line)
        return item

    # 该方法在spider被开启时调用
    def open_spider(self, spider):
        pass

    # 该方法在spider被关闭时调用
    def close_spider(self, spider):
        pass


class ImagePipeline(ImagesPipeline):
    # 通过抓取图片的URL获取一个request用于下载
    def get_media_requests(self, item, info):
        # 返回Request图片的url
        yield scrapy.Request(item['image_url'])

    # 当下载请求完成后执行的方法
    def item_completed(self, results, item, info):
        # 获取下载地址
        image_path = [x['path'] for ok, x in results if ok]
        # 判断是否成功
        if not image_path:
            raise DropItem("Item contains no images")
        # 将地址存入 item
        item['image_url'] = image_path
        return item


class MongoDBPipeline(object):
    """
    设置mongodb连接, 把爬取到的item保存到数据库中
    """
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'items'),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.__class__.__name__
        self.db[collection_name].insert(dict(item))
        return item
