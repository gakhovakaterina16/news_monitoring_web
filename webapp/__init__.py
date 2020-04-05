from flask import Flask, render_template, flash, redirect, url_for, request, jsonify

from flask_migrate import Migrate

from flask_admin import helpers as admin_helpers

import flask_admin

from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user

from flask_security.utils import encrypt_password

from flask_admin.contrib import sqla

from webapp.views import MyAdminView

from webapp.forms import dtcoorForm

from webapp.model import db, UserDTCoor, Role, User

from datetime import datetime

import requests

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.config.from_pyfile("config.py")
    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route("/")
    def start_page():
        title = "Новости"
        header1 = "Отслеживание новостей в указанной локации"
        dtcoor_form = dtcoorForm()
        return render_template("index.html", page_title=title, header1=header1, form=dtcoor_form)
       
    @app.route("/process_dtcoor", methods=["POST"])
    def process_dtcoor():
        form = dtcoorForm()
        if form.validate_on_submit:
            dt_start_enter = datetime.strptime(form.dt_start.raw_data[0],"%Y-%m-%dT%H:%M")
            dt_finish_enter = datetime.strptime(form.dt_finish.raw_data[0],"%Y-%m-%dT%H:%M")
            latitude_enter = form.latitude.raw_data[0]
            longitude_enter = form.longitude.raw_data[0]
            dtcoor_enter = UserDTCoor(dt_start=dt_start_enter, dt_finish=dt_finish_enter, latitude=latitude_enter, longitude=longitude_enter)
            db.session.add(dtcoor_enter)
            db.session.commit()     
            return redirect(url_for("start_page"))

    """
    @app.route("/get_ip", methods=["GET"])
    def get_ip():   
        return jsonify({'ip': request.remote_addr}), 200  
    
    @app.route("/get_coordinates", methods=["GET"])
    def get_coordinates(ip_address):
        try:
            response = requests.get("http://ip-api.com/json/{}".format(ip_address))
            js = response.json()
            latitude = js['lat']
            longitude = js['lon']
            return latitude, longitude
        except Exception:
            return "Unknown"
    """
    return app


app = create_app()

# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

"""
# Create admin interface
admin = admin.Admin(name="CMS", template_mode='bootstrap3')
admin.add_view(MyAdminView(name="view1", category='view1'))
admin.init_app(app)
"""
# Create admin
admin = flask_admin.Admin(
    app,
    'CMS: Auth',
    base_template='my_master.html',
    template_mode='bootstrap3',
)