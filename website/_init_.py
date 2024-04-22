from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config["SECRECT_KEY"] = "hsfhwoirhw oijqwdpü"

    from .views import views
    from .auth import auth

    app.register_blueprints(views, url_prefix="/")
    app.register_blueprints(auth, url_prefix="/")

    return app