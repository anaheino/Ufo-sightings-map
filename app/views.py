#!venv/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, flash
#from flask.ext.paginate import Pagination
import folium, flask
import csv
from datetime import datetime, timedelta
#import dataset
from sqlalchemy import *
import pandas as pd
from whoosh.fields import Schema, STORED, ID, KEYWORD, TEXT
#import os.path
from whoosh import index as wIndex
#from whoosh.index import create_in, open_dir
from whoosh.query import *
from whoosh.qparser import QueryParser

app = Flask(__name__)
app.secret_key = 'top_secret' #flash-viestit eivät toimi ilman tätä.

with open("templates/fol_template.html", "r") as a, open("templates/geojson_template.html", "r") as b:
    fol_template = a.read()
    geojson_template = b.read()

def teeMappi(sijainti_1, sijainti_2, zoomi):
    mapp = folium.Map(location=[sijainti_1, sijainti_2], width=900, height=600, zoom_start = zoomi )
    mapp.lat_lng_popover()
    return mapp

def lisaaMarkkerit(s_1, s_2, kuvaus, kartta, clustered=True):
    kartta.simple_marker([s_1, s_2], popup=kuvaus, clustered_marker = clustered)

def stringListaksi(string, delim=",", poistaTyhjat=True):
    """
    Paloittelee merkkijonon erottimen (delim) kohdalta listaksi, poistaa listasta tyhjät
    merkkijonot (jos poistaTyhjat=True), siivoaa ylimääräiset välilyönnit ja muuttaa
    tekstin kirjainkoon pieneksi. Oletuserotin on pilkku.
    """
    lista = [s.strip().lower() for s in string.split(delim)]
    if poistaTyhjat:
        return [x for x in lista if x]
    return lista

def haeHavainnot(hakuehdot, orderBy=None, limit=10000, descMukana=False):
    """
    hakuehdot: dictionary, joka sisältää kaikki hakuparametrit
    ---------------optionaaliset---------------
    limit: montako tulosta palautetaan.
    orderBy: ominaisuus, jonka mukaan haut järjestetään
    -------------------------------------------
    Rakentaa ja suorittaa sql-kyselyn. Palauttaa kyselyn tulokset listamuodossa.
    TODO: kyselyn toteutus sqlalchemy-komennoilla
    """

    query = "SELECT h.id, h.url, h.date, h.time, h.shape, h.duration,{} l.city, l.state, l.country, l.north, l.west FROM havainto h, lokaatio l WHERE l.id = h.lokaatioID".format(" h.desc, " if descMukana else "")
    hakustring = ""
    parametrit = []

    if hakuehdot['description']:
        #Full text search tietokannan desc-kentästä whooshin avulla. Palauttaa listan id:stä,
        #jotka lisätään hakuehdot['id']:n arvoon.
        hakusanat = stringListaksi(hakuehdot['description'], delim=" ")
        hakutermilista = []
        for hakusana in hakusanat:
            hakutermilista.append(Term("desc", hakusana))
        try:
            ix = wIndex.open_dir("../Tietokanta/kuvaushaku")
            with ix.searcher() as searcher:
                myquery = And(hakutermilista)
                #flash(myquery)
                #parser = QueryParser("desc", ix.schema)
                #myquery = parser.parse(querystring)
                results = searcher.search(myquery, limit=None)
                hakuehdot['id']=[[],True]
                for result in results:
                    hakuehdot['id'][0].append(str(result['dID']))
        except:
            #Tietokantaan yhdistäminen epäonnistui.
            pass

    if hakuehdot['location']:
        #Lokaatiohaku kaupungin, osavaltion ja maan mukaan.
        lokaatiot = stringListaksi(hakuehdot['location'])
        hakustring += " AND (lower(h.city) IN ({0}) OR lower(h.state) IN ({0}) OR lower(h.country) IN ({0}))".format(','.join('?' for l in lokaatiot))
        parametrit += lokaatiot * 3

    if hakuehdot['id']:
        #Havainnon hakeminen id:n perusteella. Hakuehdot['id'] on lista, jonka ensimmäinen
        #alkio sisältää listan id:st' ja toinen on boolean, joka kertoo sisällytetäänkö nämä
        #id:t hakuun vai ei. Hakua ei ole parametrisoitu, jotta sqliten rajoitukset eivät ylity.
        #Käyttäjä voi syöttää järjestelmään id:tä urlin kautta, joka parsitaan intiksi, joten
        #injektion vaaraa ei ole.
        if hakuehdot['id'][1]:
            hakustring += " AND h.id IN ({})".format(','.join(hakuehdot['id'][0]))
        else:
            hakustring += " AND NOT h.id IN ({})".format(','.join(hakuehdot['id'][0]))

    if hakuehdot['startdate']:
        #Asetetaan päivämäärä, josta lähtien havaintoja haetaan.
        hakustring += " AND date(h.date) >= ?"
        parametrit.append(hakuehdot['startdate'])

    if hakuehdot['enddate']:
        #Asetetaan päivämäärä, johon asti havaintoja haetaan.
        hakustring += " AND date(h.date) <= ?"
        parametrit.append(hakuehdot['enddate'])

    if hakuehdot['month']:
        #Haku kuukauden mukaan.
        hakustring += " AND strftime('%m', h.date) IN ({})".format(','.join('?' for m in hakuehdot['month']))
        parametrit += hakuehdot['month']

    if hakuehdot['weekday']:
        #Haku viikonpäivän mukaan. Parametrit numeroita väliltä 0-6.
        hakustring += " AND strftime('%w', h.date) IN ({})".format(','.join('?' for d in hakuehdot['weekday']))
        parametrit += hakuehdot['weekday']

    if hakuehdot['starttime']:
        #Haku kellonajan mukaan.
        hakustring += " AND strftime('%H%M', h.time) >= ?"
        parametrit.append(hakuehdot['starttime'])

    if hakuehdot['endtime']:
        #Haku kellonajan mukaan.
        hakustring += " AND strftime('%H%M', h.time) <= ?"
        parametrit.append(hakuehdot['endtime'])

    if hakuehdot['duration']:
        #Haku havainnon keston perusteella.
        #TODO: vaatii tietokannan duration-sarakkeen parsimista fiksumpaan muotoon.
        pass

    if hakuehdot['shape']:
        #Haku muodon mukaan. Tarvitaan apumuuttuja 'shapet', koska osa hakuehdot['shape']-listan
        #alkioista sisältää useampia hakuehtoja.
        shapet = []
        for s in hakuehdot['shape']:
            shapet += s.split(',')
        hakustring += " AND lower(h.shape) IN ({})".format(','.join('?' for s in shapet))
        parametrit += shapet

    if hakuehdot['koord']:
        hakustring += " AND l.north + 0 BETWEEN ? AND ? AND l.west + 0 BETWEEN ? AND ?"
        parametrit += hakuehdot['koord']

    if hakustring is "":
        #Jos hakuehtoja ei ole syötetty, palautetaan tyhjä lista.
        return []
    if orderBy is not None:
        hakustring += " ORDER BY " + orderBy
    if limit is not None:
        hakustring += " LIMIT " + str(limit)

    query += hakustring
    #flash(query)
    #flash("Parametrit: " + str(parametrit))

    #Yhdistetään tietokantaan, muutetaan kyselyn tuottama tulosobjekti listaksi ja suljetaan yhteys.
    
    try:
        db = create_engine('sqlite:///../Tietokanta/tietokanta.db')
        conn = db.connect()

        tulokset = conn.execute(query, parametrit)
        tulokset = [t for t in tulokset]

        conn.close()
        db.dispose()

        return tulokset
    except:
        #Tietokantaan yhdistäminen epäonnistui
        return []

