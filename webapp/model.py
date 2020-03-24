from flask_sqlalchemy import SQLAlchemy
from webapp.forms import dtForm, coordinatesForm

db = SQLAlchemy()

class UserDT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt_start = db.Column(db.DateTime, nullable=False)
    dt_finish = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return "<UserDT {} {}>".format(self.dt_start, self.dt_finish)

class UserCoordinates(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return "<UserCoordinates {} {}>".format(self.latitude, self.longitude)
