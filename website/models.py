from . import db
from datetime import datetime
from flask_login import UserMixin

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(100), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    street_address = db.Column(db.String(150), nullable=False)
    
    events = db.relationship('Event', backref='owner', lazy=True)
    orders = db.relationship('Order', backref='user', lazy=True)
    comments = db.relationship('Comment', back_populates='commenter')  # Define explicitly


# Event Model
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Event details
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(20), default='Open')  # 'Open', 'Inactive', 'Sold Out', 'Cancelled'
    
    # Location details
    location_name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)

    # Date and time details
    start_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    # Event creator and Price
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    price_per_ticket = db.Column(db.Float, nullable=False, default=0.0)
    
    # Relationships
    comments = db.relationship('Comment', backref='event', lazy=True)  # Keep this line
    orders = db.relationship('Order', backref='event', lazy=True)

    def __repr__(self):
        return f"<Event {self.name}>"

    # Method to check if the event is in the past or sold out
    def update_status(self):
        if self.status != 'Cancelled':
            if self.start_date < datetime.utcnow().date():
                self.status = 'Inactive'
            # Add logic for sold-out status if needed


# Comment Model
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    commenter = db.relationship('User', back_populates='comments')  # Define explicitly
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)





# Order Model
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
