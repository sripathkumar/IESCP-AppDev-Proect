from app import create_app
from flask_security import hash_password
from werkzeug.security import generate_password_hash
from database.models import db, user_datastore
from app import app

import subprocess

from database.models import *

with app.app_context():
    # Drop all tables
    db.drop_all()
    
    # Create all tables
    db.create_all()

    # Create roles
    admin_role = Current_Role(name='admin', description='Administrator')
    sponsor_role = Current_Role(name='sponsor', description='Sponsor')
    influencer_role = Current_Role(name='influencer', description='Influencer')
    db.session.add(admin_role)
    db.session.add(sponsor_role)
    db.session.add(influencer_role)
    db.session.commit()

    # Create admin user
    admin_user = user_datastore.create_user(
        email='admin@gmail.com',
        username='admin',
        password=hash_password('123456'),
        roles=[admin_role]
    )
    db.session.commit()

    print("Database initialized with default admin data")
 

    