# -*- coding: utf-8 -*-
import time
# Scrapyn asetukset

BOT_NAME = 'UFOscrapy'

SPIDER_MODULES = ['UFOscrapy.spiders']
NEWSPIDER_MODULE = 'UFOscrapy.spiders'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS=8

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY=0.5

aikaleima = time.strftime("%Y%m%d")

# Haun tulokset kirjoitetaan results.csv -tiedostoon, kentät määritellyssä järjestyksessä.
FEED_URI = 'results_' + aikaleima + '.csv'
FEED_FORMAT = 'csv'
FEED_EXPORT_FIELDS = [ "url",
                       "occur",
                       "date",
                       "time",
                       "enter",
                       "report",
                       "post",
                       "loc",
                       "city",
                       "state",
                       "country",
                       "shape",
                       "duration",
                       "desc" ]

# Itemeja käsittelevä pipeline.
ITEM_PIPELINES = {
    'UFOscrapy.pipelines.UfoscrapyPipeline': 300,
}
