import scrapy
import re
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from collections import Counter

from scraper.items import DmozItem, DmozSiteItem
import urllib


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
    #allowed_domains = ["dmoz.org"]
    start_urls = [
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Web/Web_Frameworks/",
        "http://www.dmoz.org/Computers/Programming/Languages/Python/",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/FAQs%2C_Help%2C_and_Tutorials/"
        #"http://www.dmoz.org/"
    ]

    def parse(self, response):
        topics = [urllib.unquote(x).decode('utf8').replace('_', ' ') for x in response.url.split("/")[3:-1]]

        xpaths = ['//ul[@class="directory dir-col"]/li', '//div[@class="one-third"]/span']

        for xp in xpaths:
            for sel in response.xpath(xp):
                link = "http://dmoz.org/"+sel.xpath('a/@href').extract()[0]
                yield scrapy.Request(link, callback = self.parse)
        

        for sel in response.xpath('//ul[@class="directory-url"]/li'):
            # item = DmozItem()
            # item['title'] = sel.xpath('a/text()').extract()
            # item['link'] = sel.xpath('a/@href').extract()
            # item['desc'] = [i for i in (s.strip() for s in sel.xpath('text()').extract()) if i]
            # item['topics'] = topics
            # yield item
            link = sel.xpath('a/@href').extract()[0]
            yield scrapy.Request(link, callback=self.parse_site, meta={'topics': topics})

    def parse_site(self, response):
        soup = BeautifulSoup(response.body.lower())
        to_extract = soup.findAll('script')
        for item in to_extract:
            item.extract()
        words = strip_tags(response.body).split()

        item = DmozSiteItem()
        item['url'] = response.url
        item['topics'] = response.meta['topics']
        item['words'] = words
        item['wordcounts'] = Counter(words)
        item['html'] = response.body

        return item
        