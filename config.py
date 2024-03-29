import os
from datetime import timedelta
from database.databaseCredentials import Credentials

credentials = Credentials # database credentials

class BaseConfig(object):
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
    JWT_SECRET_KEY = b'C\xae\x0c_\xbaF\x0f\xfdQ\xc8+65\xbc9\x90\xe6K\xae\xbd\x19\r\x80\xb4'


    # JWT tokens expire in
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=2)

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + credentials.user_name + ':' + credentials.password + '@' + credentials.host + ':' + credentials.port + '/' + credentials.database_name
    SQLALCHEMY_TRACK_MODIFICATIONS = False
