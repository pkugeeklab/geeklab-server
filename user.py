import uuid

import flask_login
from Crypto.Hash import SHA256

import database

login_manager = flask_login.LoginManager()


class User(flask_login.UserMixin):

    _token = None

    def __init__(self, data=None, username=None, password=None):
        if data:
            self.username = data['username']
            self.password = data['password']
            if 'token' in data:
                self._token = data['token']
        else:
            self.username = username
            self.password = hash_password(password)

    def to_object(self):
        return {
            'username': self.username,
            'password': self.password,
        }

    def get_token(self):
        if not self._token:
            token = str(uuid.uuid4())
            self._token = token
            database.db.users.update_one({'username': self.username},
                                         {'$set': {'token': token}})
        else:
            token = self._token
        return token

    def logout(self):
        database.db.users.update_one({'username': self.username},
                                     {'$unset': {'token': 1}})
        return True


@login_manager.request_loader
def request_loader(request):
    print('request_loader')
    if 'token' in request.form:
        username = request.form.get('username')
        token = request.form.get('token')
        user = database.db.users.find_one({'username': username})
        user = User(user) if user else None
        print(user.get_token(), token)
        if user.get_token() == token:
            return user
        else:
            return None
    username = request.form.get('username')
    password = request.form.get('password')
    password = hash_password(password)
    user = database.db.users.find_one(
        {'username': username, 'password': password})
    user = User(user) if user else None
    return user


def create(data):
    username = data['username']
    password = data['password']
    user_to_register = User(username=username, password=password)
    database.db.users.insert_one(user_to_register.to_object())
    return True


def get_by_name(username):
    user = database.db.users.find_one({'username': username})
    user = User(user) if user else None
    return user


def update(db, data):
    pass


def delete(db, data):
    pass


def hash_password(pwd):
    h = SHA256.new(pwd.encode())
    return h.hexdigest()


if __name__ == '__main__':
    pass
