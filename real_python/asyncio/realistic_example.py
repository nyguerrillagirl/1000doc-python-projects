import asyncio
import aiohttp

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()

async def main():
    urls = [
        "https://example.com",
        "https://python.org",
        "https://pypi.org"
    ]

    tasks = [fetch(u) for u in urls]
    results = await asyncio.gather(*tasks)

    print("Fetched all pages!")

asyncio.run(main())
