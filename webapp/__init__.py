from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_admin import helpers as admin_helpers
import flask_admin
from flask_security import Security, SQLAlchemyUserDatastore

from webapp.views import MyModelView
from webapp.forms import dtcoorForm
from webapp.model import db, UserDTCoor, Role, User
from webapp.server.tasks import main
from webapp.server.utils import return_news_to_user

from datetime import datetime


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
        return render_template("index.html", page_title=title,
                               header1=header1, form=dtcoor_form)

    @app.route("/process_dtcoor", methods=["POST"])
    def process_dtcoor():
        form = dtcoorForm()
        if form.validate_on_submit:
            dt_start_enter = datetime.strptime(form.dt_start.raw_data[0],
                                               "%Y-%m-%dT%H:%M")
            dt_finish_enter = datetime.strptime(form.dt_finish.raw_data[0],
                                                "%Y-%m-%dT%H:%M")
            latitude_enter = form.latitude.raw_data[0]
            longitude_enter = form.longitude.raw_data[0]

            # Ищем в БД нужные новости
            result_news = return_news_to_user(dt_start_enter, dt_finish_enter, latitude_enter, longitude_enter)

            dtcoor_enter = UserDTCoor(dt_start=dt_start_enter,
                                      dt_finish=dt_finish_enter,
                                      latitude=latitude_enter,
                                      longitude=longitude_enter)
            db.session.add(dtcoor_enter)
            db.session.commit()
            if result_news:
                title = "Новости"
                return render_template("result.html", page_title=title, news_list=result_news)
            else:
                return redirect(url_for("nodata"))

    @app.route("/nodata")
    def nodata():
        title = "Новости"
        header1 = "По данному запросу ничего не найдено :("
        return render_template("nodata.html", page_title=title, header1=header1)
            
    @app.route("/parse")
    def parse():
        main()
        return redirect(url_for("start_page"))


    """
    @app.route("/get_ip", methods=["GET"])
    def get_ip():
        return jsonify({'ip': request.remote_addr}), 200

    @app.route("/get_coordinates", methods=["GET"])
    def get_coordinates(ip_address):
        try:
            response = requests.get("http://ip-api.com/json/{}".format(
                                                                       ip_address))
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

# Create admin
admin = flask_admin.Admin(
    app,
    'CMS: Auth',
    base_template='my_master.html',
    template_mode='bootstrap3',
)

# Add model views
admin.add_view(MyModelView(Role, db.session))
admin.add_view(MyModelView(User, db.session))


# define a context processor for merging flask-admin's template context
# into the flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

# добавляем две роли: user и superuser, - в БД, таблица role.
# добавляем пользоватлея admin, с ролью superuser, который может
# задавать роли всем зарегистрированным пользователям.
# у такого пользователя email - admin, пароль - admin.
# всё это добавляется, если в таблице role нет роли superuser или
# если в таблице user нет пользователя с email = admin

@app.before_first_request
def add_roles_and_admin():

    with app.app_context():
        if User.query.filter_by(email='admin').count() == 0 or Role.query.filter_by(name='superuser') == 0:
            super_user_role = Role(name='superuser')
            user_role = Role(name='user')
            db.session.add(super_user_role)
            db.session.add(user_role)
            db.session.commit()
            user_datastore.create_user(
                first_name='admin',
                email='admin',
                password='admin',
                roles=[super_user_role, ]
            )
            db.session.commit()
