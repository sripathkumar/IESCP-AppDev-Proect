from flask_security import SQLAlchemyUserDatastore
from database.models import db, User_Current, Current_Role
from flask_security import Security, login_user, verify_password
from database.models import user_datastore

security = Security()

def login_fn(username, password):  # Updated to use `username`
    user = user_datastore.find_user(username=username)  # Find user by username
    if user:
        if verify_password(password, user.password):  # Verify the password
            login_user(user)
            db.session.commit()
            return user.get_auth_token()
        return 'Invalid password'
    return 'User not found'
