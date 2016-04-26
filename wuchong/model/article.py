# -*- coding: utf-8 -*-
from sqlalchemy import Column, String, Integer, TEXT, DATETIME
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Article(Base):
    __tablename__ = 'spacider_article'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    body = Column(TEXT)
    publish_time = Column(DATETIME)
    source_site = Column(String)
    source_site_url = Column(String)
    source_url = Column(String)
    spider_from = Column(Integer)
    crawler_time = Column(DATETIME)
    project_id = Column(Integer)
    site_property_id = Column(Integer)
