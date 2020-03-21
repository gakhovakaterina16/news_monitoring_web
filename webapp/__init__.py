from flask import Flask, render_template, flash, redirect, url_for, request, jsonify

from webapp.forms import dtForm

from webapp.model import db, UserDT

from datetime import datetime

import requests

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")
    db.init_app(app)

    @app.route("/")
    def start_page():
        title = "Отслеживание машин"
        header1 = "Отслеживание машин Ситимобил в указанной локации"
        dt_form = dtForm()
        return render_template("index.html", page_title=title, header1=header1, form=dt_form)
       
    @app.route("/process_dt", methods=["POST"])
    def process_dt():
        form = dtForm()
        if form.validate_on_submit:
            dt_start_enter = datetime.strptime(form.dt_start.raw_data[0],"%Y-%m-%dT%H:%M")
            dt_finish_enter = datetime.strptime(form.dt_finish.raw_data[0],"%Y-%m-%dT%H:%M")
            dt_enter = UserDT(dt_start=dt_start_enter, dt_finish=dt_finish_enter)
            db.session.add(dt_enter)
            db.session.commit()     
            return redirect(url_for("start_page"))
    
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
    
    return app