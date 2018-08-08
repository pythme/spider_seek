# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ArticleSpider.items import LagouJobItemLoader, LagouJobItem
from ArticleSpider.utils.common import get_md5
import time, os, pickle
from datetime import datetime


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com/']

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Connection": "keep-alive",
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36",
        "Referer": 'https://www.lagou.com',
        'Connection': 'keep-alive',
        "HOST": "www.lagou.com"
    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    rules = (
        Rule(LinkExtractor(allow=('zhaopin/.*',)), follow=True),
        Rule(LinkExtractor(allow=('gongsi/j\d+.html',)), follow=True),
        Rule(LinkExtractor(allow=r'jobs/\d+.html'), callback='parse_job', follow=True),
    )

    def parse_job(self, response):
        item_loader = LagouJobItemLoader(item=LagouJobItem(), response=response)
        item_loader.add_xpath("title", '//div/span[@class="name"]/text()')
        item_loader.add_xpath("url", response.url)
        item_loader.add_xpath("url_object_id", get_md5(response.url))
        item_loader.add_xpath("salary", '//dd/p/span[@class="salary"]/text()')
        item_loader.add_xpath("job_city", '//dd/p/span[2]/text()')
        item_loader.add_xpath("work_years", '//dd/p/span[3]/text()')
        item_loader.add_xpath("degree_need", '//dd/p/span[4]/text()')
        item_loader.add_xpath("job_type", '//dd/p/span[5]/text()')
        item_loader.add_xpath("tags",'//dd[@class="job_request"]/ul/li/text()')
        item_loader.add_xpath("publish_time", '//dd/p[@class="publish_time"]/text()')
        item_loader.add_xpath("job_advantage", '//dl/dd/p/text()')
        item_loader.add_xpath("job_desc", '//dd/div/p/text()')
        item_loader.add_xpath("job_addr", '//dd/div[@class="work_addr"]')
        item_loader.add_xpath("company_url", '//dl/dt/a/@href')
        item_loader.add_xpath("company_name", '//dl/dt/a/img/@alt')
        item_loader.add_value("crawl_time", datetime.now())

        job_item = item_loader.load_item()

        return job_item
        # i = {}
        # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # i['name'] = response.xpath('//div[@id="name"]').extract()
        # i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i

    def start_requests(self):
        from selenium import webdriver
        browser = webdriver.Chrome()
        # browser = webdriver.Firefox()

        browser.get("https://passport.lagou.com/login/login.html?service=https%3a%2f%2fwww.lagou.com%2f")
        # browser.get("https://passport.lagou.com/login/login.html?")
        browser.find_element_by_xpath('//div/input[@type="text"]').send_keys("")
        browser.find_element_by_xpath('//div/input[@type="password"]').send_keys("")
        time.sleep(2)
        browser.find_element_by_xpath('//div/input[@type="submit"]').click()
        time.sleep(3)
        Cookies = browser.get_cookies()
        cookie_dict = {}
        os.chdir(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
        spider_dir = os.getcwd()

        try:
            # os.path.exists(spider_dir + "/zhihu_cookies/")
            os.mkdir("lagou_cookies")
        except:
            os.chdir("lagou_cookies")

        for cookie in Cookies:
            cookies_dir = spider_dir + "/lagou_cookies/"
            f = open(cookies_dir + cookie['name'] + '.lagou', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        # browser = webdriver.Chrome()
        # browser.get("https://www.lagou.com/?msg=validation&uStatus")
        # browser.find_element_by_xpath('//div/p/a[@class="tab focus"]').click()

        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, headers=self.headers, cookies=cookie_dict)]
