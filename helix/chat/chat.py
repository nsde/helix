import os
import time
import html
import redis
import flask
import arrow
import datetime
import flask_login

from .. import system

redis_db = redis.StrictRedis(password=os.getenv('REDIS_PASS'))

chat_bp = flask.Blueprint('chat_bp',
    __name__,
    template_folder='../'
)

def chat_stream():
    pubsub = redis_db.pubsub()
    pubsub.subscribe('general')

    for message in pubsub.listen():
        if message['type'] == 'message':
            yield 'data: %s\n\n' % message['data'].decode('utf-8')

@chat_bp.route('/api/send', methods=['POST'])
def api_send():
    data = flask.request.get_json()
    content = data['message']

    if '¯' in content or '@»' or '¤' in content:
        return flask.Response(status=400) # return bad response

    try:
        author_name = flask_login.current_user.username
        author_id = flask_login.current_user.id
    except AttributeError:
        author_name = 'Guest'
        author_id = -1
    
    message_time = datetime.datetime.now().strftime("%I:%M %p")
    text = html.escape(content)

    room = system.read('room', data['room'])
    author = html.escape(author_name)

    if room: # not a guest/demo room
        room['messages'].append({
            'author_name': author,
            'author_id': author_id,
            'text': text,
            'time': message_time,
            'timestamp': time.time(),
        })
        system.write('room', data['room'], room)

        redis_db.publish('general', data)

    return flask.Response(status=204)

@chat_bp.route('/api/stream')
def api_stream():
    return flask.Response(chat_stream(), mimetype='text/event-stream')

@chat_bp.route('/@<current_room_id>')
def chat_room(current_room_id):
    if flask.request.args.get('deletion-failed') == '1':
        flask.flash('Incorrect password, your account hasn\'t been deleted.', category='error')

    rooms = []
    this_user = {}
    current_room = {}
    current_user = system.get_current_user()

    if current_user: # not a guest
        for room_id in system.read('user', current_user.id)['rooms']:
            room = system.read('room', room_id)
            
            if room is None:
                user = system.read('user', current_user.id)
                user['owns'].remove(room_id)
                user['rooms'].remove(room_id)
                system.write('user', current_user.id, user)

                continue

            try:
                room['selected'] = room['id'] == current_room_id

                if room['selected']:
                    current_room = room
            except TypeError: # room was deleted
                pass
            
            else:
                rooms.append(room)

        this_user = system.read('user', current_user.id)

        avatar = current_user.id

    else: # is guest
        avatar = '@-1'

    msgs = []

    last_message_timestamp = None
    for message in current_room['messages']:
        if message.get("timestamp") and isinstance(last_message_timestamp, float):
            if float(message.get("timestamp"))//86400 != float(last_message_timestamp)//86400:
                day = arrow.get(message.get("timestamp")).datetime.strftime('%-d.%-m.')
                msgs.append(f'¤{day}')

        msgs.append(f'{message.get("time") or "?"}¯{message.get("author_name") or "System"}¯{message.get("text") or "[No message text]"}')
        last_message_timestamp = message.get("timestamp")

    return flask.render_template('chat/templates/chat.html',
        rooms=rooms,
        avatar=f'/cloud/@{avatar}',
        room=current_room or '{}',
        this_user=this_user,
        msgs=msgs
    )

@chat_bp.route('/chat')
def chat_redirect():
    return flask.redirect('/@-1')

@chat_bp.route('/cloud/<file_id>')
def cloud(file_id):
    if '..' in file_id:
        return flask.abort(403)

    try:
        return flask.send_file(f'{system.SECRET_FOLDER}/cloud/{file_id}')
    except FileNotFoundError:
        if file_id.startswith('@'):
            return flask.send_file('static/assets/default-avatar.png')
        return flask.abort(404)
