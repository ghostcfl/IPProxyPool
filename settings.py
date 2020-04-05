MAX_SCORE = 50

STD_OUT_LOG_LEVER = "INFO"
FILE_LOG_LEVER = "ERROR"

TEST_TIMEOUT = 10

# mongodb的数据库地址
MONGODB_URL = "mongodb://127.0.0.1:27017"

PROXIES_SPIDERS = [
    # 爬虫的全类名，路径：模块，类名
    'core.proxy_spider.proxy_spiders.IP66Spider',
    'core.proxy_spider.proxy_spiders.Ip3366Spider',
    'core.proxy_spider.proxy_spiders.KDLSpider',
    'core.proxy_spider.proxy_spiders.ProxyListPlusSpider',
    'core.proxy_spider.proxy_spiders.XiCiSpider',
    'core.proxy_spider.proxy_spiders.IP89Spider',
]

# 每次执行爬虫时间的间隔,单位小时
RUN_SPIDERS_INTERVAL = 24
# 配置检测代理IP的异步数量
TEST_PROXIES_ASYNC_COUNT = 10
# 第次执行检测爬虫的时间间隔
TEST_PROXIES_INTERVAL = 3
#配置获取的代理的IP最大数量;这个数眼越小，可用性越高，但是随机差
PROXIES_MAX_COUNT = 50
