# -*- coding: utf-8 -*-
import re
import scrapy
from scrapy.http import Request
from urllib import parse

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # post_urls = response.xpath('//div[@id="archive"]/div[contains(@class,"floated-thumb")]/div[@class="post-thumb"]/a/@href').extract()
        post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()
        for post_url in post_urls:
            yield Request(url=parse.urljoin(response.url, post_url), callback=self.parse_detail)

        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url),callback=self.parse)

    def parse_detail(self, response):
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        create_date = response.xpath('//div/p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace(
            " ·", "")
        praise_nums = response.xpath('//div/span[contains(@class,"vote-post-up")]/h10/text()').extract()[0]
        fav_nums_string = response.xpath('//div/span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        match_re = re.match(r".*?(\d+).*", fav_nums_string)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        comment_nums_string = response.xpath('//div/a[@href="#article-comment"]/span/text()').extract()[0]
        match_re = re.match(r".*?(\d+).*", comment_nums_string)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        content = response.xpath('//div[@class="entry"]').extract()  #
        tag_list_comment = response.xpath('//div/p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        tag_list = [element for element in tag_list_comment if not element.strip().endswith("评论")]
        tags = ",".join(tag_list)
        pass
