import pytz
from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from .forms import EventForm, TicketBookingForm, CommentForm
from .models import Event, Order, Comment
from . import db
from werkzeug.utils import secure_filename
import os
from datetime import datetime
main_bp = Blueprint('main', __name__)




# Set the timezone to Brisbane (AEST)
def get_local_time(utc_time):
    local_tz = pytz.timezone("Australia/Brisbane")
    return utc_time.replace(tzinfo=pytz.utc).astimezone(local_tz)


main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Query all events from the database
    events = Event.query.all()
    # Render the 'index.html' template with the events data
    return render_template('index.html', events=events)

@main_bp.route('/event/create', methods=['GET', 'POST'])
@login_required
def event_create():
    form = EventForm()  # Create an instance of your form
    
    if request.method == 'POST' and form.validate_on_submit():
        # Extract form data
        name = form.name.data
        description = form.description.data
        category = form.category.data
        location_name = form.location_name.data
        address = form.address.data
        city = form.city.data
        state = form.state.data
        zip_code = form.zip_code.data
        start_date = form.start_date.data
        start_time = form.start_time.data
        end_date = form.end_date.data
        end_time = form.end_time.data
        user_id = current_user.id
        price_per_ticket=form.price_per_ticket.data
        
        # Handle the image upload
        image_file = form.image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)  # Save the file
            image_url = f"static/uploads/{filename}"  # Relative URL for the database
        else:
            image_url = None  # Or a default image URL

        # Create new event instance
        new_event = Event(
            name=name,
            description=description,
            category=category,
            image_url=image_url,
            status='open',
            location_name=location_name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            start_date=start_date,
            start_time=start_time,
            end_date=end_date,
            end_time=end_time,
            user_id=user_id,
            price_per_ticket=price_per_ticket
        )

        # Add to database
        db.session.add(new_event)
        try:
            db.session.commit()  # Commit to the database
            flash('Event created successfully!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            db.session.rollback()  # Roll back the session on error
            flash('Error creating event. Please try again.', 'danger')

    return render_template('event_create.html', form=form)  # Pass the form to the template


# About Page Route
@main_bp.route('/about')
def about():
    return render_template('about.html')  # Renders an About Us page

@main_bp.route('/events')
def event_view():
    search_query = request.args.get('search_query')
    category = request.args.get('category')
    if search_query:
        # Fetch events based on the search query
        events = Event.query.filter(Event.name.ilike(f'%{search_query}%')).all()
    elif category:
        # Fetch events based on the category
        events = Event.query.filter_by(category=category).all()
    else:
        # Fetch all events if no search query or category is provided
        events = Event.query.all()

    return render_template('event_view.html', events=events, category=category, search_query=search_query)


@main_bp.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event_detail(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash('Event not found.')
        return redirect(url_for('main.event_view'))

    related_events = Event.query.filter(Event.id != event_id).limit(2).all()

    form = CommentForm()  # Initialize the comment form

    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            event_id=event.id
        )
        db.session.add(comment)
        db.session.commit()  # Commit the comment to the database
        flash('Comment added successfully!', 'success')
        return redirect(url_for('main.event_detail', event_id=event.id))  # Redirect to the same page to see the new comment

    # Fetch existing comments with user information
    comments = Comment.query.filter_by(event_id=event_id).options(db.joinedload(Comment.commenter)).order_by(Comment.date_posted.desc()).all()

    return render_template('event_detail.html', event=event, related_events=related_events, form=form, comments=comments)


@main_bp.route('/events/category/<string:category>')
def events_by_category(category):
    events = Event.query.filter_by(category=category).all()
    if not events:
        flash(f'No events found in the "{category}" category.')
        return redirect(url_for('main.event_view'))
    return render_template('event_view.html', events=events, category=category)

@main_bp.route('/search')
def search():
    query = request.args.get('q', '')  # Get the search query from the URL parameters
    if query:
        # Search for events where the name or description contains the query string
        events = Event.query.filter(
            (Event.name.ilike(f"%{query}%")) | (Event.description.ilike(f"%{query}%"))
        ).all()
    else:
        events = []  # No results if the query is empty

    return render_template('event_view.html', events=events, search_query=query)

# Price per ticket
TICKET_PRICE = 20.00  # Example price per ticket

@main_bp.route('/event/<int:event_id>/book', methods=['GET', 'POST'])
@login_required
def book_tickets(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash('Event not found.')
        return redirect(url_for('main.event_view'))

    form = TicketBookingForm()  # Assume a form similar to EventForm with a quantity field

    if form.validate_on_submit():
        quantity = form.quantity.data
        price_per_ticket = event.price_per_ticket  # Get the price per ticket from the event model
        total_price = quantity * price_per_ticket

        order = Order(
            quantity=quantity,
            price=total_price,
            user_id=current_user.id,
            event_id=event.id
        )

        db.session.add(order)
        db.session.commit()  # Commit the order to the database

        # Print confirmation message to the terminal
        print(f"Order confirmed: {quantity} ticket(s) booked for '{event.name}' by user ID {current_user.id}.")

        flash('Tickets booked successfully!', 'success')
        return redirect(url_for('main.event_view'))

    return render_template('book_tickets.html', event=event, form=form)

@main_bp.route('/event/<int:event_id>/update', methods=['GET', 'POST'])
@login_required
def event_update(event_id):
    event = db.session.get(Event, event_id)
    # Check if the current user is the owner of the event
    if event.user_id != current_user.id:
        flash('You are not authorized to update this event.', 'danger')
        return redirect(url_for('main.event_detail', event_id=event.id))
    
    form = EventForm(obj=event)
    if request.method == 'POST' and form.validate_on_submit():
        # Update event details (excluding status)
        form.populate_obj(event)
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('main.event_detail', event_id=event.id))
    
    return render_template('event_update.html', form=form, event=event)

@main_bp.route('/event/<int:event_id>/cancel', methods=['POST'])
@login_required
def event_cancel(event_id):
    event = db.session.get(Event, event_id)
    # Check if the current user is the owner of the event
    if event.user_id != current_user.id:
        flash('You are not authorized to cancel this event.', 'danger')
        return redirect(url_for('main.event_detail', event_id=event.id))
    
    # Update the status to 'Cancelled' if authorized
    event.status = 'Cancelled'
    db.session.commit()
    flash('Event has been cancelled.', 'info')
    return redirect(url_for('main.event_detail', event_id=event.id))

