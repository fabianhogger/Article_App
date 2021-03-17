from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst
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
"""

    name = "properties"
    allowed_domains = ["realestatedatabase.net"]
    start_urls = [
        "https://realestatedatabase.net/FindAHouse/houses-for-rent-in-kampala-uganda.aspx?Title=Houses+for+rent+in+kampala"
    ]

    rules = (
        Rule(
            LinkExtractor(allow=("HouseDetails\.aspx")),
            callback="parse_property",
            follow=True,
        ),
    )

    def parse_property(self, response):
        property_loader = ItemLoader(item=ScraperItem(), response=response)
        property_loader.default_output_processor = TakeFirst()

        property_loader.add_css(
            "code", "span#ContentPlaceHolder1_DetailsFormView_CodeLabel::text"
        )
        property_loader.add_css(
            "price", "span#ContentPlaceHolder1_DetailsFormView_Shillings::text"
        )
        property_loader.add_css(
            "location", "span#ContentPlaceHolder1_DetailsFormView_LocationLabel::text"
        )
        property_loader.add_css(
            "bedrooms",
            "span#ContentPlaceHolder1_DetailsFormView_BedsInWordsLabel::text",
        )
        property_loader.add_css(
            "district", "span#ContentPlaceHolder1_DetailsFormView_DistrictLabel::text"
        )
        property_loader.add_css(
            "status", "span#ContentPlaceHolder1_DetailsFormView_StatusLabel::text"
        )
        property_loader.add_css(
            "bathrooms",
            "span#ContentPlaceHolder1_DetailsFormView_BathsInWordsLabel::text",
        )
        property_loader.add_css(
            "category", "span#ContentPlaceHolder1_DetailsFormView_CategoryLabel::text"
        )
        property_loader.add_css(
            "agent", "span#ContentPlaceHolder1_DetailsFormView_AgentLabel::text"
        )
        property_loader.add_css(
            "agent_contact", "span#ContentPlaceHolder1_FormView1_TelephoneLabel::text"
        )
        property_loader.add_css(
            "agent_email", "span#ContentPlaceHolder1_FormView1_ContactEmailLabel::text"
        )
        property_loader.add_css(
            "agent_company", "span#ContentPlaceHolder1_FormView1_CompanyLabel::text"
        )

        yield property_loader.load_item()"""
