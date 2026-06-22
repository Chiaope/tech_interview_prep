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
