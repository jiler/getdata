# -*- coding: utf-8 -*-
from threading import Thread
import urllib2
import chardet

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
def get_code(real_url):
    html='html'
    try:
        #伪装成浏览器
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(url=real_url,headers=headers)
        #读取
        page = urllib2.urlopen(req)
        html = page.read()
        page.close()
        #获取页面编码
        auto_detect_code = chardet.detect(html).get('encoding','utf-8')##通过第3方模块来自动提网页的编码
        #print '当前页面编码：'+auto_detect_code
        #根据页面编码，转码
        html = html.decode(auto_detect_code,'ignore').encode('utf-8')##先转换成unicode编码，然后转换系统编码输出
    except Exception, e:
        print e
        #print '出错啦，出错啦'
    finally:
        return html

def decorate(url):
    try:
        return get_code(url)
    except Exception,e:
        print e
        return 'html'


@timelimited(60)
def get_total_code(url1):
    html='html'
    try:
        #伪装成浏览器
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(url=url1,headers=headers)
        #读取
        page = urllib2.urlopen(req)
        html = page.read()
        page.close()
    except Exception, e:
        print e
        #print '出错啦，出错啦'
    finally:
        return html

def decorate_total(url1):
    try:
        return get_total_code(url1)
    except Exception,e:
        print e
        return 'html'

@timelimited(60)
def get_real_url(link):
    real_url='link'
    try:
        real_url=urllib2.urlopen(link).geturl()

    except Exception, e:
        print e
        #print '出错啦，出错啦'
    finally:
        return real_url

def decorate_realurl(link):
    try:
        return get_real_url(link)
    except Exception,e:
        print e
        return 'link'
