from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class UserDT(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt_start = db.Column(db.DateTime, nullable=False)
    dt_finish = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<UserDT {}>'.format(self.username)