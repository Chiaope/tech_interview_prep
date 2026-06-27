# Multithreading
Multithreading allows Python to run on multiple threads to run concurrently, enabling efficient multitasking. It is especially useful for I/O bound task like **file handling**, network requests, or user interactions.

Threading is especially good when using for file system handling.

A single process can run on multiple threads and the thread shares the same code and global storage but have their own local variables (stacks)

**IMPORTANT NOTE:** Python does not support multithreading in real life terms due to Global Interpreter Lock (GIL)

## How Multithreading Works
On a single core CPU, Python achieves concurrency using context switching (frequent switching between threads). So in practice, each task is running one at a time instead of in parallel due to `GIL`. In order to process task in true parallelism, we need to use `multiprocessing`.

## Benefits
Primary benefit of multithreading over `asyncio` in Python is the ability to handle traditional, synchronous, blocking I/O operations without requiring to rewrite entire codebase or rely on third-party libraries.

## start()
```python
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
```

## local()
When using multiple different threads all at once, sometimes we want to setup some storage for the individual threads without overlapping each other by using `threading.local()` variable. This essentially activates a storage for each of the individual threads.

```python
import threading
import random
import time
from concurrent.futures import ThreadPoolExecutor

thread_local = threading.local()

def get_local_storage():
    if not hasattr(thread_local, "my_storage"):
        print("This thread does not have my_storage value. Adding it now...")
        thread_local.my_storage = random.randint(1,10)
    time.sleep(0.5)
    return thread_local.my_storage

if __name__ == '__main__':
    task_list = []
    with ThreadPoolExecutor(max_workers=2) as tpe:
        for i in range(10):
            task_list.append(tpe.submit(get_local_storage))
    print([task.result() for task in task_list])
"""
Ouput:
This thread does not have my_storage value. Adding it now...
This thread does not have my_storage value. Adding it now...
[4, 8, 4, 8, 4, 8, 4, 8, 4, 8]
"""
```

## Daemon thread

```python
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
```

## ThreadPoolExecutor
```python
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
```

# Race conditions
```python
"""
Race conditions occurs when shared resources are used simultaneously using their own local variable value.

New data could be overwritten by old data if race conditions are not handled properly. 

The reason why race condition happens is because each thread have their own local variable and these are not stored globally. This means that if we are doing calculations and setting new variables that are not stored globally, the end results might be very different.

We can prevent race conditions by adding a lock feature, so that other threads will not be able to access a given block of code when lock is acquired before it is released.
"""
from concurrent.futures import ThreadPoolExecutor
import threading
import time


class FakeDatabase:
    def __init__(self):
        self.value = 0
    
    def update(self, name):
        print(f"Thread {name} started updating")
        # get local copy so that it is thread safe
        local_value = self.value
        local_value += 1
        # sleep to allow other threads to run
        time.sleep(0.5)
        self.value = local_value
        print(f"Thread {name} finished updating")

def race_condition_unhandled():
    print("Starting unhandled race conditions")
    db = FakeDatabase()
    with ThreadPoolExecutor(max_workers=3) as tpe:
        for i in range(1,4):
            tpe.submit(db.update, i)
    print("Finished")
    print(f"FakeDatabase value: {db.value}")  # output: FakeDatabase value: 1

class FakeLockDatabase:
    def __init__(self):
        self.value = 0
        # there can only be 1 lock and if it is used, other task will have to wait
        self.__lock= threading.Lock()
    
    def update(self, name):
        # using lock with context manager helps acquire and release lock, preventing other task from accidentally update some stuff
        with self.__lock:
            print(f"Thread {name} acquired lock")
            # get local copy so that it is thread safe
            local_value = self.value
            local_value += 1
            # sleep to allow other threads to run
            time.sleep(0.5)
            self.value = local_value
            print(f"Thread {name} release lock")

def race_condition_locked():
    print("Starting locked race conditions")
    db = FakeLockDatabase()
    with ThreadPoolExecutor(max_workers=3) as tpe:
        for i in range(1,4):
            tpe.submit(db.update, i)
    print("Finished")
    print(f"FakeDatabase value: {db.value}")  # output: FakeDatabase value: 3

if __name__ == '__main__':
    race_condition_locked()
```