import os
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()  # Create Migrate instance

def create_app():
    app = Flask(__name__)  # this is the name of the module/package that is calling this app

    # Set configuration settings
    app.debug = True  # Should be set to false in a production environment
    app.secret_key = 'somesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'sitedata.sqlite')}"
    app.config['UPLOAD_FOLDER'] = os.path.join('website', 'static', 'uploads')  # Path for image uploads

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Initialize Flask-Migrate with app and db

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

    # Register blueprints after initializing the app
    from .views import main_bp
    app.register_blueprint(main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

      # Move the Jinja2 environment update here
    from .views import get_local_time  # Import the function here
    app.jinja_env.globals.update(get_local_time=get_local_time)  # Update the Jinja2 globals

    return app
