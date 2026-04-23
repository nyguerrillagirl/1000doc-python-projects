import scrapy
from scrapy.crawler import CrawlerProcess


class DCspider(scrapy.Spider):
    name = "dc_spider"

    def start_requests(self):
        urls = ['http://www.factinate.com']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # simple example: write out the html
        html_file = 'DC_courses.html'
        with open(html_file, 'wb') as fout:
            fout.write(response.body)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    process = CrawlerProcess()
    process.crawl(DCspider)
    process.start()
