#============================================================================
#ALL IMPORTS
from tokenize import String
from flask import Flask,render_template, request_tearing_down,url_for,jsonify,session,g,request,session,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField
from wtforms_sqlalchemy.fields import QuerySelectField
from flask_cors import CORS
from jenkinsapi.jenkins import Jenkins
import jenkins
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///D:\Projects\sspinfra\sspinfra.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']='False'
#app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:abc123@localhost:5432/sspinfra_dev"


#============================================================================
#GLOBALDEFINITIONS




#============================================================================
#DBMODELS AND SCHEMA DEFINITIONS
db = SQLAlchemy(app)
migrate = Migrate(app, db)



#========TABLE GROUPS============

class Groups(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group = db.Column(db.String(50))
    users = db.relationship('Users', backref='groups') 

#========TABLE USERS============
class Users(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(50))
    authenticated = db.Column(db.Integer)
    status = db.Column(db.Integer)
    group_id = db.Column(db.Integer, db.ForeignKey('groups.id')) 

#========TABLE CUSTOMER============
class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(50))

#========TABLE PRODUCT============
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pname = db.Column(db.String(50))
    versions = db.relationship('Versions', backref='products')

#========TABLE COMPONENT============
class Components(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    compname = db.Column(db.String(50))
    versions = db.relationship('Versions', backref='components')

#========TABLE VERSION============
class Versions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.String(50))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id')) 
    comp_id = db.Column(db.Integer, db.ForeignKey('components.id')) 

