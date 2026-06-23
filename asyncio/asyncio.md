# ASync IO
# Concurrency in Python: Pros and Cons

A breakdown of the three main concurrency models in Python: **Asyncio**, **Multithreading**, and **Multiprocessing**.

---

## 1. Asyncio (Asynchronous I/O)
Runs on a single thread in a single process using cooperative multitasking via an event loop. 
**Best for:** High-volume I/O-bound tasks (e.g., thousands of simultaneous network connections, chat servers).

### ✅ Pros
* **Extremely Lightweight:** Can handle tens of thousands of simultaneous async tasks on a single thread without crashing the system.
* **No Lock Contention:** Everything runs on one thread, eliminating complex locks, mutexes, and race conditions associated with shared memory.
* **Massive Scalability:** The absolute best option for managing a huge number of concurrent network requests.

### ❌ Cons
* **Viral Nature:** Usually requires your entire codebase (and dependencies) to be async. You must use async-compatible libraries (e.g., `aiohttp` instead of `requests`). Once decided to use `async` we have to use `async` for everything else.
* **Blocks on CPU Tasks:** A single heavy CPU calculation will block the entire event loop, freezing all other tasks.
* **Steeper Learning Curve:** Requires a paradigm shift to understand event loops, futures, and callbacks.
* **File I/O Task:** `asyncio` is good for network I/O task but bad for file I/O task.

---

## 2. Multithreading
Uses the operating system to spawn multiple threads within a single Python process, sharing the same memory space.
**Best for:** Standard I/O-bound tasks using synchronous code (e.g., downloading dozens of files, simple web scraping).

### ✅ Pros
* **Shared Memory:** Because threads live in the same process, sharing variables and state between them is effortless.
* **File I/O Task:** It is very fast when doing file related I/O tasks.
* **Familiarity:** Works well with existing synchronous, blocking code without requiring an architectural overhaul. Able to work with any regular python code without the need to search for async compatible packages.
* **Bypasses GIL for I/O:** When a thread waits for I/O (like a network response), it releases the Global Interpreter Lock (GIL), allowing other threads to execute.

### ❌ Cons
* **The GIL Limitation:** Provides **zero performance benefit for CPU-bound tasks**. Only one thread can execute Python bytecode at a time.
* **Race Conditions:** Shared memory means simultaneous modifications can cause disastrous, hard-to-debug race conditions. Actively managing "locks" is required.
* **Context Switching Overhead:** The OS spends resources switching between threads. Spawning too many threads will severely degrade performance.

---

## 3. Multiprocessing
Spawns entirely new, distinct OS processes, each with its own Python interpreter, memory space, and GIL.
**Best for:** CPU-bound tasks (e.g., data science, image processing, complex math, machine learning).

### ✅ Pros
* **True Parallelism:** Completely sidesteps the GIL. Allows you to utilize all CPU cores simultaneously at full speed.
* **Memory Isolation:** Safe from race conditions and locking headaches because memory isn't shared. If one process crashes, it doesn't take down the others.

### ❌ Cons
* **High Overhead:** Creating processes takes significant time and memory. Spawning hundreds of processes is incredibly heavy on the OS.
* **Complex IPC (Inter-Process Communication):** Because memory isn't shared, passing data between processes requires Queues, Pipes, or shared memory managers, introducing serialization/deserialization latency.

---

## Summary Table

| Feature | Asyncio | Multithreading | Multiprocessing |
| :--- | :--- | :--- | :--- |
| **Concurrency Model** | Cooperative (Event Loop) | Preemptive (OS managed) | Preemptive (OS managed) |
| **Best Used For** | High-volume I/O-bound | Low/Medium-volume I/O-bound | CPU-bound |
| **Bypasses GIL?** | N/A (Single Thread) | Only for I/O | **Yes (True Parallelism)** |
| **Memory Overhead** | Very Low | Medium | Very High |
| **Shared Memory** | Yes (Trivially) | Yes (Requires Locks) | No (Requires IPC) |

## How to use asyncio

To create an asynchronous function, we need to add the keyword `async` in front of `def`.

To run an asynchronous function, we need to add the keyword `await`

For all asyncio applications, there need to be an event loop and there can be only a <b>single</b> event loop. To create an event loop we can use `asyncio.run(<function_name>)`

