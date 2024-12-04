from api import models, db
from sqlalchemy.sql import text
from flask_mail import Message
from flask import current_app  


def send_email_login_failure(email):
    """
    This function will send an email to a specified user
    """
    from app import mail 
    with current_app.app_context(): 
        msg = Message() 
        msg.subject = f"StudyCycle: Attention Required"
        msg.recipients = [email] 
        msg.sender = ("Natural Trash Noreply", "naturaltrashnoreply@gmail.com") 
        msg.html = f""" 
        <html> 
        <body> 
            <p>Hello,</p> 
            <p>There were multiple failed login attempts made on your StudyCycle account.</p>
            <p>If this was you, then ignore this message.</p>
            <p>If it wasn't you, consider resetting your StudyCycle password.</p> 
            <p>Thank you.</p> 
        </body> 
        </html> 
        """ 
        mail.send(msg)