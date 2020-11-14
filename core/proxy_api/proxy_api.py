# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
import json

from core.db.mongo_pool import MongoPool
from settings import API_COUNT
class ProxyApi(object):
    def __init__(self):
        self.app = Flask(__name__)
        self.mongo_pool = MongoPool()
        @self.app.route('/random')
        def random():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxy = self.mongo_pool.random_proxy(protocol, domain, count=API_COUNT)
            print(proxy)
            if protocol:
                return '{}://{}:{}'.format(protocol, proxy.ip, proxy.port)
            else:
                return '{}:{}'.format(proxy.ip, proxy.port)

        @self.app.route('/all')
        def all():
            protocol = request.args.get('protocol')
            domain = request.args.get('domain')
            proxies = self.mongo_pool.get_proxies(protocol, domain, count=API_COUNT)
            proxies = [proxy.__dict__ for proxy in proxies]
            return json.dumps(proxies)

        @self.app.route('/disable_domain')
        def disable_domain():
            ip = request.args.get('ip')
            domain = request.args.get('domain')
            if ip is None:
                return "请提供ip参数"
            if domain is None:
                return "请传入域名"
            self.mongo_pool.disable_domain(ip, domain)
            return "{} 禁用域名{} 成功".format(ip, domain)

    def run(self):
        self.app.run('0.0.0.0', port=80)

    @classmethod
    def start(cls):
        #统一启动方式
        proxy_api = ProxyApi()
        proxy_api.run()

if __name__ == '__main__':
    ProxyApi.start()