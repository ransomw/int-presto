import asyncio as aio

import click

from pi import model as m
from pi.aiohttp import init_app

_HANDLER_SHUTDOWN_SEC = 60.0

def _reset_db():
    m.shutdown_session()
    m.drop_all_tables()
    m.init_db()
    restaurant = m.Restaurant(name="Five Guys")
    burger = m.Item(restaurant=restaurant,
                    name="burger")
    fries = m.Item(restaurant=restaurant,
                   name="fries")
    ketchup = m.Item(restaurant=restaurant,
                     name="ketchup")
    burger.mods.append(fries)
    burger.mods.append(ketchup)
    fries.mods.append(ketchup)
    m.save_models(restaurant)
    m.shutdown_session()


def _run_aiohttp(port):
    """
    aiohttp v2 style with asyncio internals visible.
    v3 includes application runners
    https://aiohttp.readthedocs.io/en/stable/web_advanced.html#application-runners
    to eliminate the boilerplate.
    """
    loop = aio.get_event_loop()
    aio_app = init_app(loop)
    handler = aio_app.make_handler()
    srv = loop.run_until_complete(
        loop.create_server(
            handler,
            '0.0.0.0',
            port,
        ))
    print("serving on", srv.sockets[0].getsockname())
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        loop.run_until_complete(srv.wait_closed())
        loop.run_until_complete(aio_app.shutdown())
        loop.run_until_complete(handler.shutdown(_HANDLER_SHUTDOWN_SEC))
        loop.run_until_complete(aio_app.cleanup())
        loop.close()


@click.command()
@click.option('--port', default=5005)
@click.option('--reset-db', is_flag=True)
def main(port, reset_db):
    if reset_db:
        _reset_db()
    _run_aiohttp(port)


if __name__ == '__main__':
    main()

