import requests
from lxml import etree

from utils.http_headers import get_request_header
from domain import Proxy
from utils.log import logger

class BaseSpider(object):
    urls = []
    group_xpath = ''
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath='', detail_xpath={}):
        if urls:
            self.urls = urls
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath


    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_request_header())
        return response.content.decode()

    def get_proxies_from_page(self, page):
        element = etree.HTML(page)
        #包含代理信息标签列表
        trs = element.xpath(self.group_xpath)
        #遍历trl,获取代理具体信息
        for tr in trs:
            ip = tr.xpath(self.detail_xpath['ip'])[0].strip()
            port = tr.xpath(self.detail_xpath['port'])[0].strip()
            try:
                area = tr.xpath(self.detail_xpath['area'])[0].strip()
            except Exception as ex:
                #logger.debug(ex)
                area = None
            proxy = Proxy(ip, port, area=area)
            #生成器
            yield proxy

    def get_proxies(self):
        #对外提供获取代理方法
        try:
            for url in self.urls:
                page = self.get_page_from_url(url)
                proxies = self.get_proxies_from_page(page)
                yield from proxies
        except Exception as ex:
            print(ex)
            logger.debug(ex)

# if __name__ == '__main__':
#     config = {
#         'urls':[
#             'https://www.kuaidaili.com/free/inha/{}/'.format(i) for i in range(1,101)
#         ],
#         'group_xpath': '//*[@id="list"]/table/tbody/tr',
#         'detail_xpath':{
#             'ip': './td[1]/text()',
#             'port': './td[2]/text()',
#             'area': './td[5]/text()',
#         },
#     }
#     spider = BaseSpider(**config)
#     for i in spider.get_proxies():
#         print(i)