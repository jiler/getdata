#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'lenovo'
import re
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
def get_location(domain):
    #print '获取地理位置'
    #返回的省简称代码
    province_name = '北京'
    #初始化各省字典(不包含 港澳台，港澳台在维护列表中)
    province_dict = {'京':'北京','津':'天津','沪':'上海','渝':'重庆','冀':'河北','豫':'河南','云':'云南','滇':'云南','辽':'辽宁','黑':'黑龙江','湘':'湖南',
                '皖':'安徽','鲁':'山东','新':'新疆','苏':'江苏','浙':'浙江','赣':'江西','鄂':'湖北','桂':'广西','甘':'甘肃','陇':'甘肃','晋':'山西',
                '蒙':'内蒙古','陕':'陕西','秦':'陕西','吉':'吉林','闽':'福建','贵':'贵州','黔':'贵州','粤':'广东','青':'青海','藏':'西藏','川':'四川','蜀':'四川','宁':'宁夏','琼':'海南'}

    #将域名组成网址
    address = 'http://'+domain
    #打开页面
    try:
        #伪装成浏览器
        headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
        req = urllib2.Request(url=address,headers=headers)
        #读取
        page = urllib2.urlopen(req)
        html = page.read()
        page.close()
        #获取页面编码
        auto_detect_code = chardet.detect(html).get('encoding','utf-8')##通过第3方模块来自动提网页的编码
        #print '当前页面编码：',auto_detect_code
        #根据页面编码，转码
        html = html.decode(auto_detect_code,'ignore').encode('utf-8')##先转换成unicode编码，然后转换系统编码输出
        #print html
        #各种正则表达式
        locations_zhengze = ['[\x80-\xff]{3}ICP', 'ICP证：[\x80-\xff]{3}','ICP证 [\x80-\xff]{3}',
                             'ICP证[\x80-\xff]{3}','增值电信业务经营许可证：[\x80-\xff]{3}',
                             '增值电信业务经营许可证:[\x80-\xff]{3}','ICP证:[\x80-\xff]{3}']
        #编写一个字典，相当于提取结果用的switch
        get_simple_name = {0:lambda x: x.decode('utf8')[0].encode('utf8'),
                  1:lambda x: x.decode('utf8')[-1].encode('utf8'),#里面lambda的意思是参数x
                  2:lambda x: x.decode('utf8')[-1].encode('utf8'),
                  3:lambda x: x.decode('utf8')[-1].encode('utf8'),
                  4:lambda x: x.decode('utf8')[-1].encode('utf8'),
                  5:lambda x: x.decode('utf8')[-1].encode('utf8'),
                  6:lambda x: x.decode('utf8')[-1].encode('utf8')}
        i = 0
        #每一个正则表达式都走一遍
        for location_every in locations_zhengze:
            patten = re.compile(location_every)
            #得到匹配结果
            get_simple_pattern = re.findall(patten, html)
            #如果结果不为空，说明匹配到了
            if len(get_simple_pattern)!=0 :

                #print get_simple_pattern[-1]
                #根据当前循环的是哪个正则表达式，按照其特性，提取简称
                simple_name = get_simple_name[i](get_simple_pattern[-1])
                #print simple_name
                if simple_name in province_dict:
                   province_name = province_dict[simple_name]
                break

            i = i+1
    except Exception, e:
        print e
        #print '出错啦，出错啦'


    return province_name

def decorate_get_location(domain):
    try:
        return get_location(domain)
    except Exception,e:
        print e
        return 'location'



#print get_location('www.daytcj.com/news/html/?792.html') 编码识别有误。

