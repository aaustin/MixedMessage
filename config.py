import os
basedir = os.path.abspath(os.path.dirname(__file__))

dbhost = 'localhost'
dbuser = 'ajaustin' #ajaustin
dbpass = 'alex111'
dbname = 'MixedMessage'

SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://' + dbuser + ':' + dbpass + '@' + dbhost + '/' +dbname
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

# email server
MAIL_SERVER = 'smtp.googlemail.com'
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_USERNAME = 'alexjaustin@gmail.com'
MAIL_PASSWORD = 'maeph0089'

# administrator list
ADMINS = ['alexjaustin@gmail.com']