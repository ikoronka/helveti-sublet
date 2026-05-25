"""One-shot import of ImmoScout24 listings from browser-scraped JSON."""
import asyncio
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select

from db import AsyncSessionLocal
from extraction import llm_extractor
from extraction.text_parser import extract_all
from models import Listing


def _listing_id(source: str, source_id: str) -> str:
    return hashlib.sha256(f"{source}:{source_id}".encode()).hexdigest()


async def main(json_path: str) -> None:
    raw = json.loads(Path(json_path).read_text())
    print(f"Importing {len(raw)} ImmoScout24 listings...")

    now = datetime.now(timezone.utc)
    inserted = updated = 0

    async with AsyncSessionLocal() as session:
        for item in raw:
            data = {
                "source": "immoscout24",
                "source_id": item["source_id"],
                "source_url": item["source_url"],
                "title": item.get("title") or "",
                "description": item.get("description") or "",
                "price_chf": item.get("price_chf"),
                "rooms": item.get("rooms"),
                "area_m2": item.get("area_m2"),
                "address": item.get("address"),
                "city": item.get("city") or "Zürich",
                "zip_code": item.get("zip_code"),
                "latitude": item.get("latitude"),
                "longitude": item.get("longitude"),
                "images": json.dumps(item.get("images") or []),
            }

            lid = _listing_id(data["source"], data["source_id"])
            result = await session.execute(select(Listing).where(Listing.id == lid))
            existing = result.scalar_one_or_none()

            if data["price_chf"] is None:
                continue

            if existing:
                for key, value in data.items():
                    setattr(existing, key, value)
                existing.last_seen = now
                existing.is_active = True
                updated += 1
            else:
                extracted = extract_all(data["description"])
                llm_result = llm_extractor.extract(data["description"])
                for key, value in llm_result.items():
                    if key not in extracted:
                        extracted[key] = value
                session.add(Listing(
                    id=lid,
                    first_seen=now,
                    last_seen=now,
                    is_active=True,
                    **data,
                    **extracted,
                ))
                inserted += 1

        await session.commit()

    print(f"Done: {inserted} inserted, {updated} updated")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / "Downloads/is24_data.json")
    asyncio.run(main(path))
