import scrapy
from urllib.parse import quote
from ..items import ScrapyProjectItem
from ..Mapper import BaseMapper


class BaidubaikeSpider1(scrapy.Spider):
    name = 'baiduspider1'
    allowed_domains = ['baike.baidu.com']

    # df = pd.read_excel("D:/Git-Space/byte-dance/李津津/scrapy_project3.0/scrapy_project/spiders/种子词汇.xlsx")
    # df["是否已读"] = 0
    baseMapper = BaseMapper.BaseMapper()

    #count = collection.count_documents({})
    #id = 1
    def start_requests(self):
        # for i in range(len(self.word_list)):
        while True:
            item = self.baseMapper.query_one_notused_seedwords()
            if item == None:
                break
            self.start_urls = 'https://baike.baidu.com/item/{:s}'.format(quote(item["words"]))
            yield scrapy.Request(self.start_urls, callback=self.parse, dont_filter=True)
            print("spider1")
            #self.id += 1

    def parse(self, response):
        # print(response)
        # 提取列表中第一个种子
        item = ScrapyProjectItem()
        #
        # #单词
        # sel = Selector(response)
        word = response.xpath('//dl[@class="basicInfo-block basicInfo-left"]/dd[1]/text()').extract_first()
        print(word)
        if word:
            word = word.replace(
                "\n", "")
        else:
            word = '暂未收录该词汇'
        item["words"] = word
        # # url
        url = response.xpath('//link[@rel="alternate"][@hreflang="x-default"]/@href').extract_first()
        item["URL"] = url if word else "没有链接"
        # # 解释
        explain = "".join(response.xpath('//div[@class="lemma-summary"]/div[1]/text()').extract()).replace("\n", "")
        item["explain"] = explain if explain else "没有"
        #print(item)
        yield item