import time
import unittest

import retrying


def my_decorator(f):
    """ A simple decorator to apply timing """
    def method():
        f()
    return method
    

def no_error():
    return 1


@my_decorator
def dec_noerror():
    return 2


class TestRetrying(unittest.TestCase):
    def _repeat(self, method, times=1000):
        for i in range(1,times):
            method()

    def _with_retry(self):
        self._repeat(r)
        
    def test_baseline(self):
        """ Baseline timing of our method."""
        start = time.time()
        self._repeat(no_error)
        end = time.time()
        print('Baseline_time: \t{}'.format(end-start))

    def test_decorated(self):
        """ Timing for a do-nothing decorator."""
        start = time.time()
        self._repeat(dec_noerror)
        end = time.time()
        print('Decorate_time: \t{}'.format(end-start))

    def test_retry(self):
        """ Timing with retry. """

        r = retrying.retry(no_error)
        start = time.time()
        self._repeat(r)
        end = time.time()
        print('Repeat_time: \t{}'.format(end-start))

