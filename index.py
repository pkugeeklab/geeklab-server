from functools import wraps

import flask
import flask_login

import database
import user

app = flask.Flask(__name__)


def allow_cors(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        response = flask.make_response(fun(*args, **kwargs))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers[
            'Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        response.headers['Access-Control-Allow-Headers'] = allow_headers
        return response
    return wrapper_fun


@app.route('/user/register', methods=['POST'])
@allow_cors
def user_register():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    if (user.create({'username': username, 'password': password})):
        return 'register successfully'


@app.route('/user/login', methods=['POST'])
@allow_cors
def user_login():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    print(username, password)
    print(flask.session)
    user_to_login = user.get_by_name(username)
    if not user_to_login:
        return 'No such user'
    if user_to_login.password != user.hash_password(password):
        return 'Password error'
    token = user_to_login.get_token()
    return 'Successfully' + token


@app.route('/user/logout', methods=['POST'])
@allow_cors
@flask_login.login_required
def user_logout():
    print('logout')
    username = flask.request.form.get('username')
    user_to_logout = user.get_by_name(username)
    user_to_logout.logout()
    return 'Logout successfully'


@app.route('/test', methods=['POST'])
@allow_cors
@flask_login.login_required
def test():
    return 'Cong'


if __name__ == '__main__':
    database.load()
    print(database.db)
    user.login_manager.init_app(app)
    app.secret_key = 'whoami'
    app.run(debug=True)
