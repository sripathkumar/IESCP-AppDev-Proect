from flask import Flask, jsonify, request
from celery.schedules import crontab
from flask_security import verify_password
from flask_restful import Api
from flask_security import Security
from config import LocalDev
import sqlite3
from caching import cache
from database.models import db, user_datastore
from routes.security import security
from flask_cors import CORS
from worker import celery_init_app
from task import send_reminder_emails , send_new_ad_request_notifications,send_report_for_last_month
from flask import Flask, request, jsonify



def create_app():
    app = Flask(__name__)
    app.config.from_object(LocalDev)
    db.init_app(app)
    api = Api(app)
    cache.init_app(app)
    security.init_app(app, user_datastore)
    CORS(app)
    with app.app_context():
        import routes.views

    return app,api,cache

app ,api,cache = create_app()
celery_app = celery_init_app(app)

from routes.auth import  login, register
api.add_resource(login, '/api/login')
api.add_resource(register, '/api/register')

from routes.campaign import Campaigns_list, Specific_Camp,Update_Campaign
api.add_resource(Campaigns_list, '/api/campaign')
api.add_resource(Specific_Camp, '/api/campaign/<int:id>')
api.add_resource(Update_Campaign, '/api/campaignUpdate/<int:id>')

from routes.ad import Resource_Ad, Specific_Ad
api.add_resource(Resource_Ad, '/api/Ad')
api.add_resource(Specific_Ad, '/api/Ad/<int:id>')

from routes.admin import Delete_Campaign,Delete_Ad, Status_User, Resources_User ,exportCSV, Resources_Inf_List,Resources_Spon_List,Specific_Inf_Resources,Specific_Spon_Resources, Specific_User_Resources
api.add_resource(Delete_Campaign, '/api/category_delete/<int:id>')
api.add_resource(Delete_Ad, '/api/Ad_delete/<int:id>')
api.add_resource(Status_User, '/api/toggle_user_status/<int:id>')
api.add_resource(Resources_User, '/api/users')
api.add_resource(Resources_Inf_List, '/api/influencers')
api.add_resource(Resources_Spon_List, '/api/sponsors')
api.add_resource(Specific_Inf_Resources, '/api/influencer/<int:id>')
api.add_resource(Specific_Spon_Resources, '/api/sponsor/<int:id>')
api.add_resource( Specific_User_Resources, '/api/user/<int:id>')
api.add_resource(exportCSV , '/api/export-csv')

from routes.adrequest import Resources_Ad_Request , Status_Ad_request
api.add_resource(Resources_Ad_Request, '/api/ad_request')
api.add_resource(Status_Ad_request , '/api/ad_request/<int:id>')


@celery_app.on_after_configure.connect
def automated_tasks(sender, **kwargs):
    # Run the task every minute (every 1 minute)
    sender.add_periodic_task(
        crontab(minute='*'),  # Run every minute
        #crontab(hour=16, minute=1 ,day_of_month=1),
        send_report_for_last_month.s(),
    )
    
    sender.add_periodic_task(
        crontab(minute='*'),  # Run every minute
        #crontab(hour=19,minute=58),
        send_reminder_emails.s(),
    )
    
    sender.add_periodic_task(
        crontab(minute='*'),  # Run every minute
        #crontab(hour=16, minute=1),
        send_new_ad_request_notifications.s(),
    )




if __name__ == '__main__':
    app.run(debug=True)