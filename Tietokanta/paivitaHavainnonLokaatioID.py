#Paivittaa lokaatioID:t havainto-tauluun
from sqlalchemy import *
import dataset
db = dataset.connect('sqlite:///tietokanta.db')

def taydenna(havaintoID, lokaatioID):
    db.query('UPDATE havainto SET lokaatioID = "'+lokaatioID+'" WHERE id = "'+havaintoID+'"')
    testi = db.query('SELECT havainto.lokaatioID, havainto.id FROM havainto WHERE id = "'+havaintoID+'"')
    for t in testi:
        print("Alkup: " + str(lokaatioID) + ", Paivitetty: "+str(t['lokaatioID'])+", Havainnon id: "+ str(t['id']))

def updateLokaatioID():
    table = db.load_table('havainto')
    i = 1
    for rivi in table:
        if (rivi['lokaatioID'] != None):
            continue

        parametrit = [rivi['city'],rivi['state'],rivi['country']]
        dbA = create_engine('sqlite:///tietokanta.db')
        conn = dbA.connect()
        query = 'SELECT l.id FROM lokaatio l, havainto h WHERE ? LIKE l.city and ? LIKE l.state and ? LIKE l.country LIMIT 1'
        tulos = conn.execute(query, parametrit)
        #tulos = db.query('SELECT l.id FROM lokaatio l WHERE "'+ city +'" LIKE l.city and "'+ state +'" LIKE l.state and "'+ country +'" LIKE l.country LIMIT 1')

        for t in tulos:
            lokaatioID = str(t['id'])
            havaintoID = str(rivi['id'])
            #lokaatioID2 = lokaatioID.replace('"', '')
            #havaintoID2 = havaintoID.replace('"', '')
            taydenna(havaintoID, lokaatioID)
        i += 1

updateLokaatioID()