from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Ersetze durch deinen tatsächlichen geheimen Schlüssel
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/')

    from .views import views as views_blueprint
    app.register_blueprint(views_blueprint, url_prefix='/')

    with app.app_context():
        db.create_all()

    return app
