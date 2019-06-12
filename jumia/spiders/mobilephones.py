import scrapy

class MobilePhones(scrapy.Spider):
    name = "mobilephones"
    start_urls = [
        'https://www.jumia.co.ke/mobile-phones/'
    ]

    def parse(self, response):
        for mobile in response.xpath("//div[contains(@class, '-gallery')]"):
            if mobile.xpath(".//span[contains(@class, 'brand')]/text()").extract_first() is None:
                continue
            else:
                yield{
                    'brand': mobile.xpath(".//span[contains(@class, 'brand')]/text()").extract_first(),
                    'name': mobile.xpath(".//span[@class= 'name']/text()").extract_first(),
                    'price': mobile.xpath(".//span[contains(@class, 'price-box ri')]/span[contains(@class, 'price')]/span[@dir='ltr']/text()").extract_first(),
                    'link': mobile.xpath(".//a[@class='link']/@href").extract_first()
                }
        next_page = response.xpath("//a[@title='Next']/@href").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)

            yield scrapy.Request(url=next_page_link, callback=self.parse)
