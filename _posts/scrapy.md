---
title: scrapy
date: 2016-03-30 11:07:14
tags:
 - scrapy
---

### scrapy

    big python project management

taobao spider:
http://www.slideshare.net/cjhacker/spider-12966847
webkit server  -> scrapy -> scheduler( fifo, priority queue )

http://www.bjhee.com/scrapy.html
extend scrapy.Item -> this is the result
extend CrawlSpider -> parse_item()  generate item from http response, support xpath

### usage

    may save as json:
scrapy crawl my_crawler -o my_crawler.json -t json

    output utf8, not unicode escape
item['title'] = title.encode("utf8")

    scrapy shell
fetch( url )
response.body
from scrapy import Selector
sel = Selector(text='')


    'ascii' codec can't decode byte 0xe5 in position 0
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

    class SearchSpider(CrawlSpider):
override def parse(self, response): to parse the start url's content
use rules = [ Rule( LinkExtractor(), follow=False, callback='parse' ) ]
    to parse link by callback=xxx