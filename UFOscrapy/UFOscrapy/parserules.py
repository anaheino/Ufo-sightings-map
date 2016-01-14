# -*- coding: utf-8 -*-
import csv, argparse, datetime, re
# from fuzzywuzzy import fuzz
# from fuzzywuzzy import process
"""
Parsitaan UFOItemin arvoja sopivaan muotoon tietokantaa varten.
"""

regex = '([A-z A-z]+?: )' #Yleinen regex-sääntö merkkijonojen siivoamista varten.

with open("../../data/maat.txt", "r") as m_file, open("../../data/osavaltiot.txt", "r") as ov_file:
    maat = []
    for line in m_file:
        maat.append(line.strip())
    osavaltiot = []
    for line in ov_file:
        osavaltio = dict(lyh = line.split(',')[0], maa = line.split(',')[1].strip())
        osavaltiot.append(osavaltio)

# def fuzzy_match(str1, str2):
#     #Tutkitaan täsmäävätkö merkkijonot suunnilleen toisiaan.
#     if fuzz.token_sort_ratio(str1, str2) > 95:
#         print(str1 + " matches " + str2)
#         return True
#     return False

def parseUrl(rivi):
    """
    Poistaa jokaiselle urlille yhteisen alun (http://nuforc.org/webreports/) ja lopun 
    html-päätteen.
    """
    rivi['url'] = rivi['url'][33:-5]

def parseOccur(rivi):
    """
    rivi: dictionary
    rivi['occur'] on muodossa "Occurred : pvm klo (Entered as : pvm klo). Poistetaan ensin
    ylimääräiset tekstit, ja yritetään sitten parsia käypiä datetime-arvoja.
    """
    pvm = rivi['occur'].split("(")
    rivi['occur'] = re.sub(regex, "", pvm[0]).strip()

    try:
        # Parsitaan tapahtuma-aikaa. Yritetään parsia sekä päivämäärä, että kellonaika.
        dt = datetime.datetime.strptime(rivi['occur'], "%m/%d/%Y %H:%M")
        rivi['date'] = dt.strftime("%m/%d/%Y")
        rivi['time'] = dt.strftime("%H:%M")
    except:
        try:
            #Yritetään parsia päivämäärä.
            dt = datetime.datetime.strptime(rivi['occur'], "%m/%d/%Y")
            rivi['date'] = dt.strftime("%m/%d/%Y")
        except:
            rivi['date'] = ""
        try:
            #Yritetään parsia kellonaika.
            dt = datetime.datetime.strptime(rivi['occur'], "%H:%M")
            rivi['time'] = dt.strftime("%H:%M")
        except:
            rivi['time'] = ""
    
    try:
        #Parsitaan vielä Entered as -tieto.
        rivi['enter'] = re.sub(regex, "", pvm[1])[:-1].strip()
    except:
        rivi['enter'] = ""

def parseReported(rivi):
    rivi['report'] = re.sub(regex, "", rivi['report'])

def parsePosted(rivi):
    rivi['post'] = re.sub(regex, "", rivi['post'])

def parseCity(rivi):
    """
    Katkaistaan 'loc'-sarakkeen merkkijono ensimmäiseen välimerkkiin, laitetaan
    jokainen sana alkamaan isolla.
    """
    rivi['city'] = re.split('[,!?/:;#()"|]', rivi['loc'])[0].strip().title()

def parseState(rivi):
    """
    Muutetaan osavaltiolyhenne isoiksi kirjaimiksi.
    """
    rivi['state'] = rivi['state'].upper()

def parseCountry(rivi):
    if not rivi['state']:
        #Jos osavaltiota ei ole määritetty, etsitään location sarakkeesta merkkijonoa, joka täsmäisi
        #johonkin maan nimeen.
        if "puerto rico" in rivi['loc'].lower():
            rivi['state'] = "PR"
            rivi['country'] = "USA"
            return 
        for maa in maat:
            if maa.lower() in rivi['loc'].lower():
                rivi['country'] = maa
                return
    else:
        for ov in osavaltiot:
            if ov['lyh'] == rivi['state']:
                rivi['country'] = ov['maa']
                return

def parseShape(rivi):
    rivi['shape'] = rivi['shape'].title().strip()

def parseDuration(rivi):
    rivi['duration'] = rivi['duration'].strip()

def parseDesc(rivi):
    #TODO
    pass

def parseAll(rivi):
    """
    Suorittaa kaikki parsinnat.
    """
    #parseUrl(rivi) Ei tällä hetkellä käytössä
    parseOccur(rivi)
    parseReported(rivi)
    parsePosted(rivi)
    parseCity(rivi)
    parseState(rivi)
    parseCountry(rivi)
    parseShape(rivi)
    parseDuration(rivi)
    #parseDesc(rivi) Ei toteutusta tällä hetkellä