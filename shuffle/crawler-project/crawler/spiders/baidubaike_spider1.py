import scrapy
from urllib.parse import quote
from items import ScrapyProjectItem
from Mapper import BaseMapper


class BaidubaikeSpider1(scrapy.Spider):
    name = 'baiduspider1'
    allowed_domains = ['baike.baidu.com']
    baseMapper = BaseMapper.BaseMapper()

    def start_requests(self):
        while True:
            item = self.baseMapper.query_one_notused_seedwords()
            if item == None:
                break
            self.start_urls = 'https://baike.baidu.com/item/{:s}'.format(quote(item["words"]))
            yield scrapy.Request(self.start_urls, callback=self.parse, dont_filter=True)
            print("spider1")

    def parse(self, response):
        item = ScrapyProjectItem()
        # 种子词对应名词
        word1 = response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dd[1]/text()').extract_first()
        # 页面结构发生变化的种子词的解析
        word2 = response.xpath(
            '//dd[@class="lemmaWgt-lemmaTitle-title J-lemma-title" ]/span[1]/h1/text()').extract_first()
        if word1:
            word = word1.replace("\n", "")
        elif word2:
            word = word2.replace("\n", "")
        else:
            word = word1
        item["word"] = word if word else '暂无收录该词汇'
        # url
        url = response.xpath('//link[@rel="alternate"][@hreflang="x-default"]/@href').extract_first()
        item["URL"] = url if word else "没有链接"
        # 解释
        explain1 = "".join(response.xpath('//div[@class="lemma-summary"]/div[1]/text()').extract())
        # 页面结构发生变化的种子词解释的解析
        explain2 = "".join(response.xpath('//div[@class="para"]/text()').extract())
        if explain1:
            explain = explain1.replace("\n", "")
        elif explain2:
            explain = explain2.replace("\n", "")
        else:
            explain = explain1
        item["explain"] = explain if explain else "没有"
        yield item