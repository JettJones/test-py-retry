""" Shared code from retry tests.
"""
import time
from unittest.mock import patch

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


def timed_retry(method, times=1000):
    start = time.time()
    for i in range(1,times):
        method()
    end = time.time()
    print('Repeat_time: \t{}'.format(end-start))


class FakeTime():
    def __init__(self):
        self._now = time.time()

        def mock_sleep(s):
            mock_sleep.total += s
            mock_sleep.calls += 1

        def mock_time():
            return self._now + mock_sleep.total

        mock_sleep.total = 0.0
        mock_sleep.calls = 0

        self.mock_sleep = mock_sleep
        self.mock_time = mock_time


    def __enter__(self):
        self.mock_sleep.total = 0.0
        self.mock_sleep.calls = 0

        patcher = patch.multiple(
            'time', sleep=self.mock_sleep, time=self.mock_time)

        self._patcher = patcher
        patcher.start()

    def __exit__(self, type, value, traceback):
        self._patcher.stop()
