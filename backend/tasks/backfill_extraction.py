"""
Backfill Gemini extraction for listings that have no extracted fields yet.
Run once after adding the extractor:  uv run python -m tasks.backfill_extraction
"""
import asyncio
import logging
import time

from sqlalchemy import select

from db import AsyncSessionLocal, Base, engine
from extraction import llm_extractor
from extraction.text_parser import extract_all
from models import Listing

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Listing).where(
                Listing.gender_preference.is_(None),
                Listing.is_furnished.is_(None),
                Listing.description != "",
            )
        )
        listings = result.scalars().all()
        logger.info("Backfilling %d listings...", len(listings))

        llm_needed = 0
        for i, listing in enumerate(listings, 1):
            extracted = extract_all(listing.description)

            # fall back to Gemini only for fields regex couldn't determine
            needs_llm = (
                "gender_preference" not in extracted
                or "is_furnished" not in extracted
                or "is_sublet" not in extracted
            )
            if needs_llm:
                llm_needed += 1
                t0 = time.monotonic()
                llm_result = llm_extractor.extract(listing.description)
                # regex takes priority; LLM fills in what regex missed
                for key, value in llm_result.items():
                    if key not in extracted:
                        extracted[key] = value
                elapsed = time.monotonic() - t0
                if elapsed < 6:
                    await asyncio.sleep(6 - elapsed)

            for key, value in extracted.items():
                setattr(listing, key, value)

            if i % 10 == 0:
                await session.commit()
                logger.info("  %d / %d done (llm calls so far: %d)", i, len(listings), llm_needed)

        await session.commit()
        logger.info("Done.")


if __name__ == "__main__":
    asyncio.run(main())
