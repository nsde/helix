import flask
import flask_sse
import flask_login

chat_bp = flask.Blueprint('chat_bp',
    __name__,
    template_folder='../'
)

DEMO_ROOMS = [
    # {
    #     'name': 'Baz',
    #     'avatar': 'https://avatars.githubusercontent.com/u/67185896?v=4',
    #     'id': '2938989487',
    #     'is_active': True
    # },
    {
        'name': 'Guest Room',
        'icon': '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-incognito" viewBox="0 0 16 16">\n  <path fill-rule="evenodd" d="m4.736 1.968-.892 3.269-.014.058C2.113 5.568 1 6.006 1 6.5 1 7.328 4.134 8 8 8s7-.672 7-1.5c0-.494-1.113-.932-2.83-1.205a1.032 1.032 0 0 0-.014-.058l-.892-3.27c-.146-.533-.698-.849-1.239-.734C9.411 1.363 8.62 1.5 8 1.5c-.62 0-1.411-.136-2.025-.267-.541-.115-1.093.2-1.239.735Zm.015 3.867a.25.25 0 0 1 .274-.224c.9.092 1.91.143 2.975.143a29.58 29.58 0 0 0 2.975-.143.25.25 0 0 1 .05.498c-.918.093-1.944.145-3.025.145s-2.107-.052-3.025-.145a.25.25 0 0 1-.224-.274ZM3.5 10h2a.5.5 0 0 1 .5.5v1a1.5 1.5 0 0 1-3 0v-1a.5.5 0 0 1 .5-.5Zm-1.5.5c0-.175.03-.344.085-.5H2a.5.5 0 0 1 0-1h3.5a1.5 1.5 0 0 1 1.488 1.312 3.5 3.5 0 0 1 2.024 0A1.5 1.5 0 0 1 10.5 9H14a.5.5 0 0 1 0 1h-.085c.055.156.085.325.085.5v1a2.5 2.5 0 0 1-5 0v-.14l-.21-.07a2.5 2.5 0 0 0-1.58 0l-.21.07v.14a2.5 2.5 0 0 1-5 0v-1Zm8.5-.5h2a.5.5 0 0 1 .5.5v1a1.5 1.5 0 0 1-3 0v-1a.5.5 0 0 1 .5-.5Z"/>\n</svg>',
        'id': '-1',
        # 'is_active': True
    }
]

# @flask_login.login_required
@chat_bp.route('/@<room_id>')
def chat_room(room_id):
    if flask.request.args.get('deletion-failed') == '1':
        flask.flash('Incorrect password, your account hasn\'t been deleted.', category='error')

    current_room = None

    for room_no, room in enumerate(DEMO_ROOMS):
        room['is_active'] = int(room_id) == int(room['id'])
        current_room = room
        DEMO_ROOMS[room_no] = current_room

    # return str(flask_login.current_user.is_authenticated)
    return flask.render_template('chat/templates/chat.html',
        rooms=DEMO_ROOMS,
        avatar='https://github.com/nsde/strobe/raw/master/logo.png',
        current_room=current_room
    )

@chat_bp.route('/chat')
def chat_redirect():
    return flask.redirect('/@-1')
