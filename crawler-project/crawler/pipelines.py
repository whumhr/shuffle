# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
from pymongo import MongoClient
import jieba
import jieba.analyse
from Mapper import BaseMapper


class ScrapyProjectPipeline:
    def open_spider(self, spider):

        self.baseMapper = BaseMapper.BaseMapper()

    def process_item(self, item, spider):

        if item['word'] == '暂无收录该词汇':
            return item

        if self.baseMapper.contains_value('seed_words', 'words', item['word']):
            # print("*****************true*********************")
            query = {"words": item['word']}
            update = {"$set": {"explanation": item['explain'],
                               "url": item['URL']}}
            self.baseMapper.update_one('seed_words', query, update)
            # print(self.baseMapper.query_one('seed_words',query))
        else:
            id = self.baseMapper.query_max_id('seed_words')
            data = {"_id": id + 1, "words": item['word'], "explanation": item['explain'], "url": item['URL'],
                    "is_read": True}
            self.baseMapper.insert_one_seedwords(data)

        explain = item["explain"]  # exlpain是爬取完后的一个词的解释

        if len(explain) < 60:
            tags = jieba.analyse.extract_tags(explain, topK=5, withWeight=False)  # list类型，根据topk分词
        elif 60 <= len(explain) <= 120:
            tags = jieba.analyse.extract_tags(explain, topK=10, withWeight=False)
        elif 120 <= len(explain) <= 180:
            tags = jieba.analyse.extract_tags(explain, topK=15, withWeight=False)
        elif len(explain) > 180:
            tags = jieba.analyse.extract_tags(explain, topK=20, withWeight=False)
        for j in tags:  # 判断分词是否在高频词里面
            if self.baseMapper.query_count('seed_words') < 60 and not self.baseMapper.contains_value('seed_words',
                                                                                                     'words',
                                                                                                     j) and self.baseMapper.contains_value(
                    'match_words', 'words', j) and not self.baseMapper.contains_value('stop_words', 'words',
                                                                                      j):  # 分词在高频词但是不在种子词中，则加入
                # 获取字段最大值
                id = self.baseMapper.query_max_id('seed_words')
                data = {"_id": id + 1, "words": j, "explanation": None, "url": None, "is_read": False}
                self.baseMapper.insert_one_seedwords(data)
        return item

    def close_spider(self, spider):
        self.baseMapper.close_client()
