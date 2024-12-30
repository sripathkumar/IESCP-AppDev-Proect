from flask_restful import Resource
from flask import jsonify, request, make_response
from datetime import datetime
import os 
import random 
from werkzeug.utils import secure_filename
from flask_security import roles_accepted, current_user,auth_required
from caching import cache
from sqlalchemy.orm import joinedload

from database.models import *


class Campaigns_list(Resource):
    @auth_required("token")
    @roles_accepted('admin', 'sponsor')
    def post(self):
        data = request.form
        name = data['name']
        sponsor_id = data['sponsor_id']
        if not name:
            return jsonify({"message": "name is required"}), 400
        description = data['description']
        if not description:
            return jsonify({"message": "description is required"}), 400
        start_date_str = data['start_date']
        end_date_str = data['end_date']
        budget = data['budget']
        visibility = data['visibility']
        status = 'pending'


        goals = data['goals'] 
        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Invalid date format. Please use YYYY-MM-DD."}), 400
        cate = All_Campaign(
            name=name,
            sponsor_id=sponsor_id,
            description=description,
            start_date=start_date,
            end_date=end_date,
            status=status,
            budget=budget,
            visibility=visibility,
            goals=goals,
        )
        db.session.add(cate)
        db.session.commit()
        return make_response(jsonify({"message": "category created successfully", "id": cate.id, "name": cate.name}), 201)
    
    @auth_required("token")
    @cache.cached(timeout=2)
    def get(self):
        role = current_user.roles[0].name  # Assuming the first role is relevant
        #print(role)
        #print(current_user.id)
        campaigns = []
        
        if role == 'admin':
            # Admins can see all campaigns
            campaigns = All_Campaign.query.all()
        elif role == 'influencer':
            # Influencers can only see approved public campaigns
            campaigns = All_Campaign.query.all()
        elif role == 'sponsor':
    # Sponsors can see their own campaigns
            campaigns = (
                All_Campaign.query
                .join(Current_Sponsor, All_Campaign.sponsor_id == Current_Sponsor.sponsor_id)
                .filter(Current_Sponsor.user_id == current_user.id)
                .all()
            )
        data = [
            {
                'id': campaign.id,
                'name': campaign.name,
                'description': campaign.description,
                'created_at': campaign.start_date,
                'end_date': campaign.end_date,
                'start_date': campaign.start_date,
                'status': "flagged" if campaign.status == "rejected" else "unflagged",
                'sponsor_id': campaign.sponsor_id,
                'budget': campaign.budget,
                'visibility': campaign.visibility,
                'goals': campaign.goals,
            }
            for campaign in campaigns
        ]
        
        if not data:
            return make_response(jsonify({"message": "No campaigns found"}), 404)
        
        return make_response(jsonify({"message": "Fetched all campaigns", "data": data}), 200)
    
class Specific_Camp(Resource):
    @cache.cached(timeout=2)
    @auth_required("token")
    @roles_accepted('admin', 'sponsor', 'influencer')
    def get(self, id):
        campaign = All_Campaign.query.filter_by(id=id).first()
        if not campaign:
            return make_response(jsonify({"message": "No campaign found"}), 404)
        data = campaign.serialize()
        return make_response(jsonify({"message": "Campaign found", "data": data}), 200)
    
    @auth_required("token")
    @roles_accepted('admin', 'sponsor')
    def put(self, id):
        categories = All_Campaign.query.filter_by(id=id).first()
        if not categories:
            return make_response(jsonify({"message": "No campaign found by that id"}), 404)
        data = request.get_json()
        name = data['name']
        if not name:
            return jsonify({"message": "name is required"})
        description = data['description']
        if not description:
            return jsonify({"message": "description is required"})
        
        categories.name = name
        categories.description = description
        categories.sponsor_id = data['sponsor_id']
        categories.budget = data['budget']
        categories.visibility= data['visibility']
        categories.goals = data['goals']
        try:
            categories.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
            categories.end_date = datetime.strptime( data['end_date'], '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Invalid date format. Please use YYYY-MM-DD."}), 400
        db.session.commit()
        return jsonify({"message": "update specific category", 'id': id})
    
    @auth_required("token")
    def delete(self, id):
        categories = All_Campaign.query.filter_by(id=id).first()
        if not categories:
            return make_response(jsonify({"message": "No category found by that id"}), 404)
        categories.delete = True
        db.session.commit()

        ads = All_Ad.query.filter_by(campaign_id=id).all()
        for ad in ads:
            db.session.delete(ad)
        ad_request = AdRequest.query.filter_by(campaign_id=id).all()
        if(ad_request):
            for req in ad_request:
                db.session.delete(req)

        db.session.delete(categories)
        db.session.commit()
        
        return make_response(jsonify({"message": "Campaign and associated ads deleted successfully", 'id': id}), 200)

class Update_Campaign(Resource):
    @auth_required("token")
    @roles_accepted('admin')
    def put(self, id):
        campaign = All_Campaign.query.filter_by(id=id).first()
        if not campaign:
            return make_response(jsonify({"message": "No campaign found by that id"}), 404)
        data = request.get_json()
        status = data.get('status')
        if status not in ['approved', 'rejected','pending']:
            return make_response(jsonify({"message": "Invalid status"}), 400)
        campaign.status = status
        db.session.commit()
        return make_response(jsonify({"message": f"campaign status  {status} successfully", 'id': id}), 200)