from functools import wraps
import errno
import os
import signal


class TimeoutError(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            import time
            print('timeout', seconds)
            try:
                result = func(*args, **kwargs)
                return result
            except TimeoutError as e:
                return None
            finally:
                signal.alarm(0)
        return wraps(func)(wrapper)
    return decorator
