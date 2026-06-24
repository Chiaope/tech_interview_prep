"""
ThreadPoolExecutor is mainly used when you want to prevent accidental mishandling of the threads.
It will automatically clean up and join the threads when the code block is exited.
"""

from concurrent.futures import ThreadPoolExecutor
import time
import random

def some_sync_function(start, end):
    print("Starting sync function")
    sleep_time = random.uniform(start, end)
    time.sleep(sleep_time)
    max_sleep_time = 3
    if sleep_time > max_sleep_time:
        raise Exception(f"Cannot sleep more than {max_sleep_time} seconds.")
    print("Finished sync function")
    return


def done_callback(result):
    exception = result.exception()
    if exception is not None:
        print("Exception occurred!!")


if __name__ == '__main__':
    # max workers is set to 3, so only 3 threads can be running at the same time
    with ThreadPoolExecutor(max_workers=3) as tpe:
        print("Starting TPE mapping")
        # Even though max threads allowed is 3, we can submit as many future as we want and it will be waiting, but there will only be at most 3 threads running all at once
        parameters = [[1,5]] * 10
        for param in parameters:
            future = tpe.submit(some_sync_function, *param)
            # add_done_callback is used to run some function on the results after it is completed
            future.add_done_callback(done_callback)
        print("Ran all threads")
    # Exiting the with block will automatically join all of the finished threads
    print("Finished")