# -*- coding: utf-8 -*-

from flask import Flask, request
from RedisClient import RedisClient

app = Flask(__name__, static_url_path='')

HOST = ''
PORT = ''
KEY = ''
MONI_PORT = ''


@app.route('/', methods=['GET', 'POST'])
def do_response():
    redis = RedisClient(host=HOST, port=PORT, key=KEY)
    RANDOM = str(redis.random())
    RANDOM_MAX = str(redis.random_max())
    ALL = redis.all()
    all = ''
    for ip in ALL:
        all += str(ip) + "<br />"
    ALL = all
    ALL_MAX = redis.all_max()
    all = ''
    for ip in ALL_MAX:
        all += str(ip) + "<br />"
    ALL_MAX = all
    COUNT = str(redis.count())
    WRONG = 'Sorry,wrong name or wrong password,try again...'
    if request.method == "GET":
        name = request.args.get("name", "")
        password = request.args.get("password", "")
        method = request.args.get("method", "")
        if not name:
            return app.send_static_file("index.html")
        if name == "yooongchun" and password == "121561":
            if method == "random":
                return RANDOM
            elif method == "random_max":
                return RANDOM_MAX
            elif method == "all":
                return ALL
            elif method == "count":
                return COUNT
            elif method == "all_max":
                return ALL_MAX
            else:
                return WRONG
        else:
            return WRONG
    if request.method == "POST":
        name = request.form['name']
        password = request.form['password']
        method = request.form['method']
        if name == "yooongchun" and password == "121561":
            if method == "random":
                return RANDOM
            elif method == "random_max":
                return RANDOM_MAX
            elif method == "all":
                return ALL
            elif method == "count":
                return COUNT
            elif method == "all_max":
                return ALL_MAX
            else:
                return WRONG
        else:
            return WRONG


class API(object):
    def __init__(self,
                 host="localhost",
                 port='6379',
                 key='Proxy',
                 moni_port=9999):
        self.__redis = RedisClient(
            host=host, port=port, password=None, key=key)
        self.__port = moni_port
        self.__host = host
        self.__db_port = port
        self.__key = key

    def __message(self, method):
        if method == "random":
            return self.__redis.random()
        elif method == "random_max":
            return self.__redis.random_max()
        elif method == "all":
            return self.__redis.all()
        elif method == "all_max":
            return self.__redis.all_max()
        elif method == "count":
            return self.__redis.count()
        else:
            return "Sorry,wrong name or wrong password,try again..."

    def run(self):
        self.__set_api()
        app.run(host="0.0.0.0", port=self.__port)

    def __set_api(self):
        global HOST
        global PORT
        global KEY
        global MONI_PORT

        HOST = self.__host
        PORT = self.__db_port
        KEY = self.__key
        MONI_PORT = self.__port


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999)
