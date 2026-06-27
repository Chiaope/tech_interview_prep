# Requests
In python, `requests` is used to make connection to other API through TCP connections. It is normally used for `CRUD` operations.

## Session
Using `Session` will significantly speed up connection time since basic `requests.get(url)` operation will open and close new TCP connection for every API call and this will cause some delays since every fresh connection require handshake and SSL negotiation. Using `Session` will reusue the same underlying TCP connection, decreasing latency, it will also automatically store cookie that might be collected after authentication via the login page.

```python
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
```