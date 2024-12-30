from datetime import datetime, timedelta
import os
from io import StringIO
from io import StringIO, BytesIO
import csv
from flask import send_file
from celery import shared_task
from mail_service import send_message
from jinja2 import Template
from celery.utils.log import get_task_logger
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3
from jinja2 import Environment, FileSystemLoader,Template
from datetime import datetime

logger = get_task_logger(__name__)


# Jinja2 Environment Setup
template_env = Environment(loader=FileSystemLoader('.'))

def render_email_template(template_name, context):
    """Render the email template with context."""
    template = template_env.get_template(template_name)
    return template.render(context)

def execute_query(query):
    """Execute a database query and return results."""
    connection = sqlite3.connect('instance/database.sqlite3')
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    connection.close()
    return results


@shared_task(ignore_result=True)
def send_reminder_emails():
    """Send reminder emails to users to log into Sponsify."""
    users_query = "SELECT email, username FROM user"
    users = execute_query(users_query)

    for email, username in users:
        subject = "Reminder: Please visit Sponsify"
        context = {
            'name': username,
            'message': 'You have pending ad requests or haven\'t visited recently. Please log in to check them.'
        }
        email_body = render_email_template('email.html', context)
        send_message(email, subject, email_body)

@shared_task(ignore_result=True)
def send_new_ad_request_notifications():
    """Send notifications for new ad requests."""
    ad_requests_query = """
    SELECT ar.ad_id, ad.name, u.email, u.username
    FROM ad_request ar
    JOIN ad ON ar.ad_id = ad.id
    JOIN influencer i ON ar.influencer_id = i.influencer_id
    JOIN user u ON i.user_id = u.id
    WHERE ar.status = 'pending'
    """
    ad_requests = execute_query(ad_requests_query)

    for ad_id, ad_name, email, username in ad_requests:
        subject = f"New Ad Request: {ad_name}"
        context = {
            'name': username,
            'message': f'You have a new ad request opportunity for "{ad_name}". Please check Sponsify for further details.'
        }
        email_body = render_email_template('email.html', context)
        send_message(email, subject, email_body)


@shared_task(ignore_result=True)
def send_report_for_last_month():
    """Send a detailed report of the previous month's activity to sponsors."""
    thirty_days_ago = datetime.now() - timedelta(days=30)

    report_query = f"""
    SELECT u.username AS sponsor_name, s.sponsor_id, c.name, COUNT(a.id) AS ads_done, COUNT(ar.id) AS ad_requests_sent
    FROM sponsor s
    JOIN user u ON s.user_id = u.id
    LEFT JOIN campaign c ON s.sponsor_id = c.sponsor_id
    LEFT JOIN ad a ON c.id = a.campaign_id AND a.start_date > '{thirty_days_ago}'
    LEFT JOIN ad_request ar ON s.sponsor_id = ar.sponsor_id AND ar.request_date > '{thirty_days_ago}'
    GROUP BY s.sponsor_id, c.id
    """
    reports = execute_query(report_query)

    for report in reports:
        sponsor_name, sponsor_id, campaign_name, ads_done, ad_requests_sent = report
        email_query = f"SELECT email FROM user WHERE id = (SELECT user_id FROM sponsor WHERE sponsor_id = '{sponsor_id}')"
        sponsor_email = execute_query(email_query)[0][0]

        subject = "Monthly Activity Report"
        context = {
            'sponsor_name': sponsor_name,
            'campaign_name': campaign_name,
            'ads_done': ads_done,
            'ad_requests_sent': ad_requests_sent,
            'month': thirty_days_ago.strftime("%B %Y")
        }
        email_body = render_email_template('monthly_report.html', context)
        send_message(sponsor_email, subject, email_body)


def generate_campaign_csv_report(sponsor_id, sponsor_email):
    """Generate a CSV report for a sponsor's campaigns and send it via email."""
    campaigns_query = f"""
    SELECT c.name, c.description, c.start_date, c.end_date, c.budget, c.visibility, c.goals
    FROM campaign c
    WHERE c.sponsor_id = {sponsor_id}
    """
    campaigns = execute_query(campaigns_query)

    # Create CSV output
    csv_output = StringIO()
    writer = csv.writer(csv_output)
    writer.writerow(['Campaign Name', 'Description', 'Start Date', 'End Date', 'Budget', 'Visibility', 'Goals'])

    for campaign in campaigns:
        writer.writerow(campaign)

    csv_content = csv_output.getvalue().encode('utf-8')
    csv_output.close()

    # Send CSV file as attachment
    send_file(csv_content, mimetype='text/csv', download_name='campaigns_report.csv', as_attachment=True)

    # Send email notification
    subject = "Your Campaign Report is Ready"
    content_body = f"""
    <p>Hello,</p>
    <p>Your campaign report is ready for download. You can download it from the attached CSV file.</p>
    <p>Best regards,<br>Support Sponsify</p>
    """
    send_message(to=sponsor_email, subject=subject, content_body=content_body, attachment=csv_content, filename='campaigns_report.csv')
    
    print("done till last")
