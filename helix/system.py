import os
import time
import json
import string
import secrets
import datetime
import flask_login

from typing import Union
from dotenv import load_dotenv

from . import admin
from .models import User

load_dotenv()

SECRET_FOLDER = os.getenv('SECRET_FOLDER')
FILE_SUFFIX = '.json'
UPLOAD_ALLOWED = ['png', 'jpg', 'jpeg', 'gif', 'webm']

if SECRET_FOLDER.endswith('/'):
    SECRET_FOLDER = SECRET_FOLDER[:-1]

for folder in ['room', 'user', 'cloud', 'cloud/avatar']:
    path = f'{SECRET_FOLDER}/{folder}'

    if not os.path.exists(path):
        os.mkdir(path)

def allows_file(filename) -> bool: # function name is not a typo
    """Check if a file is allowed to be uploaded."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in UPLOAD_ALLOWED

def write(category: str, folder_id: str, data):
    """Writes a JSON file."""

    try:
        with open(f'{SECRET_FOLDER}/{category}/{folder_id}{FILE_SUFFIX}', 'w', encoding='utf8') as f: # e.g. 8kA8Js.json
            json.dump(data, f)

    except FileNotFoundError as exception: # NEVER, ever show the secret folder path!!
        admin.error(f'system.write (json) FileNotFound: {exception}')

def read(category: str, folder_id: str) -> Union[list, dict]:
    """Reads a JSON file."""

    try:
        with open(f'{SECRET_FOLDER}/{category}/{folder_id}{FILE_SUFFIX}', 'r', encoding='utf8') as f: # e.g. 8kA8Js.json
            data = json.load(f)

    except FileNotFoundError as exception:
        admin.error(f'system.read (json) FileNotFound: {exception}')
        return None

    else:
        return data

def random_id() -> str:
    """Generates a random string."""
    # ((26*2)+10)^6 = 56,800,235,584 possible outcomes
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(5))

def get_current_user():
    """Returns the current user object."""
    try:
        return User.query.filter_by(id=flask_login.current_user.id).first()
    except AttributeError: # guest user
        return None

def create_user():
    """Creates a new user's files and more."""
    user = get_current_user()
    write('user', user.id,
        {
            'id': user.id,
            'name': user.username,
            'owns': [], # rooms the user has created
            'flags': [], # for later use
            'rooms': [], # rooms this user has joined
            'online': False,
            'active': True,
            'friends': [],
            'verified': False,
        }
    )

def create_room(room_name: str) -> str:
    """
    Creates a room, along with all its files and returns its ID.
    The ID is a unique, randomly generated string.
    """
    owner_id = get_current_user().id

    while True:
        room_id = random_id()

        if room_id + FILE_SUFFIX in os.listdir(SECRET_FOLDER): # avoid duplicates
            continue # get a unique one
        break

    write('room', room_id,
        {
            'name': room_name,
            'id': room_id,
            'icon': '',
            'owner': [owner_id],
            'members': [owner_id],
            'verified': False,
            'messages': [
                {
                    'author_name': '#h',
                    'author_id': -1000,
                    'text': 'Channel created successfully.',
                    'time': datetime.datetime.now().strftime("%I:%M %p"),
                    'timestamp': time.time(),
                }
            ],
        }
    )

    user = read('user', owner_id)
    user['owns'].append(room_id)
    user['rooms'].append(room_id)
    write('user', owner_id, user)

    return room_id