#============================================================================
class launchrequests(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    #customer = db.Column(db.String(50))
    customer = db.Column(db.Integer)
    product = db.Column(db.String)
    version = db.Column(db.String)
    component = db.Column(db.String)
    instances = db.Column(db.Integer)
    #datastore = db.Column(db.String)
    createdby = db.Column(db.String)
    request_id=db.Column(db.Integer, db.ForeignKey('requestsmapping.id'))
    status = db.Column(db.String)
#============================================================================
class requestsmapping(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.Integer)
    createdby=db.Column(db.String)
    createdate=db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status=db.Column(db.String)
#============================================================================

""" class datastore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ds_name = db.Column(db.String) """

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
    #datastore = SelectField('datastore')
    customer = SelectField('customer', choices=[])
    created_by = StringField('createdby')

#==============================================================================
#Application Routes

@app.route("/", methods=['GET'])
def index():
    if 'username' in session:
        user = session['username']
        #print(user)
        return redirect(url_for('userservicelist'))
    return render_template('login.html')


@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['userid']
        user = session['username']
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
        table = db.session.query(Customers.cname, launchrequests.product, launchrequests.version, launchrequests.component, launchrequests.instances, launchrequests.request_id, launchrequests.status).filter(launchrequests.customer == Customers.id).filter(launchrequests.createdby == user).all()
        #print('table is :')
        #print(table)
        tabledata = []
        for items in table:
            data={}
            data['requestid'] = items.request_id
            data["customer"] = items.cname
            data["product"] = items.product
            data["version"] = items.version
            data["component"] = items.component
            data["instances"] = items.instances
            data["status"] = items.status
            tabledata.append(data)
            #print(data)
        #print(tabledata)
        return render_template('userservicelist.html',user=user, tabledata=tabledata)        
    return render_template('loginerror.html')

@app.route("/launchinstances", methods=['POST', 'GET'])
def launchinstances():
    if 'username' in session:
        user = session['username']
        form = LaunchInstanceForm()
        form.customer.choices = [(customers.id,customers.cname)for customers in Customers.query.all()]#[(customers.id,customers.cname)for customers in Customers.query.all()]
        form.product.choices = [(products.id, products.pname)for products in Products.query.all()] #.filter_by(id='1').all()
        form.version.choices = ['--select--']#[(versions.id, versions.version)for versions in Versions.query]
        form.component.choices = ['--select--']#[(components.id, components.compname)for components in Components.query]
        #form.datastore.choices = [(datastore.id, datastore.ds_name)for datastore in datastore.query.all()]
        return render_template('launchinstances.html', form=form, user=user )
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
        table = db.session.query(Customers.cname, launchrequests.product, launchrequests.version, launchrequests.component, launchrequests.instances,launchrequests.request_id, launchrequests.status).filter(launchrequests.customer == Customers.id).filter(launchrequests.createdby == user).filter(launchrequests.status=='NEW').all()
        #print('table is :')
        #print(table)
        tabledata = []
        for items in table:
            data={}
            data['requestid'] = items.request_id
            data["customer"] = items.cname
            data["product"] = items.product
            data["version"] = items.version
            data["component"] = items.component
            data["instances"] = items.instances
            #data["datastore"] = items.datastore
            data["status"] = items.status
            tabledata.append(data)
            #print(data)
        #print(tabledata)
        return render_template('reviewinstances.html',user=user, tabledata=tabledata)
    return render_template('loginerror.html')                                                   

  

@app.route("/getproducts", methods=['POST', 'GET'])
def get_products_per_customer():
        products_per_customer = db.session.query(Products.id, Products.pname).distinct(Products.id).all()#
        #print(products_per_customer)
        availableproducts = []
        for items in products_per_customer:
            products={}
            products["id"] = items.id
            products["product"] = items.pname
            availableproducts.append(products)
            #print(products)
        #print(availableproducts)
        return jsonify({"products" : availableproducts})

@app.route("/getversions/<productid>", methods=['POST', 'GET'])
def get_versions_per_product(productid):
        versions_per_product = db.session.query(Versions.id, Versions.version).filter(Versions.product_id==productid).all()
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
        components_per_version = db.session.query(Components.id, Components.compname,Versions).join(Versions).filter(Versions.id==versionid).filter().all()
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
    if request.method == 'POST':
        response = json.loads(strjson)
        #print("response recd is")
        #print(response)
        for items in response:
            createdby = items['createdby']
            dqqueryforrequestid = requestsmapping(id=None,customer=items['customer'],createdby=createdby,createdate=None, status="NEW")
        db.session.add(dqqueryforrequestid)
        db.session.commit()
        for i in response:
            requestid=dqqueryforrequestid.id
            insertdatafordb=launchrequests(id=None,customer=i['customer'],product=i['product'],version=i['version'],component=i['component'],instances=i['instance'], createdby=i['createdby'],request_id=requestid, status="NEW")
            db.session.add(insertdatafordb)
        db.session.commit()
        db.session.close()
        #print('successful')
    return ("success")

@app.route("/confirmlaunch", methods=['POST', 'GET'])
def confirmlaunch():
    #server = jenkins.Jenkins('http://someip/', username='devopsadmin', password='somepasswd!!')
    #buildnow1 = server.build_job_url('terraformexec', parameters=None, token='sometoken')
    if 'username' in session:
        user = session['username']
        server = jenkins.Jenkins('http://someinstance/', username='Deeptesh', password='abc@123')
        #job="Terraformexc-instances"
        job="terraformexc-tf"
        token="sometoken"
        table = db.session.query(Customers.cname, launchrequests.id ,launchrequests.product, launchrequests.version, launchrequests.component, launchrequests.instances, launchrequests.request_id, launchrequests.status).filter(launchrequests.customer == Customers.id).filter(launchrequests.createdby == user).filter(launchrequests.status=='NEW').all()
        tabledata = []
        for items in table:
            #print(items)
            data={}
            data['id'] = items.id
            data['requestid'] = items.request_id
            data["customer"] = items.cname
            data["product"] = items.product
            data["version"] = items.version
            data["component"] = items.component
            data["instances"] = items.instances
            #data["datastore"] = items.datastore
            data["status"]= items.status
            #buildnewjob=server.build_job(job, parameters={'id':data['id'],'requestid':data['requestid'], 'product':data['product'],'version':data['version'],'component':data['component'],'instances':data['instances']}, token=token)
            buildnewjob=server.build_job(job, parameters={'id':data['id'],'requestid':data['requestid'],'customer':data['customer'], 'product':data['product'],'version':data['version'],'component':data['component'],'instances':data['instances']}, token=token)
            print('printing new buildjob info')
            #print(buildnewjob)
            build_info = server.get_queue_item(buildnewjob, depth=0)
            print(build_info)
            tabledata.append(data)
        return redirect(url_for('userservicelist'))

#========ALL CODE ENDS HERE============

# This particular route is for testing purposes only 


@app.route("/testpage/", methods=['POST', 'GET'])
def testpage():
    return render_template('testpage.html')

#========RUN APP WITH PRE-DEFINED CONFIGS============
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, use_reloader=True)