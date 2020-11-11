from core.proxy_spider.base_spider import BaseSpider
from lxml import etree
import requests
import json

from utils.http_headers import get_request_header
from utils.log import logger
from domain import Proxy
#快代理 https://www.kuaidaili.com/free/
kuai_config = {
    'urls': [ "https://www.kuaidaili.com/free/inha/{}/".format(i) for i in range(1,202) ],
    'group_xpath': '//*[@id="list"]/table/tbody/tr',
    'detail_xpath': {
            'ip': './td[1]/text()',
            'port': './td[2]/text()',
            'area': './td[5]/text()',
    },
}

#jiangxianli代理 https://ip.jiangxianli.com/
jiangxian_config = {
    'urls': [ "https://ip.jiangxianli.com/?page={}".format(i) for i in range(1, 4) ],
    'group_xpath': '//html/body/div[1]/div[2]/div[1]/div[1]/table/tbody/tr',
    'detail_xpath': {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }
}

#齐云代理 https://www.7yip.cn/free/?action=china&page=1
# //*[@id="content"]/section/div[2]/table/tbody/tr[1]
qiyun_config = {
    'urls': [ 'https://www.7yip.cn/free/?action=china&page={}'.format(i) for i in range(1, 41) ],
    'group_xpath': '//*[@id="content"]/section/div[2]/table/tbody/tr',
    'detail_xpath': {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }
}

#89代理 https://www.89ip.cn/index_1.html
#此代理浏览器显示xpath与实际获取不符，通过JavaScript修改
config_89 = {
    'urls': ['https://www.89ip.cn/index_{}.html'.format(i) for i in range(1, 100)],
    'group_xpath': '//tbody/tr',
    'detail_xpath': {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }
}


#小幻代理 https://ip.ihuan.me/address/5Lit5Zu9.html?page=1
xiaohuan_config = {
    'urls': ['https://ip.ihuan.me/address/5Lit5Zu9.html?page={}'.format(i) for i in range(1, 41)],
    'group_xpath': '//tbody/tr',
    'detail_xpath': {
        'ip': './td[1]/a/text()',
        'port': './td[2]/text()',
        'area': './td[3]/a[2]/text()',
    }
}

#西拉代理 格式特殊 单独处理 http://www.xiladaili.com/gaoni/1/
class xilalaSpider(object):
    urls = [ "http://www.xiladaili.com/gaoni/{}/".format(i) for i in range(1, 201) ]
    group_xpath = '//html/body/div/div[3]/div[2]/table/tbody/tr'
    detail_xpath = {
        'ip_and_port':'./td[1]/text()',
        'area':'./td[4]/text()',
    }

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
        trs = element.xpath(self.group_xpath)
        for tr in trs:
            ip_and_port = tr.xpath(self.detail_xpath['ip_and_port'])[0]
            ip_and_port = str(ip_and_port)
            ip = ip_and_port.split(':')[0]
            port = ip_and_port.split(':')[1]
            try:
                area = tr.xpath(self.detail_xpath['area'])[0]
            except Exception as ex:
                # logger.debug(ex)
                area = None
            proxy = Proxy(ip, port, area=area)
            yield proxy

    def get_proxies(self):
        #对外提供获取代理方法
        try:
            for url in self.urls:
                print(url)
                page = self.get_page_from_url(url)
                proxies = self.get_proxies_from_page(page)
                yield from proxies
        except Exception as ex:
            logger.debug(ex)

#尼玛 代理 与西拉代理格式相同 http://www.nimadaili.com/putong/1/
class nimamaSpider(xilalaSpider):
    urls = ["http://www.nimadaili.com/putong/{}/".format(i) for i in range(1, 41)]
    group_xpath = '//html/body/div/div[1]/div/table/tbody/tr'
    detail_xpath = {
        'ip_and_port': './td[1]/text()',
        'area': './td[4]/text()',
    }

# 芝麻代理 通过post方式获取代理
class zhimamaSpider(object):
    url = 'http://wapi.http.cnapi.cc/index/index/get_free_ip'
    group_xpath = '//table/tr[position()>1]'
    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }

    def __init__(self, url='', group_xpath='', detail_xpath={}):
        if url:
            self.url = url
        if group_xpath:
            self.group_xpath = group_xpath
        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_data(self, data):
        response = requests.post(self.url, data=data, headers=get_request_header())
        content = response.content.decode()
        dict = json.loads(content)
        data = dict['ret_data']['html']
        html = etree.HTML(data)
        trs = html.xpath(self.group_xpath)
        for tr in trs:
            ip = tr.xpath(self.detail_xpath['ip'])[0]
            port = tr.xpath(self.detail_xpath['port'])[0]
            area = tr.xpath(self.detail_xpath['area'])[0]
            proxy = Proxy(ip, port, area=area)
            yield proxy

    def get_proxies(self):
        try:
            for num in range(1, 41):
                data = {'page': num}
                proxies = self.get_data(data)
                yield from proxies
        except Exception as ex:
            logger.debug(ex)

kuaiSpider = BaseSpider(**kuai_config)
jiangxianSpider = BaseSpider(**jiangxian_config)
xilaSpider = xilalaSpider()
zhimaSpider = zhimamaSpider()
nimaSpider = nimamaSpider()
qiyunSpider = BaseSpider(**qiyun_config)
spider89 = BaseSpider(**config_89)
xiaohuanSpider = BaseSpider(**xiaohuan_config)

if __name__ == '__main__':
    for i in spider89.get_proxies():
        print(i)
