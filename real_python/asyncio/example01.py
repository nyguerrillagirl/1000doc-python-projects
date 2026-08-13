import asyncio

async def main():
    print("Hello...")
    task = asyncio.create_task(lorraine())
    await asyncio.sleep(1.0)
    print("...World!")
    await task

async def lorraine():
    await asyncio.sleep(2.5)
    print("Lorraine")

asyncio.run(main())
