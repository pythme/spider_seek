# coding=utf-8
__author__ = 'pythme'

"""
Scrapy默认是不能在IDE中调试的，我们在根目录中新建一个py文件叫：main.py


Python的scrapy框架在pycharm软件里面没有调试的功能

所以需要自己编写main文件，执行命令行，然后调试程序


## Xpath

文章标题
title.extract()[0]

发布时间
response.xpath('//div/p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0].strip().replace(" ·","")

点赞数
response.xpath('//div/span/h10/text()').extract()[0]

收藏数
fav_nums = response.xpath('//div/span[contains(@class,"bookmark-btn")]/text()').extract()[0]
match_re = re.match(r".*?(\d+).*",fav_nums)
if match_re: # 不做判断的话，没有该值会返回None
    fav_nums = match_re.group(1)
	
	
评论
comment_nums = response.xpath('//div/a[@href="#article-comment"]/span/text()').extract()[0]
match_re = re.match(r".*?(\d+).*",comment_nums)
if match_re: # 不做判断的话，没有该值会返回None
    comment_nums = match_re.group(1)
	
正文	
content = response.xpath('//div[@class="entry"]').extract()


标签列
tags_list = response.xpath('//div/p[@class="entry-meta-hide-on-mobile"]/a/text()').extract() 
tags_list = [element for element in tags_list if not element.strip().endswith("评论")]
tags = ",".join(tag_list)
"""