```python
import asyncio


async def asynchronous_sleep(i):
    print(f"Async sleep for {i} seconds")
    await asyncio.sleep(i)
    return i


async def main():
    sleep_timer = 10
    # here is our custom asynchronous function
    await asynchronous_sleep(sleep_timer)
    print(f"Managed to run async function for {sleep_timer} seconds")


if __name__ == "__main__":
    asyncio.run(main)
```

We can start an event loop directly in the terminal without using `asyncio.run()` by running asyncio module direction in the terminal
```bash
$ python -m asyncio
asyncio REPL 3.13.3 (main, Jun 25 2025, 17:27:59) ... on darwin
Use "await" directly instead of "asyncio.run()".
Type "help", "copyright", "credits" or "license" for more information.
>>> import asyncio

>>> async def main():
...     print("Hello...")
...     await asyncio.sleep(1)
...     print("World!")
...

>>> await main()
Hello...
World!
```
## Chaining Functions
There can be multiple `awaits` in each asynchronous function and each `await` acts like a checkpoint, waiting to see if there are any processes that are completed.

```python
import asyncio
import random
import time


async def main():
    user_ids = [1, 2, 3]
    start = time.perf_counter()
    await asyncio.gather(*(get_user_with_posts(user_id) for user_id in user_ids))
    end = time.perf_counter()
    print(f"\n==> Total time: {end - start:.2f} seconds")


async def get_user_with_posts(user_id):
    user = await fetch_user(user_id)
    await fetch_posts(user)


async def fetch_user(user_id):
    delay = random.uniform(0.5, 2.0)
    print(f"User coro: fetching user by {user_id=}...")
    await asyncio.sleep(delay)
    user = {"id": user_id, "name": f"User{user_id}"}
    print(f"User coro: fetched user with {user_id=} (done in {delay:.1f}s).")
    return user


async def fetch_posts(user):
    delay = random.uniform(0.5, 2.0)
    print(f"Post coro: retrieving posts for {user['name']}...")
    await asyncio.sleep(delay)
    posts = [f"Post {i} by {user['name']}" for i in range(1, 3)]
    print(
        f"Post coro: got {len(posts)} posts by {user['name']} (done in {delay:.1f}s):"
    )
    for post in posts:
        print(f" - {post}")


if __name__ == "__main__":
    random.seed(444)
    asyncio.run(main())
```

## TaskGroup vs gather
There are quite some differences between `TaskGroup` and `gather`.
TaskGroup have an implicit `await` the runs immediately after `async with` block so we do not need to explicitly mention `await` after `create_task()`. Whereas for `gather`, we have to use `await` in order for it to run all of the tasks.

Use `TaskGroup` if unsure since it is more modern and it have a better exception handling

| Features           | TaskGroup                                                                                      | gather                                                                                                                                     |
| ------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Paradigm           | Structured concurrency                                                                         | Unstructured concurrency                                                                                                                   |
| Safety             | High (Guarantees context completion)                                                           | Lower (can leave tasks running if  cancelled)                                                                                              |
| Exception Handling | Stop running the rest of the functions if a single function hit an exception, saving resources | Every function is isolated, if a function hit an exception, other functions will continue to run, which might be dangerous if not intended |
| Result Retrival    | Returned implicitly, accessed via individual tasks                                             | Returned directly as an ordered list                                                                                                       |
| Dynamic Addition   | Added tasks during context execution                                                           | Fixed list of tasks at call time                                                                                                           |

```python
import asyncio


async def count_basic():
    print("One")
    await asyncio.sleep(1)
    print("Two")
    await asyncio.sleep(1)


async def count_return(i):
    print("One")
    await asyncio.sleep(1)
    print("Two")
    await asyncio.sleep(1)
    return f"Count: {i}"


async def tg_basic():
    task = []
    async with asyncio.TaskGroup() as tg:
        task.append(tg.create_task(count_basic()))
        task.append(tg.create_task(count_basic()))
        task.append(tg.create_task(count_basic()))
    results = [t.result() for t in task]
    print(results)
    return results


async def tg_return():
    task = []
    async with asyncio.TaskGroup() as tg:
        task.append(tg.create_task(count_return(1)))
        task.append(tg.create_task(count_return(2)))
        task.append(tg.create_task(count_return(3)))
    results = [t.result() for t in task]
    print(results)
    return results


async def gather_basic():
    results = await asyncio.gather(*[count_basic(), count_basic(), count_basic()])
    print(results)
    return results


async def gather_return():
    results = await asyncio.gather(*[count_return(1), count_return(2), count_return(3)])
    print(results)
    return results


if __name__ == "__main__":
    import time

    start = time.perf_counter()
    asyncio.run(tg_basic())
    elapsed = time.perf_counter() - start
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")
```

