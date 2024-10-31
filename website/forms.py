from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField, SubmitField, StringField, SelectField, FileField, PasswordField, DateTimeField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired

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

class EventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    description = TextAreaField('Event Description', validators=[DataRequired()])
    category = SelectField('Event Category', choices=[
        ('Sports', 'Sports'),
        ('Music', 'Music'),
        ('Arts', 'Arts'),
        ('Technology', 'Technology')
    ], validators=[DataRequired()])
    image_url = FileField('Event Image')  # Adjust this if you want to handle the image upload differently
    location_name = StringField('Location Name', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zip_code = StringField('Zip Code', validators=[DataRequired()])
    start_date = DateTimeField('Start Date', format='%Y-%m-%d', validators=[DataRequired()])
    start_time = DateTimeField('Start Time', format='%H:%M:%S', validators=[DataRequired()])
    end_date = DateTimeField('End Date', format='%Y-%m-%d', validators=[DataRequired()])
    end_time = DateTimeField('End Time', format='%H:%M:%S', validators=[DataRequired()])
    submit = SubmitField('Create Event')