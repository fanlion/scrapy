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


class ZhihuItem(scrapy.Item):
    """
    知乎 用户
    """
    name = scrapy.Field()  # 姓名
    # follower = scrapy.Field()  # 关注他的人


class ZhaoPinItem(scrapy.Item):
    """
    百度招聘 工作
    """
    end_date = scrapy.Field()  # 截止日期
    title_jd = scrapy.Field()  # 岗位名称
    common_name = scrapy.Field()
    experience = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()
    ori_experience = scrapy.Field()
    district = scrapy.Field()
    ori_district = scrapy.Field()
    domain = scrapy.Field()
    title = scrapy.Field()
    province = scrapy.Field()
    start_date = scrapy.Field()
    source = scrapy.Field()  # 信息来源
    description = scrapy.Field()  # 职位描述
    type = scrapy.Field()  # 职位类型
    n_official_name = scrapy.Field()  # 公司名称
    company_description = scrapy.Field()  # 公司描述
    industry = scrapy.Field()  # 行业
    company_address = scrapy.Field()  # 公司地址
