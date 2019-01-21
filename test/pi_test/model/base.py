import unittest

from pi import model as m

def reset_db():
    m.shutdown_session()
    m.drop_all_tables()
    m.init_db()


class Base(unittest.TestCase):

    def setUp(self):
        reset_db()

    def tearDown(self):
        pass
