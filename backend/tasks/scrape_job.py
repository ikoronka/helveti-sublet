import asyncio

from db import AsyncSessionLocal, engine, Base
from scrapers.runner import run_all


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        print("Scraping Flatfox...")
        counts = await run_all(session)
        print(f"Done — inserted: {counts['inserted']}, updated: {counts['updated']}")


if __name__ == "__main__":
    asyncio.run(main())
