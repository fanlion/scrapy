import scrapy
from scrapy_redis.spiders import RedisSpider

from tutorial.items import CourseItem


class MoocRedisSpider(RedisSpider):
    name = 'MoocRedisSpider'
    redis_key = 'mooc:urls'

    start_urls = ["http://www.imooc.com/course/list"]

    def parse(self, response):
        item = CourseItem()
        for box in response.xpath(
                '//ul[@class="clearfix"]/div[@class="index-card-container course-card-container container "]'):
            item['category'] = box.xpath('.//span/text()').extract_first()
            item['title'] = box.xpath('.//h3/text()').extract_first()
            item['introduction'] = box.xpath('.//p/text()').extract_first()
            item['type'] = box.xpath('.//div[@class="course-card-info"]/text()').extract()[0].strip()
            item['student'] = box.xpath('.//div[@class="course-card-info"]/text()').extract()[1].strip()[:-3]
            item['url'] = 'http:www.imooc.com' + box.xpath('.//@href').extract_first()
            item['image_url'] = box.xpath('.//img/@src')[1].extract()
            yield item

        # url跟进
        url = response.xpath("//a[contains(text(),'下一页')]/@href").extract_first()
        if url is not None:
            next_page = response.urljoin(url)
            yield scrapy.Request(next_page, callback=self.parse)
