"""
view this module as an object in the OOP sense
with database connection (engine and session) state as members
and functions as methods.

depending on use-case, it might be more sensible to use a class
rather than a module to encapsulate database connection functionality.
this module is written for the case where the database's location
is considered immutable once the python interpreter starts.
"""
import os

import sqlalchemy as sa
import sqlalchemy.orm as sao
import sqlalchemy.ext.declarative as sad
from sqlalchemy.schema import MetaData

SA_DB_URI = os.environ.get('PRESTO_DATABASE', 'sqlite:///pi.db')

engine = sa.create_engine(SA_DB_URI,
                          convert_unicode=True,
)
db_session = sao.scoped_session(sao.sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
))

@sad.as_declarative()
class Base(object):
    """
    base class for all ORM models.
    could be extended in several ways, for example by adding
    the table name as lowercased class name.
    """

    query = db_session.query_property()

    @classmethod
    def by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def all(cls):
        return cls.query.all()


def save_models(*models):
    for model in models:
        db_session.add(model)
    db_session.commit()


def shutdown_session():
    db_session.remove()


def reset_session(scopefunc=None):
    global db_session
    shutdown_session()
    db_session = sao.scoped_session(db_session.session_factory,
                                scopefunc=scopefunc,
    )
    Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)


def drop_all_tables():
    """
    remove all tables, not just those with metadata present in
    this package
    """
    Base.metadata.drop_all(bind=engine)
    meta = MetaData()
    meta.reflect(bind=engine)
    meta.drop_all(bind=engine)
