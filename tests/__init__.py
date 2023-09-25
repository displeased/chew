"""
Tests; Top-Level Modules contains shared testing utilities.
"""

import unittest
import contextlib
from chew.error import Error


@contextlib.contextmanager
def assert_error(self: unittest.TestCase, error: Error):
    with self.assertRaises(Error) as context:
        yield None

    self.assertEqual(context.exception, error)
