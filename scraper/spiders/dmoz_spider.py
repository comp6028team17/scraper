import scrapy
import re
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from collections import Counter

from scraper.items import DocumentItem
import urllib
import sys


from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class DmozSpider(scrapy.Spider):
    name = "dmoz"

    def __init__(self, topic="Computers/Programming/Languages/Python/Web/Web_Frameworks", *args, **kwargs): 
        super(DmozSpider, self).__init__(*args, **kwargs) 
        
        self.start_urls = ["http://www.dmoz.org/"+topic]

        print "Spidering: "+self.start_urls[0]
    def parse(self, response):
        topics = [urllib.unquote(x).decode('utf8').replace('_', ' ') for x in response.url.split("/")[3:-1]]

        xpaths = ['//ul[@class="directory dir-col"]/li', '//div[@class="one-third"]/span']

        for xp in xpaths:
            for sel in response.xpath(xp):
                link = "http://dmoz.org/"+sel.xpath('a/@href').extract()[0]
                yield scrapy.Request(link, callback = self.parse)
        

        for sel in response.xpath('//ul[@class="directory-url"]/li'):
            link = sel.xpath('a/@href').extract()[0]
            yield scrapy.Request(link, callback=self.parse_site, meta={'topics': topics})

    def parse_site(self, response):
        soup = BeautifulSoup(response.body.lower())
        to_extract = soup.findAll('script')
        for item in to_extract:
            item.extract()
        words = [w.lower() for w in strip_tags(response.body).split()]

        item = DocumentItem()
        item['url'] = response.url
        item['topics'] = response.meta['topics']
        item['hierarchy'] = '.'.join(response.meta['topics'])
        item['words'] = words
        wordcounts = Counter(words)
        item['wordcounts'] = wordcounts
        item['html'] = response.body
        item['source'] = "dmoz"

        return item
        