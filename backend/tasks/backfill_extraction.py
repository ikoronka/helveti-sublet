"""
Backfill extraction (regex + Ollama LLM fallback) for listings missing
any of the extracted fields.

Run:  uv run python -m tasks.backfill_extraction
"""
import asyncio
import logging
import time

from sqlalchemy import or_, select, text

from db import AsyncSessionLocal, Base, engine
from extraction import llm_extractor
from extraction.summer import is_summer_sublet
from extraction.text_parser import extract_all
from kreis import kreis_from_zip
from models import Listing

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)

EXTRACTED_FIELDS = (
    "gender_preference",
    "is_furnished",
    "is_sublet",
    "available_from",
    "available_to",
)


async def _backfill_kreis(session) -> None:
    # create_all won't add a column to an existing table, so add it if missing.
    cols = await session.run_sync(
        lambda s: [row[1] for row in s.execute(text("PRAGMA table_info(listings)"))]
    )
    if "kreis" not in cols:
        await session.execute(text("ALTER TABLE listings ADD COLUMN kreis INTEGER"))
        logger.info("Added kreis column.")

    listings = (await session.execute(select(Listing))).scalars().all()
    updated = 0
    for listing in listings:
        kreis = kreis_from_zip(listing.zip_code)
        if listing.kreis != kreis:
            listing.kreis = kreis
            updated += 1
    await session.commit()
    logger.info("Backfilled kreis on %d / %d listings.", updated, len(listings))


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await _backfill_kreis(session)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Listing).where(
                or_(
                    Listing.gender_preference.is_(None),
                    Listing.is_furnished.is_(None),
                    Listing.is_sublet.is_(None),
                    Listing.available_from.is_(None),
                    Listing.available_to.is_(None),
                    Listing.is_summer_sublet.is_(None),
                ),
                Listing.description != "",
            )
        )
        listings = result.scalars().all()
        logger.info("Backfilling %d listings...", len(listings))

        llm_needed = 0
        for i, listing in enumerate(listings, 1):
            extracted = extract_all(listing.description)

            needs_llm = any(f not in extracted for f in EXTRACTED_FIELDS)
            if needs_llm:
                llm_needed += 1
                t0 = time.monotonic()
                llm_result = llm_extractor.extract(listing.description)
                for key, value in llm_result.items():
                    if key not in extracted:
                        extracted[key] = value
                elapsed = time.monotonic() - t0
                if elapsed < 6:
                    await asyncio.sleep(6 - elapsed)

            for key, value in extracted.items():
                setattr(listing, key, value)

            listing.is_summer_sublet = is_summer_sublet(
                listing.available_from,
                listing.available_to,
            )

            if i % 10 == 0:
                await session.commit()
                logger.info("  %d / %d done (llm calls so far: %d)", i, len(listings), llm_needed)

        await session.commit()
        logger.info("Done.")


if __name__ == "__main__":
    asyncio.run(main())
