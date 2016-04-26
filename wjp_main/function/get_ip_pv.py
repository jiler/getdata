#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lenovo'

#该方法摒弃了BeautifulSoup，使用selenium自动化测试工具+PhantomJs（虚拟浏览器，一个没有GUI的Safari）
#主要解决页面的Ajax数据获取

import urllib2
from bs4 import BeautifulSoup
from threading import Thread
from selenium import webdriver
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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
def get_ip_pv(domain, website_flag):
    #print '获取网站的ip/pv量'
    ip_pv = ['0','0','未知']
    ip_pv_url = 'http://www.alexa.cn/index.php?url='+domain
    #打开页面
    sitename = ''
    driver = webdriver.PhantomJS(executable_path='phantomjs')
    try:
        #读取
        #page = urllib2.urlopen(ip_pv_url)
        #html = page.read()
        #page.close()
        #soup = BeautifulSoup(html, 'lxml',from_encoding="utf-8")#这里设置编码只是为了加快速度，和准确度
        #driver = webdriver.PhantomJS(executable_path='phantomjs')  #这要需要制定phatomjs可执行文件的位置
	driver.get(ip_pv_url)
	#print soup
        #if website_flag:
            #sitename = soup.find("font").text.rstrip().decode('utf8')#rstrip()除右边空格
            #find_element查一个，find_elements查多个，这里要查的font恰好是第一个
            #print driver.find_element_by_class_name("biaoge").text.rstrip().decode('utf8');
        sitename = driver.find_element_by_tag_name("font").text.rstrip().decode('utf8');         
	    #这两行是这是得到名字的方式
            # for every_website in sitenames:
            #     print 'sitename:'+every_website.contents[0]
            #
            #这行是为了得到名字
            #print sitename
            #如果网站名包含汉字，则返回，如果不包含汉字，则放弃
            #if len(sitename)==len(sitename.decode('utf8')):
            #  sitename = '未知'


        #这里有两个结果：“日均 IP 访问量[一周平均]”和“日均 PV 浏览量[一周平均]”
        ip_str = driver.find_element_by_id('w_10').text
        pv_str = driver.find_element_by_id('w_11').text
        #ip_str = '54654'
        #pv_str = '789'
        #ip_str = ip_str.isdigit() and ip_str or 0 #c ? :
        #pv_str = pv_str.isdigit() and pv_str or 0
        ip_pv = [ip_str, pv_str, sitename]
        driver.quit

    except Exception, e:
        driver.quit
        print 'get_ip_pv', e
        #print '出错啦，出错啦'

    return ip_pv

def decorate_get_ip_pv(domain, website_flag):
    try:
        return get_ip_pv(domain, website_flag)
    except Exception,e:
        print 'decorate_get_ip_pv', e
        return ['0','0','未知']
#
#aaa = decorate_get_ip_pv('www.baidu.com', 1)
#print aaa[0],aaa[1],aaa[2]
