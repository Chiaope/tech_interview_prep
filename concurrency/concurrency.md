# Concurrency
Definition of concurrency is simultaneous occurance. In Python there are 3 main things:
1. Thread
2. Task
3. Process

| Module          | CPU  | Multitasking | Switching Decision                                     | Category |
| --------------- | ---- | ------------ | ------------------------------------------------------ | -------- |
| asyncio         | 1    | Cooperative  | Task decide when to yield control                      | Task     |
| threading       | 1    | Preemptive   | OS decide when to switch task                          | Thread   |
| multiprocessing | Many | Preemptive   | All process run at the same time on different CPU core | Process  |


## Parallelism
Parallelism can be achieved by running processes on different CPU cores, essentially, each process will be running its own Python interpreter. This can be achieved using `multiprocessing`.

True parallelism means running multiple processes simultaneously all at once and **cap at the number of cores** the computer have. 

Operating system (OS) can run more things together (not in parallel) than the number of cores available because OS uses a method called `Time-Slicing` something similar to how `asyncio` works, there is a loop and schedule that the OS use to switch between task and work on them. Thus making them running concurrently, not parallelly.

## Diffent type of problems
There are mainly 2 different type of problems
1. I/O bound
2. CPU bound

### I/O Bound
I/O bound problems cause the program to slow down because it needs to wait for input or output from external resources. This happens when the wait is much longer than the CPU processing speed.

Some examples of I/O bound issues is, `file system` and `network connections`.

### CPU Bound
CPU bound problems requires a significant time to compute, like for example, `complex maths equations` or `machine learning`. This causes the process to take up all of the CPU resources in order to process them and essentially block other task from running.

| I/O Bound Process | CPU Bound Process |
| - | - |
| Spend most time waiting for slower devices or interface | Spend most time doing CPU operations |
| Speeds up by overlapping wait times | Speeds up by doing more operations at the same time |

## Speed up I/O bound programs
Speeding up I/O bound programs like making multiple API request, we can make sure of `thread` and `asyncio` this will help to stack the waiting time from the API response, reduce the total waiting time.
```python
import requests
from concurrent.futures import ThreadPoolExecutor
import time
import threading
import asyncio
import aiohttp

url_list = [
    "https://www.jython.org",
    "http://olympus.realpython.org/dice",
] * 80


def get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def fetch_url(url):
    session = get_session()
    with session.get(url) as response:
        print(f"Read {len(response.content)} bytes from {url}")


def get_content_with_session(url_list):
    with requests.Session() as session:
        for url in url_list:
            with session.get(url) as response:
                print(f"Read {len(response.content)} bytes from {url}")


def get_content_with_threadpoolexecutor(url_list):
    with ThreadPoolExecutor(max_workers=5) as tpe:
        tpe.map(fetch_url, url_list)
    return


async def fetch_with_asyncio(url, session):
    async with session.get(url) as response:
        content = await response.read()
        print(f"Read {len(content)} bytes from {url}")


async def get_content_with_task_group(url_list):
    async with aiohttp.ClientSession() as session:
        async with asyncio.TaskGroup() as tg:
            for url in url_list:
                tg.create_task(fetch_with_asyncio(url, session))


if __name__ == "__main__":
    use_thread = False
    use_async = True
    start = time.perf_counter()
    if use_thread:
        print("Using thread")
        # Thread-local storage to ensure each thread gets its own session
        thread_local = threading.local()
        get_content_with_threadpoolexecutor(url_list)  # Completed in 4.053 seconds
    elif use_async:
        print("Using async")
        asyncio.run(get_content_with_task_group(url_list))  # Completed in 0.636 seconds
    else:
        print("Using basic session")
        get_content_with_session(url_list)  # Completed in 17.417 seconds
    print(f"Completed in {(time.perf_counter() - start):.3f} seconds")
```

## Speed up CPU bound programs
Some task require a lot of computational power, for example **hyperparameter tuning** or **machine learning**. Using `mulltithreading` or `asyncio` will not speed things up since there are no waiting for I/O operations, everything depends on the computational speed.

In order to help speed up the computational time, we can leverage `multiprocessing`. This allows the computational to be running in **true parallelism**. Multiple processes will be running simultatneously and computing the results in parallel.

**Important Note:** **ALWAYS USE** `if __name__ == "__main__"` since multiprocessing works by spinning up new process and importing the module. If this block is not included, it will essentially spin up infinite process recursively.

```python
import time
from concurrent.futures import ProcessPoolExecutor


def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)


def main():
    start_time = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ppe:
        fib_list = [35] * 20
        ppe.map(fib, fib_list)
    end_time = time.perf_counter()
    print(f"Time taken: {end_time - start_time:.3f} seconds")


if __name__ == "__main__":
    main()
```