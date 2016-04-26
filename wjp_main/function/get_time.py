# coding=utf-8
__author__ = 'lenovo'

import re
from threading import Thread

class TimeoutException(Exception):
    pass

ThreadStop = Thread._Thread__stop#获取私有函数

def timelimited(timeout):
    def decorator(function):
        def decorator2(*args,**kwargs):
            class TimeLimited(Thread):
                def __init__(self,_error= None,):
                    Thread.__init__(self)
                    self._error =  _error

                def run(self):
                    try:
                        self.result = function(*args,**kwargs)
                    except Exception,e:
                        self._error =e

                def _stop(self):
                    if self.isAlive():
                        ThreadStop(self)

            t = TimeLimited()
            t.start()
            t.join(timeout)

            if isinstance(t._error,TimeoutException):
                t._stop()
                raise TimeoutException('timeout for %s' % (repr(function)))

            if t.isAlive():
                t._stop()
                raise TimeoutException('timeout for %s' % (repr(function)))

            if t._error is None:
                return t.result

        return decorator2
    return decorator

@timelimited(60)
def get_time(html):
    #print '获取时间'
    time = []

    zhengze = ['\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}','\d{4}-\d{2}-\d{2} \d{2}:\d{2}',
              '\d{4}/\d{2}/d{2} d{2}:d{2}:d{2}'#,'\d{4}-\d{1}-\d{2} \d{2}:\d{2}:\d{2}'
        ,'\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}:\d{2}','\d{4}年\d{2}月\d{2}日 \d{2}:\d{2}'
              ,'\d{4}年\d{2}月\d{2}日\d{2}:\d{2}'
               ,'\d{4}年\d{2}月\d{2}日 \d{2}时\d{2}分','\d{4}-\d{2}-\d{2}','\d{4}年\d{2}月\d{2}日']

    for zhengze_every in zhengze:
        patten = re.compile(zhengze_every)
        time = re.findall(patten, html)
        if len(time)!=0 :
            #提取数字，格式化
            #多个时间的情况，取第一个时间。
            if len(time)>1:
                for e_time in time:
                    time[0] = filter(str.isdigit, e_time)
                    #print '多个时间，取第1个：',time[0]
                    #将得到的时间进行格式化，
                    while len(time[0]) < 14 :
                        time[0] = time[0]+'0'
                    break
            else:
                time[0] = filter(str.isdigit, time[0])
                while len(time[0]) < 14 :
                        time[0] = time[0]+'0'
            break
        #如果没有得到时间，则设置空，



    #返回文章标题。
    # 再根据flag，确定是否爬取标题。


    if len(time)==0 :
        time = ['00000000000000']
    return time[0]

def decorate_get_time(html):
    try:
        return get_time(html)
    except Exception,e:
        print e
        return '00000000000000'

#print get_time('http://www.chengdu.gov.cn/zt/1/detail.jsp?id=764991')
#print get_time('http://www.qgtjh.com/news.asp?tid=&id=821')
