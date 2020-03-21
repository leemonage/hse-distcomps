from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
import os

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


while True:
    try:
        db.create_all()
        break
    except Exception:
        pass

# end init db


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
