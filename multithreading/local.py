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