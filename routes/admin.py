from flask_restful import Resource
from flask import jsonify, request, make_response
from datetime import datetime
from flask_security import roles_accepted, current_user
import sqlite3
from task import generate_campaign_csv_report

from database.models import *


class Delete_Campaign(Resource):
    @roles_accepted('admin','sponsor')
    def delete(self, id):
        status = All_Campaign.admin_delete(id)
        if status:
            return make_response(jsonify({"message": "campaign deleted successfully"}), 201)
        return make_response(jsonify({"message": "No campaign found by that id"}), 404)
    
class Delete_Ad(Resource):
    @roles_accepted('admin','sponsor')
    def delete(self, id):
        # print(id)
        status = All_Ad.admin_delete(id)
        # status = True
        if status:
            return make_response(jsonify({"message": "Advertisement deleted successfully"}), 201)
        return make_response(jsonify({"message": "No Advertisement found by that id"}), 404)
    
class Status_User(Resource):
    @roles_accepted('admin')
    def put(self, id):
        user = user_datastore.find_user(id=id)
        if not user:
            return make_response(jsonify({"message": "No user found by that id"}), 404)
        user_datastore.toggle_active(user)
        db.session.commit()
        return make_response(jsonify({"message": "user status updated successfully", "email": user.email, "status": user.active}), 201)

class Resources_User(Resource):
    @roles_accepted('admin','sponsor','influencer')
    def get(self):
        users = User_Current.query.all()
        data = [user.serialize() for user in users]
        if not data:
            return make_response(jsonify({"message": "No user found"}), 404)
        return make_response(jsonify({"message": "get all users", "data": data}), 200)
       
class Specific_User_Resources(Resource):
    @roles_accepted('admin','sponsor')
    def get(self,id):
        users = User_Current.query.filter_by(id=id).first()
        data = users.serialize()
        if not data:
            return make_response(jsonify({"message": "No user found"}), 404)
        return make_response(jsonify({"message": "get  users", "data": data}), 200)
    
    @roles_accepted('admin')
    def delete(self, id):
        user = user_datastore.find_user(id=id)
        if not user:
            return make_response(jsonify({"message": "No user found by that id"}), 404)
        user_datastore.delete_user(user)
        db.session.commit()
        return make_response(jsonify({"message": "user deleted successfully", "email": user.email}), 200)
    
class Resources_Inf_List(Resource):
    def get(self):
        influencers = current_Influencer.query.all()
        if(influencers):
             data = [influencer.serialize() for influencer in influencers]
        else:
            data=""
        if not data:
            return make_response(jsonify({"message": "No influencer found"}), 404)
        return make_response(jsonify({"message": "get all influencers", "data": data}), 200)
    
class Specific_Inf_Resources(Resource):
    def get(self,id):
        influencer = current_Influencer.query.filter_by(influencer_id=id).first()
        if(influencer):
            data = influencer.serialize()
        else:
            data=""
        if not data:
            return make_response(jsonify({"message": "No influencer found"}), 404)
        return make_response(jsonify({"message": "get all influencers", "data": data}), 200)
    
    @roles_accepted('admin')
    def delete(self,id):
        influencer = current_Influencer.query.filter_by(influencer_id=id).first()
        user_id = influencer.user_id
        user = User_Current.query.filter_by(id=user_id).first()
        ad_request= AdRequest.query.filter_by(influencer_id=id).all()
        if(ad_request):
            for ad_req in ad_request:
                db.session.delete(ad_req)
        if influencer:
            db.session.delete(influencer)
            db.session.delete(user)
            db.session.commit()
           
    
class Resources_Spon_List(Resource):
    def get(self):
        sponsors = Current_Sponsor.query.all()
        if(sponsors):
            data = [sponsor.serialize() for sponsor in sponsors]
        else:
            data=""
        if not data:
            return make_response(jsonify({"message": "No sponsor found"}), 404)
        return make_response(jsonify({"message": "get all sponsors", "data": data}), 200)
    
    
class Specific_Spon_Resources(Resource):
    def get(self,id):
        sponsor = Current_Sponsor.query.filter_by(sponsor_id=id).first()
        if(sponsor):
            data = sponsor.serialize()
        else:
            data=""
        if not data:
            return make_response(jsonify({"message": "No sponsor found"}), 404)
        return make_response(jsonify({"message": "get all sponsors", "data": data}), 200)
    
    @roles_accepted('admin')
    def put(self, id):
        sponsor = Current_Sponsor.query.filter_by(sponsor_id=id).first()
        if not sponsor:
            return make_response(jsonify({"message": "No sponsor found by that id"}), 404)
        data = request.get_json()
        status = data.get('status')
        if status not in ['approved', 'rejected','pending']:
            return make_response(jsonify({"message": "Invalid status"}), 400)
        sponsor.status = status
        db.session.commit()
        return make_response(jsonify({"message": f"sponsor status  {status} successfully", 'id': id}), 200)
    
    @roles_accepted('admin')
    def delete(self,id):
        sponsor = Current_Sponsor.query.filter_by(sponsor_id=id).first()
        user_id = sponsor.user_id
        campaigns = All_Campaign.query.filter_by(sponsor_id=id).all()
        if(campaigns):
            for camp in campaigns:
                ads = All_Ad.query.filter_by(campaign_id=camp.id).all()
                if(ads):
                    for ad in ads:
                        db.session.delete(ad)
                db.session.delete(camp)
        user = User_Current.query.filter_by(id=user_id).first()
        ad_request= AdRequest.query.filter_by(sponsor_id=id).all()
        if(ad_request):
            for ad_req in ad_request:
                db.session.delete(ad_req)
        if sponsor:
            db.session.delete(sponsor)
            db.session.delete(user)
            db.session.commit()
            
    

class exportCSV(Resource):
    def post(self):
        data = request.get_json()
        sponsor_id = data['sponsor_id']
        
        # Fetch sponsor email
        conn = sqlite3.connect('instance/database.sqlite3')
        if(conn):
            print('connected successfuly')
        cursor = conn.cursor()
        ans=cursor.execute("SELECT email FROM user")
        cursor.execute("SELECT email FROM user WHERE id = (SELECT user_id FROM sponsor WHERE sponsor_id = ?)", (sponsor_id,))
        sponsor_email = cursor.fetchone()[0]
        conn.close()

        # Trigger the Celery task
        generate_campaign_csv_report(sponsor_id, sponsor_email)
    
        

