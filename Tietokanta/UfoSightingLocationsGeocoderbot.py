import dataset, requests, json, csv, time

#Avaa csv-tiedoston ufohavaintojen lokaatioista ja lähettää nominatim APIlle kyselyitä puuttuvista
#koordinaateista, ja tallentaa täydennetyt rivit (yhdessä täydentämättömienkin kanssa) locations2.csv -tiedostoon.
#Vaihda csvt oikeisiib ja työnnä oma emaili ja botin selityssivu niiden kohdille saadaksesi sen toimimaan
db=dataset.connect(url='your_own_database')
ifile = open('csv_input.csv'.decode('utf-8'), 'rb')
ofile = open('csv_output.csv'.encode('utf-8'), 'wb')
reader = csv.DictReader(ifile)
writer = csv.DictWriter(ofile, None)

headers = {
    #'User-Agent': 'UfoSightingLocationsGeocoderbot (+site that explains your bot)',
    #'From': 'your_own_email'
}


def parseCoord(rivi):

	if rivi['north'] == "" and rivi['west'] =="" and rivi['loc'] != "":
            if rivi['country'] == 'USA' or rivi['country'] == 'Canada':
                r = requests.get('http://nominatim.openstreetmap.org/search/%s/%s/%s?format=json&accept-language=engs' % (rivi['country'], rivi['state'], rivi['city']), headers=headers)
                if r.text == '[]':
                    time.sleep(1.1)
                    return
                paikat = json.loads(r.text.encode('utf-8'))
                rivi['north'] = paikat[0]['lat']
                rivi['west'] = paikat[0]['lon']

            else:
                r = requests.get('http://nominatim.openstreetmap.org/search/%s/%s?format=json&accept-language=engs&' % (rivi['country'], rivi['city']), headers=headers)
                if r.text == '[]':
                    time.sleep(1.1)
                    return
                paikat = json.loads(r.text.encode('utf-8'))
                rivi['north'] = paikat[0]['lat']
                rivi['west'] = paikat[0]['lon']
        time.sleep(1.1)
	return


laskuri = 0
for rivi in reader:
    if writer.fieldnames is None:
        dh = dict((h, h) for h in reader.fieldnames)
        writer.fieldnames = reader.fieldnames
        writer.writerow(dh)
    if rivi['north'] == '' and rivi['west'] == '':
        parseCoord(rivi)
    laskuri += 1
    print(str(laskuri))
    writer.writerow(rivi)



    if laskuri >= 24:
        break