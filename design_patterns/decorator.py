from functools import wraps
import time
import random

"""
The main purpose of decorators is to make sure something is ran before the actual function is ran
"""


def timer_wrapper(func):
    @wraps(func)  # This is needed to preserve the original function's metadata
    def decorator_function(*args, **kwargs):
        start = time.perf_counter()  # Run whatever the decorator is supposed to run before running the actual function
        results = func(*args, **kwargs)  # Run the function and save it or we can return it directly
        time_spend = time.perf_counter() - start  # Run any function that is after the actual function
        print(f"Function ran for {time_spend:.3f} seconds.")
        return results


    return decorator_function  # Return the decorator function without the brackets so it doesnt get ran until it is decorated


@timer_wrapper
def just_sleep(start, end):
    """My job is to sleep"""
    print("Going to sleep")
    time.sleep(random.uniform(start,end))
    return "Woken up"


if __name__ == "__main__":
    print(just_sleep(1, 3))
    print(just_sleep.__doc__)
    print(just_sleep.__name__)
