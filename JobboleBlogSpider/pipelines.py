# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline


class ArticlespiderPipeline(object):

    def process_item(self, item, spider):
        # 重写该方法可以从 results 中获取图片的真实下载地址

        return item


class ArticleImagePipeline(ImagesPipeline):
    """
    继承 ImagesPipeline 这个类，不要忘记了
    """
    # 理解这个方法，我个人感觉像一个拦截器，把 item 拦截下来，去做一些操作
    def item_completed(self, results, item, info):
        print(1)
        if "front_image_url" in item:
            for ok, value in results:
                image_file_path = value["path"]
                item["front_image_path"] = image_file_path
        return item
