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
