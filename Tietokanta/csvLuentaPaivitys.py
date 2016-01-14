#Koodi tietokannan paivittamiseksi csv-tiedostosta. Kesken.
import csv
import dataset, argparse
from sqlalchemy import INTEGER
import dataset, requests, json, csv, time

def koordinaatit(rivi, riviavain):

	if rivi['north'] == "" and rivi['west'] =="" and rivi['loc'] != "":
            if rivi['country'] == 'USA' or rivi['country'] == 'Canada':
                r = requests.get('http://nominatim.openstreetmap.org/search/%s/%s/%s?format=json&accept-language=engs&email=matti.o.leinonen@student.jyu.fi' % (rivi['country'], rivi['state'], rivi['city']), headers=headers)
                if r.text == '[]':
                    time.sleep(1.1)
                    return
                paikat = json.loads(r.text.encode('utf-8'))
                db.query('UPDATE lokaatio SET north = "'+paikat[0]['lat']+'" WHERE id = "'+riviavain+'"')
                db.query('UPDATE lokaatio SET west = "'+paikat[0]['lon']+'" WHERE id = "'+riviavain+'"')
                db.query('UPDATE havainto SET lokaatioID = "'+riviavain+'" WHERE id = "'+rivi['id']+'"')


            else:
                r = requests.get('http://nominatim.openstreetmap.org/search/%s/%s?format=json&accept-language=engs&email=matti.o.leinonen@student.jyu.fi' % (rivi['country'], rivi['city']), headers=headers)
                if r.text == '[]':
                    time.sleep(1.1)
                    return
                paikat = json.loads(r.text.encode('utf-8'))
                db.query('UPDATE lokaatio SET north = "'+paikat[0]['lat']+'" WHERE id = "'+riviavain+'"')
                db.query('UPDATE lokaatio SET west = "'+paikat[0]['lon']+'" WHERE id = "'+havaintoID+'"')
                db.query('UPDATE havainto SET lokaatioID = "'+riviavain+'" WHERE id = "'+rivi['id']+'"')
        time.sleep(1.1)
	return



# Tsekataan ohjelmalle sytetyt parametrit.
parser = argparse.ArgumentParser()
parser.add_argument('-i','--input', help = 'Parsittava .csv-tiedosto', required=True)
parser.add_argument('-o','--output', help = 'Tiedosto, johon lopputulos kirjoitetaan.', required=True)
parser.add_argument('-t','--table', help = 'Taulu, joka .csv-tiedostosta tehdaan', required=True)
args = parser.parse_args()

with open(args.input) as f:
    reader = csv.reader(f, delimiter=',')
    data = [(col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14)
                for col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14 in reader]


#decoded = [[s.decode('utf8') for s in t] for t in data]

db = dataset.connect(url='sqlite:///'+args.output)
#if db[args.table] not in db.tables: #Rivi toimii, vaikka on jarjeton. Nahdakseni ehto toteutuu, jos haettua taulua ei tietokannasta loydy. Ja sitten se olematon taulu poistetaan...
#    db[args.table].drop()
taulu = db[args.table]

#Huomaa silmukassa tapahtuva indeksointi. Csv-tiedoston tietokannalle turhia sarakkeita jaetaan pois.
#Taman kanssa oltava hyvin tarkkana.
i = 0
while(i < len(data) -1):
    i += 1
    arvo1=data[i][0].decode('utf-8')
    apuDateTaulukko = data[i][2].split('/') #Muutetaan date oikeaan muotoon
    apuDate = apuDateTaulukko[2] + '-' + apuDateTaulukko[0] + '-' + apuDateTaulukko[1]
    arvo2=apuDate.decode('utf-8')
    arvo3=data[i][3].decode('utf-8')
    arvo4=data[i][7].decode('utf-8')
    arvo5=data[i][8].decode('utf-8')
    arvo6=data[i][9].decode('utf-8')
    arvo7=data[i][10].decode('utf-8')
    arvo8=data[i][11].decode('utf-8')
    arvo9=data[i][12].decode('utf-8')
    arvo10=data[i][13].decode('utf-8')
    taulu.insert(dict(url=arvo1, date=arvo2, time=arvo3, loc=arvo4, city=arvo5, state=arvo6, country=arvo7, shape=arvo8, duration=arvo9, desc=arvo10, lokaatioID=None), types={lokaatioID=sqlalchemy.INTEGER})
#    table.insert(dict(url=arvo1, occur=arvo2, date=arvo3))
i=0
for rivi in taulu:
    if rivi['lokaatioID'] not None:
        continue
    result = db['lokaatio'].find_one(country=rivi['country'], state=rivi['state'], city=rivi['city'])
    if len(result) not 0:
        db.query('UPDATE havainto SET lokaatioID = "'+result['id']+'" WHERE id = "'+rivi['id']+'"')
        continue
    riviavain = db['lokaatio'].insert(dict(loc=rivi['loc'], city=rivi['city'], state=rivi['state'], country=rivi['country'], north='', west=''))
    koordinaatit(rivi, riviavain)
    tulos = db['lokaatio'].find_one(id=riviavain)
    lokaatiorivi
    for t in tulos:
        lokaatiorivi = t
    i += 1
    print(str(i)+", Havaintorivin lokaatioID: "+rivi['lokaatioID']+", Lokaatiorivin id: "+t['id'])


x=0
for havainto in db['havainto']:

#    print(havainto['date'])
#    if(havainto['date'] == ""):
#        x += 1
    if havainto['id'] == 57:
        print(havainto)
        break
#    print(havainto['id'])
#print(x)