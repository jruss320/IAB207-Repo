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