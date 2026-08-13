import asyncio

async def worker(id, lock):
    async with lock:
        print(f"Lock acquired by worker: {id}")
        await asyncio.sleep(1)
    print(f"Lock released by worker: {id}")

async def main():
    lock = asyncio.Lock()
    await asyncio.gather(worker("1", lock), worker("2", lock))

asyncio.run(main())