## Queue
We can create Producers and Consumers design pattern by using asynchronous queue.
```python
import asyncio
import random
import time


async def main():
    queue = asyncio.Queue()
    user_ids = [1, 2, 3]

    start = time.perf_counter()
    await asyncio.gather(
        producer(queue, user_ids),
        *(consumer(queue, ids) for ids in user_ids),
    )
    end = time.perf_counter()
    print(f"\n==> Total time: {end - start:.2f} seconds")


async def producer(queue, user_ids):
    async def fetch_user(user_id):
        delay = random.uniform(0.5, 2.0)
        print(f"Producer: fetching user by {user_id=}...")
        await asyncio.sleep(delay)
        user = {"id": user_id, "name": f"User{user_id}"}
        print(f"Producer: fetched user with {user_id=} (done in {delay:.1f}s)")
        await queue.put(user)

    await asyncio.gather(*(fetch_user(uid) for uid in user_ids))
    # gather is a blocking line thus, the for loop below will only run after gather is completed
    for _ in range(len(user_ids)):
        await queue.put(None)  # Sentinels for consumers to terminate


async def consumer(queue, ids):
    while True:
        user = await queue.get()
        if user is None:
            break
        delay = random.uniform(0.5, 2.0)
        print(f"Consumer {ids}: retrieving posts for {user['name']}...")
        await asyncio.sleep(delay)
        posts = [f"Post {i} by {user['name']}" for i in range(1, 3)]
        print(
            f"Consumer {ids}: got {len(posts)} posts by {user['name']}"
            f" (done in {delay:.1f}s):"
        )
        for post in posts:
            print(f"  - {post}")


if __name__ == "__main__":
    random.seed(444)
    asyncio.run(main())
```

## Generator
The difference between asynchronous generator and synchronous generator is that for async generator, other async processes can run in between the iteration process while, synchronouse generator does not allow that.

So the main benefit of using asynchronouse generator is when you know that the generator will have a lot of waiting required, for example, making http requests in each of the loop.

Asynchronous generators can be created using the `yield` in a async function, then it can be called using `async for` to iterate through then function.

```python
import asyncio


async def powers_of_two(stop=10):
    exponent = 0
    while exponent < stop:
        yield 2**exponent
        exponent += 1
        await asyncio.sleep(0.2)  # Simulate some asynchronous work


async def main():
    g = []
    async for i in powers_of_two(5):
        g.append(i)
    print(g)
    f = [j async for j in powers_of_two(5) if not (j // 3 % 5)]
    print(f)


if __name__ == "__main__":
    asyncio.run(main())
```

## Exception Handling
For `TaskGroup`, if there is a single function that run into exception, the entire task group will fail. 

So there is 2 ways to mitigate this issue.
1. Wrap `try except` clause in each of the functions and then in the `except` clause, we return the exception. This way the other functions can still run while we are aware of the specific function that hit an exception and do somehting about it.
2. Wrap `try except` clause around the `TaskGroup` itself. This way we can handle the `TaskGroup` exception as a whole.

```python
import asyncio
async def coro_a():
    try:
        await asyncio.sleep(1)
        # raise ValueError("Error in coro A")
        print("Completed A")
    except Exception as e:
        return e

async def coro_b():
    try:
        await asyncio.sleep(2)
        raise TypeError("Error in coro B")
        # print("Completed B")
    except Exception as e:
        return e

async def coro_c():
    try:
        await asyncio.sleep(0.5)
        raise IndexError("Error in coro C")
        # print("Completed C")
    except Exception as e:
        return e

async def main():
    task = []
    async with asyncio.TaskGroup() as tg:
        task.append(tg.create_task(coro_a()))
        task.append(tg.create_task(coro_b()))
        task.append(tg.create_task(coro_c()))
    
    results = [t.result() for t in task]
    exceptions = [e for e in results if isinstance(e, Exception)]
    if exceptions:
        raise ExceptionGroup("Errors", exceptions)

if __name__ == '__main__':
    asyncio.run(main())
```

