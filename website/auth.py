from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        user_name = login_form.user_name.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.name == user_name))
        
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password):  # Kept as `user.password_hash`
            error = 'Incorrect password'

        if error is None:
            login_user(user)
            nextp = request.args.get('next')  # URL the user was originally trying to access
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.index'))  # Redirect to home if no next URL or invalid path
            return redirect(nextp)
        else:
            flash(error)
    
    return render_template('login.html', form=login_form, heading='Login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    register_form = RegisterForm()
    if register_form.validate_on_submit():
        # Collect form data
        user = User(
            first_name=register_form.first_name.data,
            last_name=register_form.last_name.data,
            name=register_form.user_name.data,
            email=register_form.email.data,
            password=generate_password_hash(register_form.password.data).decode('utf-8'),
            contact_number=register_form.contact_number.data,
            street_address=register_form.street_address.data
        )
        
        # Save to the database
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('auth.login'))

    return render_template('signup.html', form=register_form, heading='Sign Up')
