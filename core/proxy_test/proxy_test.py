from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy
from settings import MAX_SCROE
from settings import ASYNC_NUM
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import time
import schedule
from queue import Queue

class ProxyTest(object):
    def __init__(self):
        self.mongo_pool = MongoPool()
        self.queue = Queue()
        self.coroutine_pool = Pool()

    #回调函数
    def __check_callback(self, temp):
        self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)

    #队列实现
    def run(self):
        proxies = self.mongo_pool.find_all()
        for proxy in proxies:
            self.queue.put(proxy)
        for i in range(ASYNC_NUM):
            self.coroutine_pool.apply_async(self.__check_one_proxy, callback=self.__check_callback)
        self.queue.task_done()

    def __check_one_proxy(self):
        proxy = self.queue.get()
        proxy = check_proxy(proxy)
        if proxy.delay == -1:
            proxy.score -= 1
            if proxy.score == 0:
                self.mongo_pool.delete_one(proxy)
            else:
                self.mongo_pool.update_one(proxy)
        else:
            proxy.score == MAX_SCROE
            self.mongo_pool.update_one(proxy)
        self.queue.task_done()

    #调用接口，定时任务
    @classmethod
    def start(cls):
        rs = ProxyTest()
        rs.run()
        schedule.every().hours.do(rs.run)
        while True:
            schedule.run_pending()
            time.sleep(30)


if __name__ == '__main__':
    pt = ProxyTest()
    pt.run()
