# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CommunityItem(scrapy.Item):
    name = scrapy.Field()
    # link = scrapy.Field()
    No_of_members = scrapy.Field()

class RedditscrapperItem(scrapy.Item):
    Link = scrapy.Field()
    Post_Date = scrapy.Field()
    Post = scrapy.Field()
    Detail = scrapy.Field()
    Img = scrapy.Field()

    # SearchId=scrapy.Field()
