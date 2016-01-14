# -*- coding: utf-8 -*-
from .parserules import parseAll

class UfoscrapyPipeline(object):
    
    def process_item(self, item, spider):        
    	"""
    	Parsitaan regexin ja datetimen avulla kentät oikeaan muotoon.
    	"""

        try:
            item['loc'] = item['loc'][0]
        except:
            item['loc'] = ""
        try:
            item['shape'] = item['shape'][0]
        except:
            item['shape'] = ""
        try:
            item['state'] = item['state'][0]
        except:
            item['state'] = ""
        try:
            item['duration'] = item['duration'][0]
        except:
            item['duration'] = ""
            
        parseAll(item)

        return item

                                
