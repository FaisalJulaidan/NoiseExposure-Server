from datetime import datetime
from utilities.helpers import Callback, jsonResponse, isValidEmail
from flask_jwt_extended import create_access_token, get_jwt_identity, create_refresh_token
from services import user_services
from app import db, jwt, User
from config import BaseConfig


@jwt.invalid_token_loader
def my_expired_token_callback(error):
    return jsonResponse(False, 401, "Token expired")


def signup(details) -> Callback:
    try:
        # Validate Email
        if not isValidEmail(details['email']):
            return Callback(False, 'Invalid Email.')

        # Check if user exists
        user = user_services.getByEmail(details['email']).Data
        if user:
            return Callback(False, 'User already exists.')

        # Create a new user with its associated company and owner role
        user_callback = user_services.create(details['email'], details['password'])
        if not user_callback.Success:
            return user_callback

        # Return a callback with a message
        return Callback(True, 'Signed up successfully!')

    except Exception as e:
        print(e)
        db.session.rollback()
        return Callback(False, "Failed to signup!", None)


def authenticate(email: str, password_to_check: str) -> Callback:
    try:
        # find user
        user_callback: Callback = user_services.getByEmail(email)

        # If user is not found
        if not user_callback.Success:
            print("Email not found")
            return Callback(False, "Record with the current email or password was not found")

        # Get the user from the callback object
        user: User = user_callback.Data
        if not password_to_check == user.password:
            print("Invalid request: Incorrect Password")
            return Callback(False, "Record with the current email or password was not found")

        # If all the tests are valid then do login process
        data = {'user': {"email": user.email}}

        # for security, hide them in the token
        tokenData = {'user': {"id": user.id, "email": user.email}}

        print(tokenData)

        # create the JWT token
        access_token = create_access_token(identity=tokenData)
        refresh_token = create_refresh_token(identity=tokenData)
        data['token'] = access_token
        data['refresh'] = refresh_token

        # set LastAccess
        user.lastAccess = datetime.now()
        db.session.commit()

        # send the token back
        return Callback(True, "Authorised!", data)

    except Exception as e:
        print(e)
        db.session.rollback()
        return Callback(False, "Unauthorised!", None)


def refreshToken() -> Callback:
    try:
        # get logged in user from the submitted refresh token
        current_user = get_jwt_identity()
        # generate a new access token
        data = {'token': create_access_token(identity=current_user),
                'expiresIn': datetime.now() + BaseConfig.JWT_ACCESS_TOKEN_EXPIRES}

        print(data)
        return Callback(True, "Authorised!", data)

    except Exception as e:
        return Callback(False, "Unauthorised!", None)
