"""
This is the basic way on how to start a thread to be ran behind the scenes.
Problem with this is that, even after the program have finished, the thread task is still running
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
    my_thread = threading.Thread(target=some_sync_function, args=[1, 5])
    print("Starting thread")
    my_thread.start()
    print("Continue some other stuff...")
    # join() is optional, and this is only used to block the rest of the code from running before the thread finishes
    # my_thread.join()
    # print("Thread finished and released")
    print("Entire program finished")
