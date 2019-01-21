from aiohttp import web as aioweb
from aiohttp_wsgi import WSGIHandler

from pi.flask import create_app as create_flask_app

def init_app(loop):
    flask_app = create_flask_app()

    aio_app = aioweb.Application(loop=loop)

    aio_app.router.add_route(
        '*', '/{path_info:.*}',
        WSGIHandler(flask_app.wsgi_app))

    return aio_app