For `gather` if a single function run into an exception, the rest of the functions will still continue running without any issues. Main benefit for using `gather` is for it's parameter `return_exceptions=True`. This will not cause the function to fail and the exception will be part of the returned value instead. To handle exception, we can also use the `try except` clause if `return_exceptions=True` is not set.

```python
import asyncio
async def coro_a():
    await asyncio.sleep(1)
    raise ValueError("Error in coro A")
    # print("Completed A")

async def coro_b():
    await asyncio.sleep(2)
    # raise TypeError("Error in coro B")
    print("Completed B")

async def coro_c():
    await asyncio.sleep(0.5)
    raise IndexError("Error in coro C")
    # print("Completed C")

async def main():
    results = await asyncio.gather(
        coro_a(),
        coro_b(),
        coro_c(),
        return_exceptions=True
    )
    exceptions = [e for e in results if isinstance(e, Exception)]
    if exceptions:
        raise ExceptionGroup("Errors", exceptions)

if __name__ == '__main__':
    asyncio.run(main())
```

## Semaphore
Semaphore is the setting for the number of concurrent task that can be running at once. It is mainly to control the resource usage. 

eg. control the number of API call to external server and prevent being blocked.

```python
import asyncio 
import random

async def demo_semaphore(semaphore, worker_id):
    print(f"{worker_id} is waiting to start")
    async with semaphore:
        print(f"{worker_id} started working")
        await asyncio.sleep(random.uniform(1,3))
        print(f"{worker_id} finished working")
    return

async def main():
    # allow 1 concurrent task to run only
    semaphore_1 = asyncio.Semaphore(1)
    # allow 3 concurrent task to run only
    semaphore_3 = asyncio.Semaphore(3)

    async with asyncio.TaskGroup() as tg:
        for i in range(10):
            tg.create_task(demo_semaphore(semaphore_1, i))
            tg.create_task(demo_semaphore(semaphore_3, i+10))
    return

if __name__ == '__main__':
    asyncio.run(main())
```

## BoundedSemaphore
Main difference between bounded semaphore and normal semaphore is that in normal semaphore, you can `release()` more amount than the set amount of slots, whereas bounded semaphore will throw an error if you are releasing more than the set amount of idle slots.

**Important note:** Even though bounded semaphore does not allow more than X amount of idle slots, if there are any coroutine is that waiting to run, the moment the semaphore release a slot, the coroutine will immediately take up the slot, reducing the idle slots available by 1. So this means that even though we set our slots to eg. `2`, if there are `1000` coroutine waiting, the semaphore can release `1002` times and **no exception will be thrown**, all `1000` coroutine will be running together. 

We need to be very specific on the number of slots we are allowed to release, and how we release those slots, if not it will defeat the purpose of bounded semaphore.

**FYI:** we can also use context manager for bounded semaphore, `async with asyncio.BoundedSemaphore(5)`

```python
import asyncio
import random

async def acquire_semaphore(semaphore, worker_id):
    print(f"{worker_id} is waiting to acquire semaphore")
    await semaphore.acquire()
    print(f"{worker_id} managed to get semaphore and started working")
    await asyncio.sleep(random.uniform(1,3))
    print(f"{worker_id} finished working")
    return

async def release_semaphore(semaphore, slots):
    while True:
        await asyncio.sleep(1)
        try:
            for _ in range(slots):
                print("Releasing more semaphore slots")
                semaphore.release()
        except ValueError:
            print("Releasing too many")
            pass

async def main():
    value_limit = 2
    # BoundedSemaphore does not allow more than X idle slots available.
    semaphore = asyncio.BoundedSemaphore(value_limit)
    asyncio.create_task(release_semaphore(semaphore, value_limit))

    async with asyncio.TaskGroup() as tg:
        for i in range(5):
            tg.create_task(acquire_semaphore(semaphore, i))

if __name__ == '__main__':
    asyncio.run(main())

```