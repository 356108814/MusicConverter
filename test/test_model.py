# encoding: utf-8
"""

@author Yuriseus
@create 2016-8-4 11:15
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine, Index

Base = declarative_base()
db_url = 'mysql+pymysql://root:root@localhost:3306/test'
engine = create_engine(db_url, echo=True)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer(), primary_key=True)
    name = Column(String(32))
    sex = Column(String(1))
    age = Column(Integer())

Index('my_index', User.name, User.sex)    # 联合索引


if __name__ == '__main__':
    Base.metadata.create_all(engine)
