"""
目标：检查代理IP速度，匿名程序以及支持的协议
步骤：
    1.代理IP速度和匿名程度：
        ·对http://httpbin.org/get或https://httpbin.org/get 发送请求
        ·如果响应的origin中有','分割的两个IP就是透明代理IP
        ·如果响应的headers 中包含 Proxy-Connection 说明是匿名代理IP
        ·否则就是高匿代理IP
    2.检查代理IP协议
        ·如果 http://httpbin.org/get 发送请求可以成功，说明支持http协议
        ·如果 https://httpbin.org/get 发送请求可以成功，说明支持https协议
"""
import requests
import time
import json
from utils.http import get_request_headers
from settings import TEST_TIMEOUT
from utils.log import logger
from model import Proxy


def check_proxy(proxy):
    """
    用于检查指定 代理IP的响应速度，匿名程度，支持的协议类型
    :param proxy: 代理IP的数据模型对象
    :return: 返回检查后的代理IP
    """

    proxies = {
        'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
        'https': 'https://{}:{}'.format(proxy.ip, proxy.port),
    }

    http, http_nick_type, http_speed = _check_http_proxies(proxies)
    https, https_nick_type, https_speed = _check_http_proxies(proxies, False)

    if http and https:
        proxy.protocol = 2
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    elif https:
        proxy.protocol = 1
        proxy.nick_type = https_nick_type
        proxy.speed = https_speed
    elif http:
        proxy.protocol = 0
        proxy.nick_type = http_nick_type
        proxy.speed = http_speed
    else:
        proxy.protocol = -1
        proxy.nick_type = -1
        proxy.speed = -1

    return proxy


def _check_http_proxies(proxies, is_http=True):
    nick_type = -1  # 代理IP的匿名类型，高匿是0，匿名是1，透明是2
    speed = -1  # 代理IP的响应速度,单位秒
    if is_http:
        test_url = "http://httpbin.org/get"
    else:
        test_url = "https://httpbin.org/get"

    start_time = time.time()

    try:
        response = requests.get(test_url, headers=get_request_headers(), proxies=proxies, timeout=TEST_TIMEOUT)

        if response.ok:
            speed = round(time.time() - start_time, 2)

            dic = json.loads(response.text)

            origin = dic['origin']

            proxy_connection = dic['headers'].get("['Proxy-Connection']", None)

            if "," in origin:
                nick_type = 2
            elif proxy_connection:
                nick_type = 1
            else:
                nick_type = 0

            return True, nick_type, speed
        return False, nick_type, speed
    except Exception as e:
        logger.error(e)
        return False, nick_type, speed


if __name__ == '__main__':
    proxy = Proxy(ip="58.218.214.151", port="8708")
    check_proxy(proxy)
    # print(proxy)
