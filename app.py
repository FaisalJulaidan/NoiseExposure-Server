# inspired by: https://github.com/bradtraversy/flask_sqlalchemy_rest/blob/master/app.py
# inspired by: http://zetcode.com/db/sqlalchemy/exprlang/ 

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from database.databaseCredentials import Credentials

app = Flask(__name__)
#Getting credentials from credentials csv file
credentials = Credentials
# Linking to external database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + credentials.user_name + ':' + credentials.password + '@' + credentials.host + ':' + credentials.port + '/' + credentials.database_name 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Initialising the database
db = SQLAlchemy(app)
#Initialising Marshmallow
ma = Marshmallow(app)

#Setting up database table schema
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

    #Constructor
    def __init__(self, level, locationName, timeStamp, longitude, latitude, deviceModel, noiseType, isPublic):
        self.level = level
        self.locationName = locationName
        self.timeStamp = timeStamp
        self.longitude = longitude
        self.latitude = latitude
        self.deviceModel = deviceModel
        self.noiseType = noiseType
        self.isPublic = isPublic

#setting which columns will be shown on data return
class NoiseDataSchema(ma.Schema):
    class Meta:
        fields = ('level', 'locationName', 'timeStamp', 'longitude', 'latitude', 'deviceModel', 'noiseType')

#Schema containing one record being added
noiseData_schema = NoiseDataSchema(strict=True)
#Schema containing all data
noiseDataList_schema = NoiseDataSchema(many=True, strict=True)

#--------------------------------------------------Routing-----------------------------------------------------------#

#Routing to get all public data
@app.route('/', methods = ['GET'])
def getNoise():
    all_noise = NoiseData.query.filter(NoiseData.isPublic.is_(True))
    # result = noiseDataList_schema.dump(all_noise)
    # print(all_noise[0].locationName)
    # print(result.data) another way of doing it
    # return jsonify.
    return noiseDataList_schema.jsonify(all_noise)


if __name__ == '__main__':
    app.run()
