import asyncio

async def say(what, when):
    await asyncio.sleep(when)
    print(what)

async def main():
    await asyncio.gather(
        say("first", 1),
        say("second", 2),
        say("third", 3),
    )

asyncio.run(main())