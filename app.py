from flask import Flask
from api import app
from api.routes.signup import signup_route
from api.routes.admin import admin_route
from api.routes.login import login_route

app.register_blueprint(signup_route, url_prefix="/api/signup")
app.register_blueprint(admin_route, url_prefix="/api/admin")
app.register_blueprint(login_route, url_prefix="/api/login")

if __name__ == '__main__':
    app.run(debug=True)