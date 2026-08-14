import asyncio
import aiohttp


async def fetch(session, url):
    async with session.get(url) as response:
        content = await response.text()
        return url, len(content)


async def main():
    urls = [
        "https://python.org",
        "https://realpython.com",
        "https://google.com",
        "https://example.com",
        "https://brainycode.com"
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        for coro in asyncio.as_completed(tasks):
            try:
                url, length = await coro
                print(f"{url} => {length} chars")
            except Exception as e:
                print(f"Failed to fetch url: {e}")

asyncio.run(main())