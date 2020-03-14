from flask import Flask, render_template, flash, redirect, url_for

from webapp.forms import dtForm

from webapp.model import db, UserDT

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
            dt_start = UserDT.query.filter_by(dt_start=form.dt_start.data).first()
            dt_finish = UserDT.query.filter_by(dt_finish=form.dt_finish.data).first()
            return redirect(url_for("start_page"))

    return app