# coding=utf-8
__author__ = 'pythme'

from scrapy.cmdline import execute
import os

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))spider_dir
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])
# execute(["scrapy", "crawl", "zhihu"])
execute(["scrapy", "crawl", "lagou"])
# after go into spider project directory,ready to debug this main.py document.

