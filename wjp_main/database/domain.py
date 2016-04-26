# coding=utf-8
__author__ = 'lenovo'

from sqlalchemy import Column, String, create_engine
from sqlalchemy import BIGINT, BINARY, BLOB, BOOLEAN, CHAR, DATE, \
        DATETIME, DECIMAL, DECIMAL, FLOAT, INTEGER, NCHAR, VARBINARY, \
        NUMERIC, NVARCHAR, REAL, SMALLINT, TEXT, TIME, TIMESTAMP,  VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Domain(Base):
    # 表的名字:
    __tablename__ = 'spacider_siteproperty'
    id = Column(INTEGER, primary_key=True)
    domain = Column(String)
    site_name = Column(String)
    locate = Column(String)
    nature =Column(SMALLINT)
    ip =Column(INTEGER)
    pv =Column(INTEGER)
    flag = Column(SMALLINT)
