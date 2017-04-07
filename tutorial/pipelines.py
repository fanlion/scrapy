# -*- coding: utf-8 -*-
import json

import pymongo
import scrapy
from scrapy.exceptions import DropItem

from scrapy.pipelines.images import ImagesPipeline


class MoocPipeline(object):
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
    def __init__(self):
        host = 'localhost'
        port = 27017
        db_name = 'douban'
        client = pymongo.MongoClient(host=host, port=port)
        tdb = client[db_name]
        self.post = tdb['books']

    def process_item(self, item, spider):
        course = dict(item)
        self.post.insert(course)
        return item
