import scrapy
import re
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup, Comment
from collections import Counter
import urllib2
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

if __name__ == '__main__':
    response = urllib2.urlopen('http://python.org/')
    html = response.read()
    soup = BeautifulSoup(html.lower()).body

    for item in soup.findAll('script'):
        item.extract()
    for item in soup.findAll(text=lambda text:isinstance(text, Comment)):
        item.extract()

    stripped = strip_tags(str(soup)).lower()

    for c in remove_chars:
        stripped=stripped.replace(c,"")
    
    words = stripped.split()

    print words
    # TODO: unique words only?

    # item = DocumentItem()
    # item['url'] = response.url
    # item['topics'] = response.meta['topics']
    # item['hierarchy'] = '.'.join(response.meta['topics'])
    # item['words'] = words
    # wordcounts = Counter(words)
    # item['wordcounts'] = wordcounts
    # item['html'] = response.body
    # item['source'] = "dmoz"            

    # return item







        