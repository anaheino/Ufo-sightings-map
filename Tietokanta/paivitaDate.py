import dataset, datetime

db = dataset.connect('sqlite:///tietokanta.db')

havaintoTable = db.load_table('havainto')
for row in havaintoTable:
    if row['date'] == '':
        continue
    dateTaulukko = row['date'].split('/')
    dateSqlite = dateTaulukko[2] + '-' + dateTaulukko[0] + '-' + dateTaulukko[1]
    data = dict(id=row['id'], date=dateSqlite)
    havaintoTable.update(data, ['id'])