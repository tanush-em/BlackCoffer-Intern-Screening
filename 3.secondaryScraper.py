import json
import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess

with open('compiled_data.json', 'r') as file:
    data = json.load(file)

scraped_urls = {entry["URL_ID"] for entry in data}
all_urls = set([f"blackassign{str(i).zfill(4)}" for i in range(1, 101)])
missing_urls = all_urls - scraped_urls

class SpiderScraper(scrapy.Spider):
    name = 'spiderScraper'
    
    def __init__(self, *args, **kwargs):
        super(SpiderScraper, self).__init__(*args, **kwargs)
        self.url_dict = kwargs.get('url_dict', {})

    def start_requests(self):
        for url_id, url in self.url_dict.items():
            yield scrapy.Request(url, callback=self.parse, meta={'url_id': url_id})

    def parse(self, response):
        article_title = response.css('h1.tdb-title-text *::text').get()
        paragraphs = response.css('div.tdb-block-inner *::text').getall()
        article_text = ' '.join(paragraphs).strip()
        article_content = article_title + article_text
        url_id = response.meta['url_id']
        yield {
            'URL_ID': url_id,
            'article_content': article_content
        }

if __name__ == "__main__":
    url_dict = {
        "blackassign0007": "https://insights.blackcoffer.com/rise-of-cyber-crime-and-its-effects/",
        "blackassign0014": "https://insights.blackcoffer.com/rise-of-e-health-and-its-imapct-on-humans-by-the-year-2030-2/",
        "blackassign0020": "https://insights.blackcoffer.com/how-advertisement-increase-your-market-value/",
        "blackassign0029": "https://insights.blackcoffer.com/ai-in-healthcare-to-improve-patient-outcomes/",
        "blackassign0036": "https://insights.blackcoffer.com/how-neural-networks-can-be-applied-in-various-areas-in-the-future/",
        "blackassign0043": "https://insights.blackcoffer.com/future-of-work-how-ai-has-entered-the-workplace/",
        "blackassign0049": "https://insights.blackcoffer.com/covid-19-environmental-impact-for-the-future/",
        "blackassign0083": "https://insights.blackcoffer.com/human-rights-outlook/",
        "blackassign0084": "https://insights.blackcoffer.com/how-voice-search-makes-your-business-a-successful-business/",
        "blackassign0092": "https://insights.blackcoffer.com/estimating-the-impact-of-covid-19-on-the-world-of-work-3/",
        "blackassign0099": "https://insights.blackcoffer.com/how-covid-19-is-impacting-payment-preferences/",
        "blackassign0100": "https://insights.blackcoffer.com/how-will-covid-19-affect-the-world-of-work-2/"
    }

    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'json',
        'FEED_URI': 'compiled_data.json'
    })
    process.crawl(SpiderScraper, url_dict=url_dict)
    process.start()