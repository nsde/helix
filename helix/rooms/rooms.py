import flask

from .. import system

rooms_bp = flask.Blueprint('rooms_bp',
    __name__,
    template_folder='../'
)

@rooms_bp.route('/room/create', methods=['POST'])
def chat_redirect():
    room_name = flask.request.form.get('room')
    system.create_room(room_name)
    return flask.redirect('/chat')
