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
        try:
            if request.method == 'POST':
                db = get_db()
                name = request.form['userid']
                uname = db.execute('SELECT * FROM users WHERE username=?', [name]).fetchone()[1]
                gid =  db.execute('SELECT * FROM users WHERE username=?', [name]).fetchone()[2]
                print(name)
                if uname == name and gid == 1:
                        return render_template('cisgservices.html')
                elif uname == name and gid == 2:
                            return render_template('userservicelist.html')
                else:
                    return render_template('loginerror.html')
            else:
                return render_template('login.html')
        except TypeError:
            return render_template('loginerror.html')
        

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('user', None)
    return render_template('logout.html')

@app.route("/launchinstances", methods=['POST', 'GET'])
def launchinstances():
    if request.method == 'GET':
                db = get_db()
                availableproducts = db.execute('SELECT cus.cust_id as customer, p.pname as product, co.type as component, v.version as version FROM versions v, product p, component co, customer cus WHERE v.cust_id =1 AND v.pid=p.id AND v.cid=co.id AND v.cust_id=cus.id ORDER BY v.cid').fetchall()
                for rows in availableproducts:
                    print(rows['customer']+'>'+ rows['product']+'>'+rows['component']+'>'+rows['version'])
                

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

@app.route("/reviewinstances", methods=['POST', 'GET'])
def review():
    return render_template('reviewinstances.html')


# This particular route is for testing purposes only 
@app.route("/testpage", methods=['POST', 'GET'])
def testpage():
    
    return render_template('testpage.html')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
