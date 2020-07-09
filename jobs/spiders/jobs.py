import scrapy
from scrapy import Request


class JobsSpider(scrapy.Spider):
    name = "jobs"

    def __init__(self):
        self.start_urls = [
            'https://www.indeed.com/q-internship-computer-science-jobs.html',
        ]

        # for url in urls:
        #     yield scrapy.Request(url=url, callback=self.parse)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, dont_filter=False)

    def parse(self, response):
        for job in response.xpath('//h2[@class="title"]'):
            if (str(job.xpath('./a/text()').extract_first()) != "\n"):
                yield {
                    'title': job.xpath('./a/text()').extract_first(),
                    'link': job.xpath('./a/@href').extract_first()
                }

        next_page_url = response.xpath("//ul[@class='pagination-list']/li[last()]/a/@href").extract_first()

        # if the next page is not empty
        # go to it
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))