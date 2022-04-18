"""Import packages and modules."""
import os
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from events_app.models import Event, Guest

# Import app and db from events_app package so that we can run app
from events_app import app, db

main = Blueprint('main', __name__)


##########################################
#           Routes                       #
##########################################

@main.route('/')
def index():
    """Show upcoming events to users!"""
    events = Event.query.all()
    return render_template('index.html', events=events)


@main.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new event."""
    if request.method == 'POST':
        new_event_title = request.form.get('title')
        new_event_description = request.form.get('description')
        date = request.form.get('date')
        time = request.form.get('time')

        try:
            date_and_time = datetime.strptime(
                f'{date} {time}',
                '%Y-%m-%d %H:%M')
        except ValueError:
            return render_template('create.html', 
                error='Incorrect datetime format! Please try again.')

        # Create a new event with the given title, description, & 
        # datetime, then add and commit to the database
        new_event = Event(title=new_event_title, description=new_event_description, date_and_time=date_and_time)
        db.session.add(new_event)
        db.session.commit()

        flash('Event created.')
        return redirect(url_for('main.index'))
    else:
        return render_template('create.html')


@main.route('/event/<event_id>', methods=['GET'])
def event_detail(event_id):
    """Show a single event."""
    event = Event.query.get(event_id)
    event_time = str(event.date_and_time).split(' ')
    return render_template('event_detail.html', event=event, event_time=event_time)


@main.route('/event/<event_id>', methods=['POST'])
def rsvp(event_id):
    """RSVP to an event."""
    event = Event.query.get(event_id)
    is_returning_guest = request.form.get('returning')
    guest_name = request.form.get('guest_name')

    if is_returning_guest:
        guest = Guest.query.filter_by(name=guest_name).first()
        if not guest:
            return render_template('event_detail.html', error='error', event=event)

        else:
            # add guest to db & commit
            event.guests.append(guest)
            db.session.add(event)
            db.session.commit()
    else:
        # create new guest with the given name, email, and phone
        guest_email = request.form.get('email')
        guest_phone = request.form.get('phone')

        guest = Guest(name=guest_name, email=guest_email, phone=guest_phone)
        event.guests.append(guest)
        db.session.add(event)
        db.session.commit()
    
    flash('You have successfully RSVP\'d! See you there!')
    return redirect(url_for('main.event_detail', event_id=event_id))


@main.route('/guest/<guest_id>')
def guest_detail(guest_id):
    guest = Guest.query.get(guest_id)
    return render_template('guest_detail.html', guest=guest)
