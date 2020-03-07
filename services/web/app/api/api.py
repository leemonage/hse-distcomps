from .. import app, db, Product
from flask import Blueprint, request, jsonify, make_response, abort
import logging


api = Blueprint('api', __name__)


def get_blueprint():
    return api


# error handlers

@app.errorhandler(400)
def handle400(error):
    return make_response(jsonify({'error': '400 Bad request'}), 400)


@app.errorhandler(404)
def handle404(error):
    return make_response(jsonify({'error': '404 Not found'}), 404)

# end error handlers

# api methods

@api.route('/products', methods=['GET'])
def get_products():
    products = db.session.query(Product).all()
    return jsonify({'products': list(map(lambda x: x.to_dict(), products))})


@api.route('/product', methods=['GET'])
def get_product():
    if not request.args:
        abort(400)

    try:
        logging.info('requested id: ' + str(request.args.get('id')))
        id = int(request.args.get('id'))
    except Exception:
        abort(400)

    found = db.session.query(Product).filter(Product.id == id).first()

    if found is None:
        abort(404)

    return jsonify({'product': found.to_dict()})


@api.route('/product', methods=['POST'])
def add_product():
    if not request.json:
        abort(400)

    if 'name' not in request.json:
        return jsonify({'error': '400 Bad request Product should have name'}), 400

    id_list = list(map(lambda x: x.to_dict()['id'], db.session.query(Product).all()))

    try:
        if 'id' in request.json and int(request.json['id']) in id_list:
            return jsonify({'error': '400 Bad request Product with id already exists'}), 400
    except Exception:
        abort(400)

    new_product = Product(
        int(request.json['id']) if 'id' in request.json else (max(id_list) + 1 if len(id_list) > 0 else 0),
        request.json['name'],
        request.json.get('category', '')
    )

    db.session.merge(new_product)
    db.session.commit()
    return jsonify({'success': True})


@api.route('/product', methods=['PUT'])
def update_product():
    if not request.json or not request.args:
        abort(400)

    try:
        logging.info('requested id: ' + str(request.args.get('id')))
        id = int(request.args.get('id'))
    except Exception:
        abort(400)

    found = db.session.query(Product).filter(Product.id == id).first()

    if found is None:
        abort(404)

    found.name = request.json.get('name', found.name)
    found.category = request.json.get('category', found.category)

    db.session.merge(found)
    db.session.commit()
    return jsonify({'product': found.to_dict()})


@api.route('/product', methods=['DELETE'])
def delete_product():
    if not request.args:
        abort(400)

    try:
        logging.info('requested id: ' + str(request.args.get('id')))
        id = int(request.args.get('id'))
    except Exception:
        abort(400)

    d = db.session.query(Product).filter(Product.id == id).delete()

    if d == 0:
        abort(404)

    db.session.commit()
    return jsonify({'success': True})

# end api methods

