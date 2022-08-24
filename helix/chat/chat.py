import flask
import flask_sse

chat_bp = flask.Blueprint('chat_bp',
    __name__,
    template_folder='../'
)

@chat_bp.route('/chat')
def chat():
    return flask.render_template('base/templates/home.html')
