# coding=utf-8
__author__ = 'lenovo'


from bs4 import BeautifulSoup
import time
import get_time
import keywords_judge
from function import get_code, get_articlename_websitename, get_ip_pv, get_location
from config import Redis
from config import DBSession
from database.domain import Domain
from database.article import Article


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

@timelimited(600)
def get_search_engine_result(url, keywords, pid):
    #读取整个页面
    duplicate_num = 0
    new_num = 0
    #print '将要访问搜索引擎界面。。。'
    page_message = get_code.decorate_total(url)
    if page_message=='html':
        #print '请求搜索引擎页面函数超时，放弃此页面'+url
        return [url, 0, 0]


    #封装成BeautifulSoup对象，
    soup = BeautifulSoup(page_message, from_encoding="utf-8")#这里设置编码只是为了加快速度，和准确度
    #对soup对象进行处理，找到class标签等于“t”的标签，（10条记录）
    websites = soup.find_all(attrs={"class": "t"})
    #将10条结果循环输出
    #print '将要10项结果的每一项。。。'
    for index, every_website in enumerate(websites):
        #print '将要访问某页搜索引擎10项结果中的第',index+1,'项。。。'
        #定义标题
        search_engine_title=''


        session = DBSession()

        #print '这里是要获取搜索引擎界面的文章名'
        #得到文章标题
        for every in every_website.a.contents:
            search_engine_title = search_engine_title + every.encode("utf-8")
        search_engine_title = search_engine_title.replace('<em>', '').replace('</em>', '')
        #print '这里是要判断是否包含关键字'

        #判断汉字标题是否包含必要的关键字。
        key_flag = keywords_judge.keywords_judge(search_engine_title, keywords)
        #如果不包含必要的关键字，则直接判断下一条

        #过滤掉“百度网站：百度百科，百度视频，百度知道等等，优酷网”
        cantlist = ['百度百科','百度视频','百度知道','百度贴吧','百度学术','优酷视频','新浪博客','腾讯微博','百度图片','微博']
        for index,cal in enumerate(cantlist):
            if search_engine_title.find(cantlist[index]) != -1:
                key_flag=0
                break



        #print '这里判断是否包含关键字，判断完毕'
        if key_flag == 0:
            #print '此条数据不包含必要的关键字。开始下一条。', search_engine_title
            continue

        #获取具体网站的链接
        search_engine_link = every_website.a['href']
        #转成真正的url
        #print '这里转变成真正的url2'
        #print search_engine_link
        #在这里，如果链接有问题，就会执行不下去，死等，一定消除这种情况。
        #因此，此处也用装饰器限制执行时间。
        real_url = get_code.decorate_realurl(search_engine_link)
        if real_url=='link':
            #print '请求实际url函数超时，放弃此页面'+search_engine_link
            continue

        #print '这里转变成真正的url3'



        #判断url是否已经存在与redis，若存在，则continue，查询下一条；存在，存储起来，继续。
        if Redis.exists('url:%s:%s' % (real_url, pid)):
            #print "Duplicate item found:", real_url
            duplicate_num = duplicate_num + 1
            continue
        #文章不存在
        else:
            #打开页面，获得页面内容，这样就获取一次，节约流量
            #这个函数是用装饰器，限制程序执行时间，让其在一分钟之内完成。
            html = get_code.decorate(real_url)
            if html=='html':
                #print '请求详细页面函数超时，放弃此页面'+real_url
                continue




            #通过url得到域名
            domain = real_url.split('/')[2]
            #print '域名是：'+domain



            #查询域名是否存在
            query = session.query(Domain.id).filter(Domain.domain==domain)
            session.commit()
            #域名不存在
            if query.count()<=0:

                #访问"转码后的网页"得到文章名和网站名的list
                article_website = get_articlename_websitename.decorate_get_articlename_websitename(html, keywords)
                #如果article_website[1]内容是“未知”，则网站名有问题。
                if article_website[0]=='aaa':
                    #print '未得到文章名和网站名。忽略。下一条。'
                    continue
                #初始化网站名字是否需要重新获取，默认是不需要
                website_flag = 0
                if article_website[1]== '未知':
                    website_flag = 1




                #得到网站所属的物理位置。也就是备案号。这里有问题。。。。。。。。。。。。。。。。。。。。。。
                #备案号，默认值是全国
                locate_place = get_location.decorate_get_location(domain)
                if locate_place=='location':
                    #print '请求位置函数超时，放弃此页面'+real_url
                    continue
                #根据得到的号码，查询数据库，得到最终的省份，数据库应该有的顺序见例子word中

                #根据域名得到ip/pv量
                #ip和pv默认值是0,网站名如果没获取到是空串。
                #返回的数字，是字符串的形式，里面有逗号，用filter函数过滤即可
                ip_pv_list = get_ip_pv.decorate_get_ip_pv(domain, website_flag)
                #第一个元素是ip量，第二个是pv量，第三个是网站名，也许不需要。
                if website_flag:
                    article_website[1] == ip_pv_list[2]

                #此处应该有根据时间过滤的函数。时间不对的话，结束本次循环
                #存储网站属性
                if domain.endswith("gov.cn"):
                    natures = 1
                else:
                    natures = 3
                d = Domain(domain=domain, site_name=article_website[1], locate=locate_place, nature=natures, ip=int(ip_pv_list[0]), pv=int(ip_pv_list[1]), flag =1)
                session.add(d)
                session.commit()
                query = session.query(Domain.id).filter(Domain.domain==domain).one()
                site_id = query.id

            else:

                #域名已经存在，则取出id关联文章
                site_id = query.one().id

                #访问"转码后的网页"得到文章名和网站名的list
                article_website = get_articlename_websitename.decorate_get_articlename_websitename(html, keywords)
                #如果article_website[1]内容是“未知”，则网站名有问题。
                if article_website[0]=='aaa':
                    #print '未得到文章名和网站名。忽略。下一条。'
                    continue


            #访问"转码后的网页"得到文章发布时间
            time_str = get_time.decorate_get_time(html)
            #如果time是14个0的字符串，则表示时间没找到。
            if(time_str.startswith('0')):
                continue
            #将得到的综合数据，写进数据库
            #存储文章
            time_now = time.strftime("%Y-%m-%d %H:%M:%S")
            a = Article(title=article_website[0], url=real_url, publish_time=time_str, spider_from=2, project_id=pid, site_property_id=site_id,crawler_time=time_now )
            session.add(a)
            session.commit()
            new_num = new_num + 1

            #将url放到redis数据库中
            Redis.set('url:%s:%s' % (real_url, pid), 1)

            session.close()

    next_page = 's'
    try:
        next_page = 'http://www.baidu.com'+soup.strong.next_sibling['href']


    except Exception, e:
        print e

    finally:
        return [next_page, duplicate_num, new_num]

def decorate_get_search_engine_result(url, keywords, pid):
    try:
        return get_search_engine_result(url, keywords, pid)
    except Exception,e:
        print e
        return [url, 0, 0]