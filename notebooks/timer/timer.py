import time
import logging

logger = logging.getLogger("Timer")

class Timer:
    LAST_REPORTED_TIME = 0

    def get_time(self):
        return self.LAST_REPORTED_TIME

    def time_this(self, function):
        def timed_function(*args, **kwargs):
            start_time = time.perf_counter()
            value = function(*args, **kwargs)
            self.LAST_REPORTED_TIME = time.perf_counter() - start_time
            return value
        return timed_function
