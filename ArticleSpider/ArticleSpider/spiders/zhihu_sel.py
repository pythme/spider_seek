# coding=utf-8
__author__ = 'pythme'

import scrapy
import os, time, pickle


# from scrapy.selector import Selector

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu_sel'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']


    def start_requests(self):
        from selenium import webdriver
        browser = webdriver.Chrome()

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("17602150801")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys("Teng@2314")
        browser.find_elements_by_css_selector(".Button.SignFlow-submitButton").click()
        time.sleep(10)
        Cookies = browser.get_cookies()
        # print(Cookies)
        cookie_dict = {}
        for cookie in Cookies:
            os.chdir(os.path.dirname(__file__))
            os.chdir("../../")
            basedir = os.getcwd()
            f = open(basedir + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()
        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookie=cookie_dict)]
        # t_selector = Selector(text=browser.page_source)
        # t_selector.xpath("")
        # browser.quit()
