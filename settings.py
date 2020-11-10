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