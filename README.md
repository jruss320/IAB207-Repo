# UniVents

UniVents is a Flask web application for discovering, creating, and booking events.
Users can register for an account, browse and search events, publish and manage
their own events, book tickets, and leave comments on event pages.

## Features

- User registration, login, and logout
- Event creation, editing, cancellation, and image uploads
- Event browsing by category and keyword search
- Ticket booking and a personal bookings page
- Event comments
- SQLite database with Flask-Migrate/Alembic migrations
- Brisbane local-time display for event dates and times

## Requirements

- Python 3.10 or newer
- `pip`

## Installation

Clone the repository and create a virtual environment:

```bash
git clone <repository-url>
cd IAB207-Repo
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies listed by the project:

```bash
pip install -r requirements.txt
```

The application also imports `Flask-Migrate` and `pytz`. Install them if they
are not already available in your environment:

```bash
pip install Flask-Migrate pytz
```

## Database Setup

The application uses SQLite and stores the database in
`instance/sitedata.sqlite`. Apply the existing migrations before the first run:

```bash
export FLASK_APP=main.py
flask db upgrade
```

To create a new migration after changing the models:

```bash
flask db migrate -m "describe the schema change"
flask db upgrade
```

## Running the Application

Start the development server with either command:

```bash
python main.py
```

or:

```bash
flask --app main.py run
```

Open <http://127.0.0.1:5000/> in a browser.

## Project Structure

```text
main.py                  Application entry point
univents/                Flask application package
  auth.py                Authentication routes
  forms.py               WTForms definitions
  models.py              SQLAlchemy models
  views.py               Event and booking routes
  templates/             Jinja2 templates
  static/                CSS, images, and uploads
migrations/              Flask-Migrate/Alembic migrations
instance/                Local SQLite database files
requirements.txt         Python dependencies
```

## Configuration Notes

The current development configuration enables Flask debug mode and uses a
development secret key. Set a secure secret key and disable debug mode before
deploying this application publicly. Uploaded event images are stored locally
and should be backed up or replaced with managed storage in production.