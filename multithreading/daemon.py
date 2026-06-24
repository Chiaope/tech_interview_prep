"""
Daemon thread will shut down immediately when the program ends.
So we do not need to worry about shutting down the thread.
"""

import threading
import time
import random


def some_sync_function(start, end):
    print("Starting sync function")
    time.sleep(random.uniform(start, end))
    print("Finished sync function")
    return


if __name__ == "__main__":
    print("Creating thread")
    my_thread = threading.Thread(target=some_sync_function, args=[1, 5], daemon=True)
    print("Starting thread")
    my_thread.start()
    print("Continue some other stuff...")
    # join() is optional, and this is only used to block the rest of the code from running before the thread finishes
    # my_thread.join()
    # print("Thread finished and released")
    print("Entire program finished")
