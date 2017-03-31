import flask
import pymongo
from functools import wraps

app = flask.Flask(__name__)
def allow_cors(fun):
    @wraps(fun)
    def wrapper_fun(*args, **kwargs):
        response = flask.make_response(fun(*args, **kwargs))
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'PUT,GET,POST,DELETE'
        allow_headers = "Referer,Accept,Origin,User-Agent"
        response.headers['Access-Control-Allow-Headers'] = allow_headers
        return response
    return wrapper_fun


@app.route('/', methods=['GET'])
@allow_cors
def index():
    return 'hello'


@app.route('/register', methods=['POST'])
@allow_cors
def register():
    username = flask.request.form.get('username')
    password = flask.request.form.get('password')
    return username + password


if __name__ == '__main__':
    app.run(debug=True)
