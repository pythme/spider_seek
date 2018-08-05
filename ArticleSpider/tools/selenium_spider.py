# coding=utf-8
__author__ = 'pythme'

from selenium import webdriver
from scrapy.selector import Selector

browser = webdriver.Chrome()

browser.get("https://www.zhihu.com/")
t_selector = Selector(text=browser.page_source)
t_selector.xpath("")
browser.quit()