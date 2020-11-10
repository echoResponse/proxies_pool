#使用httpbin网站检测代理

import requests
import time
import json
from utils import http_headers
import settings
from domain import Proxy
from utils.log import logger

def check_proxy(proxy):
    '''检测协议类型，匿名程度
    ：param
    :return(协议：http和https:2，https：1，http：0；匿名程度：高匿：0，匿名：1，透明：2；延迟)
    '''
    proxies = {
        'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.port),
    }

    http, http_nick_type, http_delay = _check_http_proxy(proxies)
    https, https_nick_type, https_delay = _check_http_proxy(proxies, False)
    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.delay = http_delay
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.delay = http_delay
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.delay = https_delay
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.delay = -1
    logger.debug(proxy)
    return proxy

def _check_http_proxy(proxies, is_http=True):
    nick_type = -1
    delay = -1
    if is_http:
        test_url = 'http://httpbin.org/get'
    else:
        test_url = 'https://httpbin.org/get'
    try:
        start = time.time()
        r = requests.get(url=test_url, headers=http_headers.get_request_header(), timeout=settings.TIMEOUT, proxies=proxies)
        if r.ok:
            delay = round(time.time() - start, 2)
            content = json.loads(r.text)
            headers = content['headers']
            ip = content['origin']
            proxy_connection = headers.get('Proxy-Connection', None)
            if ',' in ip:
                nick_type = 2 #ip中有多个IP则说明透明
            elif proxy_connection:
                nick_type = 1
            else:
                nick_type = 0
            return True, nick_type, delay
        else:
            return False, nick_type, delay
    except Exception as e:
        logger.exception(e)
        return False, nick_type, delay

if __name__ == '__main__':
    proxy = Proxy('36.248.133.204', '9999')
    check_proxy(proxy)
    print(proxy)
