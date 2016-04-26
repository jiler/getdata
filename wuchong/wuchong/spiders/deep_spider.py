# -*- coding: utf-8 -*-

import scrapy
import time
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from wuchong.items import WuchongItem
class Article(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    publish_time = scrapy.Field()
    source_site = scrapy.Field()

class DeepSpider(CrawlSpider):
    name = "Deep"

    def __init__(self,rule, id, keywords):

        self.id = id
        self.keywords = keywords
        self.rule = rule
        self.attr_id = rule.attr_id
        self.name = rule.name
        self.allowed_domains = rule.allow_domains.split(",")
        self.start_urls = rule.start_urls.split(",")
        rule_list = []
        #添加`下一页`的规则
        if self.rule.next_page:
            rule_list.append(Rule(LinkExtractor(restrict_xpaths = self.rule.next_page)))
        #添加抽取文章链接的规则
        rule_list.append(Rule(LinkExtractor(
            allow=[rule.allow_url],
            restrict_xpaths = [rule.extract_from]),
            callback='parse_item'))
        self.rules = list(rule_list)
        super(DeepSpider, self).__init__()


    def parse_item(self, response):
        self.log('Hi, this is an article page! %s' % response.url)

        items = WuchongItem()


        title = response.xpath(self.rule.title_xpath).extract()
        # 判断标题是否包含关键字 如果包含，那就带个标识1，标识存储，否则是0，不存储。
        flag = self.keywords_judge(title[0].encode("utf-8"), self.keywords.split('|'))
        if flag==0 :
            items["flag"]=0

        else:
            #print '符合记录--parse_item--',self.id,'-------',title[0].encode("utf-8")

            items["flag"]=1
            items["title"] = title[0]
            items["url"] = response.url

            body = response.xpath(self.rule.body_xpath).extract()
            items["body"] = '\n'.join(body) if body else ""

            pub_time = response.xpath(self.rule.publish_time_xpath).extract()
            # 过滤时间，使其符合标准。
            if pub_time:

                pu_time = pub_time[0].encode("utf8")
                p_time = filter(str.isdigit, pu_time)
                while len(p_time) < 14 :
                    p_time = p_time+'0'
                items["publish_time"] = p_time
            else:
                items["publish_time"]=time.strftime("%Y%m%d%H%M%S")
            # 如果是第二次爬取，发布时间是昨天，则继续，如果小于昨天，则结束。rule.next_page 置空，当然，数据库中不变。

            source_site = response.xpath(self.rule.source_site_xpath).extract()
            items["source_site"] = source_site[0] if source_site else ""

            items["project_id"] = self.id

            items["site_property_id"] = self.attr_id
        return items

    def keywords_judge(self, titles, keywords):
        #print 'keywords_judge----',self.id,'-------',titles,'-------',keywords[0]

        related_flag = 1
        must_key_flag = 1
        #循环每个必要的关键字

        for must_key in keywords:
            must_key=must_key.encode("utf-8")
            if must_key_flag == 0:
                break
            must_key_flag = 0
            #切分必要的关键字
            same_mean_keys = must_key.split()
            #循环切分好的关键字
            for key in same_mean_keys:
                if titles.find(key) != -1:
                    must_key_flag = 1
                    break


        if must_key_flag == 0:
            related_flag = 0

        return related_flag








