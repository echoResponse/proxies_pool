import importlib #动态导入类名
from core.proxy_validate.httpbin_validator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger
#打猴子补丁，进行异步操作，提升爬取效率
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
#定时器，用于定时执行爬虫
import schedule
import time
from settings import RUN_SPIDER_INTERVAL

class RunSpider(object):

    spider_list = [
        'kuaiSpider', 'jiangxianSpider', 'xilaSpider',
        'xiaohuanSpider', 'zhimaSpider', 'nimaSpider', 'qiyunSpider', 'spider89',
    ]
    module_name = 'core.proxy_spider.proxy_spiders'

    def __init__(self, module_name='', spider_list=[]):
        if module_name:
            self.module_name = module_name
        if spider_list:
            self.spider_list = spider_list
        self.mongo_pool = MongoPool()
        #创建协程池
        self.coroutine_pool = Pool()

    def get_spider_cls(self, spider_list, module_name):
        module = importlib.import_module(module_name)
        for spider_name in spider_list:
            spider_cls = getattr(module, spider_name)
            yield spider_cls

    def run_spider(self):
        for spider in self.get_spider_cls(self.spider_list, self.module_name):
            #self.__execute_one_spider_task(spider)
            self.coroutine_pool.apply_async(self.__execute_one_spider_task,args=(spider,))
        self.coroutine_pool.join()

    def __execute_one_spider_task(self, spider):
        try:
            for proxy in spider.get_proxies():
                proxy = check_proxy(proxy)
                if proxy.delay != -1:
                    self.mongo_pool.insert_one(proxy)
                    print("新代理插入成功"+dict(proxy))
        except Exception as ex:
            logger.exception(ex)

    @classmethod
    def start(cls):
        rs = RunSpider()
        rs.run_spider()
        schedule.every(RUN_SPIDER_INTERVAL).hours.do(rs.run_spider)
        while True:
            schedule.run_pending()
            time.sleep(30)

if __name__ == '__main__':
    RunSpider.start()
# class RunSpider(object):
# for i in kuaiSpider.get_proxies():
#     print(i)
#     # def run_spider(self):
