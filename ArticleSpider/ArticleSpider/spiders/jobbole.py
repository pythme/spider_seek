# -*- coding: utf-8 -*-
from datetime import datetime
import re
import scrapy
from scrapy.http import Request
from urllib import parse
from ArticleSpider.items import JobBoleArticleItem, ArticleItemLoader
from ArticleSpider.utils.common import get_md5
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
# from scrapy.loader import ItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    # def __init__(self):
    #     self.browser = webdriver.Chrome()
    #     super(JobboleSpider, self).__init__()
    #     dispatcher.connect(self.spider_close,signals.spider_closed)
    #
    # def spider_close(self,spider):
    #     print("spider closed")
    #     self.browser.quit()


    def parse(self, response):
        # post_urls = response.xpath('//div[@id="archive"]/div[contains(@class,"floated-thumb")]/div[@class="post-thumb"]/a/@href').extract()
        # post_urls = response.css("#archive .floated-thumb .post-thumb a::attr(href)").extract()

        post_nodes = response.css("#archive .floated-thumb .post-thumb a")
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url},
                          callback=self.parse_detail)

        next_url = response.css(".next.page-numbers::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobBoleArticleItem()
        front_image_url = response.meta.get("front_image_url", "")

        # title = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # create_date = response.xpath('//div/p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace(
        #     " ·", "")
        # praise_nums = response.xpath('//div/span[contains(@class,"vote-post-up")]/h10/text()').extract()[0]
        # fav_nums_string = response.xpath('//div/span[contains(@class,"bookmark-btn")]/text()').extract()[0]
        # match_re = re.match(r".*?(\d+).*", fav_nums_string)
        # if match_re:
        #     fav_nums = int(match_re.group(1))
        # else:
        #     fav_nums = 0
        #
        # comment_nums_string = response.xpath('//div/a[@href="#article-comment"]/span/text()').extract()[0]
        # match_re = re.match(r".*?(\d+).*", comment_nums_string)
        # if match_re:
        #     comment_nums = int(match_re.group(1))
        # else:
        #     comment_nums = 0
        # content = response.xpath('//div[@class="entry"]').extract()  #
        # tag_list_comment = response.xpath('//div/p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag_list = [element for element in tag_list_comment if not element.strip().endswith("评论")]
        # tags = ",".join(tag_list)
        #
        # article_item["url_object_id"] = get_md5(response.url)
        # article_item["title"] = title
        # article_item["url"] = response.url
        #
        # try:
        #     create_date = datetime.strptime(create_date, "%Y/%m/%d").date()
        # except Exception as e:
        #     create_date = datetime.now().date()
        #
        # article_item["create_date"] = create_date
        # article_item["front_image_url"] = [front_image_url]
        # article_item["praise_nums"] = praise_nums
        # article_item["fav_nums"] = fav_nums
        # article_item["comment_nums"] = comment_nums
        # article_item["tags"] = tags
        # article_item["content"] = content

        item_loader = ArticleItemLoader(item=JobBoleArticleItem(), response=response)
        item_loader.add_xpath("title", '//div[@class="entry-header"]/h1/text()')
        item_loader.add_xpath("create_date", '//div/p[@class="entry-meta-hide-on-mobile"]/text()')
        item_loader.add_value("url", response.url)
        item_loader.add_value("url_object_id", get_md5(response.url))
        item_loader.add_value("front_image_url", front_image_url)
        # item_loader.add_xpath("front_image_path",)
        item_loader.add_xpath("praise_nums", '//div/span[contains(@class,"vote-post-up")]/h10/text()')
        item_loader.add_xpath("fav_nums", '//div/span[contains(@class,"bookmark-btn")]/text()')
        item_loader.add_xpath("comment_nums", '//div/a[@href="#article-comment"]/span/text()')
        item_loader.add_xpath("content", '//div[@class="entry"]')
        item_loader.add_xpath("tags", '//div/p[@class="entry-meta-hide-on-mobile"]/a/text()')

        article_item = item_loader.load_item()

        yield article_item
