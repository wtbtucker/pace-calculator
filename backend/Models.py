from extensions import db

class Zones(db.Model):
    id = db.Column(db.String(6), primary_key=True)
    type = db.Column(db.Text)

class Zipcodes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(5), nullable=False, unique=True)
    zone = db.Column(db.String(6), db.ForeignKey(Zones.id))

class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.DateTime)
    temperature = db.Column(db.Float)
    dew_point = db.Column(db.Float)
    forecast = db.Column(db.Text)
    zone = db.Column(db.String(6), db.ForeignKey(Zones.id))

class SimpleForecasts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_time = db.Column(db.Text)
    weather = db.Column(db.Text)
    zone = db.Column(db.String(6), db.ForeignKey(Zones.id))

