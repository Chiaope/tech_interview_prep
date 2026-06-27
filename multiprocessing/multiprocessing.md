# Multiprocessing
**IMPORTANT NOTE:** **ALWAYS USE** `if __name__ == "__main__"` since multiprocessing works by spinning up new process and importing the module. If this block is not included, it will essentially spin up infinite process recursively.

There are many situations where `multiprocessing` is better than `threading` or `asyncio`. Whenever there are any CPU bounded task, using multiprocessing will reduce the wait time quite significantly. If there are computational task that does not depend on one another, like **hyperparameter tuning** or **parameter scanning**, using multiprocessing will effectively prove **true parallelism** and reduce the computational time.

How it works is basically it uses subprocesses instead of thread to run a separate Python program. So multiprocessing depends on the number of cores available on the CPU and it will also have it's own set of Python interpreter, storage, etc. This helps to side step `GIL`, providing **true parallism**.

## ProcessPoolExecutor
One way to use multiprocessing effectively is using `ProcessPoolExecutor`. This is similar to `ThreadPoolExecutor` and the API used to run this is also very similar.

```python
import time
import math
from concurrent.futures import ProcessPoolExecutor


def total_square_root():
    total = 0
    for i in range(1_000_000):
        total += math.sqrt(i)
    return total


def main():
    start = time.perf_counter()
    results = []
    with ProcessPoolExecutor(max_workers=4) as ppe:
        for _ in range(1000):
            results.append(ppe.submit(total_square_root))
    end_time = time.perf_counter()
    print(f"Time taken: {end_time - start:.3f} seconds")
    # print([result.result() for result in results])


if __name__ == "__main__":
    main()
```

## shared_memory
In multiprocessing, since it is spinning up a new subprocess, there are many things that are not shared amount each other. In order to share data between each other we can use `shared_memory.SharedMemory`. This basically take up a memory space and that memory space will be shared between processes.

Dam complex so dont get too deep into it lol.

## CPU Affinity/Pinning
CPU affinity/pinning means allowing a selected set of CPU cores to process data.
Each core have their own L1/L2 cache and if the OS decided to switch the process to another core, the cache will no longer be hot and then data will have to be reloaded again.





## What to know
1. Polars/Pandas multiprocessing
2. forkserver
3. shared_memory - Died
4. CPU Affinity (Pinning) - Died
5. Lock-free architecture (Ring Buffers) - Died
6. websockets - Done
7. Dataclass - Done
8. Factory design pattern
9. Observer Pattern
10. collections.deque
11. SOLID Design Principles
12. Finite State Machines
13. Designing heartbeats
14. OLAP vs OLTP
15. Message brokers
16. Redis cache
17. Sliding Window and Two-Pointer Algorithms
18. heapq
19. Idempotency and Fault Tolerance in Event Streams (Kubernetes)