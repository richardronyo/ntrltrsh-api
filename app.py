from flask import Flask
from flask_mail import Mail, Message
from api import app
from api.routes.signup import signup_route
from api.routes.admin import admin_route
from api.routes.login import login_route
from api.routes.schedule import schedule_route
from api.routes.messaging import messaging_route
from api.routes.user import user_route
from api.routes.email import email_route


from datetime import timedelta
app.register_blueprint(signup_route, url_prefix="/api/signup")
app.register_blueprint(admin_route, url_prefix="/api/admin")
app.register_blueprint(login_route, url_prefix="/api/login")
app.register_blueprint(schedule_route, url_prefix="/api/schedule")
app.register_blueprint(messaging_route, url_prefix="/api/message")
app.register_blueprint(user_route, url_prefix="/api/user")
app.register_blueprint(email_route, url_prefix="/api/email")

#Key that will be used to generate tokens
app.config['JWT_SECRET_KEY'] = "NTRLTRSH"
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)



if __name__ == '__main__':
    app.run(debug=True)