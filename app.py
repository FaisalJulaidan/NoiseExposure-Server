# inspired by: https://github.com/bradtraversy/flask_sqlalchemy_rest/blob/master/app.py
# inspired by: http://zetcode.com/db/sqlalchemy/exprlang/ 

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow_enum import EnumField
from datetime import datetime
from sqlalchemy_utils import create_database, database_exists, PasswordType
from config import BaseConfig
import enum


app = Flask(__name__)
app.config.from_object('config.BaseConfig')
# Getting credentials from credentials csv file
# credentials = Credentials
# Linking to external database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + credentials.user_name + ':' + credentials.password + '@' + credentials.host + ':' + credentials.port + '/' + credentials.database_name
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialising the database
db = SQLAlchemy(app)
# Initialising Marshmallow
ma = Marshmallow(app)


# Severity Column Enum
class SeverityEnum(enum.Enum):
    Normal = 1
    High = 2
    Dangerous = 3


# Setting up database table schema
class NoiseData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Float)
    locationName = db.Column(db.String(50))
    timeStamp = db.Column(db.DateTime)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    deviceModel = db.Column(db.String(50))
    noiseType = db.Column(db.String(50))
    severity = db.Column(db.Enum(SeverityEnum))
    isPublic = db.Column(db.BOOLEAN)

    # Relationships:
    # userId = db.Column(db.Integer, db.ForeignKey('company.ID', ondelete='cascade'), nullable=False)
    # noiseData = db.relationship('User', back_populates='noiseData')


    # Constructor
    def __init__(self, level, locationName, timeStamp, longitude, latitude, deviceModel, noiseType, severity, isPublic):
        self.level = level
        self.locationName = locationName
        self.timeStamp = timeStamp
        self.longitude = longitude
        self.latitude = latitude
        self.deviceModel = deviceModel
        self.noiseType = noiseType
        self.severity = severity
        self.isPublic = isPublic


# setting which columns will be shown on data return
class NoiseDataSchema(ma.Schema):
    # by_value=False makes sure that the Name is returned and not the number
    # Using https://github.com/justanr/marshmallow_enum
    severity = EnumField(SeverityEnum, by_value=False)

    class Meta:
        fields = ('level', 'locationName', 'timeStamp', 'longitude', 'latitude', 'deviceModel', 'noiseType', 'severity')




# Schema containing one record being added
noiseData_schema = NoiseDataSchema(strict=True)
# Schema containing all data
noiseDataList_schema = NoiseDataSchema(many=True, strict=True)


# --------------------------------------------------Routing-----------------------------------------------------------#

# Routing to get all public data
@app.route('/api/noise', methods=['GET'])
def getNoise():
    all_noise = NoiseData.query.filter(NoiseData.isPublic.is_(True))
    # result = noiseDataList_schema.dump(all_noise)
    # print(all_noise[0].locationName)
    # print(result.data) ####### another way of doing it
    # return jsonify(result.data).
    return noiseDataList_schema.jsonify(all_noise)


@app.route('/')
def getReact():
    return 'this is where the react project will be'


if __name__ == '__main__':
    url = BaseConfig.SQLALCHEMY_DATABASE_URI
    print(database_exists(url))
    if not database_exists(url):
        print('Create db tables')
        create_database(url)
        db.create_all()
    app.run()
