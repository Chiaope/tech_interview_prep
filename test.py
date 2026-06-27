import requests
import time

url_list = [
    "https://www.jython.org",
    "http://olympus.realpython.org/dice",
] * 80


def get_content_with_session(url_list):
    with requests.Session() as session:
        for url in url_list:
            with session.get(url) as response:
                print(f"Read {len(response.content)} bytes from {url}")


def get_content(url_list):
    for url in url_list:
        with requests.get(url) as response:
            print(f"Read {len(response.content)} bytes from {url}")


if __name__ == "__main__":
    use_session = False
    start = time.perf_counter()
    if use_session:
        get_content_with_session(url_list)  # Completed in 17.417 seconds
    else:
        get_content(url_list)  # Completed in 38.257 seconds
    print(f"Completed in {(time.perf_counter() - start):.3f} seconds")
