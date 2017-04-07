
import scrapy
from tutorial.items import BookItem


class DbbookSpider(scrapy.Spider):

    name = "dbbook"
    start_urls = (
        'https://www.douban.com/doulist/1264675/',
    )

    def parse(self, response):
        selector = scrapy.Selector(response)
        item = BookItem()
        books = selector.xpath('//div[@class="doulist-item"]')
        for book in books:
            source = book.xpath('.//div[@class="source"]/text()').extract()  # 来源
            item['source'] = ''.join(source).replace('\n', '').replace(' ', '')

            title = book.xpath('.//div[@class="title"]/a/text()').extract_first()   # 标题
            item['title'] = ''.join(title).replace('\n', '').replace(' ', '')

            item['url'] = book.xpath('.//div[@class="title"]/a/@href').extract_first()  # url

            item['img'] = book.xpath('.//div[@class="post"]/a/img/@src').extract_first()  # 图片url

            item['rating'] = book.xpath('.//div[@class="rating"]/span[@class="rating_nums"]/text()').extract_first()  # 评分
            comment_count = book.xpath('.//div[@class="rating"]/span[3]/text()').extract()[0]
            item['comment_count'] = comment_count[1:-4]

            desc = book.xpath('.//div[@class="abstract"]/text()').extract()

            if len(desc) == 3:
                author = desc[0]   # 作者
                item['author'] = author.replace('\n', '').replace(' ', '')[3:]

                publisher = desc[1]  # 出版商
                item['publisher'] = publisher.replace('\n', '').replace(' ', '')[4:]

                pub_date = desc[2]  # 出版日期
                item['pub_date'] = pub_date.replace('\n', '').replace(' ', '')[4:]
            else:
                publisher = desc[0]  # 出版商
                item['publisher'] = publisher.replace('\n', '').replace(' ', '')[4:]

                pub_date = desc[1]  # 出版日期
                item['pub_date'] = pub_date.replace('\n', '').replace(' ', '')[4:]

            yield item

        next_page = response.xpath('//div[@class="paginator"]/span[@class="next"]/a/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)


