from flask_restful import Resource
from flask import jsonify, request, make_response
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_security import roles_accepted, current_user,auth_required
from caching import cache
import random
import os 


from database.models import *

class Resource_Ad(Resource):
    @roles_accepted('admin', 'sponsor')
    def post(self):
        data = request.form
        name = data['name']
        if not name:
            return jsonify({"message": "name is required"})
        
        content = data['content']
        campaign_id = data['campaign_id']
        sponsor_id = data['sponsor_id']
        start_date = data['start_date']
        requirements = data['requirements']
        budget = data['budget']
        status = data.get('status').lower() == 'true'
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({"message": "Invalid date format. Please use YYYY-MM-DD."}), 400
        ad = All_Ad(name=name,content=content, campaign_id=campaign_id, sponsor_id=sponsor_id,
                start_date=start_date, requirements=requirements, budget=budget
               , status=status)
        
        db.session.add(ad)
        db.session.commit()
        
        return make_response(jsonify({"message": "ad created successfully", "id": ad.id, "name": ad.name}), 201)


    @cache.cached(timeout=2)
    @auth_required("token")
    @roles_accepted('admin', 'sponsor', 'influencer')
    def get(self):
        role = current_user.roles[0].name  # Assuming the first role is relevant
        print(role)
        print(current_user.id)
        ads = []
        
        if role == 'admin':
            # Admins can see all campaigns
            ads = All_Ad.query.all()
        elif role == 'influencer':
            # Influencers can only see approved public campaigns
            ads = All_Ad.query.all()
        elif role == 'sponsor':
    # Sponsors can see their own campaigns
            ads = (
                All_Ad.query
                .join(Current_Sponsor, All_Ad.sponsor_id == Current_Sponsor.sponsor_id)
                .filter(Current_Sponsor.user_id == current_user.id)
                .all()
            )

        data = [ad.serialize() for ad in ads]
        if not data:
            return make_response(jsonify({"message": "No advertisements found"}), 404)
        return make_response(jsonify({"message": "get all advertisements", "data": data}), 200)


class Specific_Ad(Resource):
    @cache.cached(timeout=2)
    @auth_required("token")
    def get(self, id):
        ad = All_Ad.query.filter_by(id=id).first()
        if not ad:
            return make_response(jsonify({"message": "No Advertisment found by that id"}), 404)
        ad = ad.serialize()
        return jsonify({"message": "get specific advertisment", "data": ad})
    
    @roles_accepted('admin', 'sponsor','influencer')
    def put(self, id):
        ad = All_Ad.query.filter_by(id=id).first()
        if not ad:
            return make_response(jsonify({"message": "No Advertisment found by that id"}), 404)
        data = request.get_json()
        name = data.get('name')
        if not name:
            return jsonify({"message": "name is required"})
        content = data.get('content')
        if not content:
            return jsonify({"message": "ad_content is required"})
        budget = data.get('budget')
        if budget is None:  # Assuming price can be 0, which is falsy
            return jsonify({"message": "budget is required"})
        requirements = data.get('requirements')
        if budget is None:  # Assuming price can be 0, which is falsy
            return jsonify({"message": "requirements is required"})
        ad.name = name
        ad.content = content
        ad.budget=budget
        ad.requirements = requirements
        # if current_user.has_role('admin'):
        #     product.status = True
        # else:
        #     product.status = False
        db.session.commit()
        return jsonify({"message": "update specific ad", 'id': id})
    
    @roles_accepted('admin', 'sponsor')
    def delete(self, id):
        ad = All_Ad.query.filter_by(id=id).first()
        if not ad:
            return make_response(jsonify({"message": "No ad found by that id"}), 404)
        ad.delete = True  # Assuming there's a 'delete' attribute; might need adjustment
        ad_request=AdRequest.query.filter_by(ad_id=id).all()
        if(ad_request):
            for req in ad_request:
                db.session.delete(req)
        db.session.delete(ad)
        db.session.commit()
        return jsonify({"message": "delete specific ad", 'id': id})
    
    
