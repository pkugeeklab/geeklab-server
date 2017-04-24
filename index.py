import re
from functools import wraps

import flask
import flask_login

import database
import user
from pdfs.pdfGenerator import addInfo

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


@app.route('/gen-pdf/activity', methods=['POST'])
@allow_cors
def pdftest():
    requied_keys = ['username', 'contact', 'title',
                    'desc', 'people', 'principal',
                    'starttime', 'stoptime', 'additional',
                    'item', 'contactplus']
    items = ['exp', 'speech', 'desk', 'projector', 'board', 'tv']
    data = dict((k, flask.request.form.get(k)) for k in requied_keys)
    for k, v in data.items():
        if not v:
            return 'No "{}" provided.'.format(k)
        if k == 'starttime' or k == 'stoptime':
            if not re.match('^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}$', v):
                return 'Time format error.'
            data[k] = v.split('-')
        if k == 'item':
            data[k] = v.split('-')
            if any([i not in items for i in data[k]]):
                return 'Some items do not exist.'
    f = addInfo('activity', data)
    return flask.send_file(f, attachment_filename='activity.pdf', as_attachment=True)


if __name__ == '__main__':
    database.load()
    print(database.db)
    user.login_manager.init_app(app)
    app.secret_key = 'whoami'
    app.run(debug=True)
