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