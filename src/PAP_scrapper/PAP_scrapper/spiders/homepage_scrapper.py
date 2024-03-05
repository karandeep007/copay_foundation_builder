from typing import Iterable
import scrapy
import pandas as pd

items = []
df = pd.read_csv("tmp/seed_urls.csv")
link_list = df['link']

class HomepageScrapperSpider(scrapy.Spider):
    name = "homepage_scrapper"

    def start_requests(self):
        urls = list(link_list)
        for link in urls:
            next_page = link
            yield scrapy.Request(next_page, callback=self.parse)

    def parse(self, response):
        response.selector.remove_namespaces()

        html_text = response.xpath('//html//body//*[not(self::script) and not(self::style)]//text()').extract()
        html_text = "".join(html_text)
        html_text = html_text.replace("\n","").replace("\t","")
        html_text = " ".join(html_text.split())

        item = {
            'link': response.request.url,
            'HTML Text': html_text
        }

        items.append(item)

    def closed(self, reason):
        dataframe = pd.DataFrame(items, columns=['link','HTML Text'])
        dataframe.to_excel("Scraped_Data.xlsx")

