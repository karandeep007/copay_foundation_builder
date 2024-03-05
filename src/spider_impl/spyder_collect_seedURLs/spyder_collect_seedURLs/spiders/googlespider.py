import scrapy
from spyder_collect_seedURLs.items import SpyderCollectSeedurlsItem
import logging
from scrapy.utils.log import configure_logging 


class GooglespiderSpider(scrapy.Spider):
    name = "googlespider"
    allowed_domains = ["google.com"]
    keyword = "Patient Access Network Foundation"
    start_urls = [f"https://google.com/search?q={keyword}"]

    configure_logging(install_root_handler=False)
    logging.basicConfig(        
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def parse(self, response):
        keyword = "Patient Access Network Foundation"
        item = SpyderCollectSeedurlsItem()
        item['programName'] = keyword
        links = response.xpath('//div[@class="g"]/a/@href').getall()
        item['programLinks'] = links
        self.logger.info("Item is  : " +  item)
        
