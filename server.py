from flask import Flask, render_template, Response
import cgi
app = Flask(__name__)

@app.route('/')
def start_page():
    title = 'Отслеживание машин'
    header1 = 'Отслеживание машин Ситимобил в указанной локации'
    return render_template('index.html', page_title = title, header1 = header1)

@app.route("/forward/", methods=['POST'])
def get_dt():
    dt_form = cgi.FieldStorage()
    dt_start = dt_form.getvalue("dt_start_html")
    return dt_start
    
if __name__ == "__main__":
    app.run(debug=True)