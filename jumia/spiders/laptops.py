import scrapy

class LaptopsSpider(scrapy.Spider):
    name="laptops"
    start_urls = [
        'https://www.jumia.co.ke/laptops/'
    ]

    def parse(self, response):
        for laptops in response.xpath("//*[contains(@class, '-gallery')]"):
            yield{
                "brand": laptops.xpath(".//span[contains(@class, 'brand')]/text()").extract_first(),
                "name": laptops.xpath(".//span[@class='name']/text()").extract_first(),
                "price": laptops.xpath(".//span[@class='price-box ri']/span[contains(@class, 'price')][1]/span[@dir='ltr']/text()").extract_first(),
                "link": laptops.xpath(".//a[@class='link']/@href").extract_first(),
            }
        next_page = response.xpath("//a[@title='Next']/@href").extract_first()

        if next_page is not None:
            next_page_link = response.urljoin(next_page)

            yield scrapy.Request(url=next_page_link, callback=self.parse)
