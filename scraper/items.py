# -*- coding: utf-8 -*-

import scrapy


class DmozItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    topics = scrapy.Field()

class DmozSiteItem(scrapy.Item):
	url = scrapy.Field()
	topics = scrapy.Field()
	wordcounts = scrapy.Field()
	words = scrapy.Field()
	html = scrapy.Field()
