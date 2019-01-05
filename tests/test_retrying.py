import functools
import time
import unittest
from unittest.mock import patch

import retrying
from util import no_error, fail_n, timed_retry


class TestRetrying(unittest.TestCase):
    def test_retry(self):
        """ Timing with retry. """

        r = retrying.retry(no_error)
        timed_retry(r)

    def test_n_retry(self):
        """ Retries a fixed number of times. """
        r = retrying.retry(stop_max_attempt_number=10)(fail_n(9))

        def mock_sleep(s):
            mock_sleep.calls += 1
        mock_sleep.calls = 0

        with patch('time.sleep', mock_sleep):
            r()
        self.assertEqual(mock_sleep.calls, 9)

    def test_backoff(self):
        """ Retries with exponential backoff. """
        r = retrying.retry(wait_exponential_multiplier=1000)(fail_n(9))

        def mock_sleep(s):
            mock_sleep.total += s
        mock_sleep.total = 0.0

        with patch('time.sleep', mock_sleep):
            r()
        self.assertGreaterEqual(mock_sleep.total, 2**9 - 1)

    def test_deadline(self):
        """ Retry limit based on total time. """
        r = retrying.retry(stop_max_delay=1000, wait_fixed=200)(fail_n(5))

        def mock_sleep(s):
            mock_sleep.total += s
        mock_sleep.total = 0.0
        start = time.time()

        def mock_time():
            return start + mock_sleep.total

        with patch.multiple('time', sleep=mock_sleep, time=mock_time):
            r()

        self.assertGreaterEqual(mock_sleep.total, 1.0)
