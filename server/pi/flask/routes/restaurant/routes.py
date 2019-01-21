from flask import jsonify

from pi import model as m
from . import blueprint

@blueprint.route('/')
def health():
    return 'hello'


@blueprint.route('/<int:restaurant_id>/item', methods=['GET'])
def items(restaurant_id):
    restaurant = m.Restaurant.by_id(restaurant_id)
    return jsonify(m.restaurant_schema.dump(restaurant).data['items'])
