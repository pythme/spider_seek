# # -*- coding: utf-8 -*-
import scrapy
import re, time, os, pickle, json, datetime
from scrapy.loader import ItemLoader
from ArticleSpider.items import ZhihuAnswerItem, ZhihuQuestionItem

try:
    import urlparse as parse
except:
    from urllib import parse


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    start_answer_url = "https://www.zhihu.com/api/v4/questions/{0}/answers?sort_by=default&include=data%5B%2A%5D.is_normal%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccollapsed_counts%2Creviewing_comments_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Cmark_infos%2Ccreated_time%2Cupdated_time%2Crelationship.is_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cupvoted_followees%3Bdata%5B%2A%5D.author.is_blocking%2Cis_blocked%2Cis_followed%2Cvoteup_count%2Cmessage_thread_token%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit={1}&offset={2}"

    headers = {
        "HOST": "www.zhihu.com",
        "Referer": "https://www.zhizhu.com",
        # 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"

    }

    custom_settings = {
        "COOKIES_ENABLED": True
    }

    def parse(self, response):
        all_urls_incomplete = response.css("a::attr(href").extract()
        all_urls_others = [parse.urljoin(response.url, url) for url in all_urls_incomplete]
        all_urls = filter(lambda x: True if x.startswith("https") else False, all_urls_others)
        for url in all_urls:
            match_obj = re.match("(.*zhihu.com/question/(\d+)(/|$)).*", url)
            if match_obj:
                request_url = match_obj.group(1)
                yield scrapy.Request(request_url, headers=self.headers, callback=self.parse_question)
            else:
                yield scrapy.Request(url, headers=self.headers, callback=self.parse)

    def parse_question(self, response):
        if "QuestionHeader-title" in response.text:
            match_obj = re.match("(.*zhihu.com/question/(\d+)(/|$)).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            item_loader.add_xpath("title", '//div/h1[@class="QuestionHeader-title"]/text()')
            item_loader.add_xpath("content", '//div[@class="QuestionHeader-detail"]/text()')
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_xpath("answer_num", '//div/h4[@class="List-headerText"]/span/text()')
            item_loader.add_xpath("comments_num", '//div[@class="QuestionHeaderActions"]/div/button/text()')
            item_loader.add_xpath("watch_user_num",
                                  '//div[contains(@class,"NumberBoard QuestionFollowStatus-counts")]/div[1]/div/strong/text()')
            item_loader.add_xpath("click_num",
                                  '//div[contains(@class,"NumberBoard QuestionFollowStatus-counts")]/div[2]/div/strong/text()')
            item_loader.add_xpath("topics", '//div[@class="QuestionHeader-topics"]/div/span/a/div/text()')

            question_item = item_loader.load_item()
        else:
            match_obj = re.match("(.*zhihu.com/question/(\d+)(/|$)).*", response.url)
            if match_obj:
                question_id = int(match_obj.group(2))

            item_loader = ItemLoader(item=ZhihuQuestionItem(), response=response)
            # item_loader.add_css("title", ".zh-question-title h2 a::text")
            item_loader.add_xpath("title",
                                  "//*[@id='zh-question-title']/h2/a/text()|//*[@id='zh-question-title']/h2/span/text()")
            item_loader.add_css("content", "#zh-question-detail")
            item_loader.add_value("url", response.url)
            item_loader.add_value("zhihu_id", question_id)
            item_loader.add_css("answer_num", "#zh-question-answer-num::text")
            item_loader.add_css("comments_num", "#zh-question-meta-wrap a[name='addcomment']::text")
            # item_loader.add_css("watch_user_num", "#zh-question-side-header-wrap::text")
            item_loader.add_xpath("watch_user_num",
                                  "//*[@id='zh-question-side-header-wrap']/text()|//*[@class='zh-question-followers-sidebar']/div/a/strong/text()")
            item_loader.add_css("topics", ".zm-tag-editor-labels a::text")

            question_item = item_loader.load_item()

        yield scrapy.Request(self.start_answer_url.format(question_id, 20, 0), headers=self.headers,
                             callback=self.parse_answer)
        yield question_item

    def parse_answer(self, reponse):
        ans_json = json.loads(reponse.text)
        is_end = ans_json["paging"]["is_end"]
        total_answer = ans_json["paging"]["totals"]
        next_url = ans_json["paging"]["next"]

        for answer in ans_json["data"]:
            answer_item = ZhihuAnswerItem()
            answer_item["zhihu_id"] = answer["id"]
            answer_item["url"] = answer["url"]
            answer_item["question_id"] = answer["question"]["id"]
            answer_item["author_id"] = answer["author"]["id"] if "id" in answer["author"] else None
            answer_item["content"] = answer["content"] if "content" in answer else None
            answer_item["parise_num"] = answer["voteup_count"]
            answer_item["comments_num"] = answer["comment_count"]
            answer_item["create_time"] = answer["created_time"]
            answer_item["update_time"] = answer["updated_time"]
            answer_item["crawl_time"] = datetime.datetime.now()

            yield answer_item

        if not is_end:
            yield scrapy.Request(next_url, headers=self.headers, callback=self.parse_answer)

    def start_requests(self):
        from selenium import webdriver
        browser = webdriver.Chrome()
        # browser = webdriver.Firefox()

        browser.get("https://www.zhihu.com/signin")
        browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys("1760215XXXX")
        browser.find_element_by_css_selector(".SignFlow-password input").send_keys("XXXX")
        time.sleep(5)
        # browser.find_element_by_css_selector(".Button.SignFlow-submitButton").click()
        browser.find_element_by_xpath('//button[contains(@class,"Button SignFlow-submitButton")]').click()
        time.sleep(5)
        Cookies = browser.get_cookies()
        cookie_dict = {}
        os.chdir(os.path.dirname(__file__))
        os.chdir("../../")
        basedir = os.getcwd()

        try:
            if os.path.exists(basedir + "/Zhihu_Cookies/"):
                return
        except:
            os.mkdir("Zhihu_Cookies")

        for cookie in Cookies:
            cookies_dir = basedir + "/Zhihu_Cookies/"
            f = open(cookies_dir + cookie['name'] + '.zhihu', 'wb')
            pickle.dump(cookie, f)
            f.close()
            cookie_dict[cookie['name']] = cookie['value']
        browser.close()

        return [scrapy.Request(url=self.start_urls[0], dont_filter=True, headers=self.headers, cookies=cookie_dict)]
