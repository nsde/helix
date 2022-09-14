import os
import time
import json
import string
import secrets

from . import jsondata

from dotenv import load_dotenv

load_dotenv()

SECRET_FOLDER = os.getenv('SECRET_FOLDER')
FILE_SUFFIX = '.json'

if SECRET_FOLDER.endswith('/'):
    SECRET_FOLDER = SECRET_FOLDER[:-1]

def create_folder(name: str):
    path = f'{SECRET_FOLDER}/{name}'

    if not os.path.exists(path):
        os.mkdir(path)

for folder in ['rooms', 'users']:
    create_folder(folder)

def write(category: str, folder_id: str, data):
    with open(f'{SECRET_FOLDER}/{category}/{folder_id}{FILE_SUFFIX}', 'w') as f: # e.g. 8kA8Js.json
        json.dump(data, f)

def random_id() -> str:
    # ((26*2)+10)^6 = 56,800,235,584 possible outcomes
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(5))
 
def create_room(owner_id: int, room_name: str) -> str:
    """
    Creates a room, along with all its files and returns its ID.
    The ID is a unique, randomly generated string.
    """

    while True:
        room_id = random_id()

        if room_id + FILE_SUFFIX in os.listdir(SECRET_FOLDER): # avoid duplicates
            continue # get a unique one
        break

    with open(f'{SECRET_FOLDER}/rooms/{room_id}{FILE_SUFFIX}', 'w') as f: # e.g. 8kA8Js.json
        json.dump({
            'name': room_name,
            'id': room_id,
            'icon': '',
            'owner': [owner_id],
            'members': [owner_id],
            'messages': [
                {
                    'author': '',
                    'text': '{}',
                    'timestamp': time.time()
                }
            ],
        }
    , f)

    with open(f'{SECRET_FOLDER}/users/{owner_id}{FILE_SUFFIX}', 'w') as f: # e.g. 8kA8Js.json
        json.dump(f)

    return room_id
