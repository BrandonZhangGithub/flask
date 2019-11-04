# coding: utf-8
from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.dialects.mysql.enumerated import ENUM
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata

class Order(Base):
    __tablename__ = 'order'

    oid = Column(Integer, primary_key=True)
    uid = Column(Integer)
    brand = Column(String(64))
    ctype = Column(String(64))
    price = Column(Float)
    by_at = Column(DateTime)


class User(Base):
    __tablename__ = 'user'

    uid = Column(Integer, primary_key=True)
    name = Column(String(64))
    idcard = Column(String(18))
    sex = Column(ENUM('男', '女', '保密'))
