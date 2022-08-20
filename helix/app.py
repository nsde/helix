import flask
import logging

app = flask.Flask(__name__, static_url_path='/static', static_folder='static/')
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 ** 2 # MB → B

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

from base.base import base_bp
app.register_blueprint(base_bp)

app.run(port=8585, debug=True)