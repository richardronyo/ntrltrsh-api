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

def find_email(email):
    """
    This function determines if the email exists in database
    """
    #this function will take in a string, could be username or email
    #assume email first, do a query/filter on loginInformation and return
    #the email if variable matches entry in database
    emailAddress = models.LoginInformation.query.filter(
        models.LoginInformation.email == email
    ).one_or_none()

    #if no matches, assume username is entered
    #username query to find account, then return attached email
    if emailAddress is None:
        emailAddress = models.LoginInformation.query.filter(
        models.LoginInformation.username == email
    ).one_or_none()
        
    #if email exists, return email String
    if emailAddress is not None:
        #emailAddress is LoginInformation type
        return emailAddress.email
    #if both does not exist, return false or similar (String type)
    else:
        return "False"