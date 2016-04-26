# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WuchongItem(scrapy.Item):

    title = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    publish_time = scrapy.Field()
    source_site = scrapy.Field()
    source_site_url = scrapy.Field()
    source_url = scrapy.Field()
    spider_from = scrapy.Field()
    crawler_time = scrapy.Field()
    project_id = scrapy.Field()
    site_property_id = scrapy.Field()
    flag = scrapy.Field()#是否丢弃当前文章
