import time
import functools


def time_it(func):
    """
    Декоратор для замера времени выполнения функции.
    Использует time.perf_counter() для максимальной точности.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        elapsed = end - start
        print(f"[Профайлер] '{func.name}' выполнена за {elapsed:.6f} сек.")
        return result
    return wrapper
