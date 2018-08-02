# -*- coding: utf-8 -*-

# @Author: yooongchun
# @File: Crawler.py
# @Time: 2018/7/31
# @Contact: yooongchun@foxmail.com
# @blog: blog.csdn.net/zyc121561
# @Description: validate IP module

import aiohttp
import asyncio
from RedisClient import RedisClient
from UA import UserAgent


class Validation(object):
    def __init__(self,
                 validation_addr="http://www.baidu.com",
                 host="www.baidu.com",
                 batch_size=100,
                 db_host='localhost',
                 port='6379',
                 key='Proxy'):
        self.__redis = RedisClient(
            host=db_host, port=port, password=None, key=key)
        self.__host = host
        self.__addr = validation_addr
        self.__batch_size = batch_size

    async def validation_single(self, proxy):
        '''validate single proxy'''
        # print("validation proxy: ", proxy)
        headers = UserAgent(host=self.__host).headers()
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = 'http://' + proxy
                async with session.get(
                        self.__addr, proxy=real_proxy, headers=headers,
                        timeout=15) as response:
                    if response.status == 200:
                        self.__redis.max(proxy)
                        # print("proxy {} is good.".format(proxy))
                    else:
                        self.__redis.decrease(proxy)
                        # print("proxy {} is not good".format(proxy))
            except Exception:
                # print("proxy {} is not good".format(proxy))
                self.__redis.decrease(proxy)

    def run(self):
        try:
            proxies = self.__redis.all()
            for i in range(0, len(proxies), self.__batch_size):
                # print("processing i: {}\tprogress:{}/{} {:.2f}%".format(i + 1, i + 1, len(proxies),
                # (i + 1) / len(proxies) * 100))
                task_proxies = proxies[i:self.__batch_size + i]
                loop = asyncio.get_event_loop()
                tasks = [
                    self.validation_single(proxy) for proxy in task_proxies
                ]
                loop.run_until_complete(asyncio.wait(tasks))
            # print("After validation,total {} in database".format(self.__redis.count()))
        except Exception as e:
            pass
            # print(e.args)


if __name__ == "__main__":
    validation = Validation(
        validation_addr="http://www.baidu.com",
        host="www.baidu.com",
        batch_size=100,
        db_host='localhost',
        port='6379',
        key='Proxy')
    validation.run()
