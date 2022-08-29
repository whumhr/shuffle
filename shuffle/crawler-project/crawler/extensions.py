import logging
from scrapy import signals
import datetime
from Mapper import BaseMapper

logger = logging.getLogger(__name__)


class SpiderStatLogging:

    def __init__(self, crawler):
        self.exit_code = False
        self.crawler = crawler
        self.baseMapper = BaseMapper.BaseMapper()
        self.stats_keys = set()
        self.cur_d = {
            'log_info': 0,
            'log_warning': 0,
            'requested': 0,
            'request_bytes': 0,
            'response': 0,
            'response_bytes': 0,
            'response_200': 0,
            'response_301': 0,
            'response_404': 0,
            'responsed': 0,
            'item': 0,
            'filtered': 0,
        }

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        return ext

    def spider_closed(self, spider, reason):
        logger.info(self.stats_keys)
        data = {
            "measurement": "spider_closed",
            "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "tags": {
                'spider_name': spider.name
            },
            "fields": {
                'end_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'reason': reason,
                'spider_name': spider.name
            }
        }
        self.baseMapper.insert_one('spider_log', data)

    def item_scraped(self, item):
        data = {
            "measurement": "newspider",
            "spider_status": "fail" if item['word'] == '暂无收录该词汇' else 'success',
            "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            'spider_name': self.crawler.spider.name
        }
        self.baseMapper.insert_one('spider_log', data)

    def spider_opened(self, spider):
        data = {
            "measurement": "spider_opened",
            "time": datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
            "tags": {
                'spider_name': spider.name
            },
            "fields": {
                'start_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'spider_name': spider.name
            }
        }
        self.baseMapper.insert_one('spider_log', data)

    def engine_stopped(self):
        self.exit_code = True
