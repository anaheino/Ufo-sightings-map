# UFO-Project

The goal of the project is to display UFO sightings on the map, and let the user filter sightings with various parameters. 

The UFO reports are copyrighted by the National UFO Reporting Center. The database itself won't be included in the version control.

### Overview

The project is divided into three modules: 
- Flask-based web application with folium maps.
- Sqlite3 database, coordinates via OpenStreetMap.
- Scrapy-based spider to retrieve data from nuforc.org.
- Due to the wishes of nuforc.org, this project doesn't include the original database or some of the csv files required for this application to be fully operational.
- Project is launched by navigating to app folder and starting 'views.py' file.

### UFO-Project

Our subject was the research of UFO phenomena. Our goal was to develop an application that would make UFO sightings more easily
accessible and comprehensible. We thought that a good way to achieve this would be displaying the UFO sightings on a map,
let the user filter sightings with various parameters such as country and date and also show some statistics about
the UFO sightings. The UFO reports are copyrighted by the National UFO Reporting Center and thus our application is intended
for personal use only.

Our project is divided into three modules: Flask-based web application with folium maps, Sqlite3 database with sighting
coordinates via OpenStreetMap API Nominatim and Scrapy-based spider to retrieve data from nuforc.org. The application is
easily modifiable to present other types of (especially location) data. The code is written in Python (v2.7). To run the
flask application, run views.py located in app folder. To run the scrapy crawler go to ufoscrapy folder and run "scrapy
crawl ufo".

Licenced under MIT Licence.


### Tech

* [Flask]
* [Twitter Bootstrap] 
* [folium]
* [jQuery]
* [SQlite]
* [SQLAlchemy]
* [Whoosh]
* [dataset]
* [Pygal]
* [Scrapy]

### Requirements

Python 2.7, requirements.txt



   [Flask]: <http://flask.pocoo.org>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>   
   [folium]: <https://pypi.python.org/pypi/folium>   
   [jQuery]: <http://jquery.com>
   [SQlite]: <https://www.sqlite.org/>
   [SQLAlchemy]: <http://www.sqlalchemy.org>
   [Whoosh]: <http://pythonhosted.org/Whoosh/>
   [dataset]: <https://dataset.readthedocs.org/en/latest/>
   [Pygal]: <http://www.pygal.org/en/latest/>
   [Scrapy]: <http://scrapy.org/>
