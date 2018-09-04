from pymysql import connect
class Mysqlp(object):
    def __init__(self, database, host='localhost',
                 user='root', password='123456',
                 port=3306, charset='utf8'):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.database = database
        self.charset = charset

    def open(self):
        self.conn = connect(host=self.host, port=self.port,
                            user=self.user, password=self.password,
                            database=self.database, charset=self.charset)

        self.cur = self.conn.cursor()

    def close(self):
        self.cur.close()
        self.conn.close()

    def action(self, sql, L=[]):
        self.open()
        try:
            self.cur.execute(sql, L)
            self.conn.commit()
            

        except Exception as e:
            self.conn.rollback()
            print('error ==> ', e)
        else:
            return 'done'
        finally:
            self.close()


    def all(self, sql, L = []):
        self.open()
        try:
            self.cur.execute(sql, L)
            res = self.cur.fetchall()
            self.conn.commit()
            print('数据库语句执行结束!')
            return res
        except Exception as e:
            self.conn.rollback()
            print('error ==> ', e)
        finally:
            self.close()

    def get_page(self, sql_select, sql_size, L1 = [], L2 = []):
        self.open()
        try:
            self.cur.execute(sql_select, L1)
            res = self.cur.fetchall()
            self.cur.execute(sql_size, L2)
            size = self.cur.fetchone()
            self.conn.commit()
            print('分页获取完毕')
            return (size, res)
        except Exception as e:
            self.conn.rollback()
            print('error ==> ', e)
        finally:
            self.close()
