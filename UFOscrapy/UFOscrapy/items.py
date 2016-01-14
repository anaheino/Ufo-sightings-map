# -*- coding: utf-8 -*-

import scrapy

"""
NUFORC:sta saatuja tietoja tallentava item.
"""
class UfoItem(scrapy.Item):
    occur = scrapy.Field() # havaintoaika muodossa "pp/kk/vvvv tt:mm"
    date = scrapy.Field()
    time = scrapy.Field()
    enter = scrapy.Field() # käyttäjän ilmoittama havaintoaika 
    report = scrapy.Field() # milloin havainto on kirjattu ylös
    post = scrapy.Field() # milloin havainto on lisätty sivulle
    loc = scrapy.Field() # parsimaton location
    city = scrapy.Field() 
    state = scrapy.Field() 
    country = scrapy.Field()
    shape = scrapy.Field() # UFO:n muoto
    duration = scrapy.Field() # havainnon kesto
    desc = scrapy.Field() # kuvaus
    url = scrapy.Field() # linkki yksittäiseen havaintoon
