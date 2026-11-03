"""Lesson 1: Fetch a page and extract text with CSS and XPath. Run: python l1.py"""
from scrapling.fetchers import Fetcher

def main():
    # HTTP requests are lightweight but do NOT run page JavaScript.

    response = Fetcher.get('https://quotes.toscrape.com/', timeout=30)
    if response.status != 200:
        raise RuntimeError(f'Fetch failed: HTTP {response.status}')
    print('Title:', response.css('title::text').get())
    # Select each quote card first to keep each text paired with its author.
    for card in response.css('.quote')[:3]:
        print('Quote:', card.css('.text::text').get())
        print('Author:', card.xpath('.//small[@class="author"]/text()').get())
    # get() = first value; getall() = all values; absent get() returns None.
    print('Authors:', response.css('.author::text').getall())
if __name__ == '__main__': main()
