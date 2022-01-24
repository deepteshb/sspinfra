from flask import Flask,render_template,url_for,session,g,request
from flask_sqlalchemy import SQLAlchemy
from database import get_response

app = Flask(__name__)

#database helpers
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route("/")
def index():
    return render_template('login.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    return render_template('login.html')

@app.route("/logout")
def logout():
    return render_template('logout.html')

@app.route("/catalog")
def catalog():
    return render_template('servicecatalog.html')

@app.route("/myservices")
def myservices():
    return render_template('myservices.html')

@app.route("/platform")
def platform():
    return render_template('platform.html')

@app.route("/selectvm")
def selectvm():
    return render_template('selectvm.html')

@app.route("/addservice")
def addservice():
    return render_template('cisgaddservice.html')

@app.route("/multistep")
def multistep():
    return render_template('multistep.html')

@app.route("/cisghome")
def cisghome():
    get_response()
    return render_template('cisgservices.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
