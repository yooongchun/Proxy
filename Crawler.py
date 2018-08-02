# -*- coding: utf-8 -*-

# @Author: yooongchun
# @File: Crawler.py
# @Time: 2018/7/31
# @Contact: yooongchun@foxmail.com
# @blog: blog.csdn.net/zyc121561
# @Description: crawl ip module

import requests
import re
import threading
from random import shuffle
from bs4 import BeautifulSoup
from UA import UserAgent
from RedisClient import RedisClient


class Crawler(object):
    '''crawl proxy ip from proxy website'''

    def __init__(self, host="localhost", port='6379', key='Proxy'):
        self.__redis = RedisClient(
            host=host, port=port, password=None, key=key)

    def __select_crawl_func(self):
        '''select function start with "crawl_" '''
        return filter(
            lambda x: x.startswith('crawl_') and callable(getattr(self, x)),
            dir(self))

    def get_proxies(self):
        '''run all "crawl_*" function '''
        proxies = []
        funcs = self.__select_crawl_func()
        for func in funcs:
            proxy = eval("self.{}()".format(func))
            if proxy:
                proxies.append(proxy)
        return proxies

    def run(self):
        proxies = self.get_proxies()
        thread_pool = []
        for proxy in proxies:
            th = threading.Thread(target=self.__single_run, args=(proxy, ))
            thread_pool.append(th)
            th.start()
        for th in thread_pool:
            th.join()

    def __single_run(self, proxy):
        '''crawler for specific website'''
        for ip in proxy:
            # print(threading.current_thread().name, "\t", ip)
            self.__redis.add(ip)

    def __base_crawl_func(self, page_num, url_base, host, id_anonymous,
                          name_anonymous):
        '''base function for crawler'''

        urls = []
        if page_num > 1:
            for page in range(page_num):
                url = url_base.format(page + 1)
                urls.append(url)
            shuffle(urls)
        else:
            urls.append(url_base)
        for page in range(page_num):
            if page % 10 == 0:
                headers = UserAgent(host).headers()
            try:
                if page % 5 == 0:
                    proxy = self.__redis.random_max()
            except Exception:
                proxy = None
            url = urls[page]
            try:
                if proxy:
                    proxies = {"http": "http://" + proxy}
                    response = requests.get(
                        url=url, headers=headers, proxies=proxies, timeout=15)
                else:
                    response = requests.get(
                        url=url, headers=headers, timeout=15)
            except Exception:
                # print(threading.current_thread().name, "Request url error:", url)
                continue
            if not response.status_code == 200:
                continue
            for code in ['utf-8', 'gbk', 'gb2312']:
                try:
                    html = response.content.decode(code)
                    break
                except Exception:
                    # print('code error:{}'.format(code))
                    pass
            if not html:
                continue
            soup = BeautifulSoup(html, "lxml")
            tds = soup.find_all("td")
            for index, td in enumerate(tds):
                text = re.sub(r"[\s\n\t]+", "", td.text)
                rule = r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$"
                if not re.match(rule, text):
                    continue
                if name_anonymous not in re.sub(
                        r"[\s\n\t]+", "", tds[index + id_anonymous - 1].text):
                    continue
                IP = re.sub(r"[\s\n\t]+", "", tds[index + 0].text)
                PORT = re.sub(r"[\s\n\t]+", "", tds[index + 1].text)
                proxy = "{}:{}".format(IP, PORT)
                yield proxy

    def crawl_xici(self):
        '''crawl proxy ip from xici website'''
        page_num = 3336
        url_base = "http://www.xicidaili.com/nn/{}"
        host = "www.xicidaili.com"
        id_anonymous = 4
        name_anonymous = '高匿名'

        return self.__base_crawl_func(page_num, url_base, host, id_anonymous,
                                      name_anonymous)

    def crawl_kuaidaili(self):
        '''crawl proxy ip from kuaidaili website'''
        page_num = 2367
        url_base = "https://www.kuaidaili.com/free/inha/{}"
        host = "www.kuaidaili.com"
        id_anonymous = 3
        name_anonymous = '高匿名'

        return self.__base_crawl_func(page_num, url_base, host, id_anonymous,
                                      name_anonymous)

    def crawl_66(self):
        '''crawl proxy ip from 66 website'''
        page_num = 1288
        url_base = "http://www.66ip.cn/{}.html"
        host = "www.66ip.cn"
        id_anonymous = 4
        name_anonymous = '高匿代理'

        return self.__base_crawl_func(page_num, url_base, host, id_anonymous,
                                      name_anonymous)

    def crawl_yqie(self):
        '''crawl proxy ip from yqie website'''
        page_num = 1
        url_base = "http://ip.yqie.com/ipproxy.htm"
        host = "ip.yqie.com"
        id_anonymous = 4
        name_anonymous = '高匿'

        return self.__base_crawl_func(page_num, url_base, host, id_anonymous,
                                      name_anonymous)

    def crawl_yundaili(self):
        '''crawl proxy ip from yundaili website'''
        page_num = 7
        url_base = "http://www.ip3366.net/?stype=1&page={}"
        host = "www.ip3366.net"
        id_anonymous = 3
        name_anonymous = '高匿代理IP'

        return self.__base_crawl_func(page_num, url_base, host, id_anonymous,
                                      name_anonymous)


if __name__ == "__main__":
    crawler = Crawler(host="localhost", port="6379", key="Proxy")
    crawler.run()
