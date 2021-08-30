from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_nav import Nav
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_message = "Please log in to access this page."
login.login_view = 'login'
bootstrap = Bootstrap(app)
nav = Nav(app)
app.config['FLASK_ADMIN_SWATCH'] = 'flatly'
admin = Admin(app, name=app.config['SITE_NAME'], template_mode='bootstrap3')

from app import routes, models


@login.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))
