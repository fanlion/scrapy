# -*- coding: utf-8 -*-

import scrapy


class CourseItem(scrapy.Item):
    """
    慕课网 课程实体
    """
    title = scrapy.Field()  # 标题
    category = scrapy.Field()  # 分类
    type = scrapy.Field()  # 等级
    url = scrapy.Field()  # 链接
    image_url = scrapy.Field()  # 图片链接
    introduction = scrapy.Field()  # 介绍
    student = scrapy.Field()  # 学习人数


class BookItem(scrapy.Item):
    """
    豆瓣网 书籍实体
    """
    title = scrapy.Field()  # 标题
    source = scrapy.Field()  # 来源
    author = scrapy.Field()  # 作者
    publisher = scrapy.Field()  # 出版社
    rating = scrapy.Field()  # 评分
    url = scrapy.Field()  # 图书url
    img = scrapy.Field()  # 图片url
    pub_date = scrapy.Field()  # 出版日期
    comment_count = scrapy.Field()  # 评论数量
