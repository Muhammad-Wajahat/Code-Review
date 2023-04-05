import os
import time
from datetime import date as dates
from urllib import parse

import scrapy
from langdetect.lang_detect_exception import ErrorCode
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
# from sqlalchemy import create_engine
import pandas as pd
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
# from Reddit.Scroll_to_bottom import scroll_to_bottom
from Reddit.Reddit.items import RedditscrapperItem
from langdetect import detect, LangDetectException


class Redditspider(scrapy.Spider):
    name = 'Reddit'

    def __init__(self, query=''):
        self.querry = query.replace('%20', ' ')
        self.querry = self.querry.strip("\'")
        self.url = f"https://www.reddit.com/{self.querry}"
        self.i = 1
        # self.engine = create_engine(
        #     "postgresql://postgres:{password}@109.205.182.203:5432/daraz".format(password=parse.quote('orca@4418')))

    def start_requests(self):
        options = Options()
        options.add_argument('--headless')
        path = "D:/Shaheer/chrome_driver/chromedriver.exe"
        driver = Chrome(executable_path=path,options=options)

        driver.get(self.url)
        time.sleep(10)
        # scroll_to_bottom(driver)
        # time.sleep(120)
        sn = 50
        for i in range(1, sn):
            driver.execute_script(f"window.scrollTo(1,50000)")
            time.sleep(2)
        path = os.path.join('D:/Shaheer/FYP/RedditAPI/Reddit/Reddit/spiders', 'Post.html')
        file = open(path, 'w', encoding="utf-8")
        file.write(driver.page_source)
        file.close()
        driver.close()
        yield scrapy.Request(url=f'file:///D:/Shaheer/FYP/RedditAPI/Reddit/Reddit/spiders/Post.html',
                             callback=self.parse)

    def parse(self, response):
        table = response.css('div.rpBJOHq2PR60pnwJlUyP0')
        Data = table.css('div._1oQyIsiPHYt6nx7VOmd1sz')

        Image = []
        Link = []
        date = []
        Post = []
        detail = []
        for i in range(len(Data)):

            val = Data[i].css('div._1poyrkZ7g36PawDueRza-J')
            post_date = val.css('span._2VF2J19pUIMSLJFky-7PEI::text').get()
            if (post_date == None):
                date.append('None')
            else:
                date.append(post_date)

            rec = Data[i].css('h3._eYtD2XCVieq6emjKBH3m::text').get()
            star = ""
            rec = star.join(rec)
            if (rec == None):
                Post.append('None')
            else:
                Post.append(rec)

            dat = Data[i].css('div.STit0dLageRsa2yR4te_b')
            Details = dat.css('p._1qeIAgB0cPwnLhDF9XSiJM::text').getall()
            if (Details == None or Details==""):
                detail.append('None')
            else:
                Det = "".join(Details)
                detail.append(Det)

            ref=Data[i].css("div._10wC0aXnrUKfdJ4Ssz-o14")
            Links = ref.css("a::attr('href')").get()
            if (Links == None):
                Link.append('None')
            else:
                Link.append(Links)

            img=Data[i].css("div._3Oa0THmZ3f5iZXAQ0hBJ0k")
            pic = img.css("img._2_tDEnGMLxpM6uOa2kaDB3.ImageBox-image.media-element._1XWObl-3b9tPy64oaG6fax::attr('href')").get()
            if (pic == None):
                Image.append('None')
            else:
                # spos = pic.find('(')
                # epos = pic.find(')')
                # pic = pic[spos + 1:epos]
                Image.append(pic)


        item = RedditscrapperItem()
        for i in range(len(date)):
            try:
                language = detect(Post[i])

                if language =="en":
                    # item['SearchId'] = self.i
                    item['Post_Date'] = date[i]
                    item['Post'] = Post[i]
                    item['Detail'] = detail[i]
                    item['Img'] = Image[i]
                    item['Link'] = Link[i]
                    yield item
                else:
                    continue
            except LangDetectException as e:
                print(e)







