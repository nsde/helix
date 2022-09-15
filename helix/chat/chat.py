import os
import time
import html
import redis
import flask
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

    if content.startswith('»') and not data.get('room'): # join message
        return

    if '¯' in content: #seperators
        return flask.Response(status=400) # return bad response

    try:
        author_name = flask_login.current_user.username
        author_id = flask_login.current_user.id
    except AttributeError:
        author_name = 'Guest'
        author_id = -1
    
    message_time = datetime.datetime.now().strftime("%I:%M %p")
    text = html.escape(content)

    print(data)
    room = system.read('room', data['room'])
    room['messages'].append({
        'author_name': author_name,
        'author_id': author_id,
        'text': text,
        'time': message_time,
        'timestamp': time.time()
    })
    system.write('room', data['room'], room)

    redis_db.publish('general', u'%s¯%s¯%s' % (message_time, html.escape(author_name), text))

    return flask.Response(status=204)

@chat_bp.route('/api/stream')
def api_stream():
    return flask.Response(chat_stream(), mimetype='text/event-stream')

@chat_bp.route('/@<current_room_id>')
def chat_room(current_room_id):
    if flask.request.args.get('deletion-failed') == '1':
        flask.flash('Incorrect password, your account hasn\'t been deleted.', category='error')

    rooms = []
    current_room = {}

    if system.get_current_user(): # not a guest
        for room_id in system.read('user', system.get_current_user().id)['rooms']:
            room = system.read('room', room_id)
            
            try:
                room['selected'] = room['id'] == current_room_id

                if room['selected']:
                    current_room = room
            except TypeError: # room was deleted
                pass
            
            else:
                rooms.append(room)

    # return str(flask_login.current_user.is_authenticated)
    return flask.render_template('chat/templates/chat.html',
        rooms=rooms,
        avatar='',
        room=current_room or '{}'
    )

@chat_bp.route('/chat')
def chat_redirect():
    return flask.redirect('/@-1')
