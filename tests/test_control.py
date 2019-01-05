import unittest
import time

from util import no_error, timed_retry

def my_decorator(f):
    """ A simple decorator to apply timing """
    def method():
        f()
    return method


@my_decorator
def dec_noerror():
    return 2


class TestRetry(unittest.TestCase):
    def test_baseline(self):
        """ Baseline timing of our method."""
        timed_retry(no_error)

    def test_decorated(self):
        """ Timing for a do-nothing decorator."""
        timed_retry(dec_noerror)
