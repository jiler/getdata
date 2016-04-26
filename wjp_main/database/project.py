# coding=utf-8
__author__ = 'lenovo'
# 导入:
from sqlalchemy import Column, String, DATE, DATETIME, INTEGER
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义project对象:
class Project(Base):
    # 表的名字:
    __tablename__ = 'spacider_project'
    id = Column(INTEGER, primary_key=True)
    pname = Column(String)
    keywords = Column(String)
    project_type = Column(INTEGER)
    locate = Column(INTEGER)
    exhibition_type = Column(String)
    start_time =Column(DATE)
    end_time =Column(DATE)
    area = Column(INTEGER)
    com_num_local = Column(INTEGER)
    com_num_provin = Column(INTEGER)
    com_num_broad = Column(INTEGER)
    peo_num_local = Column(INTEGER)
    peo_num_provin = Column(INTEGER)
    peo_num_broad = Column(INTEGER)
    industry = Column(String)
    period = Column(INTEGER)
    status = Column(INTEGER)
    create_time=Column(DATETIME)
