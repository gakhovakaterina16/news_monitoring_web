from flask import Flask, render_template, flash, redirect, url_for, request

from webapp.forms import dtForm

from webapp.model import db, UserDT

from datetime import datetime

import requests

import http.client

import socket

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

    def get_coordinates(ip_address):
        try:
            response = requests.get("http://ip-api.com/json/{}".format(ip_address))
            js = response.json()
            latitude = js['lat']
            longitude = js['lon']
            return latitude, longitude
        except Exception:
            return "Unknown"

    def get_ip_v1():
        # Возвращается ip=b'91.78.94.26'. Если этот ip давать в get_coordinates без b, 
        # то возвращаются координаты Сенатской площади
        conn = http.client.HTTPConnection("ifconfig.me")
        conn.request("GET", "/ip")
        ip_v1 = conn.getresponse().read()
        return ip_v1
    
    def get_ip_v2():
        # Возвращается ip=192.168.1.66. Если этот ip давать в get_coordinates, то возвращается Unknown
        ip_v2 = socket.gethostbyname(socket.getfqdn())
        return ip_v2
    
    def get_ip_v3():
        # Возвращается ip localhost
        ip_v3 = request.remote_addr
        return ip_v3
        
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
    
    ip_v1 = get_ip_v1()
    print(f"ip_v1 = {ip_v1}")
    ip_v1 = "91.78.94.26"
    print(f"coordinates: {get_coordinates(ip_v1)}")

    ip_v2 = get_ip_v2()
    print(f"ip_v2 = {ip_v2}")
    print(f"coordinates: {get_coordinates(ip_v2)}")

    ip_v3 = get_ip_v3()
    print(f"ip_v3 = {ip_v3}")
    print(f"coordinates: {get_coordinates(ip_v3)}")
    
    return app