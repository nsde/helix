import flask
import sqlalchemy
import flask_login
import werkzeug.security

from .. import db
from .. import system
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

            try:
                db.session.commit()
            except sqlalchemy.exc.OperationalError:
                return '''
                    Sorry, the account system is currently under maintenance! You account was not created.<br>
                    Please <a href="https://onlix.me/contact">contact</a> the server administrator<br>
                    or <a href="/">return back home</a>.
                '''

            flask_login.login_user(user, remember=True)
            system.create_user()

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
    """User logout"""
    flask_login.logout_user()
    return flask.redirect('/')

@flask_login.login_required
@base_bp.route('/delete', methods=['POST'])
def delete_user():
    """Deletes the current user account."""
    user = system.get_current_user()

    if not user: # guest
        return flask.redirect('/')

    if werkzeug.security.check_password_hash(user.password, flask.request.form.get('password')):
        db.session.delete(user)
        db.session.commit()

        return flask.redirect('/?deleted=1')
    return flask.redirect('/chat?deletion-failed=1')

@flask_login.login_required
@base_bp.route('/avatar/change', methods=['POST'])
def change_avatar():
    """Edit the user avatar/profile picture."""

    if not system.get_current_user():
        return flask.abort(403)

    if 'file' not in flask.request.files:
        set_error('No file part!')

    uploaded_file = flask.request.files['avatar']

    if uploaded_file.filename == '':
        set_error('No file selected!')

    if uploaded_file and system.allows_file(uploaded_file.filename):
        # {system.random_id()}.{uploaded_file.filename.rsplit(".", 1)[1].lower()}'
        uploaded_file.save(f'{system.SECRET_FOLDER}/cloud/@{system.get_current_user().id}')
    else:
        set_error(f'This file type is not allowed. Please upload a {"/".join(system.UPLOAD_ALLOWED)} file.')

    set_success('Upload successful! <a href="">Reload</a> to see the changes.')
    return '<script>window.history.go(-1);</script>'

@base_bp.route('/about')
def about():
    """The website's about page"""
    return flask.render_template('base/templates/about.html')
