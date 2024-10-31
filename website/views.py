from flask import Blueprint, render_template, request, redirect, url_for, flash
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

@main_bp.route('/event/create', methods=['GET', 'POST'])
@login_required
def event_create():
    form = EventForm()  # Create an instance of your form
    
    if request.method == 'POST': # and form.validate_on_submit():  # Ensure form validation
        print("Form submitted successfully!")  # Debugging line
        print("Form data:", form.data)  # Print form data

        # Retrieve form data directly from the form instance
        # Extract data from the form
        name = form.name.data
        description = form.description.data
        category = form.category.data
        image_file = form.image.data  # Corrected reference to image upload field
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

        # Handle the image upload
        if image_file:
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)  # Save the file locally
            image_url = f"/{file_path}"  # Generate URL to save in DB
        else:
            image_url = None  # Or a default image URL if preferred
        
        # Insert into the database
        new_event = Event(
            name=name,
            description=description,
            category=category,
            image_url=image_url,
            status='pending',  # Provide a default status here
            location_name=location_name,
            address=address,
            city=city,
            state=state,
            zip_code=zip_code,
            start_date=start_date,
            start_time=start_time,
            end_date=end_date,
            end_time=end_time,
            user_id=user_id
        )

        # Add to database
        db.session.add(new_event)
        try:
            db.session.commit()  # Try committing to the database
            flash('Event created successfully!', 'success')
            return redirect(url_for('main.index'))
        except Exception as e:
            print("Error committing to the database:", e)  # Debugging line
            db.session.rollback()  # Roll back the session on error
            flash('Error creating event. Please try again.', 'danger')
        
    return render_template('event_create.html', form=form)  # Pass the form to the template

# About Page Route
@main_bp.route('/about')
def about():
    return render_template('about.html')  # Renders an About Us page

@main_bp.route('/events')
def event_view():
    events = Event.query.all()  # Fetch all events
    return render_template('event_view.html', events=events)


@main_bp.route('/event/<int:event_id>')
def event_detail(event_id):
    event = db.session.get(Event, event_id)
    if not event:
        flash('Event not found.')
        return redirect(url_for('main.event_view'))
    
    related_events = Event.query.filter(Event.id != event_id).limit(2).all()  # Optional related events
    return render_template('event_detail.html', event=event, related_events=related_events)

