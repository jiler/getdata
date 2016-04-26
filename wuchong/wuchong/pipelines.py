# -*- coding: utf-8 -*-


from scrapy.exceptions import DropItem
from model.config import DBSession
from model.config import Redis
from model.article import Article
import time

# 去重
class DuplicatesPipeline(object):
    def process_item(self, item, spider):
	# 判断item是否是所需要的文章。或者丢弃，或者存储
        # 如果需要存储，才查重。否则直接丢弃即可。
        if item["flag"]==1:

            if Redis.exists('url:%s:%s' % (item['url'],item['project_id'])):
                raise DropItem("Duplicate item found: %s" % item)
            else:
                Redis.set('url:%s:%s' % (item['url'], item['project_id']), 1)
                return item
        else:
            raise DropItem("Duplicate item found: %s" % item)

# 存储到数据库
class DataBasePipeline(object):
    def open_spider(self, spider):
        self.session = DBSession()

    def process_item(self, item, spider):
        a = Article(title=item["title"].encode("utf-8"),
                    url=item["url"],
                    body=item["body"].encode("utf-8"),
                    publish_time=item["publish_time"],
                    source_site=item["source_site"].encode("utf-8"),
                    spider_from=1,
                    crawler_time=time.strftime("%Y-%m-%d %H:%M:%S"),
                    project_id=item["project_id"],
                    site_property_id=item["site_property_id"])
        self.session.add(a)
        self.session.commit()
        #print 'process_item----',a.project_id,'--------',a.title
        return item

    def close_spider(self, spider):
        self.session.close()