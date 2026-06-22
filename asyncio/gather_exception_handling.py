import asyncio
async def coro_a():
    await asyncio.sleep(1)
    raise ValueError("Error in coro A")
    # print("Completed A")

async def coro_b():
    await asyncio.sleep(2)
    # raise TypeError("Error in coro B")
    print("Completed B")

async def coro_c():
    await asyncio.sleep(0.5)
    raise IndexError("Error in coro C")
    # print("Completed C")

async def main():
    results = await asyncio.gather(
        coro_a(),
        coro_b(),
        coro_c(),
        return_exceptions=True
    )
    exceptions = [e for e in results if isinstance(e, Exception)]
    if exceptions:
        raise ExceptionGroup("Errors", exceptions)

if __name__ == '__main__':
    asyncio.run(main())
