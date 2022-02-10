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
    users = db.relationship('Users', backref='group')

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
    versions = db.relationship('Versions', backref='cname')

    def __repr__(self):
        return (self.name)
#========TABLE PRODUCT============
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String())
    versions = db.relationship('Versions', backref='pname')

#========TABLE COMPONENT============
class Components(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compname = db.Column(db.String())
    versions = db.relationship('Versions', backref='compname')

#========TABLE VERSION============
class Versions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String)
    cust_id = db.Column(db.Integer, db.ForeignKey('customers.id')) 
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
#============================================================================

#DB-QUERIES


# def version_query(): return Versions.query

#============================================================================

#FORMMODELS

#========FORM-SCHEMA-LAUNCHINSTANCES============
class LaunchInstanceForm(FlaskForm):
    customer = SelectField('customer', choices=[])
    product = SelectField('product', choices=[])
    component = SelectField('component', choices=[])
    version = SelectField('version', choices=[])
    instance = StringField('instance')


#==============================================================================
#Application Routes

@app.route("/", methods=['GET'])
def index():
        return render_template('login.html')

@app.route("/login", methods=['POST', 'GET'])
def login():
            return render_template('launchinstances.html')
        
@app.route("/logout", methods=['POST', 'GET'])
def logout():
    return render_template('logout.html')

@app.route("/launchinstances", methods=['POST', 'GET'])
def launchinstances():
    form = LaunchInstanceForm()
    form.customer.choices = [(customers.id,customers.cname)for customers in Customers.query.all()]
    form.product.choices =[(products.id, products.pname)for products in Products.query] #.filter_by(id='1').all()
    form.version.choices = [(versions.id, versions.version)for versions in Versions.query]
    form.component.choices = [(components.id, components.compname)for components in Components.query]
    return render_template('launchinstances.html', form=form)

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

@app.route("/testpage/", methods=['POST', 'GET'])
def testpage():
    form = LaunchInstanceForm()
    form.customer.choices = [(customers.id,customers.cname)for customers in Customers.query.all()]
    form.product.choices = ['--select--']#[(products.id, products.pname)for products in Products.query] #.filter_by(id='1').all()
    form.version.choices = ['--select--']#[(versions.id, versions.version)for versions in Versions.query]
    form.component.choices = ['--select--']  #[(components.id, components.compname)for components in Components.query]
    return render_template('testpage.html', form=form )

@app.route("/getproducts/<customerid>", methods=['POST', 'GET'])
def get_products_per_customer(customerid):
        products_per_customer = db.session.query(Products.pname, Products.id).join(Versions, Products.id==Versions.product_id).distinct(Products.id).all()#
        print(products_per_customer)
        availableproducts = []
        for items in products_per_customer:
            products={}
            products['id'] = items.id
            products['product'] = items.pname
            availableproducts.append(products)
            #print(products)
        #print(availableproducts)
        return jsonify({"products" : availableproducts})

@app.route("/getversions/<productid>", methods=['POST', 'GET'])
def get_versions_per_product(productid):
        versions_per_product = db.session.query(Versions.id, Versions.version, Products).join(Versions, Products.id==Versions.product_id).filter(Versions.product_id==productid).all()
        #print(versions_per_product)
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
        components_per_version = db.session.query(Components.id, Components.compname, Products, Versions).join(Versions, Products.id==Versions.product_id).filter(Versions.id==versionid).all()
        #print(components_per_version)
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
    response = json.loads(strjson)
    for i in response:
        insertdatafordb=launchrequests(id=None,customer=i['customer'],product=i['product'],version=i['version'],component=i['component'],instances=i['instance'])
        db.session.add(insertdatafordb)
        db.session.commit()
        print('successfully inserted data in db')
    return redirect(url_for('userservicelist'))

#========ALL CODE ENDS HERE============



#========RUN APP WITH PRE-DEFINED CONFIGS============
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)