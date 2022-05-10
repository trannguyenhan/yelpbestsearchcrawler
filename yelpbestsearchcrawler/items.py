# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpbestsearchcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    url_profile = scrapy.Field()
    review_count = scrapy.Field()
    star = scrapy.Field()
    categories = scrapy.Field()
    address = scrapy.Field()
    short_description = scrapy.Field()