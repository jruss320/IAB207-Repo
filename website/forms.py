from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import InputRequired, Length, Email, EqualTo

# creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

 # this is the registration form
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[InputRequired("Please enter your first name.")])
    last_name = StringField("Last Name", validators=[InputRequired("Please enter your last name.")])
    user_name = StringField("User Name", validators=[InputRequired()])
    email = StringField("Email Address", validators=[Email("Please enter a valid email.")])
    password = PasswordField("Password", validators=[InputRequired(), EqualTo('confirm', message="Passwords should match")])
    confirm = PasswordField("Confirm Password")
    contact_number = StringField("Contact Number", validators=[Length(10, 15, "Please enter a valid contact number.")])
    street_address = StringField("Street Address", validators=[InputRequired("Please enter your address.")])
    submit = SubmitField("Register")