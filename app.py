#============================================================================
#ALL IMPORTS
from flask import Flask,render_template,url_for,jsonify,session,g,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_cors import CORS
import json
import sqlite3
import os
import datetime
import sys

#============================================================================
#CORE APP INITIALIZATION


app = Flask(__name__)

#============================================================================
#GLOBAL APP CONFIGURATION

app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:/myProjects/sspinfra/sspinfra.db'

#============================================================================
#GLOBALDEFINITIONS




#============================================================================
#DBMODELS AND SCHEMA DEFINITIONS
db = SQLAlchemy(app)


#========TABLE GROUPS============
class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String)
    users = db.relationship('Users', backref='groups')

#========TABLE USERS============
class Users(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String)
    authenticated = db.Column(db.Integer)
    status = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id')) 

#========TABLE CUSTOMER============
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String())

#========TABLE PRODUCT============
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String())
    versions = db.relationship('Versions', backref='products')

#========TABLE COMPONENT============
class Components(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compname = db.Column(db.String())
    versions = db.relationship('Versions', backref='components')

#========TABLE VERSION============
class Versions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id')) 
    comp_id = db.Column(db.Integer, db.ForeignKey('components.id')) 

#============================================================================
class launchrequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String)
    product = db.Column(db.String)
    version = db.Column(db.String)
    component = db.Column(db.String)
    instances = db.Column(db.Integer)
    createdby = db.Column(db.String)
    request_id=db.Column(db.Integer, db.ForeignKey('requestsmapping.id'))
#============================================================================
class requestsmapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.Integer)
    createdby=db.Column(db.String)
    createdate=db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status=db.Column(db.String)
#============================================================================

#DB-QUERIES


# def version_query(): return Versions.query

#============================================================================

#FORMMODELS

#========FORM-SCHEMA-LAUNCHINSTANCES============
class LaunchInstanceForm(FlaskForm):
    product = SelectField('product', choices=[])
    component = SelectField('component', choices=[])
    version = SelectField('version', choices=[])
    instance = StringField('instance')
    customer = SelectField('customer', choices=[])
    created_by = StringField('createdby')

#==============================================================================
#Application Routes

@app.route("/", methods=['GET'])
def index():
    if 'username' in session:
        user = session['username']
        print(user)
        return render_template('userservicelist.html',user=user)
    return render_template('login.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['userid']
        return redirect(url_for('index'))
    return render_template('loginerror.html')

@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return render_template('logout.html')

@app.route("/userservicelist", methods=['POST', 'GET'])
def userservicelist():
    if 'username' in session:
        user = session['username']
        return render_template('userservicelist.html',user=user)
    return render_template('loginerror.html')

@app.route("/launchinstances", methods=['POST', 'GET'])
def launchinstances():
    if 'username' in session:
        user = session['username']
        
        
        form = LaunchInstanceForm()
        form.customer.choices = [(customers.id,customers.cname)for customers in Customers.query.all()]
        form.product.choices =[(products.id, products.pname)for products in Products.query] #.filter_by(id='1').all()
        form.version.choices = [(versions.id, versions.version)for versions in Versions.query]
        form.component.choices = [(components.id, components.compname)for components in Components.query]
        return render_template('launchinstances.html', form=form, user=user)
    return render_template('loginerror.html')



@app.route("/addtemplate", methods=['POST', 'GET'])
def addtemplate():
    if 'username' in session:
        user = session['username']
        return render_template('addtemplate.html',user=user)
    return render_template('loginerror.html')

@app.route("/cisghome", methods=['POST', 'GET'])
def cisghome():
    if 'username' in session:
        user = session['username']
        return render_template('cisgservices.html',user=user)
    return render_template('loginerror.html')

@app.route("/reviewinstances", methods=['POST', 'GET'])
def reviewinstances():
    if 'username' in session:
            user = session['username']
            return render_template('reviewinstances.html',user=user)
    return render_template('loginerror.html')                                                   

# This particular route is for testing purposes only 

@app.route("/testpage/", methods=['POST', 'GET'])
def testpage():
    if 'username' in session:
        user = session['username']
        form = LaunchInstanceForm()
        form.customer.choices = [(customers.id,customers.cname)for customers in Customers.query.all()]#[(customers.id,customers.cname)for customers in Customers.query.all()]
        form.product.choices = [(products.id, products.pname)for products in Products.query.all()] #.filter_by(id='1').all()
        form.version.choices = ['--select--']#[(versions.id, versions.version)for versions in Versions.query]
        form.component.choices = ['--select--']#[(components.id, components.compname)for components in Components.query]
        return render_template('testpage.html', form=form, user=user )
    return render_template('loginerror.html')

@app.route("/getproducts", methods=['POST', 'GET'])
def get_products_per_customer():
        products_per_customer = db.session.query(Products.id, Products.pname).distinct(Products.id).all()#
        print(products_per_customer)
        availableproducts = []
        for items in products_per_customer:
            products={}
            products["id"] = items.id
            products["product"] = items.pname
            availableproducts.append(products)
            print(products)
        print(availableproducts)
        return jsonify({"products" : availableproducts})

@app.route("/getversions/<productid>", methods=['POST', 'GET'])
def get_versions_per_product(productid):
        versions_per_product = db.session.query(Versions.id, Versions.version).filter(Versions.product_id==productid).all()
        print(versions_per_product)
        availableversions = []
        for items in versions_per_product:
            versions={}
            versions['id'] = items.id
            versions['version'] = items.version
            availableversions.append(versions)
            #print(versions)
        #print(availableversions)
        return jsonify({"versions" : availableversions})

@app.route("/getcomponents/<versionid>", methods=['POST', 'GET'])
def get_components_per_version(versionid):
        components_per_version = db.session.query(Components.id, Components.compname,Versions).join(Versions).filter(Versions.id==versionid).filter().all()
        print(components_per_version)
        availablecomponents = []
        for items in components_per_version:
            component={}
            component['id'] = items.id
            component['compname'] = items.compname
            availablecomponents.append(component)
            #print(component)
        #print(availablecomponents)
        return jsonify({"components" : availablecomponents})


@app.route("/createformcollection/<strjson>", methods=['POST', 'GET'])
def createformcollection(strjson):
    if request.method == 'POST':
        response = json.loads(strjson) 
        print("response recd is")
        print(response)
        for items in response:
            createdby = items['createdby']
            dqqueryforrequestid = requestsmapping(id=None,customer=items['customer'],createdby=items['createdby'],createdate=None, status=None)
        db.session.add(dqqueryforrequestid)
        db.session.commit()
        for i in response:
            requestid=dqqueryforrequestid.id
            insertdatafordb=launchrequests(id=None,customer=i['customer'],product=i['product'],version=i['version'],component=i['component'],instances=i['instance'], createdby=i['createdby'],request_id=requestid)
            db.session.add(insertdatafordb)
        db.session.commit()
        db.session.close()
        #print('successful')
    return ("success")

#========ALL CODE ENDS HERE============



#========RUN APP WITH PRE-DEFINED CONFIGS============
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)