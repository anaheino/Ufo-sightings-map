#Lisaa lokaatiotaulun tietokantaan

import csv
import dataset, argparse

# Tsekataan ohjelmalle sytetyt parametrit.
parser = argparse.ArgumentParser()
parser.add_argument('-i','--input', help = 'Parsittava .csv-tiedosto', required=True)
parser.add_argument('-o','--output', help = 'Tiedosto, johon lopputulos kirjoitetaan.', required=True)
parser.add_argument('-t','--table', help = 'Taulu, joka .csv-tiedostosta tehdaan', required=True)
args = parser.parse_args()

with open(args.input) as f:
    reader = csv.reader(f, delimiter=',')
    data = [(col1, col2, col3, col4, col5, col6)
                for col1, col2, col3, col4, col5, col6 in reader]


#decoded = [[s.decode('utf8') for s in t] for t in data]

db = dataset.connect(url='sqlite:///'+args.output)
if db[args.table] not in db.tables: #Rivi toimii, vaikka on jarjeton. Nahdakseni ehto toteutuu, jos haettua taulua ei tietokannasta loydy. Ja sitten se olematon taulu poistetaan...
    db[args.table].drop()
taulu = db[args.table]
i = 0
while(i < len(data) -1):
    i += 1
    arvo1=data[i][0].decode('utf-8')
    arvo2=data[i][1].decode('utf-8')
    arvo3=data[i][2].decode('utf-8')
    arvo4=data[i][3].decode('utf-8')
    arvo5=data[i][4].decode('utf-8')
    arvo6=data[i][5].decode('utf-8')
    taulu.insert(dict(loc=arvo1, city=arvo2, state=arvo3, country=arvo4, north=arvo5, west=arvo6))

for havainto in db['lokaatio']:
    if havainto['id'] == 300:
        print(havainto)
        break
print(db.tables)