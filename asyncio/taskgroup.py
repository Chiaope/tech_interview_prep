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