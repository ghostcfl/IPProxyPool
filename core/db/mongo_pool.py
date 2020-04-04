import pymongo
import random
from pymongo import MongoClient
from settings import MONGODB_URL
from utils.log import logger
from model import Proxy


class MongoPool(object):

    def __init__(self):
        self.client = MongoClient(MONGODB_URL)
        self.proxies = self.client['proxy_pool']['proxies']

    def __del__(self):
        self.client.close()

    def insert_one(self, proxy):
        """
        实现插入功能
        :param proxy:
        :return:
        """
        if not self.proxies.count_documents({'_id': proxy.ip}):
            dic = proxy.__dict__
            dic['_id'] = proxy.ip
            self.proxies.insert_one(dic)
            logger.info('插入新的代理：{}'.format(proxy))
        else:
            logger.warning("代理已存在：{}".format(proxy))

    def update_one(self, proxy):
        """
        实现修改功能
        :param proxy:
        :return:
        """
        self.proxies.update_one({'_id': proxy.ip}, {"$set": proxy.__dict__})

    def delete_one(self, proxy):
        """
        实现删除功能
        :param proxy:
        :return:
        """
        self.proxies.delete_one({'_id': proxy.ip})
        logger.info("删除代理IP：{}".format(proxy))

    def find_all(self):
        """
        查询所有代理IP的功能
        :return:
        """
        cursor = self.proxies.find()
        for item in cursor:
            item.pop('_id')
            proxy = Proxy(**item)
            yield proxy

    def find(self, conditions=None, count=0):
        """
        实现条件查询功能，先分数降序，速度升序
        :param conditions: 查询条件字典
        :param count: 限制最多取出的多少个代理IP
        :return: 返回满足条件的代理IP列表
        """
        cursor = self.proxies.find(conditions, limit=count).sort([
            ('score', pymongo.DESCENDING), ('speed', pymongo.ASCENDING)
        ])
        proxy_list = []
        for item in cursor:
            item.pop("_id")
            proxy = Proxy(**item)
            proxy_list.append(proxy)
        return proxy_list

    def get_proxies(self, protocol=None, domain=None, nick_type=0, count=0):
        """
        实现根据协议类型，要访问的网站域名，获取代理IP列表
        :param protocol: 协议http or https
        :param domain: 域名
        :param nick_type: 匿名类型，默认高匿的IP
        :param count: 限制最多取出的多少个代理IP
        :return: 返回满足条件的代理IP列表
        """
        conditions = {"nick_type": nick_type}
        if not protocol:
            conditions['protocol'] = 2
        elif protocol.lower() == 'http':
            conditions['protocol'] = {'$in': [0, 2]}
        else:
            conditions['protocol'] = {'$in': [1, 2]}

        if domain:
            conditions['disable_domains'] = {'$nin': [domain]}
        # print(conditions)
        return self.find(conditions, count=count)

    def random_proxy(self, **kwargs):
        """
        :param protocol: 协议http or https
        :param domain: 域名
        :param nick_type: 匿名类型，默认高匿的IP
        :param count: 限制最多取出的多少个代理IP
        :return: 返回一个随机的代理IP
        """
        proxy_list = self.get_proxies(**kwargs)
        return random.choice(proxy_list)

    def disable_domain(self, ip, domain):
        """
        实现把指定域名添加到指定IP的disable_domain列表中
        :param ip: IP地址
        :param domain: 域名
        :return: True，添加成功,Flase,添加失败
        """
        if not self.proxies.count_documents({"_id": ip, 'disable_domains': domain}):
            self.proxies.update_one({'_id': ip}, {'$push': {'disable_domains': domain}})
            return True
        return False


if __name__ == '__main__':
    mongo = MongoPool()
    # proxy = Proxy(**{'ip': '58.218.214.155', 'port': '8888', 'protocol': 0, 'nick_type': 2, 'speed': 30, 'area': None, 'score': 90, 'disable_domains': ['taobao.com']})
    # mongo.insert_one(proxy)

    # for x in mongo.get_proxies("http", domain='jd.com'):
    #     print(x)

    print(mongo.disable_domain('58.218.214.152', 'jd.com'))
    for x in mongo.find_all():
        print(x)
