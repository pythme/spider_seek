# coding=utf-8
__author__ = 'pythme'

from scrapy.cmdline import execute
# import sys
import os

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "jobbole"])
# after go into spider project directory,ready to debug this main.py document.
