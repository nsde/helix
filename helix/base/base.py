import flask
import sqlalchemy
import flask_login
import werkzeug.security

from .. import db
from ..models import User

base_bp = flask.Blueprint('base_bp',
    __name__,
    template_folder='../'
)

def set_error(message: str):
    flask.flash(message, category='error')

def set_success(message: str):
    flask.flash(message, category='success')

@base_bp.route('/')
def index():
    return flask.render_template('base/templates/home.html')

@base_bp.route('/register', methods=['GET', 'POST'])
def register():
    if flask.request.method == 'POST':
        form_get = flask.request.form.get
        username = form_get('username')
        password = form_get('password')

        try:
            user = User.query.filter_by(username=username).first()
        except sqlalchemy.exc.OperationalError: # SQL database empty
            user = None
        
        if user:
            set_error('User already exists.')
        elif len(username) < 3:
            set_error('Username must be longer than 2 characters.')
        elif len(username) > 24:
            set_error('Username can\'t be longer than 24 characters.')
        elif len(password) < 7:
            set_error('Password must be at least 7 characters.')
        else:
            user = User(
                username=username,
                password=werkzeug.security.generate_password_hash(password, method='sha512')
            )
            
            db.session.add(user)
            db.session.commit()
            flask_login.login_user(user, remember=True)
            set_success('Account created!')

            return flask.redirect('/')

    return flask.render_template('base/templates/register.html')

@base_bp.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if werkzeug.security.check_password_hash(user.password, password):
                set_success('Logged in successfully!')
                flask_login.login_user(user, remember=True)
                return flask.redirect('/')
            else:
                set_error('Incorrect password, try again.')
        else:
            set_error('User does not exist.')

    return flask.render_template('base/templates/login.html')

@base_bp.route('/legal')
def legal():
    return flask.render_template('base/templates/legal.html')
