# -*- coding: utf-8 -*-

import sys
sys.path.append('/home/csc/getdata')


from wuchong.spiders.deep_spider import DeepSpider
from model.config import DBSession
from model.rules import Rules
from model.project import Project

# scrapy api
from scrapy import signals, log
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy.settings import Settings
import time

#定义爬取列表
RUNNING_CRAWLERS = []

#spider关闭后，移出爬取列表
def spider_closing(spider):
    """Activates on spider closed signal"""
    log.msg("Spider closed: %s" % spider, level=log.INFO)
    RUNNING_CRAWLERS.remove(spider)
    if not RUNNING_CRAWLERS:
        reactor.stop()


time_now = time.strftime("%Y-%m-%d %H:%M:%S")
print '当前时间：',time_now


#定义日志信息
#log.start(loglevel=log.DEBUG)

settings = Settings()
settings.set("USER_AGENT", "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36")
settings.set("ITEM_PIPELINES" , {
    'wuchong.pipelines.DuplicatesPipeline': 200,
    # 'pipelines.CountDropPipline': 100,
    'wuchong.pipelines.DataBasePipeline': 300
})
dbp = DBSession()
nump = dbp.query(Project).filter(Project.status == 1).distinct().count()
if nump==0:
    print '暂时没有可运行的项目'
    dbp.commit()
    dbp.close()
    exit()

dbr = DBSession()
numr = dbr.query(Rules).filter(Rules.enable == 1).distinct().count()
if numr==0:
    print '暂时没有可运行的规则网站'
    dbr.commit()
    dbr.close()
    exit()


# 查询数据库，传参数，开始运行。
db1 = DBSession()
projects = db1.query(Project).filter(Project.status == 1)

db1.commit()
db1.close()

db2 = DBSession()
rules = db2.query(Rules).filter(Rules.enable == 1)
db2.commit()
db2.close()


for pro in projects:
    for rule in rules:
        print 'this is  project',pro.id
        crawler = Crawler(settings)
        spider = DeepSpider(rule, pro.id, pro.keywords)  # instantiate every spider using rule
        RUNNING_CRAWLERS.append(spider)

        # stop reactor when spider closes
        crawler.signals.connect(spider_closing, signal=signals.spider_closed)
        crawler.configure()
        crawler.crawl(spider)
        crawler.start()




# blocks process so always keep as the last statement
reactor.run()














