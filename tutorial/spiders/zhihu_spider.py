import scrapy
from tutorial.items import ZhihuItem


class ZhihuSpider(scrapy.Spider):

    """
    知乎 用户爬虫
    """

    name = 'zhihu'
    start_urls = ['https://www.zhihu.com/people/huan-pu-8/followers']

    schema = 'https://www.zhihu.com'

    def __init__(self):
        self.follows = set({'/huan-pu-8/followers'})
        self.current_end_page = 1

    def parse(self, response):
        # 获取用户名
        name = response.xpath('//h1/span[@class="ProfileHeader-name"]/text()').extract()  # 姓名

        print(name)

        # 获取该用户关注分页
        self.current_end_page = response.xpath('//div[@class="Pagination"]/button/text()').extract()[-2]  # 最后一页页码

        # 访问该用户所有的 关注分页
        for i in range(0, int(self.current_end_page)):
            yield scrapy.Request(response.urljoin('?page=' + str(i)), callback=self.url_parse)

        if self.follows is not None:
            url = self.follows.pop()
            yield scrapy.Request(response.urljoin(url), callback=self.parse)

    # 保存每一页所得到打链接
    def url_parse(self, response):
        urls = response.xpath('//a[@class="UserLink-link"]/@href').extract()  # 一页取到的链接
        print(urls)
        # 保存爬到打url
        if urls is not None:
            self.follows = self.follows | set(urls)




