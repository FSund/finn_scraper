import scrapy
import re


class FinnSpider(scrapy.Spider):
    """Run 'scrapy crawl properties' in virtualenv"""
    allowed_domains = ['finn.no']
    name = "FinnSpider"

    # V70
    # start_urls = ["https://www.finn.no/car/used/search.html?filters=&make=0.818&model=1.818.3077"] 

    # XC70
    # start_urls = ["https://www.finn.no/car/used/search.html?filters=&make=0.818&model=1.818.7781"]
    # start_urls = []

    def parse(self, response):
        ''' 
        This method, as well as any other Request callback, must return an
        iterable of Request and/or dicts or Item objects.
        '''

        for ad_data, ad_title in zip(response.css('div.ads__unit__content__keys'), response.css('h2.ads__unit__content__title')):
            keys = ad_data.css('*::text').getall()
            title = ad_title.css('*::text').getall()

            if len(keys) > 1:
                item = dict()
                # parse year, remove non-numbers
                item['year'] = re.sub('[^0-9]', "", keys[0])
                # parse mileage, remove non-numbers
                item['mileage'] = re.sub('[^0-9]', "", keys[1])
                # parse price, remove non-numbers
                item['price'] = re.sub('[^0-9]', "", keys[2])

                try:
                    # convert to integers
                    item['year'] = int(item['year'])
                    item['mileage'] = int(item['mileage'])
                    item['price'] = int(item['price'])

                except ValueError:
                    continue

                item['title'] = title[0]

                yield item

        for a in response.css('a.button--icon-right'):
            print('RESPONSE: ', a)
            yield response.follow(a, callback=self.parse)
