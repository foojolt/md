
# -*- coding: utf8 -*-
import scrapy

from demo.items import DemoItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import re
import urllib
import sys

default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
 
class SearchSpider(CrawlSpider):

    name = 'search'
    allowed_domains = [ "www.baidu.com" ]
    search_url_pattern = re.compile(r"http://www.baidu.com/s\?.*wd=([^&]+).*")
    start_urls = [
        "http://www.baidu.com"
    ]

    rules = [ Rule( LinkExtractor(), follow=False, callback='parse' ) ]



    def extractInnerText( self, items ):
        if len(items) <= 0:
            return ""
        return re.sub( r'</?[^>]+>', '', items[0] )

    def parseSearchPages(self, response):
        requestUrl = response.request.url
        mat = self.search_url_pattern.match( requestUrl )

        print "=== request url", requestUrl
        if not mat:
            return

        keyword = urllib.unquote(mat.groups()[0])
        print "=== keyword", keyword
        results = response.xpath('//div[@class="result c-container "]')
        for result in results:
            item = DemoItem()
            result.xpath( "h3/a[]" )
            title = self.extractInnerText(result.xpath('h3/a').extract())
            print "title======", title
            # skip none match result
            if keyword not in title:
                continue
            url = self.extractInnerText(result.xpath('div[@class="f13"]/a').extract())
            item['title'] = title.encode("utf8")
            item['url'] = url.encode("utf8")
            item['keyword'] = keyword.encode("utf8")
            yield item

    def parse(self, response):
        f = open( "eiNames1", 'r' )
        for line in f:
            line = line.strip()
            url = "http://www.baidu.com/s?wd="+line
            yield Request(url, callback = self.parseSearchPages)
        f.close()