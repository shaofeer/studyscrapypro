# -*- coding: utf-8 -*-
import scrapy
from studyscrapypro.items import StudyscrapyproItem


class CnBlogsSpliderSpider(scrapy.Spider):
    name = 'cn_blogs_splider'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['http://www.cnblogs.com/']

    def parse(self, response):
        post_list = response.xpath("//div[@class='post_item']")

        for post in post_list:
            title = post.xpath(".//a[@class='titlelnk']/text()").extract_first()
            author = post.xpath(".//a[@class='lightblue']/text()").extract_first()
            comm_scan = post.xpath(".//a[@class='gray']/text()").getall()
            comm = int(str(comm_scan[0]).strip()[3:-1])
            scan = int(str(comm_scan[1]).strip()[3:-1])

            date_str = post.xpath(".//div[@class='post_item_foot']/text()").getall()
            date_str = str(date_str[1]).strip()[4:]

            # date = time.strptime(date_str, "%Y-%m-%d %H:%M")
            all_desc = post.xpath(".//p[@class='post_item_summary']/text()").getall()

            if len(all_desc) < 2:
                continue

            desc = str(all_desc[1]).strip()

            item = StudyscrapyproItem()
            item["title"] = title
            item["author"] = author
            item["comm"] = comm
            item["scan"] = scan
            item["desc"] = desc
            item["date"] = date_str

            yield item
