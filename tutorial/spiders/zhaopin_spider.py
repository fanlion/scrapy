import scrapy
from tutorial.items import ZhaoPinItem
import json
from scrapy import FormRequest


class ZhaoPinSpider(scrapy.Spider):
    """
    百度招聘爬虫
    """
    name = 'zhaopin'

    def parse(self, response):
        pass

    def start_requests(self):
        url = "http://zhaopin.baidu.com/api/quanzhiasync"
        requests = []
        for i in range(1, 3):
            form_data = {
                "query": "射频工程师",
                "sort_type": "1",
                "detailmode": "close",
                "rn": "20",
                "city": "上海",
                "pn": str(i * 20)
            }
            request = FormRequest(url, callback=self.parse_json, formdata=form_data)
            requests.append(request)
        return requests

    def parse_json(self, response):
        json_body = json.loads(response.body.decode('utf-8'))
        # 获取工作列表
        jobs = json_body['data']['main']['data']['disp_data']

        if jobs is not None:
            for job in jobs:
                item = ZhaoPinItem()
                item['end_date'] = job['enddate']
                item['title_jd'] = job['title_jd']
                item['common_name'] = job['commonname']
                item['experience'] = job['experience']
                item['salary'] = job['salary']
                item['location'] = job['location']
                item['ori_experience'] = job['ori_experience']
                item['district'] = job['district']
                item['ori_district'] = job['ori_district']
                item['domain'] = job['domain']
                item['title'] = job['title']
                item['province'] = job['province']
                item['start_date'] = job['startdate']
                item['source'] = job['source']
                item['description'] = job['description']
                item['type'] = job['type']
                item['n_official_name'] = job['n_officialname']
                item['company_description'] = job['companydescription']
                item['industry'] = job['industry']
                item['company_address'] = job['companyaddress']
                yield item
