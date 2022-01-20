from flask import Flask,render_template,url_for,session
from flask_sqlalchemy import SQLAlchemy
from database import db_conn_response
from configparser import ConfigParser

app = Flask(__name__)
dbconfig = ConfigParser()
dbconfig.read('database.ini')
app.config['SQLALCHEMY_DATABASE_URI'] = dbconfig.get('postgresdb','uri')

db_conn_response()

@app.route("/")
def index():
    return render_template('login.html')

@app.route("/login")
def login():
    return render_template('login.html')

@app.route("/logout")
def logout():
    return render_template('logout.html')

@app.route("/register")
def register():
    return render_template('register.html')

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

@app.route("/cisghome")
def cisghome():
    return render_template('cisgservice.html')

if __name__ == '__main__':
    app.run(debug=True, use_debugger=False, use_reloader=False, passthrough_errors=True)
