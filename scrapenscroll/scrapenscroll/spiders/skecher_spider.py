import scrapy
import csv
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

from scrapenscroll.items import ProductItem


## LOGGING to file
#import logging
#from scrapy.log import ScrapyFileLogObserver

#logfile = open('testlog.log', 'w')
#log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
#log_observer.start()

# Spider for crawling Puma website for shoes
class PumaSpider(scrapy.Spider):
    name = "puma"
    allowed_domains = ["puma.com"]

    #Turn links into list
    f = open('links.csv')
    reader = csv.reader(f)
    links = list(reader)
    links = [x[0] for x in links]
    links = links[1:]
    #print(len(links))
    start_urls = links


    # Function to parse information from a single product page
    def parse(self,response):
        item = ProductItem()
        item['brand'] = 'Puma'
        # Get category and Division from breadcrumb at top of page
        cat = response.css('ol.breadcrumb li:nth-last-child(1) a').xpath('text()').extract()[0];
        div = response.css('ol.breadcrumb li:nth-child(3) a').xpath('text()').extract()[0];
        # If div == "Sales" then grab the next text on the path
        if div == ("Sale"):
            div = response.css('ol.breadcrumb li:nth-child(4) a').xpath('text()').extract()[0];

        # Use category and division to remove unnecessary info from title
        title = response.css('ol.breadcrumb li:last-child span').xpath('text()').extract()[0];
        item['name'] = title.replace(div,"").replace("'s","").replace(cat,"")
        # Strip out unnecessary info from category/division
        item['division'] = div.replace("'s","")
        item['category'] = cat.replace("Shoes","").replace("New Arrivals","").replace("Best Sellers","").replace("PUMA","")
        # Get image link
        item['image_link'] = response.css('.product-primary-image a:first-child img::attr(src)').extract()[0];
        # Select the set of prices, and then take the last one
        item['price'] = response.css('.price-sales').xpath('text()').extract()[0];
        #If div == "Colection" then ignore item
        if div != "Collections":
            return item
