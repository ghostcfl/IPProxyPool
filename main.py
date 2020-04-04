from multiprocessing import Process
from core.proxy_spider.run_spiders import RunSpider
from core.proxy_test import ProxyTester
from core.proxy_api import ProxyAPI


def run():
    process_list = []
    process_list.append(Process(target=RunSpider.start))
    process_list.append(Process(target=ProxyTester.start))
    process_list.append(Process(target=ProxyAPI.start))
    for process in process_list:
        # 设置守护进程
        process.daemon = True
        process.start()

    for process in process_list:
        # 主进程等待子进程完成
        process.join()


if __name__ == '__main__':
    run()
