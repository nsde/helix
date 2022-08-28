import flask
import flask_sse

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
    },
    {
        'name': 'FooBar',
        'avatar': 'https://github.com/nsde/strobe/raw/master/logo.png',
        'id': '1029380219',
        'is_active': False
    },
    {
        'name': 'FooBar',
        'avatar': 'https://github.com/nsde/strobe/raw/master/logo.png',
        'id': '1029380219',
        'is_active': False
    },
    {
        'name': 'FooBar',
        'avatar': 'https://github.com/nsde/strobe/raw/master/logo.png',
        'id': '1029380219',
        'is_active': False
    },
    {
        'name': 'FooBar',
        'avatar': 'https://github.com/nsde/strobe/raw/master/logo.png',
        'id': '1029380219',
        'is_active': False
    },
    {
        'name': 'FooBar',
        'avatar': 'https://github.com/nsde/strobe/raw/master/logo.png',
        'id': '1029380219',
        'is_active': False
    }
]

@chat_bp.route('/chat')
def chat():
    return flask.render_template('chat/templates/chat.html', rooms=DEMO_ROOMS)
