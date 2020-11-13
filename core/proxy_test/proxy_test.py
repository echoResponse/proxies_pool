from core.db.mongo_pool import MongoPool
from core.proxy_validate.httpbin_validator import check_proxy
from settings import MAX_SCROE
from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool
import time
import schedule

class ProxyTest(object):
    def __init__(self):
        self.mongo_pool = MongoPool()

    def run(self):
        self.__check_one_proxy()

    def __check_one_proxy(self):
        proxies = self.mongo_pool.find_all()
        for proxy in proxies:
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
