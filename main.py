# coding=utf-8
__author__ = 'pythme'

from scrapy.cmdline import execute
import sys, os

os.path.dirname(os.path.abspath(__file__))
execute(['scrapy','crawl','jobbole'])
# 接着进入项目 打断点进行调试

