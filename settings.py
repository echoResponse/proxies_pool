import logging

#代理最大分数值
MAX_SCROE = 10 #默认分数

#日志信息配置
LOG_LEVEL = logging.DEBUG
LOG_FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s: %(message)s'
LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'
LOG_FILENAME = 'log.log'

#检测httpbin timeout时间
TIMEOUT = 10

#MongoDB数据库URL
MONGO_URL = 'mongodb://127.0.0.1:27017'

#爬虫运行时间间隔,单位为小时
RUN_SPIDER_INTERVAL = 2

#从数据库崎岖检测时间,单位为小时
CHECK_TIME = 1

#指定异步数量
ASYNC_NUM = 10