import unittest
import time


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


class TestRetry(unittest.TestCase):
    def _repeat(self, method, times=1000):
        for i in range(1,times):
            method()
        
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
