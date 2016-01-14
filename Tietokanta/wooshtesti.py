# -*- coding: utf-8 -*-fr
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT, NUMERIC
import os.path
from whoosh.query import *
from whoosh.qparser import QueryParser
import dataset
from whoosh import index

db = dataset.connect('sqlite:///tietokanta.db')
table = db.load_table('havainto')

schema = Schema(dID=NUMERIC(stored=True), desc=TEXT(stored=True))

if not os.path.exists("kuvaushaku"):
    os.mkdir("kuvaushaku")
ix = index.create_in("kuvaushaku", schema)

writer = ix.writer()
i = 0
for rivi in table:
    writer.add_document(dID=rivi['id'], desc=rivi['desc'].lower())
    i += 1
    print(i)
writer.commit()
'''
with ix.searcher() as searcher:
    myquery = And([Term("desc", "object"), Term("desc", "observed")])
    parser = QueryParser("desc", ix.schema)
    #myquery = parser.parse(querystring)
    results = searcher.search(myquery, limit=20)
    print(len(results))
    for result in results:
        print(result['dID'])
'''