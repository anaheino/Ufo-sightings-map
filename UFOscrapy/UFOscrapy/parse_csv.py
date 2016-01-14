# -*- coding: utf-8 -*-
from .parserules import parseAll
"""
Ajetaan komentoriviltä komennolla
"python parsecsv.py -i input.csv -o output.csv"
"""
# Tsekataan ohjelmalle syötetyt parametrit.
parser = argparse.ArgumentParser()
parser.add_argument('-i','--input', help = 'Parsittava .csv-tiedosto', required=True)
parser.add_argument('-o','--output', help = 'Tiedosto, johon lopputulos kirjoitetaan.', required=True)
args = parser.parse_args()

# Avataan tiedostonlukija ja -kirjoittaja.
ifile = open(args.input.decode('utf-8'), 'rb')     
ofile = open(args.output.encode('utf-8'), 'wb')
reader = csv.DictReader(ifile)
writer = csv.DictWriter(ofile, None)

for rivi in reader:
    parseAll(rivi)
    if writer.fieldnames is None:
        dh = dict((h, h) for h in reader.fieldnames)
        writer.fieldnames = reader.fieldnames
        writer.writerow(dh)
    writer.writerow(rivi)

ofile.close()
ifile.close()