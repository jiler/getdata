#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lenovo'

import title_split
from bs4 import BeautifulSoup
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
def get_articlename_websitename(html, keywords):

    #print '获取文章名字和网站名字'
    article_website_name = ['aaa','未知']
    try:
        #根据页面编码，确定打开url的编码，查询title
        soup = BeautifulSoup(html, from_encoding="utf-8")#这里设置编码只是为了加快速度，和准确度
        title = str(soup.title).replace('<title>', '').replace('</title>', '')
        #print title
        #将title切分
        article_website_name = title_split.title_split(title, keywords)
        #返回website和article的list
    except Exception,e:
        print e

    return article_website_name


def decorate_get_articlename_websitename(html, keywords):
    try:
        return get_articlename_websitename(html, keywords)
    except Exception,e:
        print e
        article_website_name = ['aaa','未知']
        return article_website_name



#url = 'http://www.kaixian.tv/gd/2015/0515/849895.html'
# key_words = ['92届|2015年春|2015年成都','糖酒会|糖酒商品交易会']
#
#
#liss =  get_articlename_websitename(url, [])
#print liss[0], 'ssss'+liss[1]