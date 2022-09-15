import flask

from .. import system

rooms_bp = flask.Blueprint('rooms_bp',
    __name__,
    template_folder='../'
)

@rooms_bp.route('/room/create', methods=['POST'])
def chat_redirect():
    room_name = flask.request.form.get('room')
    try:
        system.create_room(room_name)
    except AttributeError: # is guest
        return flask.abort(401) # unauthorized
    else:
        return flask.redirect('/chat')
