import os
from flask import Flask
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# Initialise extensions
db = SQLAlchemy()
migrate = Migrate()  # Create Migrate instance

def create_app():
    app = Flask(__name__)  # this is the name of the module/package that is calling this app

    # Set configuration settings
    app.debug = True  # Should be set to false in a production environment
    app.secret_key = 'somesecretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(app.instance_path, 'sitedata.sqlite')}"
    app.config['UPLOAD_FOLDER'] = os.path.join('website', 'static', 'uploads')  # Path for image uploads

    # Initialise extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Initialise Flask-Migrate with app and db

    Bootstrap5(app)

    # Initialise the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Set the login view
    login_manager.init_app(app)

    # Create a user loader function for Flask-Login
    from .models import User
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.scalar(db.select(User).where(User.id == user_id))

    # Register blueprints after initialising the app
    from .views import main_bp
    app.register_blueprint(main_bp)

    from . import auth
    app.register_blueprint(auth.auth_bp)

      # Move the Jinja2 environment update here
    from .views import get_local_time  # Import the function here
    app.jinja_env.globals.update(get_local_time=get_local_time)  # Update the Jinja2 globals

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    # Error handler for 500 Internal Server Error
    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app
