# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticlespiderItem(scrapy.Item):
    # 文章标题
    title = scrapy.Field()
    # 创建时间
    create_date = scrapy.Field()
    # 点赞数
    praise_nums = scrapy.Field()
    # 收藏数
    fav_nums = scrapy.Field()
    # 评论数
    comment_nums = scrapy.Field()
    # 文章内容
    content = scrapy.Field()
    # 标签
    tags = scrapy.Field()
    # 新增
    # 文章 url
    url = scrapy.Field()
    # 经过 hash 以后的 url
    url_object_id = scrapy.Field()
    # 列表页上的图片链接
    front_image_url = scrapy.Field()
    # 本地存放图片的路径
    front_image_path = scrapy.Field()
