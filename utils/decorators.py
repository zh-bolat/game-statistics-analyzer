import functools
import time


def time_it(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f"[Профайлер] '{func.__name__}' выполнена за {elapsed:.6f} сек.")
        return result

    return wrapper
