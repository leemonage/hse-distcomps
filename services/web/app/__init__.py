from flask import Flask, send_from_directory, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import os
from functools import wraps

app = Flask(__name__)

# init db

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default='')
    category = db.Column(db.String(100), nullable=False, default='')

    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category

    def to_dict(self):
        return {
            'id': int(self.id),
            'name': str(self.name),
            'category': str(self.category)
        }


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(300), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


while True:
    try:
        db.create_all()
        break
    except Exception:
        pass

# end init db

# jwt

from flask_jwt import JWT
from passlib.hash import pbkdf2_sha256


def authenticate(username, password):
    user = db.session.query(User).filter(User.username == username).first()
    if user and pbkdf2_sha256.verify(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return db.session.query(User).get(user_id)


app.config['SECRET_KEY'] = 'VERY_SECRET_KEY'
jwt = JWT(app, authenticate, identity)

def login_required(f):

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, app.config[SECRET_KEY])
            current_user = Users.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})

        return f(current_user, *args, **kwargs)

    return decorator

# end jwt


from .api import api
from .views import views

# init swagger blueprints

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
app.register_blueprint(api.get_blueprint())

# end init swagger blueprints
