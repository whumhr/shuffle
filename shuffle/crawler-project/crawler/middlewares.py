# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from fake_useragent import UserAgent  # 设置随机ua
from Mapper import BaseMapper


# useful for handling different item types with a single interface


class ScrapyProjectSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ScrapyProjectDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class UseragentDemoDownloaderMiddleware(object):

    def process_request(self, request, spider):
        # 下载器在发送请求之前会执行的方法，一般用来设置随机请求头或随机代理ip等
        ua = UserAgent().random
        print(ua)  # 方便展示
        request.headers['User-Agent'] = ua  # headers可以用来设置请求头
        # 设置好之后需要在settings.py里设置一下DOWNLOADER_MIDDLEWARES
        # 之后再请求的时候就是从USER_AGENTS列表里随机取一个请求头，而不是之前在settings.py里设置死的请求头了


class IPProxyDownloadMiddleware(object):
    baseMapper = BaseMapper.BaseMapper()
    result = baseMapper.query_all('ip_data')
    PROXIES = []
    for i in result:
        PROXIES.append('ip:"{:s}"'.format(i['ip']))

    def process_request(self, request, spider):
        # 下载器在发送请求之前会执行的方法，一般用来设置随机请求头或随机代理ip等

        proxy = random.choice(self.PROXIES)  # random.choice是在列表中随机选择一个
        print(proxy)  # 方便展示
        request.meta['http_proxy'] = proxy  # meta可以用来设置代理ip
        # 设置好之后需要在settings.py里设置一下DOWNLOADER_MIDDLEWARES
        # 之后再请求的时候就是从PROXIES列表里随机取一个ip
