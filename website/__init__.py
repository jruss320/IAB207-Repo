# import flask - from 'package' import 'Class'
import os
from flask import Flask 
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application
def create_app():
   app = Flask(__name__)  # this is the name of the module/package that is calling this app

   # Set configuration settings
   app.debug = True  # Should be set to false in a production environment
   app.secret_key = 'somesecretkey'
   app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'sitedata.sqlite')}"
   app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Path for image uploads

   # Ensure the upload folder exists
   os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

   # Initialize extensions
   db.init_app(app)
   Bootstrap5(app)
   
   # Initialize the login manager
   login_manager = LoginManager()
   login_manager.login_view = 'auth.login'  # Set the login view
   login_manager.init_app(app)

   # Create a user loader function for Flask-Login
   from .models import User
   @login_manager.user_loader
   def load_user(user_id):
      return db.session.scalar(db.select(User).where(User.id == user_id))

   # Register blueprints
   from . import views
   app.register_blueprint(views.main_bp)

   from . import auth
   app.register_blueprint(auth.auth_bp)
    
   return app
