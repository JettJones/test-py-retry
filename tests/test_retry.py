import time
import unittest
from unittest.mock import patch

import retry
from util import no_error, fail_n, timed_retry, FakeTime


class TestRetry(unittest.TestCase):
    def test_retry(self):
        """ Timing with retry. """
        r = retry.retry()(no_error)
        timed_retry(r)

    def test_n_retry(self):
        """ Retries a fixed number of times. """
        r = retry.retry(tries=10, logger=None)(fail_n(9))

        fake_time = FakeTime()
        with fake_time:
            r()
        self.assertEqual(fake_time.mock_sleep.calls, 9)

    def test_backoff(self):
        """ Retries with exponential backoff. """
        r = retry.retry(tries=10, delay=1, backoff=2)(fail_n(9))

        fake_time = FakeTime()
        with fake_time:
            r()
        self.assertGreaterEqual(fake_time.mock_sleep.total, 2**9 - 1)

    @unittest.skip('not supported')
    def test_deadline(self):
        """ Retry limit based on total time. """
        pass
