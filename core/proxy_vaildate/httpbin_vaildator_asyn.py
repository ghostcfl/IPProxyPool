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
import asyncio
import httpx
import time
import json
from utils.http import get_request_headers
from settings import TEST_TIMEOUT
from utils.log import logger
from model import Proxy


async def check_proxy(proxy_list):
    """
    用于检查指定 代理IP的响应速度，匿名程度，支持的协议类型
    :param proxy: 代理IP的数据模型对象
    :return: 返回检查后的代理IP
    """
    task_list = []
    for proxy in proxy_list:
        proxies = {
            'http': 'http://{}:{}'.format(proxy.ip, proxy.port),
            'https': 'https://{}:{}'.format(proxy.ip, proxy.port),
        }

        req_http = _check_http_proxies(proxies)
        task_http = asyncio.create_task(req_http)
        task_list.append(task_http)

    await asyncio.gather(*task_list)
    for task in task_list:
        print(task.result())
    # if http and https:
    #     proxy.protocol = 2
    #     proxy.nick_type = http_nick_type
    #     proxy.speed = http_speed
    # elif https:
    #     proxy.protocol = 1
    #     proxy.nick_type = https_nick_type
    #     proxy.speed = https_speed
    # elif http:
    #     proxy.protocol = 0
    #     proxy.nick_type = http_nick_type
    #     proxy.speed = http_speed
    # else:
    #     proxy.protocol = -1
    #     proxy.nick_type = -1
    #     proxy.speed = -1
    #
    # return proxy


async def _check_http_proxies(proxies):
    test_urls = {
        "http": "http://httpbin.org/get",
        "https": "https://httpbin.org/get"
    }

    start_time = time.time()

    async with httpx.AsyncClient(timeout=TEST_TIMEOUT, proxies=proxies, headers=get_request_headers()) as client:
        result = []
        for k, v in test_urls.items():
            nick_type = -1  # 代理IP的匿名类型，高匿是0，匿名是1，透明是2
            speed = -1  # 代理IP的响应速度,单位秒
            try:
                response = await client.get(v)
                if response.status_code == 200:
                    speed = round(time.time() - start_time, 2)
                    dic = json.loads(response.content.decode())

                    origin = dic['origin']

                    proxy_connection = dic['headers'].get("['Proxy-Connection']", None)

                    if "," in origin:
                        nick_type = 2
                    elif proxy_connection:
                        nick_type = 1
                    else:
                        nick_type = 0
                    result.append([k, nick_type, speed])
                else:
                    result.append(["", nick_type, nick_type])
            except Exception as e:
                logger.error(e)
                result.append(["", nick_type, nick_type])
        return result


if __name__ == '__main__':
    proxy_list = []
    proxy_list.append(Proxy(ip="58.218.214.129", port="6117"))
    # proxy_list.append(Proxy(ip="58.218.214.129", port="6117"))
    # proxy_list.append(Proxy(ip="58.218.214.129", port="6117"))
    # proxy_list.append(Proxy(ip="58.218.214.129", port="6117"))
    # proxy_list.append(Proxy(ip="58.218.214.129", port="6117"))
    asyncio.run(check_proxy(proxy_list))
    # print(proxy)
