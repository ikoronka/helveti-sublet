import json
import logging

from playwright.async_api import async_playwright

logger = logging.getLogger(__name__)

BASE_URL = "https://www.immoscout24.ch/en/real-estate/rent/city-zuerich"
PAGES_TO_SCRAPE = 15  # ~300 listings


class ImmoScoutScraper:
    SOURCE = "immoscout24"

    async def scrape(self) -> list[dict]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"],
            )
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36"
            )
            page = await context.new_page()

            # Check if DataDome blocks us on page 1
            resp = await page.goto(BASE_URL, wait_until="domcontentloaded")
            if resp and resp.status == 403:
                logger.warning("ImmoScout: blocked by DataDome (403) — skipping scrape")
                await browser.close()
                return []

            results = []
            for pn in range(1, PAGES_TO_SCRAPE + 1):
                if pn > 1:
                    url = f"{BASE_URL}?pn={pn}"
                    await page.goto(url, wait_until="domcontentloaded")

                raw = await page.evaluate("""() => {
                    const state = window.__INITIAL_STATE__;
                    if (!state) return null;
                    return state.resultList?.search?.fullSearch?.result?.listings ?? [];
                }""")

                if not raw:
                    logger.warning("ImmoScout: no __INITIAL_STATE__ on page %d — stopping", pn)
                    break

                mapped = [
                    m for item in raw
                    if (m := self._map(item)) and m["price_chf"] is not None and m["rooms"] is not None
                ]
                results.extend(mapped)
                logger.info("ImmoScout: page %d/%d — %d listings", pn, PAGES_TO_SCRAPE, len(mapped))

            await browser.close()
            logger.info("ImmoScout: scraped %d listings total", len(results))
            return results

    def _map(self, item: dict) -> dict:
        l = item["listing"]
        loc = l.get("localization", {})
        text = loc.get("de", {}).get("text") or loc.get("en", {}).get("text") or {}
        attachments = loc.get("de", {}).get("attachments") or loc.get("en", {}).get("attachments") or []
        images = [a["url"] for a in attachments if a.get("type") == "IMAGE"]

        addr = l.get("address", {})
        coords = addr.get("geoCoordinates", {})
        prices = l.get("prices", {})
        chars = l.get("characteristics", {})

        return {
            "source": self.SOURCE,
            "source_id": str(l["id"]),
            "source_url": f"https://www.immoscout24.ch/rent/{l['id']}",
            "title": text.get("title") or "",
            "description": text.get("description") or "",
            "price_chf": prices.get("rent", {}).get("gross"),
            "rooms": chars.get("numberOfRooms"),
            "area_m2": chars.get("livingSpace"),
            "address": addr.get("street"),
            "city": addr.get("locality") or "Zürich",
            "zip_code": addr.get("postalCode"),
            "latitude": coords.get("latitude"),
            "longitude": coords.get("longitude"),
            "images": json.dumps(images),
        }
