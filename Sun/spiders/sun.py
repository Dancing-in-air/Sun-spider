# -*- coding: utf-8 -*-
import scrapy
from Sun.items import SunItem


class SunSpider(scrapy.Spider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?tpye=4&page=0']

    def parse(self, response):
        tr_list = response.xpath("//div[@class='greyframe']//tr/td/table/tr")
        for tr in tr_list:
            item = SunItem()
            item["title"] = tr.xpath("./td[2]/a[2]/text()").extract_first()  # 获取帖子标题
            item["href"] = tr.xpath("./td[2]/a[2]/@href").extract_first()  # 获取帖子具体内容的地址
            item["publish_date"] = tr.xpath("./td[last()]/text()").extract_first()  # 获取帖子发行时间
            yield scrapy.Request(item["href"], callback=self.parse_detail, meta={"item": item})
        # 下一页地址
        next_url = response.xpath("//div[@class='greyframe']/div[@class='pagination']/a[text("
                                  ")='>']/@href").extract_first()
        if next_url is not None:
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail(self, response):
        item = response.meta["item"]
        # 获取帖子中的图片地址
        item["content_img"] = response.xpath(
            "//div[@class='wzy1']//tr[1]/td[@class='txt16_3']/div[1]/img/@src").extract()
        item["content_img"] = ["http://wz.sun0769.com" + i for i in item["content_img"]]
        # 获取帖子的文本内容(由于在有图片和没图片时,文本内容位置不一样,所以统一使用//text())
        item["content"] = response.xpath("//div[@class='wzy1']//tr[1]/td[@class='txt16_3']//text()").extract()
        yield item
