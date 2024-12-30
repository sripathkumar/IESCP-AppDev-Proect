import base64
import random
from datetime import datetime
from io import BytesIO
import matplotlib
from flask_security import verify_password, login_user, roles_accepted, current_user, logout_user
import matplotlib.pyplot as plt
from flask import request, jsonify
from flask_restful import Resource, Api, reqparse, fields, marshal
from flask_security import current_user, auth_required, roles_required,verify_password,login_user,roles_accepted , hash_password
from sqlalchemy import text
from werkzeug.utils import secure_filename
from flask import jsonify, request, make_response

from database.models import *

class login(Resource):
   def post(self):
        credentials = request.get_json()
        username = credentials.get('username')
        password = credentials.get('password')
        user = user_datastore.find_user(username=username)

        if not user:
            return make_response(jsonify({"message": "User not found", "email": username}), 404)

        if not verify_password(password, user.password):
            return make_response(jsonify({"message": "Incorrect password"}), 401)

        login_user(user)
        db.session.commit()

        token = user.get_auth_token()
        user_role = (
            "admin"
            if current_user.has_role("admin")
            else "sponsor"
            if current_user.has_role("sponsor")
            else "influencer"
        )

        response_payload = {
            "token": token,
            "email": user.email,
            "username": user.username,
            "user_id": user.id,
            "role": user_role,
            "message": "Login successful",
        }

        if user_role == "influencer":
            influencer_info = current_Influencer.query.filter_by(user_id=user.id).first()
            if influencer_info:
                response_payload.update(
                    {
                        "influencer_id": influencer_info.influencer_id,
                        "category": influencer_info.category,
                        "niche": influencer_info.niche,
                        "reach": influencer_info.reach,
                    }
                )

        elif user_role == "sponsor":
            sponsor_info = Current_Sponsor.query.filter_by(user_id=user.id).first()
            if sponsor_info:
                response_payload.update(
                    {
                        "sponsor_id": sponsor_info.sponsor_id,
                        "company_name": sponsor_info.company_name,
                        "industry": sponsor_info.industry,
                        "budget": sponsor_info.budget,
                        "status": sponsor_info.status,
                    }
                )

        return make_response(jsonify(response_payload), 200)
       
class register(Resource):
    def post(self):
        registration_data = request.get_json()

        email = registration_data.get("email")
        username = registration_data.get("username")
        password = registration_data.get("password")
        role = registration_data.get("role")
        sponsor_info = registration_data.get("sponsor_details", {})
        influencer_info = registration_data.get("influencer_details", {})

        if not email or not username or not password or not role:
            return make_response(
                jsonify({"message": "All fields (email, username, password, role) are required"}), 400
            )

        if user_datastore.find_user(email=email):
            return make_response(
                jsonify({"message": "A user with this email already exists", "email": email}), 400
            )

        new_user = user_datastore.create_user(
            email=email, username=username, password=hash_password(password)
        )
        db.session.flush()
        token = new_user.get_auth_token()

        if role == "sponsor":
            new_sponsor = Current_Sponsor(
                user_id=new_user.id,
                company_name=sponsor_info.get("company_name", ""),
                industry=sponsor_info.get("industry", ""),
                budget=sponsor_info.get("budget", 0),
                status=sponsor_info.get("status", ""),
            )
            db.session.add(new_sponsor)
            user_datastore.add_role_to_user(new_user, "sponsor")
            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "message": "Sponsor registered successfully",
                        "user_id": new_user.id,
                        "sponsor_id": new_sponsor.sponsor_id,
                        "email": email,
                        "username": username,
                        "company_name": new_sponsor.company_name,
                        "industry": new_sponsor.industry,
                        "budget": new_sponsor.budget,
                        "status": new_sponsor.status,
                        "token": token,
                        "role": role,
                    }
                ),
                201,
            )

        elif role == "influencer":
            new_influencer = current_Influencer(
                user_id=new_user.id,
                category=influencer_info.get("category", ""),
                niche=influencer_info.get("niche", ""),
                reach=influencer_info.get("reach", 0),
            )
            db.session.add(new_influencer)
            user_datastore.add_role_to_user(new_user, "influencer")
            db.session.commit()

            return make_response(
                jsonify(
                    {
                        "message": "Influencer registered successfully",
                        "user_id": new_user.id,
                        "influencer_id": new_influencer.influencer_id,
                        "email": email,
                        "username": username,
                        "category": new_influencer.category,
                        "niche": new_influencer.niche,
                        "reach": new_influencer.reach,
                        "token": token,
                        "role": role,
                    }
                ),
                201,
            )

        return make_response(jsonify({"message": "Invalid role provided"}), 400)

class logout(Resource):
    @roles_accepted('admin', 'sponsor', 'influencer')
    def post(self):
        user = user_datastore.find_user(id=current_user.id)
        if not user:
            return make_response(jsonify({"message": "No user found by that id"}), 404)
        logout_user(user)
        db.session.commit()
        return make_response(jsonify({"message": "user logged out successfully", "email": user.email}), 200)
