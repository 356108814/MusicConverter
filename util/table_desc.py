# encoding: utf-8
"""
mysql表转ORM模型
@author Yuriseus
@create 2016-9-3 13:50
"""
from coffeebean.db_mysql import DBMySQL
from util.parser import ParserUtil


class TableDescUtil(object):
    def __init__(self):
        self.db = DBMySQL('localhost', 3306, 'root', 'root', 'hs_office')

    def table_2_sqlalchemy_model(self, table_name):
        result = ''
        sql = 'DESC %s' % table_name
        orm_columns = []
        columns = self.db.query(sql)
        for column in columns:
            field = column['Field']
            key = column['Key']
            type_str = str(column['Type'])
            if type_str.find('(') != -1:
                tg = ParserUtil.re_group(type_str, '(?P<type>\w+)\((?P<len>\d+)\)')
                if tg:
                    ct = tg['type']
                    cl = ''
                    if 'len' in tg:
                        cl = tg['len']
                else:
                    ct = type_str
                    cl = ''
            else:    # 没有长度的，如datetime text
                ct = type_str
                cl = ''
            cd = {'field': field}
            if ct in ['int', 'tinyint']:
                cd['type'] = 'Integer'
                cl = ''
            elif ct in ['char', 'varchar']:
                cd['type'] = 'String'
            elif ct == 'datetime':
                cd['type'] = 'DateTime'
            elif ct == 'text':
                cd['type'] = 'TEXT'
            cd['len'] = cl
            cd['is_pri'] = (key == 'PRI')    # 是否为主键
            orm_columns.append(cd)
        for c in orm_columns:
            if c['is_pri']:
                c_str = '%s = Column(%s(%s), primary_key=True)\n'
            else:
                c_str = '%s = Column(%s(%s))\n'
            c_str = c_str % (c['field'], c['type'], c['len'])
            result += c_str
        return result


if __name__ == '__main__':
    util = TableDescUtil()
    print(util.table_2_sqlalchemy_model('dictionary'))
