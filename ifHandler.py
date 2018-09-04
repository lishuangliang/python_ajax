from Mysqlpython import Mysqlp
from time import time
import json

sql_list = {
    'get_user': 'select * from user where name=%s',
    'put_user': 'insert into user(name, pwd) values(%s, %s)',
    'put_user_default': 'insert into user(name) values(%s)',
    'search_word': 'select * from words where word=%s',
    'put_word_hist': 'insert into hist(name, word, date) values(%s, %s, %s)',
    'get_word_hist': 'select word,date from hist where name=%s limit %s, %s',
    'get_word_hist_size' : 'select count(id) from hist where name=%s',
    'get_word_hist_2' : 'select (select count(id) from hist where name=%s) as total, word, date from hist where name=%s limit %s, %s'
}


class InterferHandler(object):
    def __init__(self):
        self.sqlh = Mysqlp('dict')
        self.sql_list = sql_list

    def get_user(self, name):
        sql_select = self.sql_list['get_user']
        data = self.sqlh.all(sql_select, [name])
        return data

    def do_login(self, args):
        # 登录

        data_list = args.decode().split('&')
        name = data_list[0].split('=')[1]
        pwd = data_list[1].split('=')[1]

        try:
            data = self.get_user(name)
        except Exception as e:
            print('error-->', e)

            return '{"code":505, "data":{}, "msg":"服务器异常，请稍后重试"}'

        print(data)

        if not data:
            return '{"code":201, "data":{}, "msg":"没有该用户"}'

        else:
            if name == data[0][1] and pwd == data[0][2]:
                return '{"code":200, "data":{}, "msg":"OK"}'
            else:
                return '{"code":202, "data":{}, "msg":"密码错误"}'

    def do_regist(self, args):
        # 注册
        print('args', args)
        data_list = args.decode().split('&')
        name = data_list[0].split('=')[1]
        pwd = data_list[1].split('=')[1]

        try:
            data = self.get_user(name)
        except Exception as e:
            print('error-->', e)
            return '{"code":505, "data":{}, "msg":"服务器异常，请稍后重试"}'

        if data:
            return '{"code":201, "data":{}, "msg":"该用户已存在，请直接登录"}'

        print('data', data)
        try:
            if pwd == 'null':
                sql_insert = self.sql_list['put_user_default']
                self.sqlh.action(sql_insert, [name])
            else:
                sql_insert = self.sql_list['put_user']
                self.sqlh.action(sql_insert, [name, pwd])
        except Exception as e:
            print('error-->', e)
            return '{"code":505, "data":{}, "msg":"服务器异常，请稍后重试"}'
        else:
            return '{"code":200, "data":{}, "msg":"OK"}'

    def do_search_word(self, args):
        data_list = args.decode().split('&')
        name = data_list[0].split('=')[1]
        word = data_list[1].split('=')[1]

        sql_select = self.sql_list['search_word']

        try:
            data = self.sqlh.all(sql_select, [word])
        except Exception as e:
            print('error-->', e)
            return '{"code":505, "data":{}, "msg":"服务器异常，请稍后重试"}'
        else:
            if not data:
                return '{"code":505, "data":{}, "msg":"无当前查询单词解释"}'
            else:
                self.do_put_word_hist(name, word)
                return '{"code":200, "data":{"desc" :"%s"}, "msg":"OK"}' % data[0][2]

    def do_put_word_hist(self, name, word):
        print('do_put_word_hist1')
        strtime = str(time())
        sql_insert = self.sql_list['put_word_hist']
        try:
            self.sqlh.action(sql_insert, [name, word, strtime])
            print('do_put_word_hist2')
        except Exception as e:
            print('error-->', e)
            return '{"code":505, "data":{}, "msg":"服务器异常，请稍后重试"}'
        else:
            return '{"code":200, "data":{}, "msg":"OK"}'
        print('do_put_word_hist3')

    def do_search_hist(self, args):
        data_list = args.decode().split('&')
        name = data_list[0].split('=')[1]
        pageSize = int(data_list[1].split('=')[1])
        pageNum = data_list[2].split('=')[1]

        
        startPageNum = (int(pageNum) - 1) * 10
        print(startPageNum, pageSize)

        sql_select = self.sql_list['get_word_hist_2']

        try:   
            res = self.sqlh.all(sql_select, [name, name, startPageNum, pageSize])
        except Exception as e:
            print('ifHandler error-->', e)
            return '{"code":505, "data":{}, "msg":"服务器异常，请稍后重试"}'
        else:
            res_dict = {}
            res_data = []

            res_dict['pageSize'] = res[0][0]
            for total, word, date in res:
                curr_obj = {}
                curr_obj["word"] = word
                curr_obj["t"] = date
                res_data.append(curr_obj)
            res_dict['data_list'] = res_data
            # print(res_dict)
            return '{"code":200, "data":"%s", "msg":"OK"}' % str(res_dict)
