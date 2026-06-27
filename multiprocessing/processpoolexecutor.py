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
