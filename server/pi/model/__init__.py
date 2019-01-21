"""
in addition to defining a public interface, this package's module
imports also ensure sqlalchemy metadata is created, after which
schemas are created for deserialization
"""
from marshmallow import fields as marshfields
import marshmallow_sqlalchemy as msa

from .base import db_session
from .base import engine
from .base import save_models
from .base import shutdown_session
from .base import reset_session
from .base import init_db
from .base import drop_all_tables
from .base import Base
from .restaurant import Restaurant
from .item import item_mods
from .item import Item

class ItemSchema(msa.ModelSchema):
    # could dedupe some of the following
    mods = marshfields.Nested('self', many=True, exclude=(
        'id',
        'restaurant',
    ))
    class Meta:
        model = Item


class RestaurantSchema(msa.ModelSchema):
    items = marshfields.Nested(ItemSchema, many=True, exclude=(
        'id',
        'restaurant',
    ))
    class Meta:
        model = Restaurant


restaurant_schema = RestaurantSchema()

__all__ = [
    'save_models',
    'shutdown_session',
    'reset_session',
    'init_db',
    'drop_all_tables',
    'Restaurant',
    'Item',
    'restaurant_schema',
]
