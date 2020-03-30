from flask_sqlalchemy import SQLAlchemy
from webapp.forms import dtcoorForm

db = SQLAlchemy()

class UserDTCoor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt_start = db.Column(db.DateTime, nullable=False)
    dt_finish = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
  
    def __repr__(self):
        return "<UserDTCoor {} {}>".format(self.dt_start, self.dt_finish, self.latitude, self.longitude)
