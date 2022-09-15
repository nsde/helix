import flask_login

try:
    from . import db
except (ModuleNotFoundError, ImportError):
    import db

class User(db.Model, flask_login.UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
