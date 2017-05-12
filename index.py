import re
from functools import wraps
import flask
import flask_login

from utils import database
import user
from pdfs.pdfGenerator import addInfo, CACHE_DIR
import pdfs.model
from utils.utils import *
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
def genpdf_activity():
    requied_keys = ['title', 'people', 'username', 'contact',
                    'principal', 'contactplus',
                    'starttime', 'stoptime', 'desc', 'additional',
                    'item']
    items = ['exp', 'speech', 'desk', 'projector', 'board', 'tv']
    data = dict((k, flask.request.form.get(k)) for k in requied_keys)
    for k, v in data.items():
        if not v and k != 'item':
            return stringify({'error': {k: 'No "{}" provided.'.format(k)}})
        if k == 'starttime' or k == 'stoptime':
            if not re.match('^\d{4}-\d{2}-\d{2}-\d{2}-\d{2}$', v):
                return stringify({'error': 'Time format error.'})
            data[k] = v.split('-')
        if k == 'item' and v:
            data[k] = v.split('-')
            if any([i not in items for i in data[k]]):
                return stringify({'error': 'Some items do not exist.'})
    data = pdfs.model.save('activity', data)
    addInfo('activity', data)
    pdfid = data['pdfid']
    if pdfid:
        return stringify({'ok': {'pdfid': pdfid}})
    else:
        return stringify({'error': 'Unknown error'})

@app.route('/query-pdf/<pdfid>', methods=['GET'])
@allow_cors
def querypdf(pdfid):
    print(pdfid)
    data = pdfs.model.get(pdfid)
    if data:
        table_type = data['type']
        addInfo('activity', data)
        return stringify({'ok': {'pdfid': pdfid}})
    else:
        return stringify({'error': {'pdfid': 'Not found'}})

@app.route('/get-pdf/<pdfid>/', methods=['GET'])
@allow_cors
def getpdf(pdfid):
    f = open('{}/{}.pdf'.format(CACHE_DIR, pdfid), 'rb')
    return flask.send_file(f, attachment_filename='a{}.pdf'.format(pdfid), as_attachment=True)


if __name__ == '__main__':
    database.load()
    user.login_manager.init_app(app)
    app.secret_key = 'whoami'
    app.run(debug=True)
