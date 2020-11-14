from pymongo import MongoClient
import pymongo
import random

from utils.log import logger
from settings import MONGO_URL
from domain import Proxy
'''
建立数据库，存储Proxy信息
实现功能：增加，修改，删除，查询
'''
class MongoPool():

    #建立数据库连接
    def __init__(self):
        self.client = MongoClient(MONGO_URL)
        self.proxies = self.client['proxies_pool']['proxies']

    #关闭数据库连接
    def __del__(self):
        self.client.close()

    def insert_one(self, proxy):
        #增加功能
        # 使用IP作为主键
        is_exist = self.proxies.count_documents({'_id': proxy.ip})
        if is_exist == 0:
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info("新代理插入成功{}".format(proxy))
        else:
            logger.warning("代理已经存在{}".format(proxy))

    def update_one(self, proxy):
        '''修改功能'''
        self.proxies.update_one({'_id': proxy.ip}, {'$set':proxy.__dict__})

    def delete_one(self, proxy):
        '''删除功能'''
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info("删除代理IP：{}".format(proxy))

    def find_all(self):
        '''查询所有proxy'''
        cursor = self.proxies.find()
        for item in cursor:
            item.pop('_id') #删除_id键
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions={}, count=0):
        '''
            实现查询功能：
            根据条件查询，分数降序，延迟升序

            参数说明：
            conditions：查询条件字典
            count：限制取出IP数量
        '''
        cursor = self.proxies.find(conditions, limit=count).sort([
            ('score', pymongo.DESCENDING), ('delay', pymongo.ASCENDING)
        ])
        proxy_list = []
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxies(self, protocol=None, domain=None, count=0, nick_type=0):
        '''
        根据协议和访问网站域名，获取代理IP列表
        参数说明：
        protocol：协议类型，默认http&https
        domain：所访问的域名,默认无
        count：获取数量，默认所有
        nick_type：匿名类型，默认高匿
        '''
        conditions = {'nick_type': nick_type}
        if protocol is None:
            conditions['protocol'] = {'$in': [0, 1, 2]}
        elif protocol.lower() == 'http':
            conditions['protocol'] = {'$in': [0, 2]}
        else:
            conditions['protocol'] = {'$in': [1, 2]}

        if domain:
            #由于数据库中disable_domain表示无法访问的domain，
            # 所以这里disable_domain不能包含要访问的domain
            conditions['disable_domain'] = {'$nin': [domain]}
        return self.find(conditions, count=count)

    def random_proxy(self, protocol=None, domain=None, count=0, nick_type=0):
        '''
        根据协议和访问网站域名，随机获取
        参数说明：
        protocol：协议类型，默认http&https
        domain：所访问的域名,默认无
        count：获取数量，默认所有
        nick_type：匿名类型，默认高匿
        '''
        proxy_list = self.get_proxies(protocol=protocol,domain=domain, count=count, nick_type=nick_type)
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
        '''
        功能说明：
        把指定domain加入disable_domain中
        返回值，true代表添加成功，false代表失败
        '''
        if self.proxies.count_documents({'_id':ip, 'disable_domains':domain}) == 0:
            self.proxies.update_one({'_id':ip}, {'$push': {'disable_domains':domain}})
            return True
        return False


if __name__ == '__main__':
    mongo = MongoPool()
    for mongod in mongo.get_proxies():
        print(mongod)
    mongo.__del__()