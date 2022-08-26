from pymongo import MongoClient


class BaseMapper:
    def __init__(self, host="127.0.0.1", port=27017, database='2106'):
        self.client = MongoClient(host, port)  # 建立客户端对象
        self.db = self.client[database]

    def query_one(self, table, condition):
        collection = self.db[table]
        return collection.find_one(condition)

    def update_one(self, table, condition, update):
        collection = self.db[table]
        collection.update_one(condition, update)

    def find_and_update_one_seedwords(self, query, update):
        collection = self.db.seed_words
        collection.find_oneand_modify(query, {'$set': update})

    def get_agentip_byid(self, id):
        """
        根据id查询代理ip地址
        :return:
        """
        collection = self.db.agent_ip
        return collection.find_one({'_id': id})['ip']

    def get_url_from_seedwords_byword(self, word):
        """
        这里的word需要是未使用的
        :param word:
        :return: url
        """
        url, _, isRead = self.query_seedwords_byword(word)
        if isRead == True:
            print("err,该单词已被使用！")
            return None
        self.update_seedwords_byword(word, 'is_read', True)
        return url

    def get_exp_from_seedwords_byword(self, word):
        _, exp, isRead = self.query_seedwords_byword(word)
        if exp == None:
            print("err,还未添加该单词的解释！")
            if isRead == True:
                print("该单词已经使用！")
            else:
                print("该单词未使用！")
            return None
        return exp

    def query_one_notused_seedwords(self):
        """
        查找未使用的单词与url，并限制个数为limit个
        :param limit:
        :return: 返回列表[(word1,url1),(word2,url2)...]
        """

        collection = self.db.seed_words
        return collection.find_one_and_update({'is_read': False}, {'$set': {'is_read': True}})
        # list = []
        # if result != None:
        # data = (result['words'], result['url'])
        # list.append(data)
        return result

    def query_all(self, table, query={}):
        """
        根据条件查询data集合
        :param query:
        :return: Bson
        """
        collection = self.db[table]
        return collection.find(query)

    def insert_one(self, table, data):
        collection = self.db[table]
        collection.insert_one(data)

    def query_seedwords_byWord(self, word):
        """
        通过单词获取url与explanation is_read
        :param word: 需要查询的单词
        :return: url,explanation,is_used
        """
        collection = self.db.seed_words
        result = collection.find_one({'words': word})
        if result == None:
            return None, None
        return result['url'], result['explanation'], result['is_read']

    def update_seedwords_byword(self, word, key, value):
        """
        将爬取到的key value存入data表
        :return:
        """
        collection = self.db.seed_words
        collection.update_one({'words': word}, {'$set': {key: value}})

    def query_stopwords_byword(self, word):
        """
        根据单词查询stop_words表
        :param word: 单词
        :return: 返回是否包含该word
        """
        return self.contains_value(self.db.stop_words, 'words', word)

    def insert_one_seedwords(self, data):

        """data为topK的数据,
        元素为list，且元组字段为word url
        """
        collection = self.db.seed_words
        collection.insert_one(data)

    def contains_value(self, table, key, value):
        """
        判断集合中是否包含包含key:value,
        :param collection: 需要判断的集合
        :return: True or False
        """
        collection = self.db[table]
        count = collection.count_documents({key: value})
        return count != 0

    def query_count(self, table, query={}):
        return self.db[table].count_documents(query)

    def size_of_read_seedwords(self):
        """
        返回data表中已使用过的word个数
        :return:
        """
        collection = self.db.seed_words
        return collection.count_documents({'is_read': True})

    def update_many(self, table, query, update):
        collection = self.db[table]
        collection.update_many(query, update)

    def query_max_id(self, table):
        collection = self.db[table]
        return collection.find().sort("_id", -1).limit(1).next()['_id']

    def close_client(self):
        self.client.close()

    def delete_many(self, table, query):
        collection = self.db[table]
        collection.delete_many(query)


if __name__ == '__main__':
    baseMapper = BaseMapper()
    # baseMapper.delete_many('seed_words',{'_id':{'$gt':200}})
    # print(baseMapper.query_one('seed_words',{'_id':1}))
    baseMapper.update_many('seed_words', {}, {'$set': {'is_read': False}})
    baseMapper.update_many('seed_words', {}, {'$set': {'explanation': None}})
    # print(baseMapper.query_max_id('seed_words'))
    # print(baseMapper.query_count('seed_words'))
    # print(baseMapper.query_count('seed_words',{"is_read":False}))
    baseMapper.delete_many('spider_log', {})
