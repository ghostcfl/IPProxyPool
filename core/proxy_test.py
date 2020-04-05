import schedule
import time
from core.db.mongo_pool import MongoPool
from core.proxy_vaildate.httpbin_vaildator import check_proxy
from settings import MAX_SCORE, TEST_PROXIES_ASYNC_COUNT, TEST_PROXIES_INTERVAL
from gevent import monkey
from gevent.pool import Pool
from gevent.queue import JoinableQueue

monkey.patch_socket()


class ProxyTester(object):
    def __init__(self):
        self.mongo_pool = MongoPool()
        self._coroutine_pool = Pool()
        self.queue = JoinableQueue()

    def _check_callback(self, temp):
        self._coroutine_pool.apply_async(self._check_one_proxy_task, callback=self._check_callback)

    def run(self):
        proxies = self.mongo_pool.find_all()
        for proxy in proxies:
            self.queue.put(proxy)  # 把proxy加入队列
        for i in range(TEST_PROXIES_ASYNC_COUNT):
            self._coroutine_pool.apply_async(self._check_one_proxy_task, callback=self._check_callback)
        self.queue.join()

    def _check_one_proxy_task(self):
        proxy = self.queue.get()
        proxy = check_proxy(proxy)
        if proxy.speed == -1:
            proxy.score -= 1
            if not proxy.score:
                self.mongo_pool.delete_one(proxy)
            else:
                self.mongo_pool.update_one(proxy)
        else:
            proxy.score = MAX_SCORE
            self.mongo_pool.update_one(proxy)
        self.queue.task_done()  # 队列任务完成

    @classmethod
    def start(cls):
        pt = ProxyTester()
        pt.run()

        schedule.every(TEST_PROXIES_INTERVAL).minutes.do(pt.run)
        while 1:
            schedule.run_pending()
            time.sleep(1)


if __name__ == '__main__':
    ProxyTester.start()
