""" Shared code from retry tests.
"""
import time

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
