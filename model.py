from settings import MAX_SCORE


class Proxy(object):
    """
    定义代理IP的数据模型
    """

    def __init__(self, ip, port, protocol=-1, nick_type=-1, speed=-1, area=None, score=MAX_SCORE, disable_domains=[]):
        self.ip = ip  # 代理的IP地址
        self.port = port  # 代理IP的端口号
        self.protocol = protocol  # 代理IP支持的协议类型，HTTP是0,HTTPS是1,都支持是2
        self.nick_type = nick_type  # 代理IP的匿名类型，高匿是0，匿名是1，透明是2
        self.speed = speed  # 代理IP的响应速度
        self.area = area  # 代理IP所在地区
        self.score = score  # 代理IP评分,默认50分，检查可用性请求失败时减1分，请求成功恢复默认分，减到0分时删除
        self.disable_domains = disable_domains  # 不可用域名列表

    def __str__(self):
        return str(self.__dict__)
