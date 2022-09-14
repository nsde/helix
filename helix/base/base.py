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
        
        if user or username.lower() in ['Guest'] or 'helix' in username.lower():
            set_error('This username is already taken.')
        elif len(username) < 3:
            set_error('Username must be longer than 2 characters.')
        elif len(username) > 24:
            set_error('Username can\'t be longer than 24 characters.')
        elif len(password) < 7:
            set_error('Password must be at least 7 characters.')
        elif len(password) > 128:
            set_error('Password can\'t be longer than 128 characters.')
        else:
            user = User(
                username=username,
                password=werkzeug.security.generate_password_hash(password, method='sha512')
            )
            
            db.session.add(user)
            db.session.commit()
            flask_login.login_user(user, remember=True)
            set_success('Account created!')

            return flask.redirect('/chat')

    return flask.render_template('base/templates/register.html')

@base_bp.route('/login', methods=['GET', 'POST'])
def login():
    error_message = 'Incorrect user or password.'

    if flask.request.method == 'POST':
        username = flask.request.form.get('username')
        password = flask.request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if werkzeug.security.check_password_hash(user.password, password):
                set_success('Welcome back!')
                flask_login.login_user(user, remember=True)
                return flask.redirect('/chat')
            else:
                set_error(error_message)
        else:
            set_error(error_message)

    return flask.render_template('base/templates/login.html')

@flask_login.login_required
@base_bp.route('/logout')
def logout():
    flask_login.logout_user()
    return flask.redirect('/')

@flask_login.login_required
@base_bp.route('/delete', methods=['POST'])
def delete():
    try:
        user = User.query.filter_by(id=flask_login.current_user.id).first()
    except AttributeError: # guest user
        return flask.redirect('/')

    if werkzeug.security.check_password_hash(user.password, flask.request.form.get('password')):
        db.session.delete(user)
        db.session.commit()

        return flask.redirect('/?deleted=1')
    else:
        return flask.redirect('/chat?deletion-failed=1')

@base_bp.route('/about')
def about():
    return flask.render_template('base/templates/about.html')
