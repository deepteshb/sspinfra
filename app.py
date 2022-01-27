from flask import Flask,render_template,url_for,session,g,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from database import connect_db, get_db
import sqlite3
import os
import datetime
import sys

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


#database helpers
@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route("/", methods=['GET'])
def index():
        return render_template('login.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        db = get_db()
        name = request.form['userid']
       
        cur = db.execute('SELECT * FROM users WHERE username=?', [name]).fetchall()
        for item in cur:
            print(item['username'])
            #print('username provided by user is ' + name + '| username in db is '+ row.username + '|group id is ' + str(row.gid))
              
        
        return render_template('login.html')

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('user', None)
    return render_template('logout.html')

@app.route("/launchinstances", methods=['POST', 'GET'])
def launchinstances():
    return render_template('launchinstances.html')

@app.route("/userservicelist", methods=['POST', 'GET'])
def userservicelist():
    return render_template('userservicelist.html')

@app.route("/addtemplate", methods=['POST', 'GET'])
def addtemplate():
    return render_template('addtemplate.html')

@app.route("/cisghome", methods=['POST', 'GET'])
def cisghome():
    return render_template('cisgservices.html')


# This particular route is for testing purposes only 
@app.route("/testpage", methods=['POST', 'GET'])
def testpage():
    
    return render_template('testpage.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
