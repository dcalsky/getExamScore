# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Student(scrapy.Item):
    username = scrapy.Field()
    name = scrapy.Field()


class ExamItem(scrapy.Item):
    class_no = scrapy.Field()
    class_name = scrapy.Field()
    class_score = scrapy.Field()
    class_update_time = scrapy.Field()
