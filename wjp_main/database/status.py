# coding=utf-8
__author__ = 'lenovo'
# 导入:
from sqlalchemy import Column, String, DATE, DATETIME, INTEGER
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义project对象:
class Status(Base):
    # 表的名字:
    __tablename__ = 'spacider_status'
    id = Column(INTEGER, primary_key=True)
    today =Column(DATE)
    new_data = Column(INTEGER)
    duplicate_data = Column(INTEGER)