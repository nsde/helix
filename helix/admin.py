import os

def init_database(name, db, app, check=True):
    if (not check) or (not os.path.exists('helix/' + name)):
        db.create_all(app=app)
        print('Created Database!')

def error(message):
    print(f'[HX ERROR] {message}')

if __name__ == '__main__':
    from . import DB_NAME, db, app

    init_database(name=DB_NAME, db=db, app=app, check=False)
