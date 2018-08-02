# -*- coding: utf-8 -*-

# @Author: yooongchun
# @File: RedisClient.py
# @Time: 2018/7/31
# @Contact: yooongchun@foxmail.com
# @blog: blog.csdn.net/zyc121561
# @Description: database module

import redis
import random
from random import choice


class RedisClient(object):
    def __init__(self, host='localhost', port='6379', password=None, key='Proxy', init_score=10):
        self.__db = redis.StrictRedis(
            host=host, port=port, password=password, decode_responses=True)
        self.__init_score = init_score
        self.__key = key
        self.__max_score = 100
        self.__min_score = 0

    def add(self, proxy, score=None):
        '''add proxy ip to database'''
        if not self.__db.zscore(self.__key, proxy):
            return self.__db.zadd(
                self.__key, score
                if score else self.__init_score, proxy)

    def upgrade(self, proxy, score):
        return self.__db.zadd(self.__key, score, proxy)

    def random(self):
        '''return a random proxy ip'''
        for score in range(0, self.__max_score, 5):
            if random.random() > 0.7:
                continue
            result = self.__db.zrangebyscore(self.__key, self.__max_score - score, self.__max_score)
            if len(result) > 0:
                return choice(result)

    def random_max(self):
        '''return a random proxy ip which has max score'''
        result = self.__db.zrangebyscore(self.__key, self.__max_score,
                                         self.__max_score)
        if len(result) > 0:
            return choice(result)

    def decrease(self, proxy, step=1):
        '''decrease score of proxy'''
        score = self.__db.zscore(self.__key, proxy)
        if score and score > self.__min_score:
            return self.__db.zincrby(self.__key, proxy, -1 * step)
        else:
            return self.__db.zrem(self.__key, proxy)

    def exists(self, proxy):
        '''proxy exists or not?'''
        return self.__db.zscore(self.__key, proxy) is not None

    def max(self, proxy):
        '''set proxy score as MAX'''
        return self.__db.zadd(self.__key, self.__max_score, proxy)

    def count(self):
        '''get proxy number'''
        return self.__db.zcard(self.__key)

    def all_max(self):
        '''get all proxy ip whose score is max'''
        return self.__db.zrangebyscore(self.__key, self.__max_score, self.__max_score)

    def all(self):
        '''get all proxy ip'''
        return self.__db.zrangebyscore(self.__key, self.__min_score, self.__max_score)


if __name__ == "__main__":
    redis_client = RedisClient(
        host='localhost',
        port='6379',
        password=None,
        key='Proxy',
        init_score=10)
    print(redis_client.add('121.121.121.121:90'))
    print(redis_client.all())
    print(redis_client.count())
