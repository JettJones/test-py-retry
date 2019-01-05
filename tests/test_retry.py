import unittest
from unittest.mock import patch
import time

import retry


def no_error():
    return 1


def fail_n(n):
    def method():
        method.count += 1
        if method.count <= n:
            raise Exception('fail {} of {}'.format(method.count, n))
        return method.count
    method.count = 0
    return method


class TestRetry(unittest.TestCase):
    def _repeat(self, method, times=1000):
        for i in range(1,times):
            method()

    def test_retry(self):
        """ Timing with retry. """
        r = retry.retry()(no_error)
        start = time.time()
        self._repeat(r)
        end = time.time()
        print('Repeat_time: \t{}'.format(end-start))

    def test_n_retry(self):
        """ Retries a fixed number of times. """
        r = retry.retry(tries=10, logger=None)(fail_n(9))

        def mock_sleep(s):
            mock_sleep.calls += 1
        mock_sleep.calls = 0

        with patch('time.sleep', mock_sleep):
            r()
        self.assertEqual(mock_sleep.calls, 9)

    def test_backoff(self):
        """ Retries with exponential backoff. """
        r = retry.retry(tries=10, delay=1, backoff=2)(fail_n(9))

        def mock_sleep(s):
            mock_sleep.total += s
        mock_sleep.total = 0.0

        with patch('time.sleep', mock_sleep):
            r()

        self.assertGreaterEqual(mock_sleep.total, 2**9 - 1)

    @unittest.skip('not supported')
    def test_deadline(self):
        """ Retry limit based on total time. """
        pass
