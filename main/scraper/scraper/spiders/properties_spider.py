from scrapy.spiders import CrawlSpider

from scraper.scraper.items import ScraperItem

from scrapy.spiders import SitemapSpider
from django.db import models

class PropertiesSpider(SitemapSpider):
    name = 'crawlbbc'
    allowed_domains=['bbc.com']
    sitemap_urls = ['https://www.bbc.com/sitemaps/https-index-com-news.xml']
#    custom_settings = { 'CLOSESPIDER_PAGECOUNT': 10,'ROBOTSTXT_OBEY' : True, }
    def parse(self, response):
        #image=response.xpath("//span[@class='hero-image']/picture/img").xpath('@src').extract_first()
        yield ScraperItem( name= response.xpath("//title/text()").get(), url= response.url,body=response.xpath('//p/text()').getall())
