import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from app.config import Config

# app = Flask(__name__)
# app.config.from_object(Config)

# app.config['SECRET_KEY'] = 'd581f24a06b32b7a253427b66d160e12'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
# app.config['MAIL_SERVER'] = 'smtp.office365.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = 'qa_amishra@outlook.com'
#os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = 'Akshat@2311'
#os.environ.get('EMAIL_PASS')
mail = Mail()




#from app import routes

#Registering Blueprints
# from app.users.routes import users
# from app.posts.routes import posts
# from app.main.routes import main

# app.register_blueprint(users)
# app.register_blueprint(posts)
# app.register_blueprint(main)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from app.users.routes import users
    from app.posts.routes import posts
    from app.main.routes import main
    from app.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    app.app_context().push()

    return app