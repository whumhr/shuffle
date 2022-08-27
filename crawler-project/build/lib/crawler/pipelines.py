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
        # self.filename = open('word_information.txt', 'a', encoding='utf-8')
        self.baseMapper = BaseMapper.BaseMapper()

        # self.collection = self.mydb["seed_words"]  # 种子词
        # self.collection1 = self.mydb["match_words"]  # 高频词

    def process_item(self, item, spider):
        # self.filename.write(json.dumps(dict(item), ensure_ascii=False) + '\n')
        query = {"words": item['words']}
        update = {"$set": {"explanation": item['explain'],
                           "url": item['URL']}}
        self.baseMapper.update_one('seed_words', query, update)
        # self.collection.update_one(query, update)

        # word_list = df["词汇"].tolist()  # 用来模拟数据库中所有种子词汇
        explain = item["explain"]  # exlpain是爬取完后的一个词的解释
        # jieba.analyse.set_stop_words('stopwords.txt')  # 去除停用词，停用词应该存在表中
        if len(explain) < 60:
            tags = jieba.analyse.extract_tags(explain, topK=5, withWeight=False)  # list类型，根据topk分词
        elif 60 <= len(explain) <= 120:
            tags = jieba.analyse.extract_tags(explain, topK=10, withWeight=False)
        elif 120 <= len(explain) <= 180:
            tags = jieba.analyse.extract_tags(explain, topK=15, withWeight=False)
        elif len(explain) > 180:
            tags = jieba.analyse.extract_tags(explain, topK=20, withWeight=False)
        for j in tags:  # 判断分词是否在高频词里面
            if self.baseMapper.query_count('seed_words') < 200 and self.baseMapper.contains_value('match_words',
                                                                                                  'words',
                                                                                                  j) and not self.baseMapper.contains_value(
                    'stop_words', 'words', j):  # 分词在高频词但是不在种子词中，则加入
                # 获取字段最大值
                id = self.baseMapper.query_max_id('seed_words')
                data = {"_id": id + 1, "words": j, "explanation": None, "url": None, "is_read": False}
                self.baseMapper.insert_one_seedwords(data)
        return item

    def close_spider(self, spider):
        self.baseMapper.close_client()
