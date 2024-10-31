from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from .forms import EventForm
from .models import Event
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Query all events from the database
    events = Event.query.all()
    # Render the 'index.html' template with the events data
    return render_template('index.html', events=events)

@main_bp.route('/event_create', methods=['GET', 'POST'])
@login_required
def event_create():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            name=form.name.data,
            description=form.description.data,
            date=form.date.data,
            user_id=current_user.id  # Assuming Event has a user_id field to track ownership
        )
        db.session.add(event)
        db.session.commit()
        flash('Event created successfully!')
        return redirect(url_for('main.index'))
    return render_template('event_create.html', form=form)

# About Page Route
@main_bp.route('/about')
def about():
    return render_template('about.html')  # Renders an About Us page

@main_bp.route('/event/<int:event_id>')
def event_view(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash('Event not found.')
        return redirect(url_for('main.index'))
    
    # Fetch related events (this is just a placeholder logic)
    related_events = Event.query.filter(Event.id != event_id).limit(2).all()
    return render_template('event_view.html', event=event, related_events=related_events)