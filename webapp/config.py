import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:rzQgZ6Ftwv@127.0.0.1:5432/news_db"

SECRET_KEY = "fahkffdgjl45&*HJK^GIYJH&JHG#$%DUJNKHJ"

SQLALCHEMY_TRACK_MODIFICATIONS = False
SECURITY_REGISTERABLE = True
SECURITY_SEND_REGISTER_EMAIL = False

# Flask-Security config
SECURITY_URL_PREFIX = "/admin"
SECURITY_PASSWORD_HASH = "pbkdf2_sha512"
SECURITY_PASSWORD_SALT = "ATGUOHAELKiubahiughaerGOJAEGj"

# Flask-Security URLs, overridden because they don't put a / at the end
SECURITY_LOGIN_URL = "/login/"
SECURITY_LOGOUT_URL = "/logout/"
SECURITY_REGISTER_URL = "/register/"

SECURITY_POST_LOGIN_VIEW = "/admin/"
SECURITY_POST_LOGOUT_VIEW = "/admin/"
SECURITY_POST_REGISTER_VIEW = "/admin/"
