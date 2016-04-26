# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import redis

databasenames='chengdu'
usernames='bolanju'
passwords='123456'
hosts = 'localhost'
# 初始化数据库连接:
engine = create_engine('mysql+mysqldb://%s:%s@%s:3306/%s?charset=utf8' % (usernames,passwords,hosts,databasenames))
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 初始化redis数据库连接
Redis = redis.StrictRedis(host='localhost', port=6379, db=0)
