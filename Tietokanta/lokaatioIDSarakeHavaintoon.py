import dataset, sqlalchemy
db = dataset.connect('sqlite:///tietokanta.db')
table = db.load_table('havainto')
table.create_column('lokaatioID', sqlalchemy.INTEGER)