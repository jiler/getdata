# coding=utf-8

__author__ = 'lenovo'
import sys
sys.path.append('/home/csc/getdata')

from config import DBSession
from database.domain import Domain
from function import get_ip_pv
import time


time_now = time.strftime("%Y-%m-%d %H:%M:%S")
print '当前时间：',time_now
session = DBSession()
websites = session.query(Domain.id, Domain.domain,Domain.ip,Domain.pv).filter().all()
session.commit()
session.close()
index = 0
for website in websites:
    index += 1
    time.sleep(60)
    print index,  website.domain, 'Start'
    lists = get_ip_pv.decorate_get_ip_pv(website.domain, 0)
    if not lists:
        continue
    #if (lists[0] == '-' or lists[1] == '-'):
    #    print index,  'No data, Finished'
    #    continue
    try:
        ip = int(lists[0])
        pv = int(lists[1])
    except:
        print index,  'No data, Finished'
        continue
    session1 = DBSession()
    session1.query(Domain).filter(Domain.id==website.id).update({Domain.ip:ip, Domain.pv:pv})
    session1.commit()
    session1.close()
    print index,  lists[2], ip, pv, 'Finished'

print '项目结束'



