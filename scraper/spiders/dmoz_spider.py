import scrapy

# -*- coding: utf-8 -*-

from scraper.items import DmozItem
import urllib

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/Web/Web_Frameworks/",
        #"http://www.dmoz.org/Computers/Programming/Languages/Python/FAQs%2C_Help%2C_and_Tutorials/"
        "http://www.dmoz.org/"
    ]

    def parse(self, response):
        topics = [urllib.unquote(x).decode('utf8').replace('_', ' ') for x in response.url.split("/")[3:-1]]

        xpaths = ['//ul[@class="directory dir-col"]/li', '//div[@class="one-third"]/span']

        for xp in xpaths:
            for sel in response.xpath(xp):
                link = "http://dmoz.org/"+sel.xpath('a/@href').extract()[0]
                yield scrapy.Request(link, callback = self.parse)
        

        for sel in response.xpath('//ul[@class="directory-url"]/li'):
            item = DmozItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = [i for i in (s.strip() for s in sel.xpath('text()').extract()) if i]
            item['topics'] = topics
            yield item

