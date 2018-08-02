# -*- coding: utf-8 -*-

# @Author: yooongchun
# @File: Scheduler.py
# @Time: 2018/7/31
# @Contact: yooongchun@foxmail.com
# @blog: blog.csdn.net/zyc121561
# @Description: scheduler

from time import sleep
from multiprocessing import Process
from Crawler import Crawler
from Validation import Validation
from API import API


class Scheduler(object):
    def __init__(self,
                 va_time=10 * 60,
                 cr_time=15 * 60,
                 va_batch_size=100,
                 host="localhost",
                 port="6379",
                 monitor_port=9999,
                 key="Proxy",
                 va_addr="http://www.baidu.com",
                 va_host="www.baidu.com"):
        self.__va_time = va_time
        self.__cr_time = cr_time
        self.__batch_size = va_batch_size
        self.__host = host
        self.__port = port
        self.__key = key
        self.__va_addr = va_addr
        self.__va_host = va_host
        self.__moni_port = monitor_port

    def run_crawler(self):
        while True:
            try:
                crawler = Crawler(
                    host=self.__host, port=self.__port, key=self.__key)
                crawler.run()
            except Exception:
                pass
            sleep(self.__cr_time)

    def run_validation(self):
        while True:
            try:
                validation = Validation(
                    validation_addr=self.__va_addr,
                    host=self.__va_host,
                    batch_size=100,
                    db_host=self.__host,
                    port=self.__port,
                    key=self.__key)
                validation.run()
            except Exception:
                pass
            sleep(self.__va_time)

    def run_API(self):
        api = API(
            host=self.__host,
            port=self.__port,
            key=self.__key,
            moni_port=self.__moni_port)
        api.run()

    def run(self):
        Process(target=self.run_crawler).start()
        Process(target=self.run_validation).start()
        Process(target=self.run_API).start()


if __name__ == "__main__":
    scheduler = Scheduler(
        va_time=15 * 60,
        cr_time=15 * 60,
        va_batch_size=100,
        host="localhost",
        port="6379",
        key="Proxy",
        monitor_port=9999,
        va_addr="http://www.baidu.com",
        va_host="www.baidu.com")
    scheduler.run()
