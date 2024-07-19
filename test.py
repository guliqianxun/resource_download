import scrapy

class AnnasArchiveSpider(scrapy.Spider):
    name = 'annas_archive_spider'
    allowed_domains = ['annas-archive.org']
    start_urls = ['https://annas-archive.org/search?index=&page=1&q=test&sort=']

    def parse(self, response):
        # Extract the data you need
        for item in response.css('selector-for-item'):
            yield {
                'title': item.css('selector-for-title::text').get(),
                'author': item.css('selector-for-author::text').get(),
                'url': item.css('selector-for-url::attr(href)').get(),
                # add other fields as needed
            }

        # Follow pagination links
        next_page = response.css('selector-for-next-page::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
