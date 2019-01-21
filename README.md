# int-presto

interview assignment for [Presto](http://presto.com)

![logo](doc/img/presto_logo.png)

demonstrates some patterns for using SQLAlchemy along with Flask
along with

![marshmallow](doc/img/marshmallow-logo.png)

(which i find incredibly hip and meta-classy) for serialization.

other highlights that aren't found in any of my publicly-available
projects include

* spinning up aiohttp without an
  [`AppRunner`](https://aiohttp.readthedocs.io/en/stable/web_reference.html#aiohttp.web.AppRunner)
  as a demonstration of Python's standard library impedence matching Node's
  builtin api for http servers.
* [SQLAlchemy Self-Referential Many-to-Many Relationship](https://docs.sqlalchemy.org/en/latest/orm/join_conditions.html#self-referential-many-to-many-relationship)
  usage, which is pretty neat since it mixes ORM and non-ORM table
  declaration

## thoughts

let me say near the outset:  Presto is a Django shop with a GraphQL api,
and this repo is not out to be contrarian.  instead, it's meant as a
memo between Pythonistas that can hopefully add some fresh perspective.
i suppose we're all constantly learning from each other, and part of
that is looking for outside sources of influence to futher one's own
practice.  so while i'm not suggesting that i prefer Flask over Django
or vice-versa, i do suppose that there are valuable ideas contained in
both ecosystems, and to the degree that these ideas are reused to solve
cross-cutting concerns, that's a good thing.

so in addition to the assignment of creating a restful api endpoint
to plumb a restaurant's menu from a relational database to the web,
the problem i'm trying to solve is demonstrating DRY principles
without using a monolithic framework.

there's a lot left out in the way of production-readiness.
a small example is logging middleware as demonstrated in my
[simp-phone](http://github.com/ransomw/simp-phone)
project from 2017.  model-layer validation and custom exception
handling in the routes are also left out, and even this is not
exhaustive.

moreover, the entire question of what directions to scale in are
mostly treated as out-of-band:  aiohttp is intended to run in
production.  exactly how to wrap the application in further layers of
reverse proxies and multiprocessing is not treated by the code in
this assignment beyond the suggestion that, by now, the asyncio
module is probably at least as reasonable a Python standard to start
from as WSGI.

existing WSGI applications can be wrapped in aiohttp and on top of
that either GUnicorn or a bunch of instances behind Nginx can scale
"vertically".  meanwhile, fine-grained monitoring on the routes
can determine the "horizontal" pieces that might better be refactored
into several coroutines and run at the async layer outside WSGI.

`</hand-waving>`

[uv-loop](https://github.com/MagicStack/uvloop)
is one slightly more concrete example of the type of thing to
consider when worrying about perf:  Python's C interop is still one of
the better things about the language, and in addition to pure-Python
libraries based on neat linguistic paradigms like marshmallow,
we can still do a lot as Python programmers by writing idiomatic
wrappers around C implementations.

`</rant>`

## usage

`./bin/run.sh --reset-db`

in one terminal

`curl http://localhost:5005/restaurant/1/item`

in another

there are also some tests at `/bin/test.sh`

### further omissions

i haven't run a `pylint` pass yet
