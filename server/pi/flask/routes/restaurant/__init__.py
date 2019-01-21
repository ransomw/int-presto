from flask import Blueprint

blueprint = Blueprint(
    'restaurant',
    __name__,
)

from . import routes

__all__ = [
    'blueprint',
]
