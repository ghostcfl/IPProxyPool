"""
需要：爬取各个代理IP网站上的免费代理IP，进行检测，如果可用存储到数据库中
代理地址：
    西刺代理：https://www.xicidaili.com/nn/1
    ip3366:http://www.ip3366.net/free/?stype=1&page=1
    快代理：https://www.kuaidaili.com/free/inha/1/
    proxylistplus代理：https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-1
    66Ip代理：http://www.66ip.cn/1.html
"""
import requests
from lxml import etree
from utils.http import get_request_headers
from model import Proxy


class BaseSpider(object):
    urls = []
    group_xpath = ""
    detail_xpath = {}

    def __init__(self, urls=[], group_xpath="", detail_xpath={}):
        if urls:
            self.urls = urls

        if group_xpath:
            self.group_xpath = group_xpath

        if detail_xpath:
            self.detail_xpath = detail_xpath

    def get_proxies(self):
        for url in self.urls:
            page = self.get_page_from_url(url)
            proxies = self.get_proxies_from_page(page)
            yield from proxies

    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_request_headers())
        return response.content

    @staticmethod
    def get_first_from_list(lis):
        return lis[0] if len(lis) != 0 else ""

    def get_proxies_from_page(self, page):
        element = etree.HTML(page)
        trs = element.xpath(self.group_xpath)
        for tr in trs:
            ip = self.get_first_from_list(tr.xpath(self.detail_xpath['ip']))
            port = self.get_first_from_list(tr.xpath(self.detail_xpath['port']))
            area = self.get_first_from_list(tr.xpath(self.detail_xpath['area']))
            if ip and port:
                proxy = Proxy(ip, port, area=area)
                yield proxy


if __name__ == '__main__':
    config = {
        "urls": ["https://www.xicidaili.com/nn/{}".format(i) for i in range(1, 2)],
        "group_xpath": '//*[@id="ip_list"]/tr',
        'detail_xpath': {
            'ip': './td[2]/text()',
            'port': './td[3]/text()',
            'area': './td[4]/a/text()',
        }
    }
    spider = BaseSpider(**config)
    for proxy in spider.get_proxies():
        print(proxy)
