# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
import json


class StudyscrapyproPipeline(object):

    # 初始化方法
    def __init__(self):
        self.connect = MySQLdb.connect(host='localhost', port=3306, user='root', passwd='root', db='cn_blog',
                                       charset='utf8')
        self.connect.autocommit(on=False)
        self.cursor = self.connect.cursor()

        pass
        # self.file = open("result.json", 'w+')
        # self.file.write('[')

    def write_item(self, item):
        json_str = json.dumps(dict(item))
        self.file.write(json_str + ",\n")
        print(json_str)
        pass

    def insert_mysql(self, item):
        # self.cursor.execute("""
        # INSERT INTO `cn_blog`.`item` (`title`,`desc`,`author`, `comm`,`scan`)VALUES(%s,%s,%s,%s,%s);
        # """, (item['title'], 'desc', 'author', 1, 1))
        self.cursor.execute("""
            INSERT INTO `cn_blog`.`item` (`title`,`desc`,`author`, `comm`,`scan`,`date`)VALUES(%s,%s,%s,%s,%s,%s);
            """, (item['title'], item['desc'][0:100], item['author'], item['comm'], item['scan'], item['date']))

    # 解析的方法
    def process_item(self, item, spider):
        # self.write_item(item)
        self.insert_mysql(item)

        return item

    # 关闭的方法 善后
    def close_spider(self, spider):
        # self.file.write("]")
        # self.file.close()

        self.connect.commit()
        self.cursor.close()
        self.connect.close()
