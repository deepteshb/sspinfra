import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    #SECRET_KEY = 'Dresident1!!'


class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True


# database URI for MySQL using PyMysql driver
#'mysql+pymysql://root:pass@localhost/my_db'  

# database URI for PostgreSQL using psycopg2 
#'postgresql+psycopg2://root:pass@localhost/my_db' 

# database URI for MS-SQL using pyodbc driver
#'mssql+pyodbc://root:pass@localhost/my_db' 

 # database URI for Oracle using cx_Oracle driver
#'oracle+cx_oracle://root:pass@localhost/my_db'
