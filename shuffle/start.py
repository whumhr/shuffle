from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
# 引入spider
from spiders.baidubaike_spider1 import BaidubaikeSpider1
from spiders.baidubaike_spider2 import BaidubaikeSpider2
from spiders.baidubaike_spider3 import BaidubaikeSpider3
import logging

logger = logging.getLogger(__name__)

settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)


def start_spider():
    # 装载爬虫
    # runner.crawl(TestSpider)
    # 如果有多个爬虫需要启动可以一直装载下去
    runner.crawl(BaidubaikeSpider1)
    runner.crawl(BaidubaikeSpider2)
    runner.crawl(BaidubaikeSpider3)
    # ... ...

    # 爬虫结束后停止事件循环
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    # 启动事件循环
    reactor.run()


def main():
    start_spider()


if __name__ == '__main__':
    main()
