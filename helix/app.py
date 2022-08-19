import flask
import logging

app = flask.Flask(__name__)
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
app.config['MAX_CONTENT_LENGTH'] = 200 * 1024 ** 2 # MB → B

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

@app.route('/')
def index():
    return flask.render_template('home.html')

app.run(port=8585, debug=True)