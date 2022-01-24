#import psycopg2
#import sqlalchemy
from flask import g
from configparser import ConfigParser
import sqlite3

#database connection function - part of database helpers
def connect_db():
    sql = sqlite.connect('sspinfra.db')
    sql.row_factory = sqlite3.Row
    return sql

#database get database connection for app in context - part of database helpers
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


#conn = sqlite3.connect('sspinfra.db', check_same_thread=False)

def get_response():
    cur = conn.cursor()
    query = cur.execute('select platform from platform').fetchall()
    #return print (list(zip(*query))[1])
    return print(query)
    conn.close()