import scrapy
from scrapy.loader import ItemLoader
from jumia.items import JumiaItem

class LaptopsSpider(scrapy.Spider):
    name="laptops"
    start_urls = [
        'https://www.jumia.co.ke/laptops/'
    ]

    def parse(self, response):
        for laptops in response.xpath("//div[contains(@class, '-gallery')]"):
            if laptops.xpath(".//span[contains(@class, 'brand')]/text()").extract_first() is None:
                continue
            else:
                loader = ItemLoader(item=JumiaItem(), selector=laptops, response=response)
                loader.add_xpath('brand', ".//span[contains(@class, 'brand')]/text()")
                loader.add_xpath('name', ".//span[@class='name']/text()")
                loader.add_xpath('price', ".//span[@class='price-box ri']/span[contains(@class, 'price')][1]/span[@dir='ltr']/text()")
                loader.add_xpath('link', ".//a[@class='link']/@href")
                yield loader.load_item()
        next_page = response.xpath("//a[@title='Next']/@href").extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)

            yield scrapy.Request(url=next_page_link, callback=self.parse)
