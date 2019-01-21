from functools import partial

from pi_test.util_load_tests import load_tests_from_modules

from . import model

load_tests = partial(load_tests_from_modules, [
    model,
])
