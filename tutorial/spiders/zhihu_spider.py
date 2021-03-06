import scrapy
from tutorial.items import ZhihuItem


class ZhihuSpider(scrapy.Spider):
    """
    知乎 用户爬虫
    """
    name = 'zhihu'
    start_urls = ['https://www.zhihu.com/people/kaifulee/followers']
    schema = 'https://www.zhihu.com'

    def __init__(self):
        # 要访问的用户集合,初始化时只有一个用户，后续添加
        self.follows = set()

    def parse(self, response):
        item = ZhihuItem()
        # 获取用户名
        name = response.xpath('//h1/span[@class="ProfileHeader-name"]/text()').extract()  # 姓名
        urls = response.xpath('//a[@class="UserLink-link"]/@href').extract()  # 一页取到的链接
        if urls is not None:
            self.follows = self.follows | set(urls)
            print('新爬到的URL：%s' % urls)
            print('集合里保存的url：%s' % self.follows)
        item['name'] = name
        yield item

        # 存在分页
        pagination = response.xpath('//div[@class="Pagination"]')
        if pagination:
            total_page = response.xpath('//div[@class="Pagination"]/button/text()').extract()[-2]  # 最后一页页码
            # 跟进用户分页
            for i in range(0, int(total_page)):
                yield scrapy.Request(response.urljoin('?page=' + str(i)) + '/followers', callback=self.url_parse)

        # 跟进下一个用户
        if self.follows is not None:
            url = self.follows.pop()

            yield scrapy.Request(self.schema + url + '/followers', callback=self.parse)

    # 保存每一页所得到打链接
    def url_parse(self, response):
        urls = response.xpath('//a[@class="UserLink-link"]/@href').extract()  # 一页取到的链接
        # 保存爬到打url
        if urls is not None:
            self.follows = self.follows | set(urls)
            print('新爬到的URL：%s' % urls)
            print('集合里保存的url：%s' % self.follows)
