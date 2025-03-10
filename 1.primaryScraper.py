import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

class spiderScraper(scrapy.Spider):
    name = 'spiderScraper'

    def start_requests(self):
        df = pd.read_excel('Input.xlsx')  
        urls = df['URL'].tolist()
        url_ids = df['URL_ID'].tolist()
        for url, url_id in zip(urls, url_ids):
            yield scrapy.Request(url, callback=self.parse, meta={'url_id': url_id})

    def parse(self, response):
        article_title = response.css('h1.entry-title::text').get()
        paragraphs = response.css('div.td-post-content *::text').getall()
        article_text = ' '.join(paragraphs).strip()
        article_content = article_title + article_text
        url_id = response.meta['url_id']
        yield {
            'URL_ID': url_id,
            'article_content': article_content
        }

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'compiled_data.json'
    })
    process.crawl(spiderScraper)
    process.start()
