import os
import flask
import logging
import flask_login
import flask_sqlalchemy

from dotenv import load_dotenv

DB_NAME = 'database.db'

load_dotenv()
db = flask_sqlalchemy.SQLAlchemy()

# DATABASE
db = flask_sqlalchemy.SQLAlchemy()

def create_app():
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
    app.register_blueprint(base_bp)
    app.register_blueprint(chat_bp)

    db.init_app(app)

    create_database(app)

    login_manager = flask_login.LoginManager()
    login_manager.login_view = 'base.login'
    login_manager.init_app(app)

    from . import models

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))
    return app

def create_database(app):
    if not os.path.exists('helix/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
