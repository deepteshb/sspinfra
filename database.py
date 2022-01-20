import psycopg2
import sqlalchemy
from sqlalchemy import create_engine, text
engine = create_engine('postgresql+psycopg2://postgres:Dresident1@20.44.49.83/sspinfra')

conn = engine.connect()

def db_conn_response():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT datname FROM pg_database")).fetchall()
        #print(result)
        if result == [('postgres',), ('template1',), ('template0',), ('sspinfra',)]:
            print('Connection Successful')
        else:
            print('Connection Unsuccessful')