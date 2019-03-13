from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from database.databaseCredentials import Credentials
import os

app = Flask(__name__)

credentials = Credentials
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + credentials.user_name + ':' + credentials.password + '@' + credentials.host + ':' + credentials.port + '/' + credentials.database_name + ''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

ma = Marshmallow(app)


class NoiseData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Float)
    locationName = db.Column(db.String(50))
    timeStamp = db.Column(db.TIMESTAMP)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    deviceModel = db.Column(db.String(50))
    noiseType = db.Column(db.String(50))
    isPublic = db.Column(db.BOOLEAN)

    def __init__(self, level, locationName, timeStamp, longitude, latitude, deviceModel, noiseType, isPublic):
        self.level = level
        self.locationName = locationName
        self.timeStamp = timeStamp
        self.longitude = longitude
        self.latitude = latitude
        self.deviceModel = deviceModel
        self.noiseType = noiseType
        self.isPublic = isPublic


class NoiseDataSchema(ma.Schema):
    class Meta:
        strict = ('level', 'locationName', 'timeStamp', 'longitude', 'latitude', 'deviceModel', 'noiseType')


noiseData_schema = NoiseDataSchema(strict=True)
noiseDataList_schema = NoiseDataSchema(many=True, strict=True)


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
