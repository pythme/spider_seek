# coding=utf-8
__author__ = 'pythme'

from selenium import webdriver
from scrapy.selector import Selector
import time

browser = webdriver.Chrome()

browser.get("https://weibo.com/")
time.sleep(2)
browser.find_element_by_xpath('//div[@class="input_wrap"]/input[@name="username"]').send_keys('*')
browser.find_element_by_xpath('//div[@class="input_wrap"]/input[@name="password"]').send_keys('*')
browser.find_element_by_xpath('//div[contains(@class,"login_btn")]/a/span').click()

# t_selector = Selector(text=browser.page_source)
# print (t_selector.css(".tm-promo-price .tm-price::text").extract()) # taobao.com price


# for i in range(3):
#     browser.execute_script("window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight; return lenOfPage;")
#     time.sleep(3)


# # 设置chromedriver不加载图片
# chrome_opt = webdriver.ChromeOptions()
# prefs = {"profile.managed_default_content_settings.images":2}
# chrome_opt.add_experimental_option("prefs", prefs)
#
# browser = webdriver.Chrome(chrome_options=chrome_opt)
# browser.get("https://www.taobao.com")


# phantomjs, 无界面的浏览器， 多进程情况下phantomjs性能会下降很严重
# browser = webdriver.PhantomJS(executable_path="E:/phantomjs-2.1.1-windows/bin/phantomjs.exe")
# browser.get("https://detail.tmall.com/item.htm?spm=a230r.1.14.3.yYBVG6&id=538286972599&cm_id=140105335569ed55e27b&abbucket=15&sku_properties=10004:709990523;5919063:6536025")
#
# print (browser.page_source)
browser.quit()
