#!../nettisivuproto/ufohavainto/bin/python
# -*- coding: utf-8 -*-
import csv
import pygal
import dataset

"""
Päivittää tilastosivun kuvaajat. Ajaminen tapahtuu komennolla 'python paivitaTilastot.py'.
"""

def luoChart(data, otsikko, tiedosto, horizontal=False):
    """
    data: lista aineistosta, jonka perusteella kuvaaja luodaan.
    otsikko: kuvaajan otsikko
    tiedosto: tiedosto, johon kuvaaja tallennetaan
    horizontal: tuleeko kuvaaja pystyyn vai vaakasuoraan.
    -----------------------------------------------------------
    Luo pylväskuvaajan annettujen parametrien pohjalta.
    """
    
    if horizontal:
        chart = pygal.HorizontalBar()

    else:
        chart = pygal.Bar()

    for d in data:
        chart.add(d[0], d[1])
    chart.title = otsikko
    chart.render_to_file(tiedosto)

def laskeOsavaltiot():
    tulokset = db.query("SELECT l.state, COUNT(*) lkm FROM havainto h, lokaatio l WHERE h.lokaatioId = l.id GROUP BY l.state ORDER BY lkm desc")
    lista = []
    i = 0
    for t in tulokset:
        if t['state']: #Poistetaan None arvot tilastotosta
            lista.append([t['state'], t['lkm']])
            i +=1
            if i == 10:
                break
    luoChart(lista, "Top States", 'static/data/osavaltiot_chart.svg', horizontal=True)

def laskeKaupungit():
    tulokset = db.query("SELECT l.city, l.state, COUNT(*) lkm FROM havainto h, lokaatio l WHERE h.lokaatioId = l.id GROUP BY l.id ORDER BY lkm desc")
    lista = []
    i = 0
    for t in tulokset:
        if t['city']: #Poistetaan None arvot tilastotosta
            lista.append([t['city'] + " " + t['state'], t['lkm']])
            i +=1
            if i == 10:
                break
    luoChart(lista, "Top Cities", 'static/data/kaupungit_chart.svg', horizontal=True)

def laskeVuodet():
    tulokset = db.query("SELECT strftime('%Y', h.date) v, COUNT(*) lkm FROM havainto h WHERE strftime('%Y', h.date) >= strftime('%Y', '1990-01-01') GROUP BY strftime('%Y', h.date)")
    lista = []
    for t in tulokset:
        if t['v']: #Poistetaan None arvot tilastotosta
            lista.append([t['v'], t['lkm']])
    luoChart(lista, "UFOs per Year", 'static/data/vuodet_chart.svg')

def laskeKuukaudet():
    tulokset = db.query("SELECT strftime('%m', h.date) kk, COUNT(*) lkm FROM havainto h GROUP BY strftime('%m', h.date)")
    kuukaudet = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    lista = []
    i = 0
    for t in tulokset:
        if t['kk']: #Poistetaan None arvot tilastotosta
            lista.append([kuukaudet[i], t['lkm']])
            i += 1
    luoChart(lista, "UFOs per Month", 'static/data/kuukaudet_chart.svg')

def laskePaivat():
    tulokset = db.query("SELECT strftime('%w', h.date) pv, COUNT(*) lkm FROM havainto h GROUP BY strftime('%w', h.date)")
    paivat = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    lista = []
    i = 0
    for t in tulokset:
        if t['pv']: #Poistetaan None arvot tilastotosta
            lista.append([paivat[i], t['lkm']])
            i += 1
    luoChart(lista, "UFOs per Weekday", 'static/data/paivat_chart.svg')

def laskeTunnit():
    tulokset = db.query("SELECT strftime('%H', h.time) t, COUNT(*) lkm FROM havainto h GROUP BY strftime('%H', h.time)")
    lista = []
    for t in tulokset:
        if t['t']: #Poistetaan None arvot tilastotosta
            lista.append([t['t'], t['lkm']])
    luoChart(lista, "UFOs per Time of Day", 'static/data/tunnit_chart.svg')

db = dataset.connect('sqlite:///../Tietokanta/tietokanta.db')

laskeOsavaltiot()
laskeKaupungit()
laskeKuukaudet()
laskeVuodet()
laskePaivat()
laskeTunnit()



