from flask import Flask, render_template, Response

def create_app():
    app = Flask(__name__)

    @app.route('/')
    def start_page():
        title = 'Отслеживание машин'
        header1 = 'Отслеживание машин Ситимобил в указанной локации'
        return render_template('index.html', page_title = title, header1 = header1)

    return app