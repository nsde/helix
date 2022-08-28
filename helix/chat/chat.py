import flask
import flask_sse
import flask_login

chat_bp = flask.Blueprint('chat_bp',
    __name__,
    template_folder='../'
)

DEMO_ROOMS = [
    {
        'name': 'Baz',
        'avatar': 'https://avatars.githubusercontent.com/u/67185896?v=4',
        'id': '2938989487',
        'is_active': True
    }
]

@flask_login.login_required
@chat_bp.route('/chat')
def chat():
    if flask.request.args.get('deletion-failed') == '1':
        flask.flash('Incorrect password, your account hasn\'t been deleted.', category='error')

    # return str(flask_login.current_user.is_authenticated)
    return flask.render_template('chat/templates/chat.html',
        rooms=DEMO_ROOMS,
        avatar='https://github.com/nsde/strobe/raw/master/logo.png',
    )
