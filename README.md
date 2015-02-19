
# Simple DMOZ scraper

Scrape websites from DMOZ in to a JSON file using Scrapy. 
The resulting JSON document includes a list of all words in each linked website, and a count of each word.

## Requirements

Scrapy needs to be installed. To do this, run

	$ pip install scrapy

This sets up the `scrapy` command, which is used to start and manage scrapy programs.

## Usage Examples

Crawl the default heirarchy, output JSON: 

	$ scrapy crawl dmoz -o sites5.json

Crawl a custom heirarchy, output JSON:

	$ scrapy crawl dmoz -o sites.json -a topic="/Computers/Programming/"

