from app import db, User
from utilities.helpers import Callback


def create(email, password) -> Callback:
    try:
        # Create a new user
        newUser: User = User(email=email.lower(), password=password)
        db.session.add(newUser)

        db.session.commit() # save changes
        return Callback(True, 'User has been created successfully', newUser)

    except Exception as exc:
        print(exc)
        db.session.rollback() # revert changes
        return Callback(False, 'Sorry, Could not create the user.', None)


def getByEmail(email) -> User or None:
    try:
        # Get user and check if None then raise exception
        result = db.session.query(User).filter(User.email == email.lower()).first()
        if not result: raise Exception
        return Callback(True,'User with email ' + email + ' was successfully retrieved.', result)

    except Exception as exc:
        return Callback(False,'User with email ' + email + ' does not exist.', None)