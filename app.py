# inspired by: https://github.com/bradtraversy/flask_sqlalchemy_rest/blob/master/app.py
# inspired by: http://zetcode.com/db/sqlalchemy/exprlang/

import enum
from datetime import datetime

from flask import Flask, request
from flask_jwt_extended import JWTManager, jwt_refresh_token_required, jwt_required, get_jwt_identity
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow_enum import EnumField
from sqlalchemy_utils import create_database, database_exists, PasswordType
from sqlalchemy.sql import desc


from config import BaseConfig
from services import auth_services
from utilities.helpers import jsonResponse, Callback

app = Flask(__name__)

# setup the application
app.config.from_object('config.BaseConfig')
jwt = JWTManager(app)
db = SQLAlchemy(app)  # Initialising the database
ma = Marshmallow(app)  # Initialising Marshmallow



# Severity Column Enum
class SeverityEnum(enum.Enum):
    Normal = 1
    High = 2
    Dangerous = 3


# Setting up database table schema
class NoiseData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    level = db.Column(db.Float)
    locationName = db.Column(db.String(50))
    timeStamp = db.Column(db.DateTime)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    deviceModel = db.Column(db.String(50))
    noiseType = db.Column(db.String(50))
    addDetails = db.Column(db.String(200))
    severity = db.Column(db.Enum(SeverityEnum))
    isPublic = db.Column(db.BOOLEAN)

    # Relationships:
    userId = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='cascade'), nullable=False)
    user = db.relationship('User', back_populates='noiseData')


    # Constructor
    def __init__(self, level, locationName, timeStamp, longitude, latitude, deviceModel, noiseType, addDetails, severity, isPublic):
        self.level = level
        self.locationName = locationName
        self.timeStamp = timeStamp
        self.longitude = longitude
        self.latitude = latitude
        self.deviceModel = deviceModel
        self.noiseType = noiseType
        self.addDetails = addDetails
        self.severity = severity
        self.isPublic = isPublic


# setting which columns will be shown on data return
class NoiseDataSchema(ma.Schema):
    # by_value=False makes sure that the Name is returned and not the number
    # Using https://github.com/justanr/marshmallow_enum
    severity = EnumField(SeverityEnum, by_value=False)

    class Meta:
        fields = ('userId', 'level', 'locationName', 'timeStamp', 'longitude', 'latitude', 'deviceModel', 'noiseType', 'addDetails', 'severity', 'isPublic')


# Schema containing one record being added
noiseData_schema = NoiseDataSchema(strict=True)
# Schema containing all data
noiseDataList_schema = NoiseDataSchema(many=True, strict=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(PasswordType(
        schemes=['pbkdf2_sha512', 'md5_crypt'],
        deprecated=['md5_crypt']
    ))
    createdOn = db.Column(db.DateTime(), nullable=False, default=datetime.now)
    lastAccess = db.Column(db.DateTime(), nullable=True)

    # Relationships:
    noiseData = db.relationship("NoiseData", uselist=False, back_populates="user",
                                cascade="all, delete, delete-orphan")  # cascade ensure data integrity

    def __repr__(self):
        return '<User {}>'.format(self.email)


# setting which columns will be shown on data return
class UserSchema(ma.Schema):
    class Meta:
        fields = ('email', 'createdOn', 'lastAccess')


# Schema containing one record being added
user_schema = UserSchema(strict=True)
# Schema containing all data
usersList_schema = UserSchema(many=True, strict=True)


# --------------------------------------------------Routing-----------------------------------------------------------#

# Routing to get all public data
@app.route('/api/noise', methods=['GET'])
def get_noise():
    all_noise = NoiseData.query.filter(NoiseData.isPublic.is_(True)).order_by(desc(NoiseData.timeStamp))
    # result = noiseDataList_schema.dump(all_noise)
    # print(all_noise[0].locationName)
    # print(result.data) ####### another way of doing it
    # return jsonify(result.data).
    return noiseDataList_schema.jsonify(all_noise)


# login (get JWT token)
@app.route('/api/auth', methods=['POST'])
def authenticate():
    if request.method == "POST":
        # get credentials
        data = request.json
        # login
        callback: Callback = auth_services.authenticate(data.get('email', ""), data.get('password', ""))
        print(callback.Message)
        print(callback.Data)
        # return json response
        if callback.Success:
            return jsonResponse(True, 200, "Authorised!", callback.Data)
        else:
            print(callback.Message)
            return jsonResponse(False, 401, "Unauthorised!",  callback.Data)


# refresh JWT token endpoint
@app.route('/api/auth/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    if request.method == "POST":
        # refresh token
        callback = auth_services.refreshToken()

        # return json response
        if callback.Success:
            return jsonResponse(True, 200, "Authorised!", callback.Data)
        else:
            return jsonResponse(False, 401, "Unauthorised!", callback.Data)


@app.route('/api/signup', methods=['POST'])
def signup_process():
    if request.method == "POST":
        # create new user
        callback: Callback = auth_services.signup(request.json)

        # return json response
        if callback.Success:
            return jsonResponse(True, 200, callback.Message, callback.Data)
        else:
            return jsonResponse(False, 401, callback.Message, callback.Data)


@app.route('/')
def get_react():
    return 'this is where the react project will be'


@app.route('/api/upload', methods=['POST'])
@jwt_required
def store_data_in_database():
    if request.method == "POST":

        # Get current users from passed jwt token
        current_user = get_jwt_identity()['user']
        print("Current userID : " + str(current_user['id']))

        # Load noise list from post
        uploadedNoiseData = request.json['noiseList']

        print(uploadedNoiseData)

        # Loop through array to add items to database
        for x in range(0, len(uploadedNoiseData)):
            print(uploadedNoiseData[str(x)])
            noiseItem = uploadedNoiseData[str(x)]

            # Pass data to SQLAlchemy noise object
            noiseDataObj = NoiseData(noiseItem['level'], noiseItem['locationName'], noiseItem['timestamp'],
                                     noiseItem['longitude'], noiseItem['latitude'], noiseItem['deviceModel'],
                                     noiseItem['type'], noiseItem['details'], noiseItem['severity'], noiseItem['isPublic'])
            noiseDataObj.userId = current_user['id']
            db.session.add(noiseDataObj)
        # Commit all items to database
        db.session.commit()

    return jsonResponse(True, 200, "Data Stored in database!")


if __name__ == '__main__':
    url = BaseConfig.SQLALCHEMY_DATABASE_URI

    # Create database if does't exist
    if not database_exists(url):
        print('Create database')
        create_database(url)
        db.drop_all()  # drop tables
        db.create_all()  # recreate tables

        # create test users
        db.session.add(User(email='test@test.com', password='123'))
        db.session.add(User(email='test2@test.com', password='123'))
        db.session.commit()

        # insert mocked noise data
        ddl_sql = open("./database/mock_noise_data.sql").read()
        db.engine.execute(ddl_sql)

    # app.run(host='192.168.43.20', port=5000)  # run the app on specific ip address.
    app.run()  # run the app on localhost
