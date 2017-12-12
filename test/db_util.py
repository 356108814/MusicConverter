# encoding: utf-8
"""
数据库工具类
@author Yuriseus
@create 2016-7-4 16:55
"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
from apscheduler.schedulers.blocking import BlockingScheduler
from test.test_model import User, Base


class DBUtil(object):
    def __init__(self):
        self._engine = create_engine('mysql+pymysql://root:root@localhost:3306/test', echo=True)
        self._session = None

    @property
    def engine(self):
        return self._engine

    def init_session(self):
        if not self._session:
            self._session = scoped_session(sessionmaker(bind=self._engine))
        return self._session

    def close_session(self):
        if self._session:
            self._session.remove()
            self._session = None

    def execute_sql(self, sqls):
        if isinstance(sqls, str):
            sqls = [sqls]
        try:
            for _, sql in enumerate(sqls):
                sql = text(sql)
                self._session.execute(sql)
            self._session.commit()
        except Exception as e:
            self._session.rollback()

    def query_all(self, cls, order_field=None):
        query = self._session.query(cls)
        if order_field:
            query.order_by(order_field)
        return query.all()

    def query_by_sql(self, sql):
        data_array = []
        sql = text(sql)
        result_proxy = self._session.execute(sql)
        for _, row in enumerate(result_proxy.fetchall()):
            data_array.append(row)
        return data_array

    def add_user(self):
        session = self.init_session()
        # ed_user = User(name='yuri', age=18)
        # session.add(ed_user)
        # session.commit()
        self.execute_sql('INSERT INTO user (name, age) VALUES ("yuri", 18)')
        print(self.query_by_sql('select * from user'))
        self.close_session()

    def interval_add(self):
        scheduler = BlockingScheduler()
        scheduler.add_job(self.add_user, 'interval', seconds=1)
        scheduler.start()


dbUtil = DBUtil()


if __name__ == '__main__':
    pass
    # dbutil = DBUtil()
    # scheduler = BlockingScheduler()
    # scheduler.add_job(dbutil.add_user, 'interval', seconds=1)
    # scheduler.start()

    # Base.metadata.create_all(dbutil.engine)
    u = {'name': 'yuri', 'age': 20}
    # ed_user = User(name='yuri', age=18)
    user = User(**u)
    session = dbUtil.init_session()
    session.add(user)
    session.commit()
    print(session.query(User).all())





