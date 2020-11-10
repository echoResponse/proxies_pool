from settings import MAX_SCROE

#实现Proxy类，定义代理内容
#protocol 协议类型 0:http 1:https 2 http&https
#nike_type 匿名类型 0:高匿 1:匿名 2:透明
#delay 延迟，响应时间
#area 所属地区
#score 分数 在settings中设置，每检测失败一次减1，-1为不可用
class Proxy():
    def __init__(self, ip, port, protocol=-1, nike_type=-1, delay=-1, area=None, score=MAX_SCROE, disable_domains=[]):
        self.ip = ip
        self.port = port
        self.protocol = protocol #默认为-1，
        self.nick_type = nike_type
        self.delay = delay
        self.area = area
        self.score = score
        self.disable_domains = disable_domains

    #返回数据字符串
    def __str__(self):
        return str(self.__dict__)