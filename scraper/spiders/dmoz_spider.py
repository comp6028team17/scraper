import scrapy
import re
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Comment
from collections import Counter

from scraper.items import DocumentItem
import urllib
import sys
import string


from HTMLParser import HTMLParser

keep = "-"
remove_chars = ''.join(ch for ch in string.punctuation if ch not in keep)

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

    def __init__(self, topic="Computers/Programming/Languages/Python/Web", depth=2, *args, **kwargs): 
        super(DmozSpider, self).__init__(*args, **kwargs) 
        
        self.start_urls = ["http://www.dmoz.org/"+topic]
        self.depth = depth

        print "Spidering: "+self.start_urls[0]
    def parse(self, response):
        if not 'depth' in response.meta:
            response.meta['depth'] = 0

        topics = [urllib.unquote(x).decode('utf8').replace('_', ' ').lower() for x in response.url.split("/")[3:-1]]

        xpaths = ['//ul[@class="directory dir-col"]/li', '//div[@class="one-third"]/span']

        if response.meta['depth'] < self.depth:
            for xp in xpaths:
                for sel in response.xpath(xp):
                    link = "http://dmoz.org/"+sel.xpath('a/@href').extract()[0]
                    yield scrapy.Request(link, callback = self.parse, meta = {'depth': response.meta['depth'] + 1})

        for sel in response.xpath('//ul[@class="directory-url"]/li')[:10]:
            link = sel.xpath('a/@href').extract()[0]
            yield scrapy.Request(link, callback=self.parse_site, meta={'topics': topics})

    def parse_site(self, response):
        
        soup = BeautifulSoup(response.body.lower()).body

        for item in soup.findAll('script'):
            item.extract()
        for item in soup.findAll('style'):
            item.extract()
        for item in soup.findAll(text=lambda text:isinstance(text, Comment)):
            item.extract()

        stripped = strip_tags(str(soup))

        stripped = re.sub(r'[^A-Za-z0-9- ]|(\b[\d-]+\b)', '', stripped)

        words = stripped.split()
        # TODO: unique words only?

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







        