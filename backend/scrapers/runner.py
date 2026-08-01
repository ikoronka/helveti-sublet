import hashlib
import logging
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from extraction import llm_extractor
from extraction.summer import is_summer_sublet
from extraction.text_parser import extract_all
from kreis import kreis_from_zip
from models import Listing
from scrapers.flatfox import FlatfoxScraper
from scrapers.immoscout import ImmoScoutScraper

logger = logging.getLogger(__name__)


def _listing_id(source: str, source_id: str) -> str:
    return hashlib.sha256(f"{source}:{source_id}".encode()).hexdigest()


async def run_all(session: AsyncSession) -> dict[str, int]:
    now = datetime.now(timezone.utc)
    scraped_ids: set[str] = set()
    counts = {"inserted": 0, "updated": 0}

    flatfox_listings = []
    async with FlatfoxScraper() as scraper:
        flatfox_listings = await scraper.scrape()

    immoscout_scraper = ImmoScoutScraper()
    immoscout_listings = await immoscout_scraper.scrape()

    listings = flatfox_listings + immoscout_listings

    for data in listings:
        lid = _listing_id(data["source"], data["source_id"])
        scraped_ids.add(lid)
        data["kreis"] = kreis_from_zip(data.get("zip_code"))

        result = await session.execute(select(Listing).where(Listing.id == lid))
        existing = result.scalar_one_or_none()

        if existing:
            for key, value in data.items():
                setattr(existing, key, value)
            existing.last_seen = now
            existing.is_active = True
            counts["updated"] += 1
        else:
            try:
                extracted = extract_all(data.get("description", ""))
            except Exception:
                logger.exception("text extraction failed for listing %s, continuing with regex fields unset", lid)
                extracted = {}
            llm_result = llm_extractor.extract(data.get("description", ""))
            for key, value in llm_result.items():
                if key not in extracted:
                    extracted[key] = value
            extracted["is_summer_sublet"] = is_summer_sublet(
                extracted.get("available_from"),
                extracted.get("available_to"),
            )
            listing = Listing(
                id=lid,
                first_seen=now,
                last_seen=now,
                is_active=True,
                **data,
                **extracted,
            )
            session.add(listing)
            counts["inserted"] += 1

    # mark listings not seen this run as inactive
    all_result = await session.execute(
        select(Listing).where(Listing.is_active == True)
    )
    for listing in all_result.scalars():
        if listing.id not in scraped_ids:
            listing.is_active = False

    await session.commit()
    return counts
