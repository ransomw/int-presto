import logging

from flask import _app_ctx_stack
from flask import Flask

from pi import model

def create_app():
    app = Flask(__name__)

    model.reset_session(scopefunc=_app_ctx_stack.__ident_func__)
    @app.teardown_appcontext
    def shutdown_db(exception=None):
        model.shutdown_session()

    from .routes.restaurant import blueprint as restaurant_blueprint
    app.register_blueprint(
        restaurant_blueprint,
        url_prefix='/restaurant',
    )

    return app

