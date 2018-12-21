# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from JobboleBlogSpider.items import ArticlespiderItem
from JobboleBlogSpider.utils.commons import get_md5
import datetime
import re


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
            # .extract_first() 和 .extract()[0] 的效果是一样的
            post_url = post_node.xpath("a/@href").extract_first()
            front_image_url = post_node.xpath("a/img/@src").extract()[0]
            print('文章 url:{} \t 图片 url:{}'.format(post_url, front_image_url))

            # 对于爬取到的每一个链接，即 post_url，都新开一个线程爬取里面的内容
            # yield 是生成器机制
            # meta 是向回调方法里面传入 kv 键值对，因为 callback 传递的是函数名，所以，只能通过在 meta 里面设置键值对的方式传递参数
            # callback 编写回调方法
            # 遇到 href 没有域名的时候，就直接使用拼接 response.url + post_url
            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_image_url': front_image_url},
                          callback=self.parse_detail)

    # 第 2 个参数是 response
    def parse_detail(self, response):
        # 新建一个实体对象
        article_item = ArticlespiderItem()

        # 从回调方法里面获得上一级方法传递进来的参数
        front_image_url = response.meta.get('front_image_url', '')
        # 提取文章的具体字段
        title = response.xpath('//div[@class="entry-header"]/h1/text()').extract()[0]
        # 或者使用 response.xpath('//div[@class="entry-header"]/h1/text()').extract_first("")
        # 创建日期
        create_date = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract()[0] \
            .strip().replace(".", "").strip()

        try:
            create_date = datetime.datetime.strptime(create_date, '%Y/%m/%d').date()
        except Exception as e:
            # 如果日期爬取有误，就换成今天的日期
            create_date = datetime.datetime.now().date()

        # 点赞数
        praise_nums = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]

        # 收藏数
        fav_nums = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0]

        # 从收藏数中提取出数字
        match_re = re.match('.*?(\d+).*', fav_nums)
        if match_re:
            fav_nums = int(match_re.group(1))
        else:
            fav_nums = 0

        # 评论数
        comment_nums = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0]
        match_re = re.match('.*?(\d+).*', comment_nums)
        if match_re:
            comment_nums = int(match_re.group(1))
        else:
            comment_nums = 0
        # 内容
        content = response.xpath("//div[@class='entry']").extract()[0]
        # tag_list
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        # 把评论部分过滤掉
        tag_list = [element for element in tag_list if not element.strip().endswith("评论")]
        tags = ','.join(tag_list)

        article_item['title'] = title
        article_item['url'] = response.url
        article_item['create_date'] = str(create_date)
        article_item['praise_nums'] = praise_nums
        article_item['fav_nums'] = fav_nums
        article_item['comment_nums'] = comment_nums
        # article_item['content'] = content
        article_item['tags'] = tags
        # 文章封面图
        article_item['front_image_url'] = [front_image_url]
        # 将 id 使用 MD5 编码
        article_item['url_object_id'] = get_md5(response.url)
        yield article_item