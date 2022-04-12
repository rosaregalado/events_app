"""Create database models to represent tables."""
from events_app import db
from sqlalchemy.orm import backref
import enum


class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    email = db.Column(db.String(70), nullable=False)
    phone = db.Column(db.String(70), nullable=False)
    events_attending = db.relationship('Event', secondary='event_table', back_populates='guests')


# STRETCH CHALLENGE: Add a field `event_type` as an Enum column that denotes the
# type of event (Party, Study, Networking, etc)
class Eventtype(enum.Enum):
    PARTY = 1
    STUDY = 2
    NETWORKING = 3
    ALL = 4

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    description = db.Column(db.String(70), nullable=False)
    date_and_time = db.Column(db.DateTime, nullable=False)
    event_type = db.Column(db.Enum(Eventtype), default=Eventtype.ALL)
    guests = db.relationship('Guest', secondary='event_table', back_populates='events_attending')

guest_event_table = db.Table('event_table',
    db.Column('guest_id', db.Integer, db.ForeignKey('guest.id'), primary_key=True),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'), primary_key=True)
)