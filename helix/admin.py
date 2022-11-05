"""Base functions."""

import os
import flask
import colorama
import flask_sqlalchemy

colorama.init(autoreset=True)

def init_database(name: str, db: flask_sqlalchemy.SQLAlchemy, app: flask.Flask, check: bool=True) -> None:
    """Prepares the database. Is only needed to be run once."""

    if (not check) or (not os.path.exists('helix/' + name)):
        db.create_all(app=app)
        print(f'{colorama.Fore.GREEN}[HX SUCCESS] Created Database!')

def error(message):
    """Send an error log message."""

    print(f'{colorama.Fore.RED}[HX ERROR] {message}')

if __name__ == '__main__':
    from . import DB_NAME, db, app

    init_database(name=DB_NAME, db=db, app=app, check=False)
