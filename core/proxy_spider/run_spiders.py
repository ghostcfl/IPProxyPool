import importlib
import schedule
import time
from settings import PROXIES_SPIDERS, RUN_SPIDERS_INTERVAL
from core.proxy_vaildate.httpbin_vaildator import check_proxy
from core.db.mongo_pool import MongoPool
from utils.log import logger
from gevent import monkey
from gevent.pool import Pool

monkey.patch_socket()


class RunSpider(object):
    def __init__(self):
        self.mongo_pool = MongoPool()
        self._coroutine_pool = Pool()

    @staticmethod
    def get_spider_from_setting():
        for full_class_name in PROXIES_SPIDERS:
            # core.proxy_spider.proxy_spiders.IP66Spider
            # 截取模块名和类名
            module_name, class_name = full_class_name.rsplit(".", 1)
            module = importlib.import_module(module_name)
            cls = getattr(module, class_name)
            spider = cls()
            yield spider

    def run(self):
        spiders = self.get_spider_from_setting()
        for spider in spiders:
            self._coroutine_pool.apply_async(self._execute_one_spider_task, args=(spider,))
        self._coroutine_pool.join()

    def _execute_one_spider_task(self, spider):
        try:
            for proxy in spider.get_proxies():
                proxy = check_proxy(proxy)
                if proxy.speed != -1:
                    self.mongo_pool.insert_one(proxy)
        except Exception as e:
            logger.exception(e)

    @classmethod
    def start(cls):
        rs = RunSpider()
        rs.run()

        schedule.every(RUN_SPIDERS_INTERVAL).hours.do(rs.run)
        while 1:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    RunSpider.start()
