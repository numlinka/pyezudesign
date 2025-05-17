# Licensed under the GNU Lesser General Public License v3.0.
# ezudesign Copyright (C) 2023 numlinka.

# std
import unittest

# tests
from ezudesign.utils import *


class TestUtils (unittest.TestCase):
    def func_test(self, a, b):
        return a + b

    def test_try_exec(self):
        def func(a, b):
            return a + b

        self.assertEqual(try_exec(exec_item("func", 1, 2)), 3)
        self.assertEqual(try_exec(exec_item("self.func_test", 2, 3)), 5)
        self.assertEqual(try_exec(exec_item("func_test_globals", 3, 4)), 7)


def func_test_globals(a, b):
    return a + b
