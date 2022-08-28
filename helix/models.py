import sqlalchemy
import flask_login

from . import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=sqlalchemy.sql.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    notes = db.relationship('Note')
