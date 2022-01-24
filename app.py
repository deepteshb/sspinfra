from flask import Flask,render_template,url_for,session,g,request
from flask_sqlalchemy import SQLAlchemy
from database import connect_db, get_db

app = Flask(__name__)

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
        query = db.execute('SELECT uname, groupid FROM users WHERE uname = ?', [name]).fetchall()
        print('query')
        return render_template('cisgservices.html')
    return render_template('login.html')

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    return render_template('logout.html')

@app.route("/catalog", methods=['POST', 'GET'])
def catalog():
    return render_template('servicecatalog.html')

@app.route("/myservices", methods=['POST', 'GET'])
def myservices():
    return render_template('myservices.html')

@app.route("/platform", methods=['POST', 'GET'])
def platform():
    return render_template('platform.html')

@app.route("/selectvm", methods=['POST', 'GET'])
def selectvm():
    return render_template('selectvm.html')

@app.route("/addservice", methods=['POST', 'GET'])
def addservice():
    return render_template('cisgaddservice.html')

@app.route("/cisghome", methods=['POST', 'GET'])
def cisghome():
    return render_template('cisgservices.html')

@app.route("/multistep", methods=['POST', 'GET'])
def multistep():
    return render_template('multistep.html')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
