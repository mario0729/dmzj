# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class comicInfoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    comicinfo = scrapy.Field()
    comicname = scrapy.Field()
    comic_url = scrapy.Field()
    chapter_url = scrapy.Field()
    chapter_name = scrapy.Field()
    page_url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_name = scrapy.Field()
    x = scrapy.Field()