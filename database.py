import psycopg2
import sqlalchemy
from configparser import ConfigParser
import sqlite3

conn = sqlite3.connect('sspinfra.db', check_same_thread=False)

def get_response():
    cur = conn.cursor()
    query = cur.execute('select platform from platform').fetchall()
    #return print (list(zip(*query))[1])
    return print(query)
    conn.close()