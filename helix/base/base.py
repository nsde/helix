import flask

base_bp = flask.Blueprint('base_bp',
    __name__,
    template_folder='../'
)

@base_bp.route('/')
def index():
    return flask.render_template('base/templates/home.html')

@base_bp.route('/login')
def login():
    return flask.render_template('base/templates/home.html')
