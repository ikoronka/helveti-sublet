import json
from scrapers.base import BaseScraper

BASE = "https://flatfox.ch/api/v1"

# Zurich canton bounding box (covers city + surroundings)
ZURICH_BBOX = {
    "north": 47.696,
    "south": 47.220,
    "east": 8.799,
    "west": 8.361,
}

PK_BATCH_SIZE = 50


class FlatfoxScraper(BaseScraper):
    SOURCE = "flatfox"

    async def _fetch_pks(self) -> list[int]:
        data = await self._get(
            f"{BASE}/pin/",
            params={**ZURICH_BBOX, "max_count": 400},
        )
        return [item["pk"] for item in data]

    async def _fetch_listings(self, pks: list[int]) -> list[dict]:
        results = []
        for i in range(0, len(pks), PK_BATCH_SIZE):
            batch = pks[i : i + PK_BATCH_SIZE]
            params = [("pk", pk) for pk in batch]
            params += [
                ("expand", "cover_image"),
                ("include", "is_liked"),
                ("include", "is_disliked"),
                ("include", "is_subscribed"),
                ("limit", 0),
            ]
            url = f"{BASE}/public-listing/"
            await self._throttle()
            response = await self._client.get(url, params=params)
            response.raise_for_status()
            results.extend(response.json())
        return results

    async def scrape(self) -> list[dict]:
        pks = await self._fetch_pks()
        raw = await self._fetch_listings(pks)
        return [self._map(item) for item in raw if self._is_rental(item)]

    @staticmethod
    def _is_rental(item: dict) -> bool:
        return (
            item.get("offer_type") == "RENT"
            and item.get("status") == "act"
            and item.get("price_display") is not None
            and item.get("number_of_rooms") is not None
        )

    @staticmethod
    def _map(item: dict) -> dict:
        address_parts = [
            item.get("street"),
            str(item["zipcode"]) if item.get("zipcode") else None,
            item.get("city"),
        ]
        address = ", ".join(p for p in address_parts if p) or None

        images = []
        cover = item.get("cover_image")
        if cover and cover.get("url"):
            url = cover["url"]
            if url.startswith("/"):
                url = f"https://flatfox.ch{url}"
            images.append(url)

        return {
            "source": "flatfox",
            "source_id": str(item["pk"]),
            "source_url": f"https://flatfox.ch{item['url']}",
            "title": item.get("description_title") or item.get("public_title") or item.get("short_title", ""),
            "description": item.get("description") or "",
            "price_chf": int(item["price_display"]),
            "rooms": float(item["number_of_rooms"]),
            "area_m2": item.get("surface_living"),
            "address": address,
            "city": item.get("city") or "",
            "zip_code": str(item["zipcode"]) if item.get("zipcode") else None,
            "latitude": item.get("latitude"),
            "longitude": item.get("longitude"),
            "images": json.dumps(images),
        }
