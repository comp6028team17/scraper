# -*- coding: utf-8 -*-

import scrapy
from scrapy import Field, Item

class DocumentItem(Item):
	url = Field()
	topics = Field()
	hierarchy = Field() 
	wordcounts = Field()
	words = Field()
	html = Field()
