# -*- coding: utf-8 -*-

import scrapy, datetime
from UFOscrapy.items import UfoItem

class UfoSpider(scrapy.Spider):
    name = "ufo"
    allowed_domains = ["nuforc.org"]
    start_urls = [
        "http://www.nuforc.org/webreports/ndxpost.html"
    ]

    def parse(self, response):
        """
        Haetaan linkit jokaiseen päivityskertaan.
        """
        viimeinen_update = datetime.datetime(2015, 10, 16)
        for href in response.xpath('//td/font/a/@href'):
            url = response.urljoin(href.extract())
            pvm = datetime.datetime.strptime(url, "http://www.nuforc.org/webreports/ndxp%y%m%d.html")
            if (pvm <= viimeinen_update):
                continue
            yield scrapy.Request(url, callback=self.parse_post_date)

    def parse_post_date(self, response):
        """
        Kaivetaan yhden päivityskerran tiedot taulukon riveiltä.
        """
        for rivi in response.xpath('//tbody/tr'):
            solut = rivi.xpath('td/font')
            item = UfoItem()         
            item['loc'] = solut[1].xpath('text()').extract()
            item['state'] = solut[2].xpath('text()').extract()
            item['shape'] = solut[3].xpath('text()').extract()
            item['duration'] = solut[4].xpath('text()').extract()
            
            url = response.urljoin(solut[0].xpath('a/@href').extract()[0])
            yield scrapy.Request(url, callback=self.parse_ufo, meta={'item': item})      
        
    def parse_ufo(self, response):
        """
        Haetaan lisätietoja yksittäisen havainnon sivulta.
        """
        item = response.meta['item']
        sel = response.xpath('//tr/td/font/text()').extract()
        item['occur'] = sel[0].strip()
        item['report'] = sel[1].strip()     
        item['post'] = sel[2].strip()
        item['desc'] = '<br>'.join(sel[6:]).strip()
        item['url'] = response.url.strip()
        yield item

