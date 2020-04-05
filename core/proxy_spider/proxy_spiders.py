import time
import random
import requests
from utils.http import get_request_headers
from core.proxy_spider.base_spider import BaseSpider


class XiCiSpider(BaseSpider):
    urls = ["https://www.xicidaili.com/nn/{}".format(i) for i in range(1, 11)]

    group_xpath = '//*[@id="ip_list"]/tr[position()>1]'

    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[4]/a/text()',
    }


class Ip3366Spider(BaseSpider):
    urls = ["http://www.ip3366.net/free/?stype={}&page={}".format(i, j) for i in range(1, 4, 2) for j in range(1, 8)]

    group_xpath = '//*[@id="list"]/table/tbody/tr'

    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }


class KDLSpider(BaseSpider):
    urls = ["https://www.kuaidaili.com/free/inha/{}/".format(i) for i in range(1, 6)]

    group_xpath = '//*[@id="list"]/table/tbody/tr'

    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[5]/text()',
    }

    def get_page_from_url(self, url):
        time.sleep(random.uniform(1, 3))
        return super().get_page_from_url(url)


class ProxyListPlusSpider(BaseSpider):
    urls = ["https://list.proxylistplus.com/Fresh-HTTP-Proxy-List-{}".format(i) for i in range(1, 7)]

    group_xpath = '//*[@id="page"]/table[2]/tr[position()>2]'

    detail_xpath = {
        'ip': './td[2]/text()',
        'port': './td[3]/text()',
        'area': './td[5]/text()',
    }

    # def get_page_from_url(self, url):
    #     time.sleep(random.uniform(1, 3))
    #     return super().get_page_from_url(url)


class IP66Spider(BaseSpider):
    urls = ["http://www.66ip.cn/{}.html".format(i) for i in range(1, 6)]

    group_xpath = '//*[@id="main"]/div/div[1]/table/tr[position()>1]'

    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }

    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_request_headers())
        return response.content.decode("GBK")


class IP89Spider(BaseSpider):
    urls = ['http://www.89ip.cn/index_{}.html'.format(i) for i in range(1, 8)]

    group_xpath = '//table[@class="layui-table"]/tbody/tr'

    detail_xpath = {
        'ip': './td[1]/text()',
        'port': './td[2]/text()',
        'area': './td[3]/text()',
    }

    def get_page_from_url(self, url):
        response = requests.get(url, headers=get_request_headers())
        return response.content.decode()

if __name__ == '__main__':
    # spider = XiCiSpider()
    # spider = Ip3366Spider()
    # spider = KDLSpider()
    # spider = ProxyListPlusSpider()
    spider = IP89Spider()

    for proxy in spider.get_proxies():
        print(proxy)


    # r = requests.get('http://www.66ip.cn/1.html')
    # print(r.content.decode("GBK"))
