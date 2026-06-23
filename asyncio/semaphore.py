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
    semaphore_1 = asyncio.BoundedSemaphore(1)
    # allow 3 concurrent task to run only
    semaphore_3 = asyncio.Semaphore(3)

    async with asyncio.TaskGroup() as tg:
        for i in range(10):
            tg.create_task(demo_semaphore(semaphore_1, i))
            tg.create_task(demo_semaphore(semaphore_3, i+10))
    return

if __name__ == '__main__':
    asyncio.run(main())