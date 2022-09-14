# __init__ imports
from . import system
from . import jsondata

# Regular imports

import os
import flask
import logging
import flask_login
import flask_sqlalchemy

from dotenv import load_dotenv

DB_NAME = 'database.db'

load_dotenv()

# DATABASE
db = flask_sqlalchemy.SQLAlchemy()

app = None

def create_app():
    global app
    # app.config["REDIS_URL"] = os.environ.get("REDIS_URL")

    app = flask.Flask(__name__, static_url_path='/static', static_folder='static/')
    app.jinja_env.trim_blocks = True
    app.jinja_env.lstrip_blocks = True
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 ** 2 # MB → B
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

    from .base.base import base_bp
    from .chat.chat import chat_bp
    from .rooms.rooms import rooms_bp

    app.register_blueprint(base_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(rooms_bp)

    db.init_app(app)
    init_database(app)

    login_manager = flask_login.LoginManager()
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'base.login'
    login_manager.init_app(app)

    from . import models

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    @app.context_processor
    def injector():
        return dict(avatar='https://cdn.pixabay.com/photo/2017/11/10/05/48/user-2935527_960_720.png')

    return app

def init_database(app):
    if not os.path.exists('helix/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
