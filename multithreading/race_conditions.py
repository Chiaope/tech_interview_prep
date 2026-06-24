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