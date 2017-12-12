# encoding: utf-8
"""
db
@author Yuriseus
@create 2016-8-1 11:41
"""
import pymssql


class DBHelper(object):
    def __init__(self):
        self._server = '172.16.1.8'
        self._user = 'shiyong'
        self._password = 'shiyong123456'
        self._db = 'minik'

    def conn(self):
        conn = pymssql.connect(self._server, self._user, self._password, self._db, charset='utf8')
        return conn

    def query(self, sql):
        """
        查询
        :param sql:
        :return: list(dict)
        """
        conn = self.conn()
        cursor = conn.cursor(as_dict=True)
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows


if __name__ == '__main__':
    db_helper = DBHelper()
    singers = db_helper.query('SELECT top 10 * FROM mk_singer')
    for singer in singers:
        print("ID=%d, Name=%s" % (singer['id'], singer['name']))

