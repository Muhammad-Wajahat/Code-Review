from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from Reddit.Reddit.items import CommunityItem
import time
import scrapy
import os
from os.path import exists



class Redcomm(scrapy.Spider):
    name = 'comm'

    def __init__(self, query=''):
        self.url = f"https://www.reddit.com/search/?q={query}&type=sr"

    def start_requests(self):
        options = Options()
        options.add_argument('--headless')
        path = "D:/Shaheer/chrome_driver/chromedriver.exe"
        driver = Chrome(executable_path=path,options=options)
        driver.get(self.url)
        sn = 1
        # for i in range(1, sn):
        driver.execute_script(f"window.scrollTo(1,50000)")
            # time.sleep(2)
        path = os.path.join('D:/Shaheer/FYP/RedditAPI/Reddit/Reddit/spiders', 'comm.html')
        file = open(path, 'w', encoding="utf-8")
        file.write(driver.page_source)
        file.close()
        driver.close()
        yield scrapy.Request(url=f'file:///D:/Shaheer/FYP/RedditAPI/Reddit/Reddit/spiders/comm.html', callback=self.parse)

    def parse(self, response):
        item = CommunityItem()
        # links=[]
        name=[]
        No_of_memebers=[]
        table=response.css("div._2mO8vClBdPxiJ30y_C6od2")
        Data=table.css('a._3BWq3z8_9gA3oThgYXnngR')
        print(table)
        for i in range(len(Data)):
            dat=Data[i].css('div.ei8_Bq_te0jjwNIqmk8Tw')
            data=dat.css('div._1nTSkRaTteYjCY91DwVEF3')
            Nam=data.css('h6._2torGbn_fNOMbGw3UAasPl::text').get()
            if(Nam==None):
                name.append('None')
            else:
                name.append(Nam)

            mem=data.css('p._3CUjJH8t2eFynKUAv1ER7C::text').get()
            if (mem == None):
                No_of_memebers.append('None')
            else:
                No_of_memebers.append(mem)


        # NoOfMembers = response.css('p._3CUjJH8t2eFynKUAv1ER7C::text').getall()
        # name = response.css('h6._2torGbn_fNOMbGw3UAasPl::text').getall()
        # links = response.css('a.ei8_Bq_te0jjwNIqmk8Tw._2kqt-kRLvKQ1Kqi8OjMEa7::attr(href)').getall()
        for i in range(len(name)):
            item['name'] = name[i]
            item['No_of_members'] = No_of_memebers[i]
            yield item



