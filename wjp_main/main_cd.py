# coding=utf-8

__author__ = 'lenovo'
import sys
sys.path.append('/home/csc/getdata')



import datetime
import time

from function import get_search_engine_result
from config import DBSession
from database.project import Project
from database.status import Status


session = DBSession()
time_now = time.strftime("%Y-%m-%d %H:%M:%S")
print '当前时间：',time_now
#从项目表中查 当前需要爬取的项目
projects = session.query(Project.id, Project.pname, Project.keywords,Project.create_time,Project.period,Project.status).filter().all()
session.commit()
session.close()
duplicate_num = 0
new_num = 0
for project in projects:
    #print 'type:', type(project)
    pid  = project.id
    #print 'name:', project.pname.encode("utf8")
    #print 'keywords:', project.keywords.encode("utf8")
    ptitle = project.pname.encode("utf8").strip().replace(' ', '%20')
    status  = project.status
    #print '项目创建时间：',project.create_time
    #print '项目结束时间：',project.create_time+datetime.timedelta(days=project.period)
    #print '当前时间：',time_now
    if (str(project.create_time+datetime.timedelta(days=project.period))<time_now):
        if status!=3:
            #修改数据库状态
            session1 = DBSession()
            session1.query(Project).filter(Project.id == pid).update({Project.status: 3})
            session1.commit()
            session1.close()
        continue
    if status!=1:
        #不是运行状态
        continue

    #print 'hello'
    #key_words = str(ra w_input('请输入要评估的词语:\n'))
    url1 = 'http://www.baidu.com/s?wd='+ptitle
    #print url1

    #keywords =['常态','出发','成都','会展','作为']
    keywords = project.keywords.encode("utf8").split("|")
    #print keywords[0]


    for i in range(0,76):
        #print '这是第',i+1,'个网页。'
        #返回一个list，包含，url ，两个字典：url字典和媒体字典
        listssss = get_search_engine_result.decorate_get_search_engine_result(url1, keywords, pid)
        #重新更新数据
        if(url1 == listssss[0]):
            print '搜索引擎界面访问失败。'
            listssss = get_search_engine_result.decorate_get_search_engine_result(url1, keywords, pid)
            if(url1 == listssss[0]):
                listssss[0] = ''
                print '两次尝试，访问搜索引擎界面失败，现放弃此项目。'+project.pname.encode("utf8")

        url1 = listssss[0]
        duplicate_num = duplicate_num + listssss[1]
        new_num = new_num + listssss[2]

        #print '下一页网址：', listssss[0]
        #print '新增：', listssss[1]
        #print '重复：', listssss[2]

        if url1=='':
            print '一个项目结束。'
            break


session2 = DBSession()
today_date = time.strftime("%Y-%m-%d")
statuss = Status(today = today_date, new_data = new_num, duplicate_data = duplicate_num)
session2.add(statuss)
session2.commit()
session2.close()