@app.route('/statistics')
def statistics():
    geo = r'static/data/us-states.json'
    hv = r'static/data/havainnotpersatat.csv'
    hD = pd.read_csv(hv)
    smap = folium.Map(location=[48, -102], zoom_start=3, width=900, height=500)
    smap.geo_json(geo_path=geo, data=hD, data_out='static/data/data_out_perpop.json',
                  columns=['state', 'havainto'],
                  key_on='feature.id',
                  threshold_scale=[5, 25, 50, 70, 490],
                  fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2,
                  legend_name="Sightings per 100 000 people",
                  reset=True)
    smap.lat_lng_popover()
    smap.create_map(path='templates/mappi.html', template=geojson_template)
    return render_template("statistics.html",
                           title = "Statistics")

@app.route('/statisticsnopop')
def statisticsnopop():
   geo_states = r'static/data/us-states.json'
   hvp = r'static/data/havainnot_per_osavaltio.csv'
   hPD = pd.read_csv(hvp)
   pmap = folium.Map(location=[48, -102], zoom_start=3, width=900, height=500)
   pmap.geo_json(geo_path=geo_states, data=hPD, data_out='static/data/data_out_nopop.json',
                  columns=['state', 'count'],
                  key_on='feature.id',
                  threshold_scale=[200, 500, 1500, 3000, 5000, 8000],
                  fill_color='YlOrRd', fill_opacity=0.7, line_opacity=0.2,
                  legend_name="Sightings per state, excluding population",
                  reset=True)
   pmap.lat_lng_popover()
   pmap.create_map(path='templates/mappi.html', template=geojson_template)
   return render_template("statistics.html",
                           title = "UFO-stats")

@app.route('/about')
def about():
    return render_template("about.html",
                            title = "About UFO-reports")

