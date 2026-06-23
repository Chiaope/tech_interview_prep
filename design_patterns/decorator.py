from functools import wraps

"""
The main purpose of decorators is to make sure something is ran before the actual function is ran
"""


def my_wrapper(func):
    @wraps(func)  # This is needed to preserve the original function's metadata
    def decorator_function(*args, **kwargs):
        print(
            "hehe I am a decorator"
        )  # Run whatever the decorator is supposed to run before running the actual function
        return func(*args, **kwargs)  # Run the function and returns it

    return decorator_function  # Return the decorator function without the brackets so it doesnt get ran until it is decorated


@my_wrapper
def do_something(message):
    """My job is to do something"""
    print(message)


if __name__ == "__main__":
    do_something("my message")
    print(do_something.__doc__)
    print(do_something.__name__)
