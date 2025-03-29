from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '12345'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  # Fixed URI
    csrf = CSRFProtect(app)
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .models import Note, User

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id: str) -> User:
        return User.query.get(int(id))

    return app

def create_database(app):
    db_path = path.join('website', DB_NAME)
    if not path.exists(db_path):
        try:
            with app.app_context():
                db.create_all()
                print('Created Database!')
        except Exception as e:
            print(f'Error creating database: {e}')