@app.route("/report/<int:id>")
def report(id):
    hakuehdot = { 'id': [[str(id)], True], 'description': "", 'startdate': "", 'enddate': "", 
                  'month': "", 'weekday': "", 'starttime': "", 'endtime': "", 'duration': "", 
                  'location': "", 'shape': "", 'koord': ""}
    havainto = haeHavainnot(hakuehdot, limit=1, descMukana=True)[0]
    desc = havainto['desc'].split('<br>')

    #Haetaan lähellä tapahtuneita havaintoja.
    try:
        hakuehdot['id'][1] = False
        hakuehdot['startdate'] = datetime.strptime(havainto['date'], '%Y-%m-%d') - timedelta(days = 4)
        hakuehdot['enddate'] = datetime.strptime(havainto['date'], '%Y-%m-%d')  + timedelta(days = 4)
        hakuehdot['koord'] = [float(havainto['north']) - 2, float(havainto['north']) + 2,
                              float(havainto['west']) - 2, float(havainto['west']) + 2]
        nearby_havainnot = haeHavainnot(hakuehdot, orderBy="h.date desc, h.time desc", limit=10)
    except:
        nearby_havainnot = []

    if (havainto['north'] or havainto['west']) == "":
        map_osm = teeMappi(0, 0, 2)
    else:
        map_osm = teeMappi(havainto['north'], havainto['west'], 5)
        lisaaMarkkerit(havainto['north'], havainto['west'], havainto['desc'], map_osm)

    map_osm.create_map(path='templates/mappi.html', template=fol_template)
    return render_template("havainto.html",
                           title = "UFO-report #" + str(id),
                           subtitle = "Nearby Sightings",
                           map = map_osm,
                           report = havainto,
                           desc = desc,
                           hakutulokset = nearby_havainnot)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    hakuehdot = { 'id': "", 'description': "", 'startdate': "", 'enddate': "", 'month': "", 
                  'weekday': "", 'starttime': "", 'endtime': "", 'duration': "", 'location': "", 
                  'shape': "", 'koord': ""}
    hakutulokset = []
    avustus = True

    if request.method == 'GET':
        #Haetaan 100 viimeisintä havaintoa.
        hakuehdot['startdate'] = datetime.strptime('01/01/2015', '%m/%d/%Y')
        hakutulokset = haeHavainnot(hakuehdot, orderBy="h.date desc, h.time desc", limit=100)
        subtitle = "Latest Reports"


    if request.method == 'POST':
        #Poimitaan formilta käyttäjän syöttämät hakuehdot.
        hakuehdot['id'] = ""
        hakuehdot['location'] = request.form['loc-search']
        hakuehdot['description'] = request.form['desc-search']

        try:
            hakuehdot['startdate'] = datetime.strptime(request.form['startdate'], '%m/%d/%Y')
        except:
            hakuehdot['startdate'] = ""
        try:
            hakuehdot['enddate'] = datetime.strptime(request.form['enddate'], '%m/%d/%Y')
        except:
            hakuehdot['enddate'] = ""

        hakuehdot['month'] = request.form.getlist('month-search')
        hakuehdot['weekday'] = request.form.getlist('weekday-search')
        try:
            hakuehdot['starttime'] = datetime.strptime(request.form.getlist('time-start-search')[0], '%H:%M')
        except:
            hakuehdot['starttime'] = ""
        try:
            hakuehdot['endtime'] = datetime.strptime(request.form.getlist('time-end-search')[0], '%H:%M')
        except:
            hakuehdot['endtime'] = ""

        #hakuehdot['duration'] = request.form.getlist('dur-search')
        hakuehdot['shape'] = request.form.getlist('shape-search')
        hakuehdot['koord'] = ""
        #flash("Hakuehdot: " + str(hakuehdot))
        hakutulokset = haeHavainnot(hakuehdot, orderBy="h.date desc, h.time desc")

        subtitle = "Filtered Reports"

    #Asetetaan hakutulokset kartalle
    for havainto in hakutulokset:
        if (havainto['north'] or havainto['west']) == "":
            continue
        if avustus:
            map_osm = teeMappi(havainto['north'], havainto['west'], 4)
            avustus = False

        lisaaMarkkerit(havainto['north'],
                   havainto['west'],
                   havainto['date'] + "<br><a href=/report/" + str(havainto['id']) + ">View report</a>",
                   map_osm)
    if avustus:
        map_osm = teeMappi(39.8282, -98.5795, 2)


    map_osm.create_map(path='templates/mappi.html', template=fol_template)
    return render_template("index.html",
                           title = 'UFO-Main Page',
                           subtitle = subtitle,
                           map = map_osm,
                           hakutulokset = hakutulokset,
                           hakuehdot = hakuehdot)

if __name__ == "__main__":
    app.run(debug=True)
