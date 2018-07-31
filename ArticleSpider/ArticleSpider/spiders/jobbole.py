# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/114167/']

    def parse(self, response):
        # //*[@id = "post-114167"]/div[1]/h1
        re_selector = response.xpath("//div/h1/text()")
        pass