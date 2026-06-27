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
