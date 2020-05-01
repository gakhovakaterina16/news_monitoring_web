from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin

db = SQLAlchemy()


# модель для дат и координат, которые вводит пользователь
class UserDTCoor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dt_start = db.Column(db.DateTime, nullable=False)
    dt_finish = db.Column(db.DateTime, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)

    def __repr__(self):
        return "<UserDTCoor {} {}>".format(self.dt_start, self.dt_finish,
                                           self.latitude, self.longitude)


# Define models
roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)


# описание модели Role
class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __str__(self):
        return self.name


# описание модели User
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __str__(self):
        return self.email

# описание модели News
class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    link = db.Column(db.String(255))
    date_and_time = db.Column(db.DateTime, index=True)
    text = db.Column(db.String(15000))
    address = db.Column(db.String(255))
    street = db.Column(db.String(50))
    lat = db.Column(db.Float(255))
    lon = db.Column(db.Float(255))