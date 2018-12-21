# -*- coding: utf-8 -*-
import scrapy


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]

    # start_urls 是一个待爬取的 url 列表的 root
    # 先从一篇具体的文章开始
    # start_urls = ['http://blog.jobbole.com/']
    # 爬取最新文章列表页
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # text 是属性，不要写成 text() 了
        # print(response.text)
        # a 标签
        post_nodes = response.xpath("//div[@id='archive']/div[@class='post floated-thumb']/div[@class='post-thumb']")

        print('爬取了 {} 篇文章'.format(len(post_nodes)))
        for post_node in post_nodes:
            post_url = post_node.xpath("a/@href").extract()[0]
            front_image_url = post_node.xpath("a/img/@src").extract()[0]
            print('文章 url:{} \t 图片 url:{}'.format(post_url, front_image_url))
