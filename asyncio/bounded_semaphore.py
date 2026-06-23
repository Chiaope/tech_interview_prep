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
